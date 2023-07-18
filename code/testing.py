from datatypes import AlignedParallelDocument, Corpus
from loaders.alector_loader import AlectorLoader
from loaders.cbst_loader import CBSTLoader
from loaders.clear_loader import CLEARLoader
from loaders.dsim_loader import DSimLoader
from loaders.easy_japanese_extended_loader import EasyJapaneseExtendedLoader
from loaders.easy_japanese_loader import EasyJapaneseLoader
from loaders.geolino_loader import GEOLinoLoader
from loaders.german_news_loader import GermanNewsLoader
from loaders.newsela_es_loader import NewselaESLoader
from loaders.paccssit_loader import PaCCSSIT_Loader
from loaders.rsse_loader import RSSE_Loader
from loaders.ru_adapt_loader import RuAdaptLoader
from loaders.ru_wiki_large_loader import RuWikiLargeLoader
from loaders.simpitiki_loader import SimpitikiLoader
from loaders.simple_german_loader import SimpleGermanLoader
from loaders.simplext_loader import SimplextLoader
from loaders.porsimples_loader import PorSimplesLoader
from loaders.simplify_ur_loader import SimplifyUR_Loader
from loaders.terence_teacher_loader import TerenceTeacherLoader
from loaders.text_complexity_de_loader import TextComplexityDELoader
from loaders.wiki_large_fr_loader import WikiLargeFRLoader
from loaders.newsela_en_loader import NewselaENLoader
from loaders.wikiauto_en_loader import WikiAutoENLoader
from loaders.asset_loader import AssetLoader
from loaders.adminit_loader import AdminItLoader
from loaders.ts_slovene_loader import TextSimplificationSloveneLoader
from loaders.klexikon_loader import KlexikonLoader

import os

def simplext_tests(path):
    simplext_full_loader = SimplextLoader(keep_subdivisions=False)
    simplext_split_loader = SimplextLoader(keep_subdivisions=True)

    simplext_full = simplext_full_loader.load(path)[0]

    assert len(simplext_full.documents) == 193

    has_specific_doc = False
    for document in simplext_full.documents:
        if document.original_items[0] == "Chacón anuncia que se endurecerán las autorizaciones a aviones norteamericanos militares para hacer escalas en España":
            has_specific_doc = True
            assert document.original_items[-1] == "Por ende , el Ministerio de Defensa y Estados Unidos han decidido mejorar el vigente convenio ,\"a través de la introducción de mejoras\", como las relativas a las autorizaciones de escalas y sobrevuelos de aeronaves militares ."
            assert document.simplified_items[0] == "Chacón anuncia que se endurecerán las autorizaciones a aviones norteamericanos militares para hacer escalas en España"
            assert document.simplified_items[-1] == "Este acuerdo permite a los aviones de Estados Unidos volar por España ."
            assert document.original_to_simplified_alignment == [[0], [1], [2, 3], [5, 4], [], [7, 6]]
            assert document.simplified_to_original_alignment == [[0], [1], [2], [2], [3], [3], [5], [5]]
            break

    assert has_specific_doc

    simplext_p1, simplext_p2 = simplext_split_loader.load(path)

    assert len(simplext_p1.documents) == 37
    assert len(simplext_p2.documents) == 156

    has_specific_doc = False
    for document in simplext_p1.documents:
        if document.original_items[0] == "Chacón anuncia que se endurecerán las autorizaciones a aviones norteamericanos militares para hacer escalas en España":
            has_specific_doc = True
            assert document.original_items[-1] == "Por ende , el Ministerio de Defensa y Estados Unidos han decidido mejorar el vigente convenio ,\"a través de la introducción de mejoras\", como las relativas a las autorizaciones de escalas y sobrevuelos de aeronaves militares ."
            assert document.simplified_items[0] == "Chacón anuncia que se endurecerán las autorizaciones a aviones norteamericanos militares para hacer escalas en España"
            assert document.simplified_items[-1] == "Este acuerdo permite a los aviones de Estados Unidos volar por España ."
            assert document.original_to_simplified_alignment == [[0], [1], [2, 3], [5, 4], [], [7, 6]]
            assert document.simplified_to_original_alignment == [[0], [1], [2], [2], [3], [3], [5], [5]]
            break

    assert has_specific_doc

    print("Simplext Passed All Tests")

def cbst_tests(path):
    cbst_full_loader = CBSTLoader(keep_subdivisions=False)
    cbst_split_loader = CBSTLoader(keep_subdivisions=True)

    cbst_full = cbst_full_loader.load(path)[0]

    assert len(cbst_full.documents) == 6

    has_specific_doc = False
    for document in cbst_full.documents:
        if document.original_items[0] == "Bernoulli gabe hegan":
            has_specific_doc = True
            assert document.original_items[-1] == "Azken batean, hori da hegan egitearen sekretua."
            assert document.simplified_items[0] == "Bernoulli gabe hegan egiten dugu."
            assert document.simplified_items[-1] == "Azken batean, hori da hegan egitearen sekretua."
            assert document.original_to_simplified_alignment == [[0], [1], [2], [3], [4, 5], [6], [7], [8], [9], [10], [11], [12, 13], [14, 15], [16], [17], [18], [19, 20, 21], [22, 23, 24], [25], [26, 27], [28], [29, 30, 31], [32, 33], [34], [35, 36], [37], [38, 39], [40], [41, 42], [43], [44, 45], [46], [47], [48, 49, 50], [51], [52], [53, 54], [55], [56], [57], [58, 59], [60], [61], [62], [62], [63], [64], [65, 66], [67], [68], [69], [70], [71], [72], [73, 74, 75], [76, 77, 78], [79, 80], [81], [82], [83], [84, 85], [86, 87], [88, 89], [90], [91], [92], [93, 94, 95], [96], [97], [98, 99, 100], [101], [102], [103], [104], [105], [106], [107], [108, 109], [110], [111], [112, 113], [114], [115], [116, 117], [118], [119], [120], [121], [122]]
            assert document.simplified_to_original_alignment == [[0], [1], [2], [3], [3], [4], [5], [6], [7], [8], [9], [10], [11], [11], [12], [12], [13], [14], [15], [16], [16], [16], [17], [17], [17], [18], [19], [19], [20], [21], [21], [21], [22], [22], [23], [24], [24], [25], [26], [26], [27], [28], [28], [29], [30], [30], [31], [32], [33], [33], [33], [34], [35], [36], [36], [37], [38], [39], [40], [40], [41], [42], [43, 44], [45], [46], [47], [47], [48], [49], [50], [51], [52], [53], [54], [54], [54], [55], [55], [55], [56], [56], [57], [58], [59], [60], [60], [61], [61], [62], [62], [63], [64], [65], [66], [66], [66], [67], [68], [69], [69], [69], [70], [71], [72], [73], [74], [75], [76], [77], [77], [78], [79], [80], [80], [81], [82], [83], [83], [84], [85], [86], [87], [88]]
            break

    assert has_specific_doc

    cbst_str, cbst_int = cbst_split_loader.load(path)

    assert len(cbst_str.documents) == 3
    assert len(cbst_int.documents) == 3

    has_specific_doc = False
    for document in cbst_str.documents:
        if document.original_items[0] == "Bernoulli gabe hegan":
            has_specific_doc = True
            assert document.original_items[-1] == "Azken batean, hori da hegan egitearen sekretua."
            assert document.simplified_items[0] == "Bernoulli gabe hegan egiten dugu."
            assert document.simplified_items[-1] == "Azken batean, hori da hegan egitearen sekretua."
            assert document.original_to_simplified_alignment == [[0], [1], [2], [3], [4, 5], [6], [7], [8], [9], [10], [11], [12, 13], [14, 15], [16], [17], [18], [19, 20, 21], [22, 23, 24], [25], [26, 27], [28], [29, 30, 31], [32, 33], [34], [35, 36], [37], [38, 39], [40], [41, 42], [43], [44, 45], [46], [47], [48, 49, 50], [51], [52], [53, 54], [55], [56], [57], [58, 59], [60], [61], [62], [62], [63], [64], [65, 66], [67], [68], [69], [70], [71], [72], [73, 74, 75], [76, 77, 78], [79, 80], [81], [82], [83], [84, 85], [86, 87], [88, 89], [90], [91], [92], [93, 94, 95], [96], [97], [98, 99, 100], [101], [102], [103], [104], [105], [106], [107], [108, 109], [110], [111], [112, 113], [114], [115], [116, 117], [118], [119], [120], [121], [122]]
            assert document.simplified_to_original_alignment == [[0], [1], [2], [3], [3], [4], [5], [6], [7], [8], [9], [10], [11], [11], [12], [12], [13], [14], [15], [16], [16], [16], [17], [17], [17], [18], [19], [19], [20], [21], [21], [21], [22], [22], [23], [24], [24], [25], [26], [26], [27], [28], [28], [29], [30], [30], [31], [32], [33], [33], [33], [34], [35], [36], [36], [37], [38], [39], [40], [40], [41], [42], [43, 44], [45], [46], [47], [47], [48], [49], [50], [51], [52], [53], [54], [54], [54], [55], [55], [55], [56], [56], [57], [58], [59], [60], [60], [61], [61], [62], [62], [63], [64], [65], [66], [66], [66], [67], [68], [69], [69], [69], [70], [71], [72], [73], [74], [75], [76], [77], [77], [78], [79], [80], [80], [81], [82], [83], [83], [84], [85], [86], [87], [88]]
            break

    assert has_specific_doc

    print("CBST Passed All Tests")

def porsimples_tests(path):
    porsimples_full_loader = PorSimplesLoader(keep_strong_natural_split=False, keep_subdivisions=False)
    porsimples_folha_zh_loader = PorSimplesLoader(keep_strong_natural_split=False, keep_subdivisions=True)
    porsimples_nat_strong_loader = PorSimplesLoader(keep_strong_natural_split=True, keep_subdivisions=False)
    porsimples_all_split_loader = PorSimplesLoader(keep_strong_natural_split=True, keep_subdivisions=True)

    porsimples_full = porsimples_full_loader.load(path)[0]

    assert len(porsimples_full.documents) == 308

    has_specific_doc = False
    for document in porsimples_full.documents:
        if document.original_items[0] == "Quem estava torcendo para o Cristo Redentor se tornar uma das novas maravilhas do mundo tem hoje a última chance de dar uma forcinha para o candidato brasileiro. ":
            has_specific_doc = True
            assert document.original_items[-1] == "Apesar das boas intenções, a Organização das Nações Unidas para a Educação, a Ciência e a Cultura (Unesco) tratou de se desvincular da escolha"
            assert document.simplified_items[0] == "Quem estava torcendo para o Cristo Redentor se tornar uma das novas maravilhas do mundo tem hoje a última chance de votar nele. "
            assert document.simplified_items[-1] == "Apesar das boas intenções, a Organização das Nações Unidas para a Educação, a Ciência e a Cultura (Unesco) tratou de se desligar da escolha."
            assert document.original_to_simplified_alignment == [[0], [1, 2, 3], [4, 5], [6, 7, 8, 9], [10, 11], [12, 13, 14, 15, 16], [17, 18, 19, 20], [21, 22, 23, 24], [25, 26, 27], [28]]
            assert document.simplified_to_original_alignment == [[0], [1], [1], [1], [2], [2], [3], [3], [3], [3], [4], [4], [5], [5], [5], [5], [5], [6], [6], [6], [6], [7], [7], [7], [7], [8], [8], [8], [9]]
            break

    assert has_specific_doc

    porsimples_zh, porsimples_folha = porsimples_folha_zh_loader.load(path)

    assert len(porsimples_zh.documents) == 208
    assert len(porsimples_folha.documents) == 100

    has_specific_doc = False
    for document in porsimples_zh.documents:
        if document.original_items[0] == "Quem estava torcendo para o Cristo Redentor se tornar uma das novas maravilhas do mundo tem hoje a última chance de dar uma forcinha para o candidato brasileiro. ":
            has_specific_doc = True
            assert document.original_items[-1] == "Apesar das boas intenções, a Organização das Nações Unidas para a Educação, a Ciência e a Cultura (Unesco) tratou de se desvincular da escolha"
            assert document.simplified_items[0] == "Quem estava torcendo para o Cristo Redentor se tornar uma das novas maravilhas do mundo tem hoje a última chance de votar nele. "
            assert document.simplified_items[-1] == "Apesar das boas intenções, a Organização das Nações Unidas para a Educação, a Ciência e a Cultura (Unesco) tratou de se desligar da escolha."
            assert document.original_to_simplified_alignment == [[0], [1, 2, 3], [4, 5], [6, 7, 8, 9], [10, 11], [12, 13, 14, 15, 16], [17, 18, 19, 20], [21, 22, 23, 24], [25, 26, 27], [28]]
            assert document.simplified_to_original_alignment == [[0], [1], [1], [1], [2], [2], [3], [3], [3], [3], [4], [4], [5], [5], [5], [5], [5], [6], [6], [6], [6], [7], [7], [7], [7], [8], [8], [8], [9]]
            break

    assert has_specific_doc

    porsimples_natural, porsimples_strong = porsimples_nat_strong_loader.load(path)

    assert len(porsimples_natural.documents) == 154
    assert len(porsimples_strong.documents) == 154

    has_specific_doc = False
    for document in porsimples_natural.documents:
        if document.original_items[0] == "O vôo da Varig.":
            has_specific_doc = True
            assert document.original_items[-1] == "- Varig unida jamais será vencida"
            assert document.simplified_items[0] == "O vôo da Varig."
            assert document.simplified_items[-1] == "Varig unida jamais será vencida."
            assert document.original_to_simplified_alignment == [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9, 10, 11, 12], [13], [14], [15], [16], [17], [18], [19], [20], [21], [22], [23], [24], [25, 26], [27], [28], [29, 30], [31], [32], [33], [34], [35]]
            assert document.simplified_to_original_alignment == [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [9], [9], [9], [10], [11], [12], [13], [14], [15], [16], [17], [18], [19], [20], [21], [22], [22], [23], [24], [25], [25], [26], [27], [28], [29], [30], [], [], []]
            break

    assert has_specific_doc

    has_specific_doc = False
    for document in porsimples_strong.documents:
        if document.original_items[0] == "O vôo da Varig.":
            has_specific_doc = True
            assert document.original_items[-1] == "Varig unida jamais será vencida."
            assert document.simplified_items[0] == "O vôo da Varig."
            assert document.simplified_items[-1] == "Varig unida jamais será vencida"
            assert document.original_to_simplified_alignment == [[0], [1], [2, 3], [4], [5, 6], [7, 8], [9, 10], [11, 12], [13, 14, 15], [16, 17], [18], [19], [20], [21], [22], [23, 24], [25], [26], [27], [28], [29], [30], [31], [32], [33], [34], [35], [36, 37], [38, 39], [40, 41], [42], [43], [44], [45], [46], [47], [48], [49], [50]]
            assert document.simplified_to_original_alignment == [[0], [1], [2], [2], [3], [4], [4], [5], [5], [6], [6], [7], [7], [8], [8], [8], [9], [9], [10], [11], [12], [13], [14], [15], [15], [16], [17], [18], [19], [20], [21], [22], [23], [24], [25], [26], [27], [27], [28], [28], [29], [29], [30], [31], [32], [33], [34], [35], [36], [37], [38]]
            break

    assert has_specific_doc

    ps_zh_nat, ps_zh_strong, ps_folha_nat, ps_folha_strong = porsimples_all_split_loader.load(path)

    assert len(ps_zh_nat.documents) == 104
    assert len(ps_zh_strong.documents) == 104
    assert len(ps_folha_nat.documents) == 50
    assert len(ps_folha_strong.documents) == 50

    has_specific_doc = False
    for document in ps_zh_nat.documents:
        if document.original_items[0] == "O vôo da Varig.":
            has_specific_doc = True
            assert document.original_items[-1] == "- Varig unida jamais será vencida"
            assert document.simplified_items[0] == "O vôo da Varig."
            assert document.simplified_items[-1] == "Varig unida jamais será vencida."
            assert document.original_to_simplified_alignment == [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9, 10, 11, 12], [13], [14], [15], [16], [17], [18], [19], [20], [21], [22], [23], [24], [25, 26], [27], [28], [29, 30], [31], [32], [33], [34], [35]]
            assert document.simplified_to_original_alignment == [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [9], [9], [9], [10], [11], [12], [13], [14], [15], [16], [17], [18], [19], [20], [21], [22], [22], [23], [24], [25], [25], [26], [27], [28], [29], [30], [], [], []]
            break

    assert has_specific_doc

    has_specific_doc = False
    for document in ps_folha_nat.documents:
        if document.original_items[0] == "O ano era 1978. ":
            has_specific_doc = True
            assert document.original_items[-1] == "Silva adquiriu uma tela de retenção com 150 metros, que deve ser instalada para isolar o trecho da barragem mais usado pelos banhistas, com 3,7 mil hectares de área"
            assert document.simplified_items[0] == "O ano era 1978. "
            assert document.simplified_items[-1] == "O trecho tem 3,7 mil hectares de área"
            assert document.original_to_simplified_alignment == [[0], [1, 2], [3], [4, 5], [6], [7], [8], [9], [10], [11, 12, 13], [14, 15], [16, 17], [18], [19, 20], [21, 22], [23, 24, 25]]
            assert document.simplified_to_original_alignment == [[0], [1], [1], [2], [3], [3], [4], [5], [6], [7], [8], [9], [9], [9], [10], [10], [11], [11], [12], [13], [13], [14], [14], [15], [15], [15]]
            break

    assert has_specific_doc

    print("Porsimples Passed All Tests")

