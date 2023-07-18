# Code

This code is primarily included for anyone that wants to reproduce the experiments and analysis done in the paper.  The easiest way to actually use this dataset is to use the data from the `../data` folder, or from the [HuggingFace Repo](https://www.google.com) (coming soon!).

## Organization

| File/Folder | Purpose |
|---|---|
| ./MultilingualSimplification.py | HuggingFace Dataset style file for loading the dataset from csv file to HuggingFace Dataloader |
| ./main.py | File with most of the Appendix analysis experiments implemented.  Loads datasets and makes calls to other scripts. |
| ./testing.py | File to ensure that all data is loaded properly (if you are loading from other authors original formats, not from MultiSim csv files) |
| ./datatypes.py | Defines several datatypes such as 'Document' and 'AlignedParallelDocument' to load the datasets into.  For ease of use MultiSim just converts all datasets to a single sentence aligned format. |
| ./requirements.txt | The necessary python packages to run the scripts in this repository |
| ./analysis/ | Scripts to perform most of the statistical analysis reported in the appendix of the paper (ex. document compression, edit distance) |
| ./custom_tokenizers/ | Some languages required custom tokenizers such as Fugashi for Japanese or UrduHack in Urdu.  These scripts are wrappers for these tokenizers. |
| ./finetuning/ | Scripts to finetune the mT5 models on simplification both with and without control tokens.  Note that training with control tokens requires computing and prepending the control tokens separately from the script (hence no train control token script is provided). If control tokens are needed and cannot be computed, please email [Michael](mailto:michaeljryan@stanford.edu), and he will share precomputed control tokens.  Otherwise, scripts to compute control tokens are included in the util folder. |
| ./loaders/ | Data loaders for all of the custom data types in all the individual datasets that make up MultiSim.  See each file for the folder structure that the data loader is expecting (typically the default when you download the dataset from the authors). |
| ./notebooks/ | Jupyter Notebooks used in processing and analyzing the datasets.  Mostly used to create visualizations or do preprocessing.  |
| ./util/ | Util scripts to help with data processing.  (ex. compute control tokens, unzip files, map language to language code, etc.) |