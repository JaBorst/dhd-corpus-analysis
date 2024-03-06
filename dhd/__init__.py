from .corpus import Corpus
import yaml
def main(CONFIG):
    with open(CONFIG, "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    c = Corpus("dhd-corpus.parquet", cfg)