def simpitiki_tests(path):
    simpitiki_full_loader = SimpitikiLoader(keep_subdivisions=False)
    simpitiki_split_loader = SimpitikiLoader(keep_subdivisions=True)

    simpitiki_full = simpitiki_full_loader.load(path)[0]

    assert len(simpitiki_full.documents) == 2

    has_specific_doc = False
    for document in simpitiki_full.documents:
        if document.original_items[0] == "Si esprime così la volontà di forma e di espressione dell'architetto in rispondenza al suo sentire estetico e artistico.":
            has_specific_doc = True
            assert document.original_items[-1] == "Nella provincia di Grosseto, hanno determinato locali affioramenti sulla sponda occidentale del Monte Argentario con lunità di Cala Grande (argilloscisti, calcari neri e ofioliti), lungo la costa occidentale dell'Isola del Giglio e nell'area del Poggio di Moscona a nord-est della città di Grosseto.\n\nLe unità austroalpine, interna ed esterna, costituiscono un dominio continentale che ha avuto origine nel Giurassico superiore con la contemporanea formazione del bacino ligure. Tali unità si collocano tra la zona oceanica, a ovest, e il dominio toscano, a est.\n\nL'unità astroalpina interna è divisa a ovest dal dominio ligure esterno, nel punto di passaggio a livello basale dalla crosta continentale sialica a quella oceanica simatica;"
            assert document.simplified_items[0] == "Si esprime così la volontà di espressione dell'architetto in rispondenza al suo sentire estetico e artistico."
            assert document.simplified_items[-1] == "Nella provincia di Grosseto, hanno determinato locali affioramenti sulla sponda occidentale del Monte Argentario con lunità di Cala Grande (argilloscisti, calcari neri e ofioliti), lungo la costa occidentale dell'Isola del Giglio e nell'area del Poggio di Moscona a nord-est della città di Grosseto.\n\nLe unità austroalpine, interna ed esterna, costituiscono un dominio continentale che ha avuto origine nel Giurassico superiore con la contemporanea formazione del bacino ligure. Tali unità si collocano tra la zona oceanica, a ovest, e il dominio toscano, a est.\n\nL'unità astroalpina interna divisa a ovest dal dominio ligure esterno, nel punto di passaggio a livello basale dalla crosta continentale sialica a quella oceanica simatica;"
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    simpitiki_trento, simpitiki_itwiki = simpitiki_split_loader.load(path)

    assert len(simpitiki_trento.documents) == 1
    assert len(simpitiki_itwiki.documents) == 1

    has_specific_doc = False
    for document in simpitiki_trento.documents:
        if document.original_items[0] == "REQUISITI PER L'ACCESSO":
            has_specific_doc = True
            assert document.original_items[-1] == "In particolare, andranno rilevati e descritti tutti gli elementi di criticità paesaggistica, insiti nel progetto, e andranno messi in relazione a quanto è stato operato, per eliminare o mitigare tali criticità (impatti), garantendo così un migliore inserimento paesaggistico dell'intervento."
            assert document.simplified_items[0] == "REQUISITI PER ACCEDERE"
            assert document.simplified_items[-1] == "In particolare, andranno rilevati e descritti tutti gli elementi di criticità paesaggistica, insiti nel progetto, e andranno messi in relazione a quanto è stato operato, per eliminare o mitigare tali criticità (impatti), garantendo così un migliore inserimento nel paesaggio dell'intervento."
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    print("Simpitiki Passed All Tests")

def terence_teacher_tests(path):
    terence_teacher_full_loader = TerenceTeacherLoader(keep_subdivisions=False)
    terence_teacher_split_loader = TerenceTeacherLoader(keep_subdivisions=True)

    terence_teacher_full = terence_teacher_full_loader.load(path)[0]

    assert len(terence_teacher_full.documents) == 50

    has_specific_doc = False
    for document in terence_teacher_full.documents:
        if document.original_items[0] == "In una casa c’ erano molti topi.":
            has_specific_doc = True
            assert document.original_items[-1] == "La favola insegna che gli uomini prudenti, quando hanno fatto esperienza della malvagità di alcuni, non si lasciano più ingannare dalle loro finzioni."
            assert document.simplified_items[0] == "In una casa ci sono molti topi."
            assert document.simplified_items[-1] == "La favola insegna che gli uomini prudenti, quando hanno fatto esperienza della cattiveria di alcuni, non si lasciano più imbrogliare dalle loro finzioni."
            assert document.original_to_simplified_alignment == [[0], [1], [2], [], [3], [4], [5]]
            assert document.simplified_to_original_alignment == [[0], [1], [2], [4], [5], [6]]
            break

    assert has_specific_doc

    terence, teacher = terence_teacher_split_loader.load(path)

    assert len(terence.documents) == 32
    assert len(teacher.documents) == 18

    has_specific_doc = False
    for document in terence.documents:
        if document.original_items[0] == "Era il giorno di Mezza Estate e Ugolino aveva invitato a pranzo il suo amico Pietro per festeggiare allegramente il suo compleanno.":
            has_specific_doc = True
            assert document.original_items[-1] == "Da quel giorno, ad ogni compleanno Ugolino e Pietro al momento del dolce chiudono gli occhi, per immaginare di nuovo l’indimenticabile sapore del dolce forchetta."
            assert document.simplified_items[0] == "Era un giorno d’estate e Ugolino aveva invitato a pranzo il suo amico Pietro per festeggiare allegramente il suo compleanno."
            assert document.simplified_items[-1] == "Da quel giorno, ad ogni compleanno Ugolino e Pietro al momento del dolce chiudono gli occhi, per pensare di nuovo al sapore del dolce forchetta."
            assert document.original_to_simplified_alignment == [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [15], [16], [17], [18], [19], [20], [21], [22], [23]]
            assert document.simplified_to_original_alignment == [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [15], [16], [17], [18], [19], [20], [21], [22], [23]]
            break

    assert has_specific_doc

    print("Terence Teacher Passed All Tests")

def paccssit_tests(path):
    paccssit_loader = PaCCSSIT_Loader()

    paccssit = paccssit_loader.load(path)[0]

    assert len(paccssit.documents) == 1

    has_specific_doc = False
    for document in paccssit.documents:
        if document.original_items[0] == "Ma questo a cosa servirebbe ?":
            has_specific_doc = True
            assert document.original_items[-1] == "Rinvia , quindi , ad altra seduta il seguito dell' esame del provvedimento . "
            assert document.simplified_items[0] == "A che servono queste cose ? "
            assert document.simplified_items[-1] == "Rinvia pertanto il seguito dell' esame del provvedimento ad altra seduta ."
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    print("PaCCSS-IT Passed All Tests")

def clear_tests(path):
    clear_loader = CLEARLoader(keep_train_test_split=False)

    clear = clear_loader.load(path)[0]

    assert len(clear.documents) == 3

    has_specific_doc = False
    for document in clear.documents:
        if document.original_items[0] == "aucune preuve n' indiquait que l' entraînement vocal direct ou indirect , ou l' association des deux , est efficace dans l' amélioration des résultats du fonctionnement vocal auto-évalués par rapport à l' absence d' intervention":
            has_specific_doc = True
            assert document.original_items[-1] == "la première technique consiste à retirer progressivement la carie en deux visites à plusieurs mois d' intervalle , permettant ainsi à la pulpe dentaire de laisser reposer la dentine de réparation ( technique d' excavation par étapes )"
            assert document.simplified_items[0] == "aucune preuve n' indiquait que l' entraînement vocale direct ou indirect , ou l' association des deux , est efficace dans l' amélioration du fonctionnement vocal lorsqu' il était mesuré au moyen des résultats rapportés par les patients et comparé à l' absence d' intervention"
            assert document.simplified_items[-1] == "- excavation par étapes - cette technique permet de retirer progressivement une carie en deux visites à quelques mois d' intervalle , permettant ainsi à la pulpe dentaire de se régénérer et de laisser la dentine se reposer"
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    clear_train, clear_valid, clear_test = CLEARLoader(keep_train_test_split=True).load(path)
    
    has_specific_doc = False
    for document in clear_train.documents:
        if document.original_items[0] == "aucune preuve n' indiquait que l' entraînement vocal direct ou indirect , ou l' association des deux , est efficace dans l' amélioration des résultats du fonctionnement vocal auto-évalués par rapport à l' absence d' intervention":
            has_specific_doc = True
            assert document.original_items[-1] == "la première technique consiste à retirer progressivement la carie en deux visites à plusieurs mois d' intervalle , permettant ainsi à la pulpe dentaire de laisser reposer la dentine de réparation ( technique d' excavation par étapes )"
            assert document.simplified_items[0] == "aucune preuve n' indiquait que l' entraînement vocale direct ou indirect , ou l' association des deux , est efficace dans l' amélioration du fonctionnement vocal lorsqu' il était mesuré au moyen des résultats rapportés par les patients et comparé à l' absence d' intervention"
            assert document.simplified_items[-1] == "- excavation par étapes - cette technique permet de retirer progressivement une carie en deux visites à quelques mois d' intervalle , permettant ainsi à la pulpe dentaire de se régénérer et de laisser la dentine se reposer"
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    has_specific_doc = False
    for document in clear_valid.documents:
        if document.original_items[0] == "l' effet des interventions dans les pays dans lesquels existe une législation sur le port du casque de vélo et dans les pays à faible revenu et à revenu intermédiaire doit également être étudié":
            has_specific_doc = True
            assert document.original_items[-1] == "l' échographie à visée diagnostique est une technologie électronique sophistiquée qui utilise des impulsions d' ondes sonores à haute fréquence pour produire une image"
            assert document.simplified_items[0] == "l' effet des programmes de promotion du port du casque dans les pays dans lesquels existe une législation sur le port du casque de vélo et dans les pays à faible revenu et à revenu intermédiaire doit également être étudié"
            assert document.simplified_items[-1] == "l' échographie est une technologie électronique qui utilise la réflexion d' impulsions d' ondes sonores à haute fréquence pour produire une image"
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    has_specific_doc = False
    for document in clear_test.documents:
        if document.original_items[0] == "nous n' avons pas trouvé d' essais contrôlés prospectifs , randomisés ou non , portant sur un traitement pour le syndrome poems":
            has_specific_doc = True
            assert document.original_items[-1] == "de nombreux pansements et applications topiques différents sont utilisés pour couvrir les plaies chirurgicales en cicatrisation par seconde intention"
            assert document.simplified_items[0] == "cette revue n' a pas trouvé d' essais contrôlés randomisés portant sur des traitements du syndrome poems"
            assert document.simplified_items[-1] == "pansements et agents topiques pour aider les plaies chirurgicales à cicatriser par seconde intention"
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    print("CLEAR Passed All Tests")

def wiki_large_fr_tests(path):
    wiki_large_fr_loader = WikiLargeFRLoader(keep_train_test_split=True, allow_sentence_splits=False)

    wfr_train, wfr_valid, wfr_test = wiki_large_fr_loader.load(path)

    wfr = Corpus(wfr_train.documents + wfr_valid.documents + wfr_test.documents, name="WikiLargeFR Corpus", language="French")

    assert len(wfr.documents) == 3

    has_specific_doc = False
    for document in wfr.documents:
        if document.original_items[0] == "Il y a des preuves manuscrites qu'Austen a continuÃ © Ã travailler sur ces morceaux aussi tard que la pÃ © riode 1809 â €\"11, et que sa nièce et son neveu, Anna et James Edward Austen, ont fait d'autres ajouts jusqu'en 1814.":
            has_specific_doc = True
            assert document.original_items[-1] == "Dans l'ensemble, Juventus a remporté 51 compétitions officielles, plus que toute autre équipe dans le pays ; 40 dans la première division nationale, qui est aussi un record, et 11 compétitions internationales officielles, ce qui fait d'eux, dans ce dernier cas, le deuxième club italien le plus réussi dans la compétition européenne."
            assert document.simplified_items[0] == "Il y a des preuves qu'Austen a continué à travailler sur ces pièces plus tard dans la vie. Son neveu et sa nièce, James Edward et Anna Austen, ont peut-être fait d'autres ajouts à son œuvre vers 1814."
            assert document.simplified_items[-1] == "Le club est l \"équipe la plus réussie de l'histoire du football italien : le club a remporté 51 trophées officiels, plus que toute autre équipe dans le pays ; 40 en Italie, qui est aussi un record, et 11 dans les compétitions européennes et mondiales."
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc
    
    has_specific_doc = False
    for document in wfr_train.documents:
        if document.original_items[0] == "Il y a des preuves manuscrites qu'Austen a continuÃ © Ã travailler sur ces morceaux aussi tard que la pÃ © riode 1809 â €\"11, et que sa nièce et son neveu, Anna et James Edward Austen, ont fait d'autres ajouts jusqu'en 1814.":
            has_specific_doc = True
            assert document.original_items[-1] == "Dans l'ensemble, Juventus a remporté 51 compétitions officielles, plus que toute autre équipe dans le pays ; 40 dans la première division nationale, qui est aussi un record, et 11 compétitions internationales officielles, ce qui fait d'eux, dans ce dernier cas, le deuxième club italien le plus réussi dans la compétition européenne."
            assert document.simplified_items[0] == "Il y a des preuves qu'Austen a continué à travailler sur ces pièces plus tard dans la vie. Son neveu et sa nièce, James Edward et Anna Austen, ont peut-être fait d'autres ajouts à son œuvre vers 1814."
            assert document.simplified_items[-1] == "Le club est l \"équipe la plus réussie de l'histoire du football italien : le club a remporté 51 trophées officiels, plus que toute autre équipe dans le pays ; 40 en Italie, qui est aussi un record, et 11 dans les compétitions européennes et mondiales."
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    has_specific_doc = False
    for document in wfr_valid.documents:
        if document.original_items[0] == "Le haut-sorabe est une langue minoritaire parlée par les Sorabes en Allemagne dans la province historique de Haute Lusace - LRB- Hornja Å uÅ 3 \ / 4 ica en sorabe -RRB-, qui fait aujourd'hui partie de la Saxe.":
            has_specific_doc = True
            assert document.original_items[-1] == "Tikal, l'une des plus grandes des villes mayas classiques, n'avait pas d'eau autre que ce qui était recueilli dans l'eau de pluie et stocké dans dix réservoirs."
            assert document.simplified_items[0] == "Il y a environ 40 000 locuteurs du haut-sorabe vivant en Saxe. Le haut-sorabe est une langue minoritaire en Allemagne selon la Charte européenne des langues régionales ou minoritaires."
            assert document.simplified_items[-1] == "Les ruines se trouvent dans la forêt ombrophile des basses terres, mais Tikal n'avait pas d'eau autre que ce qui était recueilli dans l'eau de pluie et stocké sous terre."
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    has_specific_doc = False
    for document in wfr_test.documents:
        if document.original_items[0] == "Un aspect des conflits armés est constitué principalement par l'armée soudanaise et les Janjaouid, un groupe de milices soudanaises recrutées essentiellement parmi les tribus afro-arabes Abbala de la région nord de Rizeigat au Soudan.":
            has_specific_doc = True
            assert document.original_items[-1] == "Gable remporte également une nomination aux Oscars lorsqu'il dépeint Fletcher Christian dans Mutiny on the Bounty de 1935."
            assert document.simplified_items[0] == "L'un des aspects des conflits armés est constitué par l'armée soudanaise et les Janjaouid, une milice soudanaise recrutée parmi les tribus afro-arabes Abbala de la région nord de Rizeigat, au Soudan."
            assert document.simplified_items[-1] == "Gable obtient également une nomination aux Oscars pour son interprétation de Fletcher Christian dans le film de 1935 Mutiny on the Bounty."
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    print("WikiLargeFR Passed All Tests")

def dsim_tests(path):
    dsim_loader = DSimLoader()

    dsim = dsim_loader.load(path)[0]

    assert len(dsim.documents) == 1

    has_specific_doc = False
    for document in dsim.documents:
        if document.original_items[0] == "Forbrugerråd : Skat overdriver om kopivarer .":
            has_specific_doc = True
            assert document.original_items[-1] == "Det er uundgåeligt , at man indimellem har konflikter , men det er forældrene , der skal sørge for , at den situation bliver så behagelig som muligt , så konflikten ikke kommer til at dominere hele måltidet , siger Kirsten Muus . "
            assert document.simplified_items[0] == "Skat afviser kritikken ."
            assert document.simplified_items[-1] == "Konflikter må ikke dominere hele måltidet , siger Kirsten Muus . "
            assert document.original_to_simplified_alignment[:100] == [[0], [1], [2], [3, 4], [5], [6, 7], [8], [9], [10], [11], [12], [13], [14], [15], [16], [17], [18], [19], [20], [21], [22], [23, 24], [25], [26, 27], [28], [29], [30, 31], [32], [33], [34], [35], [36], [37, 38], [39], [40], [41], [42, 43], [44], [45, 46, 47], [48], [49], [50], [51], [52], [53], [54, 55], [56, 57], [58], [59], [60, 61], [62], [63, 64], [65, 66], [67], [68, 69], [70, 71], [72], [73], [74, 75], [76], [77, 78], [79], [80], [81], [82], [83], [84], [85, 86], [87], [88], [89, 90], [91], [92], [93, 94], [95, 96], [97, 98], [99], [100], [101], [102], [103], [104], [105, 106], [107, 108], [109, 110], [111, 112], [113], [114], [115], [116], [117], [118], [119], [120], [121], [122], [123], [124], [125], [126, 127]]
            assert document.simplified_to_original_alignment[:100] == [[0], [1], [2], [3], [3], [4], [5], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [15], [16], [17], [18], [19], [20], [21], [21], [22], [23], [23], [24], [25], [26], [26], [27], [28], [29], [30], [31], [32], [32], [33], [34], [35], [36], [36], [37], [38], [38], [38], [39], [40], [41], [42], [43], [44], [45], [45], [46], [46], [47], [48], [49], [49], [50], [51], [51], [52], [52], [53], [54], [54], [55], [55], [56], [57], [58], [58], [59], [60], [60], [61], [62], [63], [64], [65], [66], [67], [67], [68], [69], [70], [70], [71], [72], [73], [73], [74], [74], [75], [75], [76]]
            assert document.original_to_simplified_alignment[-100:] == [[60409, 60410], [60411], [60412], [60413], [60414], [60415], [60416, 60417], [60418], [60419], [60420], [60421], [60422], [60423], [60424], [60425], [60426], [60427], [60428], [60429], [60430], [60431], [60432], [60433], [60434], [60435], [60436], [60437], [60438], [60439], [60440], [60441, 60442], [60443], [60444, 60445, 60446], [60447], [60448], [60449], [60450], [60451], [60452, 60453], [60454], [60455], [60456], [60457, 60458], [60459], [60460], [60461], [60462, 60463], [60464], [60465], [60466, 60467], [60468], [60469, 60470], [60471], [60472], [60473, 60474], [60475], [60476], [60477], [60478], [60479], [60480], [60481, 60482], [60483], [60484], [60485], [60486], [60487, 60488], [60489, 60490], [60491, 60492], [60493], [60494], [60495, 60496], [60497], [60498], [60499], [60500], [60501], [60502], [60503], [60504, 60505], [60506], [60507], [60508], [60509], [60510], [60511], [60512], [60513], [60514], [60515, 60516], [60517], [60518], [60519], [60520], [60521], [60522], [60523], [60524], [60525], [60526, 60527]]
            assert document.simplified_to_original_alignment[-100:] == [[47804], [47805], [47806], [47807], [47808], [47809], [47810], [47811], [47812], [47813], [47814], [47815], [47816], [47817], [47817], [47818], [47819], [47819], [47819], [47820], [47821], [47822], [47823], [47824], [47825], [47825], [47826], [47827], [47828], [47829], [47829], [47830], [47831], [47832], [47833], [47833], [47834], [47835], [47836], [47836], [47837], [47838], [47838], [47839], [47840], [47841], [47841], [47842], [47843], [47844], [47845], [47846], [47847], [47848], [47848], [47849], [47850], [47851], [47852], [47853], [47853], [47854], [47854], [47855], [47855], [47856], [47857], [47858], [47858], [47859], [47860], [47861], [47862], [47863], [47864], [47865], [47866], [47866], [47867], [47868], [47869], [47870], [47871], [47872], [47873], [47874], [47875], [47876], [47876], [47877], [47878], [47879], [47880], [47881], [47882], [47883], [47884], [47885], [47886], [47886]]
            break

    assert has_specific_doc

    print("DSim Passed All Tests")

