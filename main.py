import dhd

# This generates the data files necessary for vizualisations in the notebooks.

from dhd.corpus import Corpus
import yaml
with open("CONFIG.yaml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)

c = Corpus(name="results/dhd-corpus.parquet", cfg=cfg, force=True)
c._abstracts.applymap(str).to_parquet("results/dhd-corpus.parquet")
c.get_authors().to_excel("results/authors.xlsx")
c.get_coauthorship().to_excel("results/coauthors.xlsx")
