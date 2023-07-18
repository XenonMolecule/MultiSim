#!/usr/bin/env python
# coding=utf-8
# Copyright The HuggingFace Team and The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Fine-tuning a 🤗 Transformers model on summarization.
"""
# You can also adapt this script on your own summarization task. Pointers for this are left as comments.

import argparse
import json
import logging
import os
from pathlib import Path
import pandas as pd

import datasets
import nltk
import numpy as np
import torch
from datasets import load_dataset
from torch.utils.data import DataLoader
from tqdm.auto import tqdm

import evaluate
import transformers
from accelerate import Accelerator
from accelerate.logging import get_logger
from accelerate.utils import set_seed
from filelock import FileLock
from huggingface_hub import Repository
from transformers import (
    MODEL_MAPPING,
    AutoConfig,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    DataCollatorForSeq2Seq,
    SchedulerType,
    get_scheduler,
)
from transformers.utils import check_min_version, is_offline_mode, send_example_telemetry
from transformers.utils.versions import require_version
from easse.sari import corpus_sari
from sacrebleu import corpus_bleu

torch.cuda.empty_cache()

# Will error if the minimal version of Transformers is not installed. Remove at your own risks.
check_min_version("4.24.0.dev0")

logger = get_logger(__name__)
require_version("datasets>=1.8.0", "To fix: pip install -r examples/pytorch/summarization/requirements.txt")

# You should update this to your particular problem to have better documentation of `model_type`
MODEL_CONFIG_CLASSES = list(MODEL_MAPPING.keys())
MODEL_TYPES = tuple(conf.model_type for conf in MODEL_CONFIG_CLASSES)

try:
    nltk.data.find("tokenizers/punkt")
except (LookupError, OSError):
    if is_offline_mode():
        raise LookupError(
            "Offline mode: run this script without TRANSFORMERS_OFFLINE first to download nltk data files"
        )
    with FileLock(".lock") as lock:
        nltk.download("punkt", quiet=True)

def calc_bleu_sari(original, sentences, references, tokenizer="13a"):

    num_refs = max([len(refs) for refs in references])

    bleu_scores = np.zeros((num_refs))
    sari_scores = np.zeros((num_refs))

    examples = [{"original": [], "sentences": [], "references": []} for _ in range(num_refs)]

    assert len(original) == len(sentences)
    assert len(sentences) == len(references)

    for original, refs, sentence in zip(original, references, sentences):
        simple = sentence
        num_ref = len(refs)
        examples[num_ref-1]['original'].append(original)
        examples[num_ref-1]['sentences'].append(simple)
        examples[num_ref-1]['references'].append(refs)

    counts = np.array([len(e['original']) for e in examples])
    total = sum(counts)
    weights = np.divide(counts, total)

    for i in range(len(examples)):
        if counts[i] > 0:
            references = np.array(examples[i]['references']).T.tolist()
            bleu_scores[i] = corpus_bleu(
                                examples[i]['sentences'],
                                references,
                                force = True,
                                tokenize = tokenizer,
                                lowercase = True
                            ).score
            sari_scores[i] = corpus_sari(
                                orig_sents = examples[i]['original'],
                                sys_sents = examples[i]['sentences'],
                                refs_sents = references,
                                tokenizer = tokenizer
                            )
    
    bleu = np.dot(bleu_scores, weights)
    sari = np.dot(sari_scores, weights)

    return bleu, sari

def parse_args():
    parser = argparse.ArgumentParser(description="Finetune a transformers model on a summarization task")
    parser.add_argument(
        "--dataset_name",
        type=str,
        default=None,
        help="The name of the dataset to use (via the datasets library).",
    )
    parser.add_argument(
        "--ignore_pad_token_for_loss",
        type=bool,
        default=True,
        help="Whether to ignore the tokens corresponding to padded labels in the loss computation or not.",
    )
    parser.add_argument(
        "--max_source_length",
        type=int,
        default=1024,
        help=(
            "The maximum total input sequence length after "
            "tokenization.Sequences longer than this will be truncated, sequences shorter will be padded."
        ),
    )
    parser.add_argument(
        "--source_prefix",
        type=str,
        default=None,
        help="A prefix to add before every source text (useful for T5 models).",
    )
    parser.add_argument(
        "--preprocessing_num_workers",
        type=int,
        default=None,
        help="The number of processes to use for the preprocessing.",
    )
    parser.add_argument(
        "--overwrite_cache", action="store_true", help="Overwrite the cached training and evaluation sets"
    )
    parser.add_argument(
        "--max_target_length",
        type=int,
        default=128,
        help=(
            "The maximum total sequence length for target text after "
            "tokenization. Sequences longer than this will be truncated, sequences shorter will be padded."
            "during ``evaluate`` and ``predict``."
        ),
    )
    parser.add_argument(
        "--val_max_target_length",
        type=int,
        default=None,
        help=(
            "The maximum total sequence length for validation "
            "target text after tokenization.Sequences longer than this will be truncated, sequences shorter will be "
            "padded. Will default to `max_target_length`.This argument is also used to override the ``max_length`` "
            "param of ``model.generate``, which is used during ``evaluate`` and ``predict``."
        ),
    )
    parser.add_argument(
        "--max_length",
        type=int,
        default=128,
        help=(
            "The maximum total input sequence length after tokenization. Sequences longer than this will be truncated,"
            " sequences shorter will be padded if `--pad_to_max_lengh` is passed."
        ),
    )
    parser.add_argument(
        "--num_beams",
        type=int,
        default=None,
        help=(
            "Number of beams to use for evaluation. This argument will be "
            "passed to ``model.generate``, which is used during ``evaluate`` and ``predict``."
        ),
    )
    parser.add_argument(
        "--pad_to_max_length",
        action="store_true",
        help="If passed, pad all samples to `max_length`. Otherwise, dynamic padding is used.",
    )
    parser.add_argument(
        "--use_slow_tokenizer",
        action="store_true",
        help="If passed, will use a slow tokenizer (not backed by the 🤗 Tokenizers library).",
    )
    parser.add_argument(
        "--per_device_eval_batch_size",
        type=int,
        default=8,
        help="Batch size (per device) for the evaluation dataloader.",
    )
    parser.add_argument("--input_dir", type=str, default=None, help="Where to read in the model epochs to validate.")
    parser.add_argument(
        "--model_type",
        type=str,
        default=None,
        help="Model type to use if training from scratch.",
        choices=MODEL_TYPES,
    )
    parser.add_argument("--push_to_hub", action="store_true", help="Whether or not to push the model to the Hub.")
    parser.add_argument(
        "--hub_model_id", type=str, help="The name of the repository to keep in sync with the local `output_dir`."
    )
    parser.add_argument("--hub_token", type=str, help="The token to use to push to the Model Hub.")
    parser.add_argument(
        "--checkpointing_steps",
        type=str,
        default=None,
        help="Whether the various states should be saved at the end of every n steps, or 'epoch' for each epoch.",
    )
    parser.add_argument(
        "--resume_from_checkpoint",
        type=str,
        default=None,
        help="If the training should continue from a checkpoint folder.",
    )
    parser.add_argument(
        "--with_tracking",
        action="store_true",
        help="Whether to enable experiment trackers for logging.",
    )
    parser.add_argument(
        "--report_to",
        type=str,
        default="all",
        help=(
            'The integration to report the results and logs to. Supported platforms are `"tensorboard"`,'
            ' `"wandb"` and `"comet_ml"`. Use `"all"` (default) to report to all integrations.'
            "Only applicable when `--with_tracking` is passed."
        ),
    )
    parser.add_argument(
        "--gradient_accumulation_steps",
        type=int,
        default=1,
        help="Number of updates steps to accumulate before performing a backward/update pass.",
    )
    parser.add_argument("--seed", type=int, default=None, help="A seed for reproducible training.")
    parser.add_argument("--tokenizer", type=str, default="13a", help="Which tokenizer to use when computing bleu and sari scores.")
    parser.add_argument("--NC", type=float, default=1.0, help="Character compression to start search with")
    parser.add_argument("--LS", type=float, default=1.0, help="Levenshtein similarity to start search with")
    parser.add_argument("--DR", type=float, default=1.0, help="Depth ratio to start search with")
    parser.add_argument("--WR", type=float, default=1.0, help="Word rank to start search with")
    parser.add_argument("--ctrl_token_output_file", type=str, default=None, help="Where to write the hyperparameter outputs to.")
    
    args = parser.parse_args()

    # Sanity checks
    if args.push_to_hub:
        assert args.output_dir is not None, "Need an `output_dir` to create a repo when `--push_to_hub` is passed."

    return args


def main():
    args = parse_args()
    # Sending telemetry. Tracking the example usage helps us better allocate resources to maintain them. The
    # information sent is the one passed as arguments along with your Python/PyTorch versions.
    send_example_telemetry("run_summarization_no_trainer", args)

    # Initialize the accelerator. We will let the accelerator handle device placement for us in this example.
    # If we're using tracking, we also need to initialize it here and it will by default pick up all supported trackers
    # in the environment
    accelerator_log_kwargs = {}

    if args.with_tracking:
        accelerator_log_kwargs["log_with"] = args.report_to
        accelerator_log_kwargs["logging_dir"] = args.output_dir

    accelerator = Accelerator(gradient_accumulation_steps=args.gradient_accumulation_steps, **accelerator_log_kwargs)

    # Make one log on every process with the configuration for debugging.
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO,
    )
    logger.info(accelerator.state, main_process_only=False)
    if accelerator.is_local_main_process:
        datasets.utils.logging.set_verbosity_warning()
        transformers.utils.logging.set_verbosity_info()
    else:
        datasets.utils.logging.set_verbosity_error()
        transformers.utils.logging.set_verbosity_error()

    # If passed along, set the training seed now.
    if args.seed is not None:
        set_seed(args.seed)

    # Load pretrained model and tokenizer
    #
    # In distributed training, the .from_pretrained methods guarantee that only one local process can concurrently
    # download model & vocab.
    config = AutoConfig.from_pretrained(args.input_dir)

    tokenizer = AutoTokenizer.from_pretrained(args.input_dir, use_fast=not args.use_slow_tokenizer)

    model = AutoModelForSeq2SeqLM.from_pretrained(
        args.input_dir,
        config=config,
    )

    model.resize_token_embeddings(len(tokenizer))
    if model.config.decoder_start_token_id is None:
        raise ValueError("Make sure that `config.decoder_start_token_id` is correctly defined")

    # Preprocessing the datasets.
    # First we tokenize all the texts.
    column_names = ['original','simple']

    # Preprocessing the datasets.
    # First we tokenize all the texts.
    column_names = ['original','simple']

    # Get the column names for input/target.
    original_column = column_names[0]
    simple_column = column_names[1]

    # Temporarily set max_target_length for training.
    max_target_length = args.max_target_length
    padding = "max_length" if args.pad_to_max_length else False

    def run_val(nc, ls, dr, wr, config, tokenizer, model):

        # Downloading and loading a dataset from the hub.
        raw_datasets = load_dataset("./MultilingualSimplification.py", name=args.dataset_name, split="validation")
        # See more about loading any type of standard or custom dataset (from files, python dict, pandas DataFrame, etc) at
        # https://huggingface.co/docs/datasets/loading_datasets.html.

        def preprocess_function(examples):
            inputs = examples[original_column]
            prefix = "<NC_" + str(round(nc,2)) +"> <LS_" + str(round(ls,2)) +"> <DR_" + str(round(dr,2)) + "> <WR_ " + str(round(wr,2)) + "> "
            inputs = [prefix + i for i in inputs]
            model_inputs = tokenizer(inputs, max_length=args.max_source_length, padding=padding, truncation=True)

            return model_inputs

        with accelerator.main_process_first():
            processed_datasets = raw_datasets.map(
                preprocess_function,
                batched=True,
                num_proc=args.preprocessing_num_workers,
                remove_columns=column_names,
                load_from_cache_file=not args.overwrite_cache,
                desc="Running tokenizer on dataset",
            )

        validation_dataset = processed_datasets

        label_pad_token_id = -100 if args.ignore_pad_token_for_loss else tokenizer.pad_token_id
        data_collator = DataCollatorForSeq2Seq(
            tokenizer,
            model=model,
            label_pad_token_id=label_pad_token_id,
            pad_to_multiple_of=8 if accelerator.use_fp16 else None,
        )

        def postprocess_text(preds):
            preds = [pred.strip() for pred in preds]

            # rougeLSum expects newline after each sentence
            preds = ["\n".join(nltk.sent_tokenize(pred)) for pred in preds]

            return preds

        val_dataloader = DataLoader(validation_dataset, collate_fn=data_collator, batch_size=args.per_device_eval_batch_size)

        # Prepare everything with our `accelerator`.
        model, val_dataloader = accelerator.prepare(
            model, val_dataloader
        )

        logger.info("***** Running validation *****")
        logger.info(f"  Num examples (val) = {len(validation_dataset)}")
        logger.info(f"  Instantaneous batch size per device = {args.per_device_eval_batch_size}")
        logger.info(f"  Batches to evaluate = {len(val_dataloader)}")
        # Only show the progress bar once on each machine.

        epoch_count = 0
        for dir_name in os.listdir(args.input_dir):
            directory = os.path.join(args.input_dir, dir_name)
            if os.path.isdir(directory) and "epoch" in dir_name:
                epoch_count += 1

        model.eval()
        if args.val_max_target_length is None:
            args.val_max_target_length = args.max_target_length

        gen_kwargs = {
            "max_length": args.val_max_target_length if args is not None else config.max_length,
            "num_beams": args.num_beams,
        }

        progress_bar = tqdm(range(len(val_dataloader)), disable=not accelerator.is_local_main_process)

        input_list, ref_list, out_list = [], [], []

        for step, batch in enumerate(val_dataloader):

            data = raw_datasets[step*args.per_device_eval_batch_size : (step+1)*args.per_device_eval_batch_size]

            with torch.no_grad():
                generated_tokens = accelerator.unwrap_model(model).generate(
                    batch["input_ids"],
                    attention_mask=batch["attention_mask"],
                    **gen_kwargs,
                )

                generated_tokens = accelerator.pad_across_processes(
                    generated_tokens, dim=1, pad_index=tokenizer.pad_token_id
                )

                generated_tokens = accelerator.gather_for_metrics((generated_tokens))
                generated_tokens = generated_tokens.cpu().numpy()

                if isinstance(generated_tokens, tuple):
                    generated_tokens = generated_tokens[0]

                decoded_preds = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)

                decoded_preds = postprocess_text(decoded_preds)

                input_list.extend(data["original"])
                for refs in data["simple"]:
                    ref_list.append(refs['simplifications'])
                out_list.extend(decoded_preds)

                if accelerator.is_main_process:
                    progress_bar.update(1)

        bleu, sari = calc_bleu_sari(input_list, out_list, ref_list, args.tokenizer)
        print("NC", round(nc,2), "LS", round(ls,2), "DR", round(dr,2), "WR", round(wr,2))
        print("BLEU", bleu)
        print("SARI", sari)
        print()
        return sari

    # Get the datasets: you can either provide your own CSV/JSON/TXT training and evaluation files (see below)
    # or just provide the name of one of the public datasets available on the hub at https://huggingface.co/datasets/
    # (the dataset will be downloaded automatically from the datasets Hub).
    #
    # For CSV/JSON files, this script will use the column called 'text' or the first column if no column called
    # 'text' is found. You can easily tweak this behavior (see below).
    #
    # In distributed training, the load_dataset function guarantee that only one local process can concurrently
    # download the dataset.

    nc = args.NC
    ls = args.LS
    dr = args.DR
    wr = args.WR

    N = 3
    mod = range(0-(N//2), 1+(N//2))

    max_sari = 0
    best_params = (0, 0, 0, 0)

    for nc_mod in mod:
        nc = min(max(0, args.NC + (0.05 * nc_mod)),2)
        for ls_mod in mod:
            ls = min(max(0, args.LS + (0.05 * ls_mod)),2)
            for dr_mod in mod:
                dr = min(max(0, args.DR + (0.05 * dr_mod)),2)
                for wr_mod in mod:
                    wr = min(max(0, args.WR + (0.05 * wr_mod)),2)
                    sari = run_val(nc,ls,dr,wr, config, tokenizer, model)
                    if sari > max_sari:
                        best_params = (nc,ls,dr,wr)
                        max_sari = sari
    
    print("---BEST---")
    print("NC", round(best_params[0],2), "LS", round(best_params[1],2), "DR", round(best_params[2],2), "WR", round(best_params[3],2))
    print("SARI:", max_sari)

    if args.ctrl_token_output_file:
        with open(args.ctrl_token_output_file, 'a') as f:
            f.write("\n" + args.dataset_name + ":\n")
            f.write("<NC_" + str(round(best_params[0],2)) + "> <LS_" + str(round(best_params[1],2)) + "> <DR_" + str(round(best_params[2],2)) + "> <WR_" + str(round(best_params[3],2)) + ">\n")


if __name__ == "__main__":
    main()