def geolino_tests(path):
    geolino_loader = GEOLinoLoader(keep_train_test_split=False)

    geolino = geolino_loader.load(path)[0]

    assert len(geolino.documents) == 2

    has_specific_doc = False
    for document in geolino.documents:
        if document.original_items[0] == "Sein Assistent Tommaso Massini brach sich bei einem Probeflug ein Bein.":
            has_specific_doc = True
            assert document.original_items[-1] == "Die Vorbereitungen dafür dauerten anderthalb Jahre."
            assert document.simplified_items[0] == "Sein Assistent Tommaso Massini brach sich bei einem Probeflug ein Bein."
            assert document.simplified_items[-1] == "Die Vorbereitungen dafür dauerten anderthalb Jahre."
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    geolino_test, geolino_valid = GEOLinoLoader(keep_train_test_split=True).load(path)

    assert len(geolino_test.documents) == 1
    assert len(geolino_valid.documents) == 1

    has_specific_doc = False
    for document in geolino_test.documents:
        if document.original_items[0] == "Sein Assistent Tommaso Massini brach sich bei einem Probeflug ein Bein.":
            has_specific_doc = True
            assert document.original_items[-1] == "Die Vorbereitungen dafür dauerten anderthalb Jahre."
            assert document.simplified_items[0] == "Sein Assistent Tommaso Massini brach sich bei einem Probeflug ein Bein."
            assert document.simplified_items[-1] == "Die Vorbereitungen dafür dauerten anderthalb Jahre."
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    has_specific_doc = False
    for document in geolino_valid.documents:
        if document.original_items[0] == "Irgendwann dann bereiten die 48 riesigen Zähne im Orca-Kiefer dem Leiden mit einem Haps ein Ende...":
            has_specific_doc = True
            assert document.original_items[-1] == "Der Schwanz, der auch Rute genannt wird, ist lang, buschig und gerade."
            assert document.simplified_items[0] == "Irgendwann beenden die 48 Zähne im Maul von dem Orca das Leiden..."
            assert document.simplified_items[-1] == "Der Schwanz ist lang, buschig und gerade. Der Schwanz wird auch Rute genannt."
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    print("GEOLino Passed All Tests")

def easy_japanese_tests(path):
    easy_japanese_loader = EasyJapaneseLoader()

    easy_japanese = easy_japanese_loader.load(path)[0]

    assert len(easy_japanese.documents) == 1

    has_specific_doc = False
    for document in easy_japanese.documents:
        if document.original_items[0] == "誰が一番に着くか私には分かりません。":
            has_specific_doc = True
            assert document.original_items[-1] == "彼はいらだちながら思った。"
            assert document.simplified_items[0] == "誰が一番に着くか私には分かりません。"
            assert document.simplified_items[-1] == "彼は怒りながら思った。"
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    print("Easy Japanese Passed All Tests")


def easy_japanese_extended_tests(path):
    easy_japanese_ext_main, easy_japanese_ext_eval = EasyJapaneseExtendedLoader(keep_subdivisions=True).load(path)

    easy_japanese_extended = Corpus(easy_japanese_ext_main.documents + easy_japanese_ext_eval.documents, name='Easy Japanese Extended', language='Japanese')

    assert len(easy_japanese_extended.documents) == 2

    has_specific_doc = False
    for document in easy_japanese_extended.documents:
        if document.original_items[0] == "あなたのご都合の良い時にその仕事をして下さい。":
            has_specific_doc = True
            assert document.original_items[-1] == "会社は深刻な営業不振に陥っている。"
            assert document.simplified_items[0] == "あなたの具合の良い時にその仕事をしください。"
            assert document.simplified_items[-1] == "会社の経営状態が悪い。"
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    assert len(easy_japanese_ext_main.documents) == 1
    assert len(easy_japanese_ext_eval.documents) == 1

    has_specific_doc = False
    for document in easy_japanese_ext_main.documents:
        if document.original_items[0] == "あなたのご都合の良い時にその仕事をして下さい。":
            has_specific_doc = True
            assert document.original_items[-1] == "会社は深刻な営業不振に陥っている。"
            assert document.simplified_items[0] == "あなたの具合の良い時にその仕事をしください。"
            assert document.simplified_items[-1] == "会社の経営状態が悪い。"
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    has_specific_doc = False
    for document in easy_japanese_ext_eval.documents:
        if document.original_items[0] == "そこに署名してください。":
            has_specific_doc = True
            assert document.original_items[-1] == "ゲームカセット一つ一つにかなりのお金を払う。"
            assert document.simplified_items[0] == "そこにあなたの名前を書いてください。"
            assert document.simplified_items[-1] == "コンピューターゲームをやるのにはお金が多くいる"
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    print("Easy Japanese Extended Passed All Tests")

def text_complexity_de_tests(path):
    text_complexity_de = TextComplexityDELoader().load(path)[0]

    assert len(text_complexity_de.documents) == 23

    has_specific_doc = False
    for document in text_complexity_de.documents:
        if document.original_items[0] == "Wegen dieser leichten Vergänglichkeit wurde ,Seifenblase‘ zu einer Metapher für etwas, das zwar anziehend, aber dennoch inhalts- und gehaltlos ist.":
            has_specific_doc = True
            assert document.original_items[-1] == "Die Erzeugung von Seifenblasen ist möglich, da die Oberfläche einer Flüssigkeit – in diesem Falle des Wassers – eine Oberflächenspannung besitzt, die zu einem elastischen Verhalten der Oberfläche führt."
            assert document.simplified_items[0] == "Weil Seifenblasen nicht lange halten, wurden sie zu einem  sprachlichen Ausdruck für etwas, das anziehend aber inhaltslos ist."
            assert document.simplified_items[-1] == "Die Erzeugung von Seifenblasen ist möglich, weil Flüssigkeiten - in diesem Falle Wasser - eine elastische Oberfläche besitzen."
            assert document.original_to_simplified_alignment == [[0], [1], [2], [3], [4], [5], [6]]
            assert document.simplified_to_original_alignment == [[0], [1], [2], [3], [4], [5], [6]]
            break

    assert has_specific_doc

    has_specific_doc = False
    for document in text_complexity_de.documents[::-1]:
        if document.original_items[0] == "Wesentlich durch Kings Einsatz und Wirkkraft ist das Civil Rights Movement zu einer Massenbewegung geworden, die schließlich erreicht hat, dass die Rassentrennung gesetzlich aufgehoben und das uneingeschränkte Wahlrecht für die schwarze Bevölkerung der US-Südstaaten eingeführt wurde.":
            has_specific_doc = True
            assert document.original_items[-1] == "Im Hauptfach Soziologie wurde er von Walter P. Chivers in die Problematik der Rassentrennung eingeführt; bei George D. Kelsey, dem Leiter der „School of Religion“, hörte er von Mahatma Gandhis gewaltfreiem Widerstand."
            assert document.simplified_items[0] == "Das Civil Rights Movement ist durch den Einsatz von King zu einer Massenbewegung geworden. Sie erreichte, dass die Rassentrennung gesetzlich aufgehoben wurde. Außerdem wurde das uneingeschränkte Wahlrecht für die schwarze Bevölkerung der US-Südstaaten eingeführt."
            assert document.simplified_items[-1] == "Sein Hauptfach war Soziologie. In die Problematik der Rassentrennuung führte ihn Walter C. Chievers ein. Bei dem Leiter der \"School of Religion\" George D. Kelsey hörte er von Mahatma Gandhis gewaltfreiem Widerstand."
            assert document.original_to_simplified_alignment == [[0], [1], [2], [3]]
            assert document.simplified_to_original_alignment == [[0], [1], [2], [3]]
            break

    assert has_specific_doc

    print("TextComplexityDE Passed All Tests")

def rsse_tests(path):
    rsse = RSSE_Loader(keep_train_test_split=False).load(path)[0]

    assert len(rsse.documents) == 2

    has_specific_doc = False
    for document in rsse.documents:
        if document.original_items[0] == "14 декабря 1944 года рабочий посёлок Ички был переименован в рабочий посёлок Советский, после чего поселковый совет стал называться Советским.":
            has_specific_doc = True
            assert document.original_items[-1] == "Изображение соцветия подсолнечника на щите означает и сегодняшний день в жизни Малосердобинского района."
            assert document.simplified_items[0] == "14 декабря 1944 года рабочий посёлок Ички переименован в Советский."
            assert document.simplified_items[-1] == "Подсолнечник, который изображён на щите, символизирует и сегодняшнюю жизнь Малосердобинского района."
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    rsse_dev, rsse_test = RSSE_Loader(keep_train_test_split=True).load(path)

    assert len(rsse_dev.documents) == 1
    assert len(rsse_test.documents) == 1

    has_specific_doc = False
    for document in rsse_dev.documents:
        if document.original_items[0] == "14 декабря 1944 года рабочий посёлок Ички был переименован в рабочий посёлок Советский, после чего поселковый совет стал называться Советским.":
            has_specific_doc = True
            assert document.original_items[-1] == "Изображение соцветия подсолнечника на щите означает и сегодняшний день в жизни Малосердобинского района."
            assert document.simplified_items[0] == "14 декабря 1944 года рабочий посёлок Ички переименован в Советский."
            assert document.simplified_items[-1] == "Подсолнечник, который изображён на щите, символизирует и сегодняшнюю жизнь Малосердобинского района."
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    has_specific_doc = False
    for document in rsse_test.documents:
        if document.original_items[0] == "14 апреля 2003 году архиепископом Новосибирским и Бердским Тихоном пострижен в монашество с наречением имени Феодор в честь праведного Феодора Томского.":
            has_specific_doc = True
            assert document.original_items[-1] == "Японские войска были разгромлены в Маньчжурии, Красная Армия заняла также южный Сахалин и Курильские острова."
            assert document.simplified_items[0] == "Был пострижен в монашество и получил имя Фёдор в честь Федора Томского."
            assert document.simplified_items[-1] == "Японское войско проиграло, русское войско одержало победу"
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    print("RSSE Passed All Tests")

def simplify_ur_tests(path):
    simplify_ur = SimplifyUR_Loader(allow_repeats=True).load(path)[0]

    assert len(simplify_ur.documents) == 1

    has_specific_doc = False
    for document in simplify_ur.documents:
        if document.original_items[0] == "یہ لگاتار مختلف جگہوں پر الاؤ جلا کر رکھتے ہیں":
            has_specific_doc = True
            assert document.original_items[-1] == "اس کو بچوں سے الفت ہے"
            assert document.simplified_items[0] == "یہ مسلسل مختلف جگہوں پر آگ جلا کر رکھتے ہیں"
            assert document.simplified_items[-1] == "اس کو بچوں سے محبت ہے"
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    simplify_ur_no_repeats = SimplifyUR_Loader(allow_repeats=False).load(path)[0]

    assert len(simplify_ur_no_repeats.documents) == 1

    has_specific_doc = False
    for document in simplify_ur_no_repeats.documents:
        if document.original_items[0] == "یہ لگاتار مختلف جگہوں پر الاؤ جلا کر رکھتے ہیں":
            has_specific_doc = True
            assert document.original_items[-1] == "اس کو بچوں سے الفت ہے"
            assert document.simplified_items[0] == "یہ مسلسل مختلف جگہوں پر آگ جلا کر رکھتے ہیں"
            assert document.simplified_items[-1] == "اس کو بچوں سے پیار ہے"
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    print("SimplifyUR Passed All Tests")

def german_news_tests(path):
    german_news = GermanNewsLoader(keep_subdivisions=False).load(path)[0]

    assert len(german_news.documents) == 3411

    has_specific_doc = False
    for document in german_news.documents:
        if document.original_items[0] == "1,765 Millionen Menschen ) im Ausland geboren .":
            has_specific_doc = True
            assert document.original_items[-1] == "1,765 Millionen Menschen ) im Ausland geboren ."
            assert document.simplified_items[0] == "Bürger in Österreich wurde im Ausland geboren"
            assert document.simplified_items[-1] == "Insgesamt sind das 1,765 Millionen Bürger in Österreich , die im Ausland geboren wurden ."
            assert document.original_to_simplified_alignment == [[0, 1]]
            assert document.simplified_to_original_alignment == [[0], [0]]
            break

    assert has_specific_doc

    german_news_a2, german_news_b1 = GermanNewsLoader(keep_subdivisions=True).load(path)

    assert len(german_news_a2.documents) == 1807
    assert len(german_news_b1.documents) == 1604

    has_specific_doc = False
    for document in german_news_a2.documents:
        if document.original_items[0] == "1,765 Millionen Menschen ) im Ausland geboren .":
            has_specific_doc = True
            assert document.original_items[-1] == "1,765 Millionen Menschen ) im Ausland geboren ."
            assert document.simplified_items[0] == "Bürger in Österreich wurde im Ausland geboren"
            assert document.simplified_items[-1] == "Insgesamt sind das 1,765 Millionen Bürger in Österreich , die im Ausland geboren wurden ."
            assert document.original_to_simplified_alignment == [[0, 1]]
            assert document.simplified_to_original_alignment == [[0], [0]]
            break

    assert has_specific_doc

    has_specific_doc = False
    for document in german_news_b1.documents:
        if document.original_items[0] == "Eine Zeugin hatte die Polizei am Donnerstag gegen 14.00 Uhr alarmiert , weil sie einen lauten Knall gehört hatte .":
            has_specific_doc = True
            assert document.original_items[-1] == "Der wegen der Bluttat im Bezirk Mistelbach vom Donnerstagnachmittag Beschuldigte ist nach Polizeiangaben geständig ."
            assert document.simplified_items[0] == "Er wurde noch am Tatort von der Polizei festgenommen und hat die Tat schon gestanden ."
            assert document.simplified_items[-1] == "Ein möglicher Grund für das Verbrechen soll aber ein Streit in der Familie sein ."
            assert document.original_to_simplified_alignment == [[0], [1]]
            assert document.simplified_to_original_alignment == [[0], [1]]
            break

    assert has_specific_doc

    print("German News Passed All Tests")

def newsela_es_tests(path):
    z_o, o_t, t_t, t_f = NewselaESLoader(keep_subdivisions=True).load(path)

    newsela_es = Corpus(z_o.documents + o_t.documents + t_t.documents + t_f.documents, name="Newsela ES Corpus", language="Spanish")

    assert len(newsela_es.documents) == 972
    assert len(z_o.documents) == 243
    assert len(o_t.documents) == 243
    assert len(t_t.documents) == 243
    assert len(t_f.documents) == 243

    has_specific_doc = False
    for document in z_o.documents:
        if document.original_items[0] == "SEATTLE — Hace poco, en una sala llena de personas dedicadas a preservar el ladino, un dialecto judío con muchos siglos de antigüedad, Doreen Alhadeff explicaba por qué estaba considerando convertirse en una ciudadana española.":
            has_specific_doc = True
            assert document.original_items[-1] == "\"No creo que en estos momentos pueda disponer de un espacio extra para recibir clases de español\", concluye."
            assert document.simplified_items[0] == "SEATTLE — Hace poco, en una sala llena de personas dedicadas a preservar el ladino, un dialecto judío de muchos siglos de antigüedad, Doreen Alhadeff explicaba por qué estaba considerando convertirse en una ciudadana española."
            assert document.simplified_items[-1] == "\"No creo que en estos momentos pueda disponer de un espacio extra para recibir clases de español\", dice."
            assert document.original_to_simplified_alignment == [[0], [1], [2], [3, 4], [5], [], [7, 8], [9], [10], [11], [12], [28], [], [], [], [], [13], [14], [15], [16], [17], [], [], [18], [19], [20], [21, 22], [], [], [], [23, 24], [25], [26], [27], [28, 28], [], [], [], [29], [30], [32], [33], [], [], [], [34], [31, 35], [], [], [], [36], [], [37], [39], [], [6, 38], [], [], [41], [], [40, 42], [43], [44], [45], [46]]
            assert document.simplified_to_original_alignment == [[0], [1], [2], [3], [3], [4], [55], [6], [6], [7], [8], [9], [10], [16], [17], [18], [19], [20], [23], [24], [25], [26], [26], [30], [30], [31], [32], [33], [11, 34, 34], [38], [39], [46], [40], [41], [45], [46], [50], [52], [55], [53], [60], [58], [60], [61], [62], [63], [64]]
            break

    assert has_specific_doc

    has_specific_doc = False
    for document in o_t.documents:
        if document.original_items[0] == "SEATTLE — Hace poco, en una sala llena de personas dedicadas a preservar el ladino, un dialecto judío de muchos siglos de antigüedad, Doreen Alhadeff explicaba por qué estaba considerando convertirse en una ciudadana española.":
            has_specific_doc = True
            assert document.original_items[-1] == "\"No creo que en estos momentos pueda disponer de un espacio extra para recibir clases de español\", dice."
            assert document.simplified_items[0] == "SEATTLE — Hace poco, Doreen Alhadeff se reunió con personas dedicadas a preservar el ladino y les explicó por qué considera convertirse en ciudadana española."
            assert document.simplified_items[-1] == "\"No creo que en estos momentos pueda disponer de un espacio extra para recibir clases de español\", dice."
            assert document.original_to_simplified_alignment == [[0, 1], [2], [3], [4, 5], [6], [7, 22], [8], [], [10, 11], [9, 12], [13], [14], [], [15], [16], [17], [18], [], [19], [20], [21], [], [], [23], [24, 25], [26], [27], [28], [29], [30], [31], [32], [33], [34], [35], [36], [], [37, 38], [39], [40], [41], [42], [43], [44], [45], [46], [47]]
            assert document.simplified_to_original_alignment == [[0], [0], [1], [2], [3], [3], [4], [5], [6], [9], [8], [8], [9], [10], [11], [13], [14], [15], [16], [18], [19], [20], [5], [23], [24], [24], [25], [26], [27], [28], [29], [30], [31], [32], [33], [34], [35], [37], [37], [38], [39], [40], [41], [42], [43], [44], [45], [46]]
            break

    assert has_specific_doc

    has_specific_doc = False
    for document in t_t.documents:
        if document.original_items[0] == "SEATTLE — Hace poco, Doreen Alhadeff se reunió con personas dedicadas a preservar el ladino y les explicó por qué considera convertirse en ciudadana española.":
            has_specific_doc = True
            assert document.original_items[-1] == "\"No creo que en estos momentos pueda disponer de un espacio extra para recibir clases de español\", dice."
            assert document.simplified_items[0] == "SEATTLE — Hace poco, Doreen Alhadeff se reunió con personas dedicadas a preservar el ladino y les explicó por qué considera convertirse en ciudadana española."
            assert document.simplified_items[-1] == "\"No creo que en estos momentos pueda disponer de tiempo extra para tomar clases de español\", dice."
            assert document.original_to_simplified_alignment == [[0], [1], [2], [3], [4, 6], [], [5], [7, 8, 9], [], [27], [13, 14], [11, 12], [15], [16, 17, 18], [19, 20, 21], [], [23], [], [22, 24, 25, 26], [], [], [10], [36], [28], [29], [30], [31], [32], [33], [], [34], [35], [], [37], [38], [39], [40], [], [], [], [41, 42], [43], [44], [45], [], [46], [47], [48]]
            assert document.simplified_to_original_alignment == [[0], [1], [2], [3], [4], [6], [4], [7], [7], [7], [21], [11], [11], [10], [10], [12], [13], [13], [13], [14], [14], [14], [18], [16], [18], [18], [18], [9], [23], [24], [25], [26], [27], [28], [30], [31], [22], [33], [34], [35], [36], [40], [40], [41], [42], [43], [45], [46], [47]]
            break

    assert has_specific_doc

    has_specific_doc = False
    for document in t_f.documents:
        if document.original_items[0] == "SEATTLE — Hace poco, Doreen Alhadeff se reunió con personas dedicadas a preservar el ladino y les explicó por qué considera convertirse en ciudadana española.":
            has_specific_doc = True
            assert document.original_items[-1] == "\"No creo que en estos momentos pueda disponer de tiempo extra para tomar clases de español\", dice."
            assert document.simplified_items[0] == "SEATTLE — Doreen Alhadeff está pensando obtener la ciudadanía española."
            assert document.simplified_items[-1] == "Él prefiere honrar a Turquía por ser \"el país que nos recibió\"."
            assert document.original_to_simplified_alignment == [[0, 1, 2], [], [], [], [3, 4], [5], [6], [7, 8], [9], [10], [], [], [26], [27], [28], [29], [30], [], [], [31], [32], [33], [], [], [12], [13], [14], [], [15, 16], [17], [18, 19], [20, 21], [22], [23], [24], [39], [11], [], [], [25, 40], [41], [], [], [], [34, 35], [36], [37, 38], [], []]
            assert document.simplified_to_original_alignment == [[0], [0], [0], [4], [4], [5], [6], [7], [7], [8], [9], [36], [24], [25], [26], [28], [28], [29], [30], [30], [31], [31], [32], [33], [34], [39], [12], [13], [14], [15], [16], [19], [20], [21], [44], [44], [45], [46], [46], [35], [39], [40]]
            break

    assert has_specific_doc

    print("Newsela ES Passed All Tests")

def ru_adapt_tests(path):
    ru_adapt = RuAdaptLoader(keep_subdivisions=False).load(path)[0]

    assert len(ru_adapt.documents) == 541

    has_specific_doc = False
    for document in ru_adapt.documents:
        if document.original_items[0] == "Василиса Прекрасная":
            has_specific_doc = True
            assert document.original_items[-1] == "— спросил царь"
            assert document.simplified_items[0] == "Жила-была красивая девушка Василиса Прекрасная. "
            assert document.simplified_items[-1] == "Так трудолюбивая, добрая девушка стала царицей."
            assert document.original_to_simplified_alignment == [[0, 9, 16, 17], [1], [2, 22], [3, 15], [4], [5], [6], [7], [8], [10], [11], [12], [13], [14, 23], [18], [19], [20], [21]]
            assert document.simplified_to_original_alignment == [[0], [1], [2], [3], [4], [5], [6], [7], [8], [0], [9], [10], [11], [12], [13], [3], [0], [0], [14], [15], [16], [17], [2], [13]]
            break

    assert has_specific_doc

    fairy, b_c, a_c, a_b, literature = RuAdaptLoader(keep_subdivisions=True).load(path)

    assert len(fairy.documents) == 9
    assert len(b_c.documents) == 266
    assert len(a_c.documents) == 62
    assert len(a_b.documents) == 61
    assert len(literature.documents) == 143

    has_specific_doc = False
    for document in fairy.documents:
        if document.original_items[0] == "Василиса Прекрасная":
            has_specific_doc = True
            assert document.original_items[-1] == "— спросил царь"
            assert document.simplified_items[0] == "Жила-была красивая девушка Василиса Прекрасная. "
            assert document.simplified_items[-1] == "Так трудолюбивая, добрая девушка стала царицей."
            assert document.original_to_simplified_alignment == [[0, 9, 16, 17], [1], [2, 22], [3, 15], [4], [5], [6], [7], [8], [10], [11], [12], [13], [14, 23], [18], [19], [20], [21]]
            assert document.simplified_to_original_alignment == [[0], [1], [2], [3], [4], [5], [6], [7], [8], [0], [9], [10], [11], [12], [13], [3], [0], [0], [14], [15], [16], [17], [2], [13]]
            break

    assert has_specific_doc

    has_specific_doc = False
    for document in b_c.documents:
        if document.original_items[0] == "Название Санкт-Петербурга (см. ":
            has_specific_doc = True
            assert document.original_items[-1] == "Ленина после его смерти в январе 1924 г."
            assert document.simplified_items[0] == "Название Санкт-Петербурга (см. "
            assert document.simplified_items[-1] == "Ленина после его смерти в январе 1924 г."
            assert document.original_to_simplified_alignment == [[0], [1], [2], [3]]
            assert document.simplified_to_original_alignment == [[0], [1], [2], [3]]
            break

    assert has_specific_doc

    has_specific_doc = False
    for document in a_c.documents:
        if document.original_items[0] == "Картина И. ":
            has_specific_doc = True
            assert document.original_items[-1] == "Устойчивое выражение золотая осень часто используется в речи, чтобы передать восхищение яркими красками природы в это время года."
            assert document.simplified_items[0] == "Картина И. "
            assert document.simplified_items[-1] == "Выражение золотая осень часто используется в речи, чтобы передать восхищение яркими красками природы в это время года."
            assert document.original_to_simplified_alignment == [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12]]
            assert document.simplified_to_original_alignment == [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12]]
            break

    assert has_specific_doc

    has_specific_doc = False
    for document in a_b.documents:
        if document.original_items[0] == "Картина И. ":
            has_specific_doc = True
            assert document.original_items[-1] == "Устойчивое выражение золотая осень часто используется в речи, чтобы передать восхищение яркими красками природы в это время года."
            assert document.simplified_items[0] == "Картина И. "
            assert document.simplified_items[-1] == "Выражение золотая осень часто используется в речи, чтобы передать восхищение яркими красками природы в это время года."
            assert document.original_to_simplified_alignment == [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12]]
            assert document.simplified_to_original_alignment == [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12]]
            break

    assert has_specific_doc

    has_specific_doc = False
    for document in literature.documents:
        if document.original_items[0] == "Тут вот он и возник неумолимым посланцем мировой суеты, которой нет дела до нежной дремлющей благодати, — румяный, крепенький, круглолицый, в куртке из кожзаменителя, толстой вязки свитере, хорошо выношенных джинсах и высоких зашнурованных ботинках. ":
            has_specific_doc = True
            assert document.original_items[-1] == "Бесшумно плыли мы по лунной реке…"
            assert document.simplified_items[0] == "Он появился в моём подмосковном жилье ноябрьским полднем — румяный, крепенький, круглолицый, в куртке из кожзаменителя, толстой вязки свитере, хорошо выношенных джинсах и высоких зашнурованных ботинках. "
            assert document.simplified_items[-1] == "Бесшумно плыли мы по лунной реке… "
            assert document.original_to_simplified_alignment == [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [15], [16], [17], [18], [19], [20], [21], [22], [23], [24], [25], [26], [27], [28], [29], [30], [31], [32], [33], [34], [35], [36], [37], [38], [39], [40, 41], [42], [43], [44], [45], [46], [47], [48], [49], [50], [51], [52], [53], [54], [55], [56], [57], [58], [59], [60], [61], [62], [63], [64], [65], [66], [67], [68], [69], [70], [71], [72], [73], [74], [75], [76], [77], [78], [79], [80], [81], [82], [83], [84], [85], [86], [87], [88], [89], [90], [91], [92], [93], [94], [95], [96], [97], [98], [99], [100], [101], [102], [103], [104], [105], [106], [107], [108], [109], [110], [111], [112], [113], [114], [115], [116], [117], [118], [119], [120], [121], [122], [123], [124], [125], [126], [127], [128], [129], [130], [131], [132], [133], [134, 135], [136, 137], [138], [139], [140], [141], [142], [143], [144], [145], [146], [147], [148], [149], [150], [151], [152], [153], [154]]
            assert document.simplified_to_original_alignment == [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [15], [16], [17], [18], [19], [20], [21], [22], [23], [24], [25], [26], [27], [28], [29], [30], [31], [32], [33], [34], [35], [36], [37], [38], [39], [40], [40], [41], [42], [43], [44], [45], [46], [47], [48], [49], [50], [51], [52], [53], [54], [55], [56], [57], [58], [59], [60], [61], [62], [63], [64], [65], [66], [67], [68], [69], [70], [71], [72], [73], [74], [75], [76], [77], [78], [79], [80], [81], [82], [83], [84], [85], [86], [87], [88], [89], [90], [91], [92], [93], [94], [95], [96], [97], [98], [99], [100], [101], [102], [103], [104], [105], [106], [107], [108], [109], [110], [111], [112], [113], [114], [115], [116], [117], [118], [119], [120], [121], [122], [123], [124], [125], [126], [127], [128], [129], [130], [131], [132], [133], [133], [134], [134], [135], [136], [137], [138], [139], [140], [141], [142], [143], [144], [145], [146], [147], [148], [149], [150], [151]]
            break

    assert has_specific_doc

    print("RuAdapt Passed All Tests")

# This test is likely to fail since everyone has to build their own version of this corpus
def simple_german_tests(path):
    simple_german = SimpleGermanLoader().load(path)[0]

    assert len(simple_german.documents) == 224

    has_specific_doc = False
    for document in simple_german.documents:
        if document.original_items[0] == "Merkblatt zum Kindesschutz  Elterliche Verantwortung Eltern haben grundsätzlich das Recht und die Pflicht, sich um die Erziehung ihrer Kinder zu kümmern und umfassend für deren Wohl zu sorgen.":
            has_specific_doc = True
            assert document.original_items[-1] == "Wenn man mit der Arbeit der Beistandsperson nicht zufrieden ist, kann man sich an die KESB wenden."
            assert document.simplified_items[0] == " Informationen zum Kindesschutz  Die Eltern erziehen ihr Kind normalerweise selber."
            assert document.simplified_items[-1] == "Seite 7 von 7"
            break

    assert has_specific_doc

    has_specific_doc = False
    for document in simple_german.documents[::-1]:
        if document.original_items[0] == "  Labelpartner - Kultur inklusiv       Sprunglinks   Zur Navigation springen   Zur Subnavigation springen   Inhalt                  Deutschde (ausgewählt)FrançaisfrItalianoit    Willkommen bei Kultur inklusiv!":
            has_specific_doc = True
            assert document.original_items[-5] == "Weitere Anregungen und Tipps finden Sie hier."
            assert document.simplified_items[0] == "  Wer hat das Label?"
            assert document.simplified_items[-1] == "Die Fachstelle ist eine Organisation von Pro Infirmis."
            break

    assert has_specific_doc

    print("Simple German Passed All Tests")

def alector_tests(path):
    alector = AlectorLoader().load(path)[0]

    assert len(alector.documents) == 79

    has_specific_doc = False
    for document in alector.documents:
        if document.original_items[0] == "Depuis notre planète, les astronomes observent l'univers.":
            has_specific_doc = True
            assert document.original_items[-1] == "Sur les autres planètes, le ciel aura une teinte différente car il dépend de la composition de son atmosphère."
            assert document.simplified_items[0] == "Depuis notre planète, les hommes regardent l'univers."
            assert document.simplified_items[-1] == "Sur les autres planètes, le ciel a une couleur différente. Cela dépend de son atmosphère."
            break

    assert has_specific_doc

    print("Alector Passed All Tests")

def ru_wiki_large_tests(path):
    ru_wiki_large = RuWikiLargeLoader(keep_train_test_split=False, allow_sentence_splits=False).load(path)[0]

    assert len(ru_wiki_large.documents) == 3

    has_specific_doc = False
    for document in ru_wiki_large.documents:
        if document.original_items[0] == "Имеются рукописные свидетельства того, что Остин продолжала работать над этими произведениями вплоть до периода 1809-11 годов, и что ее племянница и племянник Анна и Джеймс Эдвард Остен внесли дополнительные дополнения в 1814 году.":
            has_specific_doc = True
            assert document.original_items[-1] == "В целом «Ювентус» выиграл 51 официальный турнир - больше, чем любая другая команда в стране; 40 в национальном Первом Дивизионе, что также является рекордом, и 11 официальных международных соревнований, что делает их в последнем случае вторым по результативности итальянским клубом в европейских соревнованиях."
            print(document.simplified_items[0])
            assert document.simplified_items[0] == "Есть некоторые доказательства того, что Остин продолжала работать над этими произведениями позже. Ее племянник и племянница Джеймс Эдвард и Анна Остин, возможно, внесли дополнительные дополнения в ее работы примерно в 1814 году."
            assert document.simplified_items[-1] == "Клуб - самая успешная команда в истории итальянского футбола. В целом клуб завоевал 51 официальный трофей - больше, чем любая другая команда в стране; 40 в Италии, что также является рекордом, и 11 в европейских и мировых соревнованиях."
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    train, test, dev = RuWikiLargeLoader(keep_train_test_split=True, allow_sentence_splits=False).load(path)

    assert len(train.documents) == 1
    assert len(test.documents) == 1
    assert len(dev.documents) == 1

    has_specific_doc = False
    for document in train.documents:
        if document.original_items[0] == "Имеются рукописные свидетельства того, что Остин продолжала работать над этими произведениями вплоть до периода 1809-11 годов, и что ее племянница и племянник Анна и Джеймс Эдвард Остен внесли дополнительные дополнения в 1814 году.":
            has_specific_doc = True
            assert document.original_items[-1] == "В целом «Ювентус» выиграл 51 официальный турнир - больше, чем любая другая команда в стране; 40 в национальном Первом Дивизионе, что также является рекордом, и 11 официальных международных соревнований, что делает их в последнем случае вторым по результативности итальянским клубом в европейских соревнованиях."
            assert document.simplified_items[0] == "Есть некоторые доказательства того, что Остин продолжала работать над этими произведениями позже. Ее племянник и племянница Джеймс Эдвард и Анна Остин, возможно, внесли дополнительные дополнения в ее работы примерно в 1814 году."
            assert document.simplified_items[-1] == "Клуб - самая успешная команда в истории итальянского футбола. В целом клуб завоевал 51 официальный трофей - больше, чем любая другая команда в стране; 40 в Италии, что также является рекордом, и 11 в европейских и мировых соревнованиях."
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    has_specific_doc = False
    for document in test.documents:
        if document.original_items[0] == "Одна сторона вооруженных конфликтов состоит в основном из суданских вооруженных сил и «Джанджавид» - группы суданских ополченцев, набранных в основном из афро-арабских племен аббала в северном районе Ризейгат в Судане.":
            has_specific_doc = True
            assert document.original_items[-1] == "Гейбл также получил номинацию на премию Американской киноакадемии, когда сыграл Флетчера Кристиана в фильме 1935 года «Мятеж на награде»."
            assert document.simplified_items[0] == "Одной стороной вооруженных конфликтов являются суданские вооруженные силы и «Джанджавид», суданское ополчение, набранное из афро-арабских племен аббала в северном районе Ризейгат в Судане."
            assert document.simplified_items[-1] == "Гейбл также был номинирован на премию Оскар за роль Флетчера Кристиана в фильме 1935 года «Мятеж за наградой»."
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break


    assert has_specific_doc

    has_specific_doc = False
    for document in dev.documents:
        if document.original_items[0] == "«Район» оперы - это вымышленная деревня, которая имеет некоторое сходство с собственным домом Крэбба, а позже и Бриттена, Альдебург, на восточном побережье Англии, около 1830 года.":
            has_specific_doc = True
            assert document.original_items[-1] == "В Тикале, одном из крупнейших городов классического майя, не было воды, кроме той, что собиралась из дождевой воды и хранилась в десяти резервуарах."
            assert document.simplified_items[0] == "Дирижер Сергей Кусевицкий попросил Бриттена написать оперу на стихотворение Джорджа Крэбба."
            assert document.simplified_items[-1] == "Руины находятся в равнинных тропических лесах, но в Тикале не было воды, кроме той, что собиралась из дождевой воды и хранилась под землей."
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    print("RuWikiLarge Passed All Tests")

def newsela_en_tests(path):
    newsela_en = NewselaENLoader(keep_subdivisions=False).load(path)[0]

    assert len(newsela_en.documents) == 7528

    for document in newsela_en.documents:
        if document.original_items[0] == "The shoebox-size chunk of bronze didn't attract much attention when divers retrieved it from an ancient shipwreck off the Greek island of Antikythera in 1901.":
            has_specific_doc = True
            assert document.original_items[-1] == "This time, divers will be able to spend hours instead of minutes on the bottom, using a pressurized robotic suit developed in Vancouver, British Columbia, and originally used to inspect New York City's water system."
            assert document.simplified_items[0] == "The shoebox-size chunk of bronze didn't gather much attention when divers brought it up from an ancient shipwreck off the Greek island of Antikythera in 1901."
            assert document.simplified_items[-1] == "\"But you would have to think that whoever built this must at least have made use of what Archimedes had done, or came out of a tradition that started with Archimedes.\""
            assert document.original_to_simplified_alignment == [[0], [1, 2], [3], [4, 5], [7], [8], [9], [10], [11], [12], [13], [14], [15], [16], [17], [19], [20, 21], [22, 23], [24], [25, 26], [27], [28], [29], [31], [32], [33], [34], [35, 36], [37], [38], [39], [40], [41], [], [], [], [], [43], [44], [45, 46], [47], [48], [49], [], [], [], [], []]
            assert document.simplified_to_original_alignment == [[0], [1], [1], [2], [3], [3], [], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [], [15], [16], [16], [17], [17], [18], [19], [19], [20], [21], [22], [], [23], [24], [25], [26], [27], [27], [28], [29], [30], [31], [32], [], [37], [38], [39], [39], [40], [41], [42]]
            break
    
    assert has_specific_doc

    z_o, o_t, t_t, t_f = NewselaENLoader(keep_subdivisions=True).load(path)

    assert len(z_o.documents) == 1882
    assert len(o_t.documents) == 1882
    assert len(t_t.documents) == 1882
    assert len(t_f.documents) == 1882

    for document in z_o.documents:
        if document.original_items[0] == "The shoebox-size chunk of bronze didn't attract much attention when divers retrieved it from an ancient shipwreck off the Greek island of Antikythera in 1901.":
            has_specific_doc = True
            assert document.original_items[-1] == "This time, divers will be able to spend hours instead of minutes on the bottom, using a pressurized robotic suit developed in Vancouver, British Columbia, and originally used to inspect New York City's water system."
            assert document.simplified_items[0] == "The shoebox-size chunk of bronze didn't gather much attention when divers brought it up from an ancient shipwreck off the Greek island of Antikythera in 1901."
            assert document.simplified_items[-1] == "\"But you would have to think that whoever built this must at least have made use of what Archimedes had done, or came out of a tradition that started with Archimedes.\""
            assert document.original_to_simplified_alignment == [[0], [1, 2], [3], [4, 5], [7], [8], [9], [10], [11], [12], [13], [14], [15], [16], [17], [19], [20, 21], [22, 23], [24], [25, 26], [27], [28], [29], [31], [32], [33], [34], [35, 36], [37], [38], [39], [40], [41], [], [], [], [], [43], [44], [45, 46], [47], [48], [49], [], [], [], [], []]
            assert document.simplified_to_original_alignment == [[0], [1], [1], [2], [3], [3], [], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [], [15], [16], [16], [17], [17], [18], [19], [19], [20], [21], [22], [], [23], [24], [25], [26], [27], [27], [28], [29], [30], [31], [32], [], [37], [38], [39], [39], [40], [41], [42]]
            break

    assert has_specific_doc

    for document in o_t.documents:
        if document.original_items[0] == "The shoebox-size chunk of bronze didn't gather much attention when divers brought it up from an ancient shipwreck off the Greek island of Antikythera in 1901.":
            has_specific_doc = True
            assert document.original_items[-1] == "\"But you would have to think that whoever built this must at least have made use of what Archimedes had done, or came out of a tradition that started with Archimedes.\""
            assert document.simplified_items[0] == "When a shoebox-size chunk of bronze was pulled from an ancient shipwreck off the Greek island of Antikythera in 1901, it did not attract much attention."
            assert document.simplified_items[-1] == "\"But you would have to think that whoever built this must at least have made use of what Archimedes had done, or came out of a tradition that started with Archimedes.\""
            assert document.original_to_simplified_alignment == [[0], [1], [2], [3, 4], [5], [6], [], [7], [8], [9], [11, 12], [13], [14], [15], [16], [17], [18], [], [], [19, 20], [21], [22], [24], [25], [26], [27], [28], [29, 30], [31], [32, 33], [], [34], [35, 36], [38], [39], [40], [41], [42, 43], [44, 45], [46], [47], [48], [], [50], [51, 52], [53], [54], [55], [56], [57]]
            assert document.simplified_to_original_alignment == [[0], [1], [2], [3], [3], [4], [5], [7], [8], [9], [], [10], [10], [11], [12], [13], [14], [15], [16], [19], [19], [20], [21], [], [22], [23], [24], [25], [26], [27], [27], [28], [29], [29], [31], [32], [32], [], [33], [34], [35], [36], [37], [37], [38], [38], [39], [40], [41], [], [43], [44], [44], [45], [46], [47], [48], [49]]
            break
    
    assert has_specific_doc

    for document in t_t.documents:
        if document.original_items[0] == "When a shoebox-size chunk of bronze was pulled from an ancient shipwreck off the Greek island of Antikythera in 1901, it did not attract much attention.":
            has_specific_doc = True
            assert document.original_items[-1] == "\"But you would have to think that whoever built this must at least have made use of what Archimedes had done, or came out of a tradition that started with Archimedes.\""
            assert document.simplified_items[0] == "A shoebox-size chunk of bronze called the Antikythera Mechanism has scientists and people who study math excited."
            assert document.simplified_items[-1] == "\"But you would have to think that whoever built this must at least have made use of what Archimedes had done, or came out of a tradition that started with Archimedes.\""
            assert document.original_to_simplified_alignment == [[0, 1, 2], [3], [], [4], [], [6], [8, 9], [10, 11], [], [12], [], [13], [14], [15], [16, 17], [18, 19], [20, 21], [22], [23], [26], [], [27], [], [], [28], [29], [24], [30], [31, 32], [33], [34], [35], [36], [37], [38, 39], [40], [41, 42], [], [43], [44], [45], [], [47], [48], [49], [50], [51], [52], [], [], [53, 54], [55], [56], [], [], [57], [58], [59]]
            assert document.simplified_to_original_alignment == [[0], [0], [0], [1], [3], [], [5], [], [6], [6], [7], [7], [9], [11], [12], [13], [14], [14], [15], [15], [16], [16], [17], [18], [26], [], [19], [21], [24], [25], [27], [28], [28], [29], [30], [31], [32], [33], [34], [34], [35], [36], [36], [38], [39], [40], [], [42], [43], [44], [45], [46], [47], [50], [50], [51], [52], [55], [56], [57]]
            break

    assert has_specific_doc

    for document in t_f.documents:
        if document.original_items[0] == "A shoebox-size chunk of bronze called the Antikythera Mechanism has scientists and people who study math excited.":
            has_specific_doc = True
            assert document.original_items[-1] == "\"But you would have to think that whoever built this must at least have made use of what Archimedes had done, or came out of a tradition that started with Archimedes.\""
            assert document.simplified_items[0] == "Divers found a chunk of metal in a shipwreck in 1901."
            assert document.simplified_items[-1] == "Still, Evans said whoever built it at least used knowledge developed by Archimedes."
            assert document.original_to_simplified_alignment == [[], [7], [], [5, 8], [9], [], [12], [13], [14, 16], [15], [17], [18], [19], [20], [21], [22], [23], [24], [25], [26], [27, 28], [29], [], [], [31], [], [32], [33], [34], [35, 36], [], [], [], [37], [38, 39], [40], [41], [42], [43], [44], [45], [], [], [46], [47], [49], [], [50], [51], [52], [53], [54], [55], [56], [57], [], [], [60, 61], [], []]
            assert document.simplified_to_original_alignment == [[], [], [], [], [], [3], [], [1], [3], [4], [], [], [6], [7], [8], [9], [8], [10], [11], [12], [13], [14], [15], [16], [17], [18], [19], [20], [20], [21], [], [24], [26], [27], [28], [29], [29], [33], [34], [34], [35], [36], [37], [38], [39], [40], [43], [44], [], [45], [47], [48], [49], [50], [51], [52], [53], [54], [], [], [57], [57], []]
            break

    assert has_specific_doc

    print("NewselaEN Passed All Tests")

def wikiauto_en_tests(path):
    wiki_auto = WikiAutoENLoader(keep_subdivisions=False).load(path)[0]

    assert len(wiki_auto.documents) == 138095

    for document in wiki_auto.documents:
        if document.original_items[0] == "Lata Mondal ( ; born: 16 January 1993, Dhaka) is a Bangladeshi cricketer who plays for the Bangladesh national women's cricket team.":
            has_specific_doc = True
            assert document.original_items[-1] == "Mondal was a member of the team that won a silver medal in cricket against the China national women's cricket team at the 2010 Asian Games in Guangzhou, China."
            assert document.simplified_items[0] == "Lata Mondal (born: 16 January 1993) is a Bangladeshi cricketer who plays for the Bangladesh national women's cricket team."
            assert document.simplified_items[-1] == "She is a right handed bat."
            assert document.original_to_simplified_alignment == [[0], [1], [], [], [], [], []]
            assert document.simplified_to_original_alignment == [[0], [1]]
            break

    assert has_specific_doc

    part1, part2 = WikiAutoENLoader(keep_subdivisions=True).load(path)

    assert len(part1.documents) == 125059
    assert len(part2.documents) == 13036

    for document in part1.documents:
        if document.original_items[0] == "Lata Mondal ( ; born: 16 January 1993, Dhaka) is a Bangladeshi cricketer who plays for the Bangladesh national women's cricket team.":
            has_specific_doc = True
            assert document.original_items[-1] == "Mondal was a member of the team that won a silver medal in cricket against the China national women's cricket team at the 2010 Asian Games in Guangzhou, China."
            assert document.simplified_items[0] == "Lata Mondal (born: 16 January 1993) is a Bangladeshi cricketer who plays for the Bangladesh national women's cricket team."
            assert document.simplified_items[-1] == "She is a right handed bat."
            assert document.original_to_simplified_alignment == [[0], [1], [], [], [], [], []]
            assert document.simplified_to_original_alignment == [[0], [1]]
            break

    assert has_specific_doc

    for document in part2.documents:
        if document.original_items[0] == "Vex is a municipality and capital of the district of Hérens in the canton of Valais in Switzerland.":
            has_specific_doc = True
            assert document.original_items[-1] == "It was open a total of 79 days with average of 6 hours per week during that year."
            assert document.simplified_items[0] == "Vex is the capital city of the district of Hérens in the canton of Valais in Switzerland."
            assert document.simplified_items[-1] == "Vex is the capital city of the district of Hérens in the canton of Valais in Switzerland."
            assert document.original_to_simplified_alignment == [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
            assert document.simplified_to_original_alignment == [[]]
            break

    assert has_specific_doc

    for document in wiki_auto.documents:
        if document.original_items[0] == "Lahja Tuulikki Ukkola (\"née\" Parviainen; 28 November 1943 – 28 May 2019) was a Finnish politician and journalist.":
            has_specific_doc = True
            assert document.original_items[-1] == "Ukkola died on 28 May 2019 in Oulu, at the age of 75."
            assert document.simplified_items[0] == "Lahja Tuulikki Ukkola (\"née\" Parviainen; 28 November 1943 – 28 May 2019) was a Finnish politician and journalist."
            assert document.simplified_items[-1] == "She died on 28 May 2019 in Oulu, at the age of 75."
            assert document.original_to_simplified_alignment == [[0], [1], [2], [3], [4], [6]]
            assert document.simplified_to_original_alignment == [[0], [1], [2], [3], [4], [], [5]]
            break

    assert has_specific_doc

    print("WikiAutoEN Passed All Tests")

def asset_tests(path):
    asset = AssetLoader(keep_train_test_split=False).load(path)[0]

    assert len(asset.documents) == 20

    for document in asset.documents:
        if document.original_items[0] == "Adjacent counties are Marin (to the south), Mendocino (to the north), Lake (northeast), Napa (to the east), and Solano and Contra Costa (to the southeast).":
            has_specific_doc = True
            assert document.original_items[-1] == "Modern African history has been rife with revolutions and wars as well as the growth of modern African economies and democratization across the continent."
            assert document.simplified_items[0] == "countries next to it are Marin, Mendocino, Lake, Napa, Solano, and Contra Costa."
            assert document.simplified_items[-1] == "Modern African history has been full of revolutions and wars as well as the growth of modern African economies and democratization across the continent."
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    valid, test = AssetLoader(keep_train_test_split=True).load(path)

    assert len(valid.documents) == 10
    assert len(test.documents) == 10

    for document in valid.documents:
        if document.original_items[0] == "Adjacent counties are Marin (to the south), Mendocino (to the north), Lake (northeast), Napa (to the east), and Solano and Contra Costa (to the southeast).":
            has_specific_doc = True
            assert document.original_items[-1] == "Modern African history has been rife with revolutions and wars as well as the growth of modern African economies and democratization across the continent."
            assert document.simplified_items[0] == "countries next to it are Marin, Mendocino, Lake, Napa, Solano, and Contra Costa."
            assert document.simplified_items[-1] == "Modern African history has been full of revolutions and wars as well as the growth of modern African economies and democratization across the continent."
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    for document in test.documents:
        if document.original_items[0] == "One side of the armed conflicts is composed mainly of the Sudanese military and the Janjaweed, a Sudanese militia group recruited mostly from the Afro-Arab Abbala tribes of the northern Rizeigat region in Sudan.":
            has_specific_doc = True
            assert document.original_items[-1] == "Gable also earned an Academy Award nomination when he portrayed Fletcher Christian in 1935's Mutiny on the Bounty."
            assert document.simplified_items[0] == "On one side of the conflicts are the Sudanese military and the Janjaweed, a Sudanese militia group.  They are mostly recruited from the Afro-Arab Abbala tribes."
            assert document.simplified_items[-1] == "Gable earned an Academy Award nomination for portraying Fletcher Christian in Mutiny on the Bounty."
            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]
            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]
            break

    assert has_specific_doc

    print("Asset Passed All Tests")

def adminit_tests(path):
    adminit = AdminItLoader(keep_subdivisions=False).load(path)[0]

    assert len(adminit.documents) == 736

    for document in adminit.documents:
        if document.original_items[0] == "In particolare, andranno rilevati e descritti tutti gli elementi di criticità paesaggistica, insiti nel progetto, e andranno messi in relazione a quanto è stato operato, per eliminare o mitigare tali criticità (impatti), garantendo così un migliore inserimento paesaggistico dell'intervento.":
            has_specific_doc = True
            assert document.original_items[-1] == "In particolare, andranno rilevati e descritti tutti gli elementi di criticità paesaggistica, insiti nel progetto, e andranno messi in relazione a quanto è stato operato, per eliminare o mitigare tali criticità (impatti), garantendo così un migliore inserimento paesaggistico dell'intervento."
            assert document.simplified_items[0] == "In particolare, andranno rilevati e descritti tutti gli elementi di criticità paesaggistica, interni al progetto, e andranno messi in relazione a quanto è stato operato, per eliminare o mitigare tali criticità (impatti), garantendo così un migliore inserimento paesaggistico dell'intervento."
            assert document.simplified_items[-1] == "In particolare, andranno rilevati e descritti tutti gli elementi di criticità paesaggistica, interni al progetto, e andranno messi in relazione a quanto è stato operato, per eliminare o mitigare tali criticità (impatti), garantendo così un migliore inserimento paesaggistico dell'intervento."
            assert document.original_to_simplified_alignment == [[0]]
            assert document.simplified_to_original_alignment == [[0]]
            break

    assert has_specific_doc

    op, rd, rs = AdminItLoader(keep_subdivisions=True).load(path)

    assert len(op.documents) == 588

    for document in op.documents:
        if document.original_items[0] == "In particolare, andranno rilevati e descritti tutti gli elementi di criticità paesaggistica, insiti nel progetto, e andranno messi in relazione a quanto è stato operato, per eliminare o mitigare tali criticità (impatti), garantendo così un migliore inserimento paesaggistico dell'intervento.":
            has_specific_doc = True
            assert document.original_items[-1] == "In particolare, andranno rilevati e descritti tutti gli elementi di criticità paesaggistica, insiti nel progetto, e andranno messi in relazione a quanto è stato operato, per eliminare o mitigare tali criticità (impatti), garantendo così un migliore inserimento paesaggistico dell'intervento."
            assert document.simplified_items[0] == "In particolare, andranno rilevati e descritti tutti gli elementi di criticità paesaggistica, interni al progetto, e andranno messi in relazione a quanto è stato operato, per eliminare o mitigare tali criticità (impatti), garantendo così un migliore inserimento paesaggistico dell'intervento."
            assert document.simplified_items[-1] == "In particolare, andranno rilevati e descritti tutti gli elementi di criticità paesaggistica, interni al progetto, e andranno messi in relazione a quanto è stato operato, per eliminare o mitigare tali criticità (impatti), garantendo così un migliore inserimento paesaggistico dell'intervento."
            assert document.original_to_simplified_alignment == [[0]]
            assert document.simplified_to_original_alignment == [[0]]
            break

    assert has_specific_doc

    assert len(rd.documents) == 48

    for document in rd.documents:
        if document.original_items[0] == "Si fa presente che le mendaci dichiarazioni in atti pubblici e l'occupazione di immobili dichiarati inabitabili sono sanzionate penalmente.":
            has_specific_doc = True
            assert document.original_items[-1] == "Si fa presente che le mendaci dichiarazioni in atti pubblici e l'occupazione di immobili dichiarati inabitabili sono sanzionate penalmente."
            assert document.simplified_items[0] == "Le ricordiamo che la legge punisce chi rilascia false dichiarazioni o il proprietario di immobili che vengono utilizzati dopo essere stati dichiarati inabitabili o inagibili."
            assert document.simplified_items[-1] == "Le ricordiamo che la legge punisce chi rilascia false dichiarazioni o il proprietario di immobili che vengono utilizzati dopo essere stati dichiarati inabitabili o inagibili."
            assert document.original_to_simplified_alignment == [[0]]
            assert document.simplified_to_original_alignment == [[0]]
            break

    assert has_specific_doc

    assert len(rs.documents) == 100

    for document in rs.documents:
        if document.original_items[0] == "Il \"Pacchetto scuola\" sarà assegnato solo a seguito dell'assegnazione effettiva delle risorse regionale e statali, fino ad esaurimento delle risorse disponibili, ai richiedenti in possesso dei necessari requisiti, disposti in ordine crescente del valore ISEE.":
            has_specific_doc = True
            assert document.original_items[-1] == "Il \"Pacchetto scuola\" sarà assegnato solo a seguito dell'assegnazione effettiva delle risorse regionale e statali, fino ad esaurimento delle risorse disponibili, ai richiedenti in possesso dei necessari requisiti, disposti in ordine crescente del valore ISEE."
            assert document.simplified_items[0] == "I richiedenti con i requisiti necessari otterranno il \"Pacchetto scuola\", a partire da chi ha un ISEE con valore più basso. Il \"Pacchetto scuola\" sarà concesso solo dopo che le risorse regionali e statali saranno state assegnate e fino a quando le risorse saranno disponibili."
            assert document.simplified_items[-1] == "I richiedenti con i requisiti necessari otterranno il \"Pacchetto scuola\", a partire da chi ha un ISEE con valore più basso. Il \"Pacchetto scuola\" sarà concesso solo dopo che le risorse regionali e statali saranno state assegnate e fino a quando le risorse saranno disponibili."
            assert document.original_to_simplified_alignment == [[0]]
            assert document.simplified_to_original_alignment == [[0]]
            break

    assert has_specific_doc

    print("AdminIT Passed All Tests")

def text_simplification_slovene_tests(path):
    ts_slovene = TextSimplificationSloveneLoader(keep_train_test_split=False).load(path)[0]

    assert len(ts_slovene.documents) == 3

    for document in ts_slovene.documents:
        if document.original_items[0] == "Ker je bil Matevž okrog ušes tako čuden, ga ni hotelo v vasi nobeno dekle.":
            has_specific_doc = True
            assert document.original_items[-1] == "Stekel je k sestri Ruti in zaklical: \"Breda se smeje, Breda!\""
            assert document.simplified_items[0] == "Ker je bil brez ušesa, ga ni hotela nobena ženska."
            assert document.simplified_items[-1] == "Stekel je k sestri Ruti in klical: Breda se smeje!"
            assert document.original_to_simplified_alignment == [[0], [1], [1], [1], [2], [3, 4], [5, 6], [7], [7], [8], [9], [10], [11], [12, 13], [14], [15], [16, 17, 18], [19, 20, 21], [22], [23], [24], [25], [26], [27], [28, 29], [30], [31], [32], [33], [34], [35], [36], [37], [38, 39, 40], [41], [42], [43], [44, 45], [46], [47], [48, 49], [50, 51, 52, 53], [54], [55], [56], [57], [58], [59], [60], [61], [62], [63], [64], [65], [66], [67], [68], [69, 70], [71], [72, 73], [74, 75], [76], [77], [78], [79, 80], [81], [82], [83], [84], [85], [86], [87, 88], [89], [90], [91, 92], [93], [94], [95], [96], [96], [97], [98], [99, 100], [101], [102], [103], [104], [104], [105], [105], [106], [107], [108, 109], [110], [111], [112, 113], [114, 115, 116, 117, 118, 119], [120, 121], [122], [123], [124], [125], [126], [127, 128], [129, 130, 131], [132], [133, 134], [135], [136, 137], [138], [139, 140], [141, 142], [143], [144, 145, 146], [147], [148], [149], [150], [150], [151], [152], [153, 154], [155, 156, 157], [158], [159], [160, 161, 162], [163], [164], [165], [166], [167], [168], [169], [170, 171], [172], [172], [173], [174], [175], [176], [176], [177], [178], [179], [180, 181], [180, 181], [182, 183, 184, 185], [186, 187, 188], [189, 190, 191], [192, 193], [194, 195, 196, 197, 198], [199], [200, 201, 202], [203], [204], [205], [206, 207, 208, 209, 210], [211, 212], [213], [214, 215], [216, 217], [218], [219, 220, 221, 222, 223], [224], [225], [226], [227], [228], [229], [229], [230], [230], [231], [232], [233], [234], [235], [236], [237], [238], [239], [239], [240], [241], [242], [243], [244], [245], [246], [246], [247], [247], [248], [248], [249], [250], [251, 252], [253], [254], [255], [256, 257, 258], [259], [260], [260], [261], [262], [263], [264], [265], [266], [266], [267], [267], [267], [268], [269], [270], [271], [272], [273, 274, 275], [276, 277], [276, 277], [278], [278], [279], [280], [281], [281], [282], [283], [284], [284], [285], [285], [286], [287], [287], [288], [289], [290], [290], [290], [291], [292], [292], [293], [294], [295], [296], [296], [296], [297], [298], [298], [299], [300, 301], [302], [302], [302], [303], [304], [305], [306], [307, 308], [309], [309], [310], [310], [311, 312], [313], [313], [314], [315], [316], [317], [318], [318], [318], [319], [320], [320], [321], [321], [322], [323, 324], [325, 326, 327, 328, 329], [330], [331, 332], [333, 334], [335, 336], [337, 338], [339, 340, 341], [342, 343], [344, 345, 346], [347], [348], [349], [350, 351], [352, 353], [354, 355], [356, 357, 358], [359, 360], [361], [362, 363], [364], [365], [366, 367], [368, 369], [368, 369], [370, 371, 372], [373], [374], [375], [376, 377, 378], [379, 380], [381], [382, 383, 384], [385], [386], [387], [388], [389], [390], [391, 392], [393], [394], [395], [396], [397], [398], [399], [400, 401, 402], [403], [404], [405], [406], [407], [408], [409], [410, 411, 412], [410, 411, 412], [413], [414], [415, 416, 417], [418, 419], [420, 421, 422], [423], [424], [425], [426, 427, 428], [429, 430], [431], [432, 433, 434, 435], [436, 437], [438, 439, 440, 441], [442], [443], [444], [445, 446], [447], [448], [449], [450], [451], [452], [453, 454], [455], [456, 457, 458], [459], [460, 461, 462], [463], [463], [464], [465], [465], [466], [467], [468, 469], [470], [471], [472], [473], [474], [475], [476], [477], [478], [479], [480], [481], [482], [483], [484], [484], [484], [485], [486], [487], [488], [489], [490], [490], [491], [492], [493], [494], [494], [494], [495], [496], [497, 498], [499], [499], [500], [501], [501], [502], [503], [504], [504], [505], [506], [507], [508], [508], [509], [510, 511], [510, 511], [512], [513], [514], [515], [516], [516], [517], [518], [519, 520], [521], [522], [523, 524, 525], [523, 524, 525], [526], [527, 528, 529], [527, 528, 529], [530], [531], [532], [533], [534], [535], [536], [537], [538], [539], [540], [541], [542], [543], [544, 545], [546], [547], [548], [549, 550], [551], [552], [553], [554], [554], [555, 556], [557], [558, 559], [560], [560], [561], [562], [562], [562], [563], [563], [564], [565, 566], [567], [568], [569], [570], [571], [572], [573], [574], [575, 576], [575, 576], [577], [578], [578], [579], [580], [581], [582], [583], [584, 585, 586], [587], [588], [589], [590], [591], [592], [593], [594], [595], [596], [597], [598], [599], [600], [601], [601], [602], [602], [603], [604], [605], [605], [605], [606], [607], [607], [607], [608], [608], [609], [610], [611], [612], [613], [613], [614], [614], [615], [616], [617], [618], [619], [620], [621, 622], [623], [624], [625], [626], [627, 628], [629], [630, 631, 632], [633], [634], [634], [635], [636, 637], [638], [639], [640], [641], [642], [643], [644], [645], [646], [647], [648], [649], [650], [651], [652], [653], [653], [653], [654], [655], [656], [657], [658], [659], [660, 661], [662], [663], [664], [664], [665], [666], [667], [668], [669], [669], [670], [671], [672, 673, 674], [672, 673, 674], [675], [676], [677], [677], [677], [678, 679], [680], [681], [682], [683], [684, 685, 686], [687], [688], [689], [690], [691], [691], [692], [693], [694], [695], [695], [696], [697], [698], [699], [699], [700], [701, 702], [703], [704], [705], [705], [705], [706], [707], [708], [708], [709, 710, 711], [712], [713], [714], [715], [716], [717], [718], [719], [720], [721], [722], [723], [724], [725, 726, 727], [728], [728], [729], [730], [731], [732], [733], [734, 735], [736], [737], [737], [738], [739], [740], [740], [741], [742], [743], [744], [745], [746], [747], [748, 749], [750, 751], [752], [753], [754], [755], [756], [757], [758], [759, 760, 761], [762], [763], [764], [764], [765, 766, 767], [768], [768], [769], [770], [771], [772, 773], [772, 773], [772, 773], [772, 773], [774, 775, 776], [777], [777], [778], [779, 780], [779, 780], [781], [782], [783, 784, 785], [786, 787], [788, 789], [790, 791, 792, 793], [790, 791, 792, 793], [794, 795, 796], [794, 795, 796], [794, 795, 796], [794, 795, 796], [794, 795, 796], [797], [798, 799, 800, 801], [798, 799, 800, 801], [798, 799, 800, 801], [802], [803, 804], [805, 806], [805, 806], [807, 808], [809], [810, 811, 812], [810, 811, 812], [813], [813], [814, 815], [814, 815], [814, 815], [816], [816], [817], [818], [818], [819], [820, 821], [820, 821], [822, 823, 824], [822, 823, 824], [822, 823, 824], [825], [826], [827], [828, 829, 830], [831, 832], [831, 832], [833], [834], [835, 836], [835, 836], [835, 836], [837, 838, 839], [840], [841], [842], [842], [843], [844], [845], [846], [847], [848], [849], [850], [851], [852, 853], [852, 853], [854, 855], [856], [857], [858, 859], [860, 861], [862, 863], [864, 865, 866], [867, 868], [867, 868], [867, 868], [867, 868], [869], [870, 871], [870, 871], [872, 873], [872, 873], [874, 875], [874, 875], [876, 877], [876, 877], [878], [878], [878], [879, 880], [881, 882, 883], [884], [884], [885], [886], [887, 888], [887, 888], [887, 888], [889], [889], [889], [890, 891, 892, 893, 894, 895, 896], [890, 891, 892, 893, 894, 895, 896], [890, 891, 892, 893, 894, 895, 896], [890, 891, 892, 893, 894, 895, 896], [890, 891, 892, 893, 894, 895, 896], [890, 891, 892, 893, 894, 895, 896], [890, 891, 892, 893, 894, 895, 896], [897], [898], [898], [898], [898], [899], [900, 901, 902], [900, 901, 902], [903, 904, 905], [906, 907, 908, 909, 910, 911], [906, 907, 908, 909, 910, 911], [906, 907, 908, 909, 910, 911], [912, 913], [912, 913], [914], [914], [915, 916], [915, 916], [915, 916], [915, 916], [915, 916], [915, 916], [917], [918], [919, 920], [919, 920], [919, 920], [921, 922], [921, 922], [921, 922], [923], [923], [923], [924, 925], [924, 925], [924, 925], [926, 927], [928, 929], [928, 929], [930, 931, 932], [930, 931, 932], [930, 931, 932], [930, 931, 932], [933], [934, 935], [936], [937], [938], [939], [940], [941], [942], [943, 944], [943, 944], [945, 946], [947], [948, 949], [948, 949], [948, 949], [950, 951, 952, 953], [954], [955], [956], [957, 958], [957, 958], [957, 958], [957, 958], [957, 958], [959, 960], [959, 960], [959, 960], [961, 962], [961, 962], [961, 962], [961, 962], [963, 964], [963, 964], [965], [965], [966], [966], [966], [966], [967], [968], [969, 970], [971], [971], [972, 973, 974], [972, 973, 974], [972, 973, 974], [975, 976], [977], [978], [979], [979], [979], [980], [980], [981], [982, 983, 984, 985], [982, 983, 984, 985], [986, 987], [986, 987], [988], [989, 990], [989, 990], [991, 992], [993, 994, 995, 996], [993, 994, 995, 996], [993, 994, 995, 996], [993, 994, 995, 996], [993, 994, 995, 996], [993, 994, 995, 996], [997, 998], [999, 1000], [999, 1000], [999, 1000], [1001, 1002], [1001, 1002], [1003], [1003], [1004], [1005, 1006, 1007], [1005, 1006, 1007], [1005, 1006, 1007], [1008, 1009], [1010], [1011], [1012], [1012], [1013], [1014], [1014], [1015], [1015], [1016, 1017], [1018], [1019, 1020, 1021, 1022], [1023, 1024], [1023, 1024], [1023, 1024], [1023, 1024], [1025], [1026, 1027], [1028], [1029, 1030, 1031, 1032], [1033]]
            assert document.simplified_to_original_alignment == [[0], [1, 2, 3], [4], [5], [5], [6], [6], [7, 8], [9], [10], [11], [12], [13], [13], [14], [15], [16], [16], [16], [17], [17], [17], [18], [19], [20], [21], [22], [23], [24], [24], [25], [26], [27], [28], [29], [30], [31], [32], [33], [33], [33], [34], [35], [36], [37], [37], [38], [39], [40], [40], [41], [41], [41], [41], [42], [43], [44], [45], [46], [47], [48], [49], [50], [51], [52], [53], [54], [55], [56], [57], [57], [58], [59], [59], [60], [60], [61], [62], [63], [64], [64], [65], [66], [67], [68], [69], [70], [71], [71], [72], [73], [74], [74], [75], [76], [77], [78, 79], [80], [81], [82], [82], [83], [84], [85], [86, 87], [88, 89], [90], [91], [92], [92], [93], [94], [95], [95], [96], [96], [96], [96], [96], [96], [97], [97], [98], [99], [100], [101], [102], [103], [103], [104], [104], [104], [105], [106], [106], [107], [108], [108], [109], [110], [110], [111], [111], [112], [113], [113], [113], [114], [115], [116], [117, 118], [119], [120], [121], [121], [122], [122], [122], [123], [124], [125], [125], [125], [126], [127], [128], [129], [130], [131], [132], [133], [133], [134, 135], [136], [137], [138], [139, 140], [141], [142], [143], [144, 145], [144, 145], [146], [146], [146], [146], [147], [147], [147], [148], [148], [148], [149], [149], [150], [150], [150], [150], [150], [151], [152], [152], [152], [153], [154], [155], [156], [156], [156], [156], [156], [157], [157], [158], [159], [159], [160], [160], [161], [162], [162], [162], [162], [162], [163], [164], [165], [166], [167], [168, 169], [170, 171], [172], [173], [174], [175], [176], [177], [178], [179], [180, 181], [182], [183], [184], [185], [186], [187], [188, 189], [190, 191], [192, 193], [194], [195], [196], [196], [197], [198], [199], [200], [200], [200], [201], [202, 203], [204], [205], [206], [207], [208], [209, 210], [211, 212, 213], [214], [215], [216], [217], [218], [219], [219], [219], [220, 221], [220, 221], [222, 223], [224], [225], [226, 227], [228], [229], [230, 231], [232, 233], [234], [235, 236], [237], [238], [239, 240, 241], [242], [243, 244], [245], [246], [247], [248, 249, 250], [251], [252, 253], [254], [255], [255], [256, 257, 258], [259], [260], [261], [262], [263], [263], [264, 265], [266, 267], [268], [268], [269, 270], [271], [272], [273], [274], [275, 276, 277], [278], [279, 280], [281, 282], [283], [284], [284], [285], [285], [285], [285], [285], [286], [287], [287], [288], [288], [289], [289], [290], [290], [291], [291], [291], [292], [292], [293], [293], [293], [294], [295], [296], [297], [297], [298], [298], [299], [299], [300], [300], [300], [301], [301], [302], [303], [303], [304], [305], [306], [306], [307, 308], [307, 308], [309], [309], [309], [310], [311], [312], [313], [313], [313], [314], [314], [315], [316], [316], [316], [317], [318], [319], [320], [321], [322], [323], [323], [324], [325], [326], [327], [328], [329], [330], [331], [331], [331], [332], [333], [334], [335], [336], [337], [338], [339, 340], [339, 340], [339, 340], [341], [342], [343], [343], [343], [344], [344], [345], [345], [345], [346], [347], [348], [349], [349], [349], [350], [350], [351], [352], [352], [352], [352], [353], [353], [354], [354], [354], [354], [355], [356], [357], [358], [358], [359], [360], [361], [362], [363], [364], [365], [365], [366], [367], [367], [367], [368], [369], [369], [369], [370, 371], [372], [373, 374], [375], [376], [377], [377], [378], [379], [380], [381], [382], [383], [384], [385], [386], [387], [388], [389], [390], [391], [392, 393, 394], [395], [396], [397], [398], [399], [400, 401], [402], [403], [404], [405, 406, 407], [408], [409], [410], [410], [411, 412], [413], [414, 415], [416], [417], [418, 419], [420], [421], [422], [423, 424], [425], [426, 427], [426, 427], [428], [429], [430], [431], [432, 433], [434], [435], [436], [436], [437], [438], [439, 440], [439, 440], [439, 440], [441], [442, 443], [442, 443], [442, 443], [444], [445], [446], [447], [448], [449], [450], [451], [452], [453], [454], [455], [456], [457], [458], [458], [459], [460], [461], [462], [462], [463], [464], [465], [466, 467], [468], [468], [469], [470], [470], [471, 472], [473], [474, 475, 476], [477, 478], [479], [480], [480], [481], [482], [483], [484], [485], [486], [487], [488], [489, 490], [489, 490], [491], [492, 493], [494], [495], [496], [497], [498], [499], [499], [499], [500], [501], [502], [503], [504], [505], [506], [507], [508], [509], [510], [511], [512], [513], [514, 515], [516, 517], [518], [519], [520, 521, 522], [523], [524, 525, 526], [527, 528], [529], [530], [531], [532], [533, 534], [535, 536], [537], [538], [539], [540], [541], [542], [543], [543], [544], [545], [546], [547], [548], [548], [549], [550], [550], [550], [551], [552, 553], [554], [555], [555], [556], [557], [558], [559], [560], [561], [562], [563], [564], [565], [566], [567], [568], [569], [570], [571, 572, 573], [574], [575], [576], [577], [578], [579], [580], [580], [581], [582], [583, 584], [585], [586], [587], [588], [589, 590], [591], [592], [593, 594], [593, 594], [593, 594], [595], [596], [597, 598, 599], [600], [600], [601], [602], [603], [604], [605], [605], [605], [606], [607], [608], [609], [610, 611], [612], [613], [614], [615, 616], [617], [618], [619], [620, 621], [622], [623], [623], [624], [625], [626, 627, 628], [629], [630], [631, 632], [633], [633], [633], [634], [635], [636], [637], [638], [639], [640], [641], [642], [643], [644], [645], [646], [647], [647], [647], [648, 649], [650], [651], [652], [653], [654], [655], [655], [656], [657, 658], [659], [660], [661, 662], [663], [664], [665], [666], [667], [668], [669], [670], [670], [671], [671], [672], [673], [674], [675], [676], [677], [678], [679], [679], [679], [680], [681], [682, 683], [684], [684], [684], [685, 686], [687], [688], [689], [690, 691, 692, 693], [690, 691, 692, 693], [694], [694], [694], [695, 696], [697], [698, 699], [698, 699], [700], [701], [702], [702], [702], [703], [703], [704], [704], [705, 706], [705, 706], [705, 706], [705, 706], [707, 708, 709, 710, 711], [707, 708, 709, 710, 711], [707, 708, 709, 710, 711], [712], [713, 714, 715], [713, 714, 715], [713, 714, 715], [713, 714, 715], [716], [717], [717], [718, 719], [718, 719], [720], [720], [721], [722, 723], [722, 723], [722, 723], [724, 725], [726, 727, 728], [726, 727, 728], [729, 730], [731], [732, 733], [734], [735, 736], [735, 736], [737, 738, 739], [737, 738, 739], [737, 738, 739], [740], [741], [742], [743], [743], [743], [744, 745], [744, 745], [746], [747], [748, 749, 750], [748, 749, 750], [751], [751], [751], [752], [753], [754, 755], [756], [757], [758], [759], [760], [761], [762], [763], [764], [765, 766], [765, 766], [767], [767], [768], [769], [770], [770], [771], [771], [772], [772], [773], [773], [773], [774, 775, 776, 777], [774, 775, 776, 777], [778], [779, 780], [779, 780], [781, 782], [781, 782], [783, 784], [783, 784], [785, 786], [785, 786], [787, 788, 789], [790], [790], [791], [791], [791], [792, 793], [794], [795], [796, 797, 798], [796, 797, 798], [799, 800, 801], [802, 803, 804, 805, 806, 807, 808], [802, 803, 804, 805, 806, 807, 808], [802, 803, 804, 805, 806, 807, 808], [802, 803, 804, 805, 806, 807, 808], [802, 803, 804, 805, 806, 807, 808], [802, 803, 804, 805, 806, 807, 808], [802, 803, 804, 805, 806, 807, 808], [809], [810, 811, 812, 813], [814], [815, 816], [815, 816], [815, 816], [817], [817], [817], [818, 819, 820], [818, 819, 820], [818, 819, 820], [818, 819, 820], [818, 819, 820], [818, 819, 820], [821, 822], [821, 822], [823, 824], [825, 826, 827, 828, 829, 830], [825, 826, 827, 828, 829, 830], [831], [832], [833, 834, 835], [833, 834, 835], [836, 837, 838], [836, 837, 838], [839, 840, 841], [842, 843, 844], [842, 843, 844], [845], [845], [846, 847], [846, 847], [848, 849, 850, 851], [848, 849, 850, 851], [848, 849, 850, 851], [852], [853], [853], [854], [855], [856], [857], [858], [859], [860], [861, 862], [861, 862], [863], [863], [864], [865, 866, 867], [865, 866, 867], [868], [868], [868], [868], [869], [870], [871], [872, 873, 874, 875, 876], [872, 873, 874, 875, 876], [877, 878, 879], [877, 878, 879], [880, 881, 882, 883], [880, 881, 882, 883], [884, 885], [884, 885], [886, 887], [888, 889, 890, 891], [892], [893], [894], [894], [895, 896], [897, 898, 899], [897, 898, 899], [897, 898, 899], [900], [900], [901], [902], [903, 904, 905], [906, 907], [908], [909, 910], [909, 910], [909, 910], [909, 910], [911, 912], [911, 912], [913], [914, 915], [914, 915], [916], [916], [917, 918, 919, 920, 921, 922], [917, 918, 919, 920, 921, 922], [917, 918, 919, 920, 921, 922], [917, 918, 919, 920, 921, 922], [923], [923], [924, 925, 926], [924, 925, 926], [927, 928], [927, 928], [929, 930], [931], [932, 933, 934], [932, 933, 934], [932, 933, 934], [935], [935], [936], [937], [938, 939], [940], [941, 942], [943, 944], [945], [945], [946], [947], [947], [947], [947], [948, 949, 950, 951], [948, 949, 950, 951], [952], [953], [953], [954], [955], [955], [955], [955], [956]]
            break
    
    assert has_specific_doc

    train, val, test = TextSimplificationSloveneLoader(keep_train_test_split=True).load(path)

    assert len(train.documents) == 1

    for document in train.documents:
        if document.original_items[0] == "Ker je bil Matevž okrog ušes tako čuden, ga ni hotelo v vasi nobeno dekle.":
            has_specific_doc = True
            assert document.original_items[-1] == "Stekel je k sestri Ruti in zaklical: \"Breda se smeje, Breda!\""
            assert document.simplified_items[0] == "Ker je bil brez ušesa, ga ni hotela nobena ženska."
            assert document.simplified_items[-1] == "Stekel je k sestri Ruti in klical: Breda se smeje!"
            assert document.original_to_simplified_alignment == [[0], [1], [1], [1], [2], [3, 4], [5, 6], [7], [7], [8], [9], [10], [11], [12, 13], [14], [15], [16, 17, 18], [19, 20, 21], [22], [23], [24], [25], [26], [27], [28, 29], [30], [31], [32], [33], [34], [35], [36], [37], [38, 39, 40], [41], [42], [43], [44, 45], [46], [47], [48, 49], [50, 51, 52, 53], [54], [55], [56], [57], [58], [59], [60], [61], [62], [63], [64], [65], [66], [67], [68], [69, 70], [71], [72, 73], [74, 75], [76], [77], [78], [79, 80], [81], [82], [83], [84], [85], [86], [87, 88], [89], [90], [91, 92], [93], [94], [95], [96], [96], [97], [98], [99, 100], [101], [102], [103], [104], [104], [105], [105], [106], [107], [108, 109], [110], [111], [112, 113], [114, 115, 116, 117, 118, 119], [120, 121], [122], [123], [124], [125], [126], [127, 128], [129, 130, 131], [132], [133, 134], [135], [136, 137], [138], [139, 140], [141, 142], [143], [144, 145, 146], [147], [148], [149], [150], [150], [151], [152], [153, 154], [155, 156, 157], [158], [159], [160, 161, 162], [163], [164], [165], [166], [167], [168], [169], [170, 171], [172], [172], [173], [174], [175], [176], [176], [177], [178], [179], [180, 181], [180, 181], [182, 183, 184, 185], [186, 187, 188], [189, 190, 191], [192, 193], [194, 195, 196, 197, 198], [199], [200, 201, 202], [203], [204], [205], [206, 207, 208, 209, 210], [211, 212], [213], [214, 215], [216, 217], [218], [219, 220, 221, 222, 223], [224], [225], [226], [227], [228], [229], [229], [230], [230], [231], [232], [233], [234], [235], [236], [237], [238], [239], [239], [240], [241], [242], [243], [244], [245], [246], [246], [247], [247], [248], [248], [249], [250], [251, 252], [253], [254], [255], [256, 257, 258], [259], [260], [260], [261], [262], [263], [264], [265], [266], [266], [267], [267], [267], [268], [269], [270], [271], [272], [273, 274, 275], [276, 277], [276, 277], [278], [278], [279], [280], [281], [281], [282], [283], [284], [284], [285], [285], [286], [287], [287], [288], [289], [290], [290], [290], [291], [292], [292], [293], [294], [295], [296], [296], [296], [297], [298], [298], [299], [300, 301], [302], [302], [302], [303], [304], [305], [306], [307, 308], [309], [309], [310], [310], [311, 312], [313], [313], [314], [315], [316], [317], [318], [318], [318], [319], [320], [320], [321], [321], [322], [323, 324], [325, 326, 327, 328, 329], [330], [331, 332], [333, 334], [335, 336], [337, 338], [339, 340, 341], [342, 343], [344, 345, 346], [347], [348], [349], [350, 351], [352, 353], [354, 355], [356, 357, 358], [359, 360], [361], [362, 363], [364], [365], [366, 367], [368, 369], [368, 369], [370, 371, 372], [373], [374], [375], [376, 377, 378], [379, 380], [381], [382, 383, 384], [385], [386], [387], [388], [389], [390], [391, 392], [393], [394], [395], [396], [397], [398], [399], [400, 401, 402], [403], [404], [405], [406], [407], [408], [409], [410, 411, 412], [410, 411, 412], [413], [414], [415, 416, 417], [418, 419], [420, 421, 422], [423], [424], [425], [426, 427, 428], [429, 430], [431], [432, 433, 434, 435], [436, 437], [438, 439, 440, 441], [442], [443], [444], [445, 446], [447], [448], [449], [450], [451], [452], [453, 454], [455], [456, 457, 458], [459], [460, 461, 462], [463], [463], [464], [465], [465], [466], [467], [468, 469], [470], [471], [472], [473], [474], [475], [476], [477], [478], [479], [480], [481], [482], [483], [484], [484], [484], [485], [486], [487], [488], [489], [490], [490], [491], [492], [493], [494], [494], [494], [495], [496], [497, 498], [499], [499], [500], [501], [501], [502], [503], [504], [504], [505], [506], [507], [508], [508], [509], [510, 511], [510, 511], [512], [513], [514], [515], [516], [516], [517], [518], [519, 520], [521], [522], [523, 524, 525], [523, 524, 525], [526], [527, 528, 529], [527, 528, 529], [530], [531], [532], [533], [534], [535], [536], [537], [538], [539], [540], [541], [542], [543], [544, 545], [546], [547], [548], [549, 550], [551], [552], [553], [554], [554], [555, 556], [557], [558, 559], [560], [560], [561], [562], [562], [562], [563], [563], [564], [565, 566], [567], [568], [569], [570], [571], [572], [573], [574], [575, 576], [575, 576], [577], [578], [578], [579], [580], [581], [582], [583], [584, 585, 586], [587], [588], [589], [590], [591], [592], [593], [594], [595], [596], [597], [598], [599], [600], [601], [601], [602], [602], [603], [604], [605], [605], [605], [606], [607], [607], [607], [608], [608], [609], [610], [611], [612], [613], [613], [614], [614], [615], [616], [617], [618], [619], [620], [621, 622], [623], [624], [625], [626], [627, 628], [629], [630, 631, 632], [633], [634], [634], [635], [636, 637], [638], [639], [640], [641], [642], [643], [644], [645], [646], [647], [648], [649], [650], [651], [652], [653], [653], [653], [654], [655], [656], [657], [658], [659], [660, 661], [662], [663], [664], [664], [665], [666], [667], [668], [669], [669], [670], [671], [672, 673, 674], [672, 673, 674], [675], [676], [677], [677], [677], [678, 679], [680], [681], [682], [683], [684, 685, 686], [687], [688], [689], [690], [691], [691], [692], [693], [694], [695], [695], [696], [697], [698], [699], [699], [700], [701, 702], [703], [704], [705], [705], [705], [706], [707], [708], [708], [709, 710, 711], [712], [713], [714], [715], [716], [717], [718], [719], [720], [721], [722], [723], [724], [725, 726, 727], [728], [728], [729], [730], [731], [732], [733], [734, 735], [736], [737], [737], [738], [739], [740], [740], [741], [742], [743], [744], [745], [746], [747], [748, 749], [750, 751], [752], [753], [754], [755], [756], [757], [758], [759, 760, 761], [762], [763], [764], [764], [765, 766, 767], [768], [768], [769], [770], [771], [772, 773], [772, 773], [772, 773], [772, 773], [774, 775, 776], [777], [777], [778], [779, 780], [779, 780], [781], [782], [783, 784, 785], [786, 787], [788, 789], [790, 791, 792, 793], [790, 791, 792, 793], [794, 795, 796], [794, 795, 796], [794, 795, 796], [794, 795, 796], [794, 795, 796], [797], [798, 799, 800, 801], [798, 799, 800, 801], [798, 799, 800, 801], [802], [803, 804], [805, 806], [805, 806], [807, 808], [809], [810, 811, 812], [810, 811, 812], [813], [813], [814, 815], [814, 815], [814, 815], [816], [816], [817], [818], [818], [819], [820, 821], [820, 821], [822, 823, 824], [822, 823, 824], [822, 823, 824], [825], [826], [827], [828, 829, 830], [831, 832], [831, 832], [833], [834], [835, 836], [835, 836], [835, 836], [837, 838, 839], [840], [841], [842], [842], [843], [844], [845], [846], [847], [848], [849], [850], [851], [852, 853], [852, 853], [854, 855], [856], [857], [858, 859], [860, 861], [862, 863], [864, 865, 866], [867, 868], [867, 868], [867, 868], [867, 868], [869], [870, 871], [870, 871], [872, 873], [872, 873], [874, 875], [874, 875], [876, 877], [876, 877], [878], [878], [878], [879, 880], [881, 882, 883], [884], [884], [885], [886], [887, 888], [887, 888], [887, 888], [889], [889], [889], [890, 891, 892, 893, 894, 895, 896], [890, 891, 892, 893, 894, 895, 896], [890, 891, 892, 893, 894, 895, 896], [890, 891, 892, 893, 894, 895, 896], [890, 891, 892, 893, 894, 895, 896], [890, 891, 892, 893, 894, 895, 896], [890, 891, 892, 893, 894, 895, 896], [897], [898], [898], [898], [898], [899], [900, 901, 902], [900, 901, 902], [903, 904, 905], [906, 907, 908, 909, 910, 911], [906, 907, 908, 909, 910, 911], [906, 907, 908, 909, 910, 911], [912, 913], [912, 913], [914], [914], [915, 916], [915, 916], [915, 916], [915, 916], [915, 916], [915, 916], [917], [918], [919, 920], [919, 920], [919, 920], [921, 922], [921, 922], [921, 922], [923], [923], [923], [924, 925], [924, 925], [924, 925], [926, 927], [928, 929], [928, 929], [930, 931, 932], [930, 931, 932], [930, 931, 932], [930, 931, 932], [933], [934, 935], [936], [937], [938], [939], [940], [941], [942], [943, 944], [943, 944], [945, 946], [947], [948, 949], [948, 949], [948, 949], [950, 951, 952, 953], [954], [955], [956], [957, 958], [957, 958], [957, 958], [957, 958], [957, 958], [959, 960], [959, 960], [959, 960], [961, 962], [961, 962], [961, 962], [961, 962], [963, 964], [963, 964], [965], [965], [966], [966], [966], [966], [967], [968], [969, 970], [971], [971], [972, 973, 974], [972, 973, 974], [972, 973, 974], [975, 976], [977], [978], [979], [979], [979], [980], [980], [981], [982, 983, 984, 985], [982, 983, 984, 985], [986, 987], [986, 987], [988], [989, 990], [989, 990], [991, 992], [993, 994, 995, 996], [993, 994, 995, 996], [993, 994, 995, 996], [993, 994, 995, 996], [993, 994, 995, 996], [993, 994, 995, 996], [997, 998], [999, 1000], [999, 1000], [999, 1000], [1001, 1002], [1001, 1002], [1003], [1003], [1004], [1005, 1006, 1007], [1005, 1006, 1007], [1005, 1006, 1007], [1008, 1009], [1010], [1011], [1012], [1012], [1013], [1014], [1014], [1015], [1015], [1016, 1017], [1018], [1019, 1020, 1021, 1022], [1023, 1024], [1023, 1024], [1023, 1024], [1023, 1024], [1025], [1026, 1027], [1028], [1029, 1030, 1031, 1032], [1033]]
            assert document.simplified_to_original_alignment == [[0], [1, 2, 3], [4], [5], [5], [6], [6], [7, 8], [9], [10], [11], [12], [13], [13], [14], [15], [16], [16], [16], [17], [17], [17], [18], [19], [20], [21], [22], [23], [24], [24], [25], [26], [27], [28], [29], [30], [31], [32], [33], [33], [33], [34], [35], [36], [37], [37], [38], [39], [40], [40], [41], [41], [41], [41], [42], [43], [44], [45], [46], [47], [48], [49], [50], [51], [52], [53], [54], [55], [56], [57], [57], [58], [59], [59], [60], [60], [61], [62], [63], [64], [64], [65], [66], [67], [68], [69], [70], [71], [71], [72], [73], [74], [74], [75], [76], [77], [78, 79], [80], [81], [82], [82], [83], [84], [85], [86, 87], [88, 89], [90], [91], [92], [92], [93], [94], [95], [95], [96], [96], [96], [96], [96], [96], [97], [97], [98], [99], [100], [101], [102], [103], [103], [104], [104], [104], [105], [106], [106], [107], [108], [108], [109], [110], [110], [111], [111], [112], [113], [113], [113], [114], [115], [116], [117, 118], [119], [120], [121], [121], [122], [122], [122], [123], [124], [125], [125], [125], [126], [127], [128], [129], [130], [131], [132], [133], [133], [134, 135], [136], [137], [138], [139, 140], [141], [142], [143], [144, 145], [144, 145], [146], [146], [146], [146], [147], [147], [147], [148], [148], [148], [149], [149], [150], [150], [150], [150], [150], [151], [152], [152], [152], [153], [154], [155], [156], [156], [156], [156], [156], [157], [157], [158], [159], [159], [160], [160], [161], [162], [162], [162], [162], [162], [163], [164], [165], [166], [167], [168, 169], [170, 171], [172], [173], [174], [175], [176], [177], [178], [179], [180, 181], [182], [183], [184], [185], [186], [187], [188, 189], [190, 191], [192, 193], [194], [195], [196], [196], [197], [198], [199], [200], [200], [200], [201], [202, 203], [204], [205], [206], [207], [208], [209, 210], [211, 212, 213], [214], [215], [216], [217], [218], [219], [219], [219], [220, 221], [220, 221], [222, 223], [224], [225], [226, 227], [228], [229], [230, 231], [232, 233], [234], [235, 236], [237], [238], [239, 240, 241], [242], [243, 244], [245], [246], [247], [248, 249, 250], [251], [252, 253], [254], [255], [255], [256, 257, 258], [259], [260], [261], [262], [263], [263], [264, 265], [266, 267], [268], [268], [269, 270], [271], [272], [273], [274], [275, 276, 277], [278], [279, 280], [281, 282], [283], [284], [284], [285], [285], [285], [285], [285], [286], [287], [287], [288], [288], [289], [289], [290], [290], [291], [291], [291], [292], [292], [293], [293], [293], [294], [295], [296], [297], [297], [298], [298], [299], [299], [300], [300], [300], [301], [301], [302], [303], [303], [304], [305], [306], [306], [307, 308], [307, 308], [309], [309], [309], [310], [311], [312], [313], [313], [313], [314], [314], [315], [316], [316], [316], [317], [318], [319], [320], [321], [322], [323], [323], [324], [325], [326], [327], [328], [329], [330], [331], [331], [331], [332], [333], [334], [335], [336], [337], [338], [339, 340], [339, 340], [339, 340], [341], [342], [343], [343], [343], [344], [344], [345], [345], [345], [346], [347], [348], [349], [349], [349], [350], [350], [351], [352], [352], [352], [352], [353], [353], [354], [354], [354], [354], [355], [356], [357], [358], [358], [359], [360], [361], [362], [363], [364], [365], [365], [366], [367], [367], [367], [368], [369], [369], [369], [370, 371], [372], [373, 374], [375], [376], [377], [377], [378], [379], [380], [381], [382], [383], [384], [385], [386], [387], [388], [389], [390], [391], [392, 393, 394], [395], [396], [397], [398], [399], [400, 401], [402], [403], [404], [405, 406, 407], [408], [409], [410], [410], [411, 412], [413], [414, 415], [416], [417], [418, 419], [420], [421], [422], [423, 424], [425], [426, 427], [426, 427], [428], [429], [430], [431], [432, 433], [434], [435], [436], [436], [437], [438], [439, 440], [439, 440], [439, 440], [441], [442, 443], [442, 443], [442, 443], [444], [445], [446], [447], [448], [449], [450], [451], [452], [453], [454], [455], [456], [457], [458], [458], [459], [460], [461], [462], [462], [463], [464], [465], [466, 467], [468], [468], [469], [470], [470], [471, 472], [473], [474, 475, 476], [477, 478], [479], [480], [480], [481], [482], [483], [484], [485], [486], [487], [488], [489, 490], [489, 490], [491], [492, 493], [494], [495], [496], [497], [498], [499], [499], [499], [500], [501], [502], [503], [504], [505], [506], [507], [508], [509], [510], [511], [512], [513], [514, 515], [516, 517], [518], [519], [520, 521, 522], [523], [524, 525, 526], [527, 528], [529], [530], [531], [532], [533, 534], [535, 536], [537], [538], [539], [540], [541], [542], [543], [543], [544], [545], [546], [547], [548], [548], [549], [550], [550], [550], [551], [552, 553], [554], [555], [555], [556], [557], [558], [559], [560], [561], [562], [563], [564], [565], [566], [567], [568], [569], [570], [571, 572, 573], [574], [575], [576], [577], [578], [579], [580], [580], [581], [582], [583, 584], [585], [586], [587], [588], [589, 590], [591], [592], [593, 594], [593, 594], [593, 594], [595], [596], [597, 598, 599], [600], [600], [601], [602], [603], [604], [605], [605], [605], [606], [607], [608], [609], [610, 611], [612], [613], [614], [615, 616], [617], [618], [619], [620, 621], [622], [623], [623], [624], [625], [626, 627, 628], [629], [630], [631, 632], [633], [633], [633], [634], [635], [636], [637], [638], [639], [640], [641], [642], [643], [644], [645], [646], [647], [647], [647], [648, 649], [650], [651], [652], [653], [654], [655], [655], [656], [657, 658], [659], [660], [661, 662], [663], [664], [665], [666], [667], [668], [669], [670], [670], [671], [671], [672], [673], [674], [675], [676], [677], [678], [679], [679], [679], [680], [681], [682, 683], [684], [684], [684], [685, 686], [687], [688], [689], [690, 691, 692, 693], [690, 691, 692, 693], [694], [694], [694], [695, 696], [697], [698, 699], [698, 699], [700], [701], [702], [702], [702], [703], [703], [704], [704], [705, 706], [705, 706], [705, 706], [705, 706], [707, 708, 709, 710, 711], [707, 708, 709, 710, 711], [707, 708, 709, 710, 711], [712], [713, 714, 715], [713, 714, 715], [713, 714, 715], [713, 714, 715], [716], [717], [717], [718, 719], [718, 719], [720], [720], [721], [722, 723], [722, 723], [722, 723], [724, 725], [726, 727, 728], [726, 727, 728], [729, 730], [731], [732, 733], [734], [735, 736], [735, 736], [737, 738, 739], [737, 738, 739], [737, 738, 739], [740], [741], [742], [743], [743], [743], [744, 745], [744, 745], [746], [747], [748, 749, 750], [748, 749, 750], [751], [751], [751], [752], [753], [754, 755], [756], [757], [758], [759], [760], [761], [762], [763], [764], [765, 766], [765, 766], [767], [767], [768], [769], [770], [770], [771], [771], [772], [772], [773], [773], [773], [774, 775, 776, 777], [774, 775, 776, 777], [778], [779, 780], [779, 780], [781, 782], [781, 782], [783, 784], [783, 784], [785, 786], [785, 786], [787, 788, 789], [790], [790], [791], [791], [791], [792, 793], [794], [795], [796, 797, 798], [796, 797, 798], [799, 800, 801], [802, 803, 804, 805, 806, 807, 808], [802, 803, 804, 805, 806, 807, 808], [802, 803, 804, 805, 806, 807, 808], [802, 803, 804, 805, 806, 807, 808], [802, 803, 804, 805, 806, 807, 808], [802, 803, 804, 805, 806, 807, 808], [802, 803, 804, 805, 806, 807, 808], [809], [810, 811, 812, 813], [814], [815, 816], [815, 816], [815, 816], [817], [817], [817], [818, 819, 820], [818, 819, 820], [818, 819, 820], [818, 819, 820], [818, 819, 820], [818, 819, 820], [821, 822], [821, 822], [823, 824], [825, 826, 827, 828, 829, 830], [825, 826, 827, 828, 829, 830], [831], [832], [833, 834, 835], [833, 834, 835], [836, 837, 838], [836, 837, 838], [839, 840, 841], [842, 843, 844], [842, 843, 844], [845], [845], [846, 847], [846, 847], [848, 849, 850, 851], [848, 849, 850, 851], [848, 849, 850, 851], [852], [853], [853], [854], [855], [856], [857], [858], [859], [860], [861, 862], [861, 862], [863], [863], [864], [865, 866, 867], [865, 866, 867], [868], [868], [868], [868], [869], [870], [871], [872, 873, 874, 875, 876], [872, 873, 874, 875, 876], [877, 878, 879], [877, 878, 879], [880, 881, 882, 883], [880, 881, 882, 883], [884, 885], [884, 885], [886, 887], [888, 889, 890, 891], [892], [893], [894], [894], [895, 896], [897, 898, 899], [897, 898, 899], [897, 898, 899], [900], [900], [901], [902], [903, 904, 905], [906, 907], [908], [909, 910], [909, 910], [909, 910], [909, 910], [911, 912], [911, 912], [913], [914, 915], [914, 915], [916], [916], [917, 918, 919, 920, 921, 922], [917, 918, 919, 920, 921, 922], [917, 918, 919, 920, 921, 922], [917, 918, 919, 920, 921, 922], [923], [923], [924, 925, 926], [924, 925, 926], [927, 928], [927, 928], [929, 930], [931], [932, 933, 934], [932, 933, 934], [932, 933, 934], [935], [935], [936], [937], [938, 939], [940], [941, 942], [943, 944], [945], [945], [946], [947], [947], [947], [947], [948, 949, 950, 951], [948, 949, 950, 951], [952], [953], [953], [954], [955], [955], [955], [955], [956]]
            break
    
    assert has_specific_doc

    assert len(val.documents) == 1

    for document in val.documents:
        if document.original_items[0] == "Vsa vas je dobro vedela, da ga na svetu ni hudobnejšega človeka od Vrbarjevega Matevža .":
            has_specific_doc = True
            assert document.original_items[-1] == "Romeo govori Juliji: \"Prisegam ti na luno, ki se z žarki srebrnimi igra na tem drevesu, da te ljubim.\""
            assert document.simplified_items[0] == "Matevž je bil zelo hudoben človek."
            assert document.simplified_items[-1] == "Juliji Romeo priseže, da jo ljubi in da jo bo vedno ljubil."
            assert document.original_to_simplified_alignment == [[0], [1], [2], [3], [4], [5, 6], [7, 8], [9, 10, 11, 12, 13], [14], [15, 16], [17], [17], [18], [19, 20, 21], [22], [23], [24, 25], [26, 27], [28], [29], [30, 31], [32, 33, 34, 35], [36, 37, 38], [39], [40], [41], [42], [43, 44, 45], [46], [46], [47, 48, 49], [50, 51], [52], [53, 54], [55, 56], [57, 58], [59, 60], [61, 62], [63, 64, 65, 66], [67], [68], [69, 70, 71], [72], [73], [74], [75], [76], [77], [78], [79], [80], [81], [82], [83, 84, 85], [83, 84, 85], [83, 84, 85], [86], [87, 88], [89], [90], [91, 92], [93], [94], [95], [96], [97, 98], [99], [100], [101], [102], [103], [104], [105, 106], [105, 106], [107], [108], [109], [110], [110], [111], [112], [113], [114, 115], [114, 115], [116, 117], [116, 117], [118], [119, 120], [119, 120], [121], [122], [123], [124], [125, 126], [127], [128, 129], [130], [130], [131], [131], [132], [132], [133], [134], [134], [135], [136]]
            assert document.simplified_to_original_alignment == [[0], [1], [2], [3], [4], [5], [5], [6], [6], [7], [7], [7], [7], [7], [8], [9], [9], [10, 11], [12], [13], [13], [13], [14], [15], [16], [16], [17], [17], [18], [19], [20], [20], [21], [21], [21], [21], [22], [22], [22], [23], [24], [25], [26], [27], [27], [27], [28, 29], [30], [30], [30], [31], [31], [32], [33], [33], [34], [34], [35], [35], [36], [36], [37], [37], [38], [38], [38], [38], [39], [40], [41], [41], [41], [42], [43], [44], [45], [46], [47], [48], [49], [50], [51], [52], [53, 54, 55], [53, 54, 55], [53, 54, 55], [56], [57], [57], [58], [59], [60], [60], [61], [62], [63], [64], [65], [65], [66], [67], [68], [69], [70], [71], [72, 73], [72, 73], [74], [75], [76], [77, 78], [79], [80], [81], [82, 83], [82, 83], [84, 85], [84, 85], [86], [87, 88], [87, 88], [89], [90], [91], [92], [93], [93], [94], [95], [95], [96, 97], [98, 99], [100, 101], [102], [103, 104], [105], [106]]
            break

    assert has_specific_doc

    assert len(test.documents) == 1

    for document in test.documents:
        if document.original_items[0] == "Nekdaj sta se Tinče Muha, znan pijanček, in pa Matevž prepirala zavoljo poti do studenca.":
            has_specific_doc = True
            assert document.original_items[-1] == "Grem, a spravil bo plačilo grenko za predrznost svojo."
            assert document.simplified_items[0] == "Nekoč se je Matevž prepiral s pijancem ."
            assert document.simplified_items[-1] == "Odloči se, da bo počakal."
            assert document.original_to_simplified_alignment == [[0], [1, 2], [3], [4], [5], [6], [7, 8], [9, 10, 11], [12], [13, 14], [15], [15], [16], [17], [18], [19], [20], [21], [22], [23], [24, 25], [26], [27], [28], [29], [30], [31], [32], [33], [33], [34], [35], [36], [37], [38], [39], [39], [40], [41], [42, 43], [44], [44], [45], [46], [47], [48], [49], [50], [50], [50], [51], [51], [52], [53], [53], [54], [55], [56], [57], [57], [58], [59], [59], [60, 61], [60, 61], [60, 61], [62], [62], [62], [63], [64], [65], [66], [67], [67], [67], [67], [67], [68], [69, 70], [71], [72], [73, 74], [75], [76], [77], [78, 79], [80], [81, 82], [81, 82], [83], [84], [85], [86], [87, 88], [89, 90, 91, 92], [93], [94, 95], [96], [97], [98], [99, 100], [101, 102, 103], [104], [105], [106], [107], [107], [108], [109], [110], [111], [112], [113], [114], [114], [115]]
            assert document.simplified_to_original_alignment == [[0], [1], [1], [2], [3], [4], [5], [6], [6], [7], [7], [7], [8], [9], [9], [10, 11], [12], [13], [14], [15], [16], [17], [18], [19], [20], [20], [21], [22], [23], [24], [25], [26], [27], [28, 29], [30], [31], [32], [33], [34], [35, 36], [37], [38], [39], [39], [40, 41], [42], [43], [44], [45], [46], [47, 48, 49], [50, 51], [52], [53, 54], [55], [56], [57], [58, 59], [60], [61, 62], [63, 64, 65], [63, 64, 65], [66, 67, 68], [69], [70], [71], [72], [73, 74, 75, 76, 77], [78], [79], [79], [80], [81], [82], [82], [83], [84], [85], [86], [86], [87], [88, 89], [88, 89], [90], [91], [92], [93], [94], [94], [95], [95], [95], [95], [96], [97], [97], [98], [99], [100], [101], [101], [102], [102], [102], [103], [104], [105], [106, 107], [108], [109], [110], [111], [112], [113], [114, 115], [116]]
            break

    assert has_specific_doc

    print("Text-Simplification-Slovene Passed All Tests")

def klexikon_tests(path):
    klexikon = KlexikonLoader(keep_train_test_split=False).load(path)[0]

    assert len(klexikon.documents) == 2893

    for document in klexikon.documents:
        if document.original_items[0] == "ABBA ist eine schwedische Popgruppe, die aus den damaligen Paaren Agnetha Fältskog und Björn Ulvaeus sowie Benny Andersson und Anni-Frid Lyngstad besteht und sich 1972 in Stockholm formierte.":
            has_specific_doc = True
            assert document.original_items[-1] == "ABBA Charts"
            assert document.simplified_items[0] == "ABBA war eine Musikgruppe aus Schweden."
            assert document.simplified_items[-1] == "2008 erschien ein Kinofilm von diesem Musical."
            break

    assert has_specific_doc

    train, validation, test = KlexikonLoader(keep_train_test_split=True).load(path)

    assert len(train.documents) == 2346

    for document in train.documents:
        if document.original_items[0] == "ABBA ist eine schwedische Popgruppe, die aus den damaligen Paaren Agnetha Fältskog und Björn Ulvaeus sowie Benny Andersson und Anni-Frid Lyngstad besteht und sich 1972 in Stockholm formierte.":
            has_specific_doc = True
            assert document.original_items[-1] == "ABBA Charts"
            assert document.simplified_items[0] == "ABBA war eine Musikgruppe aus Schweden."
            assert document.simplified_items[-1] == "2008 erschien ein Kinofilm von diesem Musical."
            break

    assert has_specific_doc

    assert len(validation.documents) == 273

    for document in validation.documents:
        if document.original_items[0] == "Die Aare (frz. Aar/Arole; lat. Arula/Arola/Araris) ist der längste gänzlich innerhalb der Schweiz verlaufende Fluss.":
            has_specific_doc = True
            assert document.original_items[-1] == "Der Verein AareLand unterstützt verschiedene Projekte zur Koordination der Freizeitaktivitäten und zur Förderung einer nachhaltigen Entwicklung der Region."
            assert document.simplified_items[0] == "Die Aare ist der längste Fluss innerhalb der Schweiz."
            assert document.simplified_items[-1] == "An dieser Stelle liegt auch die Grenze zwischen der Schweiz und Deutschland."
            break

    assert has_specific_doc

    assert len(test.documents) == 274

    for document in test.documents:
        if document.original_items[0] == "AC/DC (; englische Abkürzung für \"Wechselstrom/Gleichstrom\") ist eine australische Hard-Rock-Band, die 1973 von den in Schottland geborenen Brüdern Angus und Malcolm Young gegründet wurde.":
            has_specific_doc = True
            assert document.original_items[-1] == "grau schraffiert: keine Chartdaten aus diesem Jahr verfügbar"
            assert document.simplified_items[0] == "AC/DC ist eine Musikgruppe, die Hardrock spielt."
            assert document.simplified_items[-1] == "Bekannte Lieder von AC/DC sind \"Highway to Hell\", \"Hells Bells\" oder \"Thunderstruck\"."
            break

    assert has_specific_doc

    print("Klexikon Passed All Tests")


def print_document_summary_test_fmt(document, document_segmented = True):
    print('        if document.original_items[0] == "' + document.original_items[0] + '":')
    print('            has_specific_doc = True')
    print('            assert document.original_items[-1] == "' + document.original_items[-1] + '"')
    print('            assert document.simplified_items[0] == "' + document.simplified_items[0] + '"')
    print('            assert document.simplified_items[-1] == "' + document.simplified_items[-1] + '"')
    if (type(document) is AlignedParallelDocument):
        if (document_segmented):
            print('            assert document.original_to_simplified_alignment == ', end='')
            print(document.original_to_simplified_alignment)
            print('            assert document.simplified_to_original_alignment == ', end='')
            print(document.simplified_to_original_alignment)
        else:
            print('            assert document.original_to_simplified_alignment == [[i] for i in range(len(document.simplified_items))]')
            print('            assert document.simplified_to_original_alignment == [[i] for i in range(len(document.original_items))]')
    print('            break')

# TODO REPLACE WITH PATH TO YOUR CORPORA FOLDER
# path = "INSERT PATH TO YOUR CORPORA FOLDER HERE"
path = "/Users/michaelryan/Downloads/Corpora"

simplext_tests(os.path.join(path,'Spanish', 'SimplextData'))
cbst_tests(os.path.join(path,'Basque','CBST', 'ETSC_CBST'))
porsimples_tests(os.path.join(path, 'Brazilian Portuguese', 'PorSimples'))
simpitiki_tests(os.path.join(path,'Italian', 'SIMPITIKI', 'simpitiki-master'))
terence_teacher_tests(os.path.join(path,'Italian', 'TerenceTeacher', 'CORPORA_TEXT_SIMP'))
paccssit_tests(os.path.join(path,'Italian','PaCCSS-IT','data-set'))
clear_tests(os.path.join(path,'French','corpus_coling'))
wiki_large_fr_tests(os.path.join(path,'French','corpus_coling'))
dsim_tests(os.path.join(path,'Danish','DSim'))
geolino_tests(os.path.join(path, 'German', 'GEOLino'))
easy_japanese_tests(os.path.join(path, 'Japanese','EasyJapanese'))
easy_japanese_extended_tests(os.path.join(path, 'Japanese', 'EasyJapaneseExtended'))
text_complexity_de_tests(os.path.join(path, 'German', 'TextComplexityDE'))
rsse_tests(os.path.join(path, 'Russian', 'RuSimpleSentEval'))
simplify_ur_tests(os.path.join(path,'Urdu','SimplifyUR'))
german_news_tests(os.path.join(path, 'German', 'APA_sentence-aligned_LHA'))
newsela_es_tests(os.path.join(path, 'Spanish','newsela_es'))
ru_adapt_tests(os.path.join(path,'Russian','RuAdaptUnreleased'))
simple_german_tests(os.path.join(path, 'German', 'Corpus_for_Text_Simplification_of_German'))
alector_tests(os.path.join(path, 'French', 'alector_corpus-master'))
ru_wiki_large_tests(os.path.join(path,'Russian','RuWikiLarge'))
newsela_en_tests(os.path.join(path,'English', 'newsela-auto', 'newsela-auto', 'all_data','newsela-auto-all-data.json'))
wikiauto_en_tests(os.path.join(path, 'English', 'wiki-auto-master'))
asset_tests(os.path.join(path,'English','asset-main'))
adminit_tests(os.path.join(path, 'Italian', 'admin-It-main'))
text_simplification_slovene_tests(os.path.join(path, 'Slovene', 'text-simplification-slovene-main'))
klexikon_tests(os.path.join(path, 'German', 'klexikon'))