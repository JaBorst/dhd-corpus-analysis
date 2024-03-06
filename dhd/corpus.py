import pandas as pd
from tqdm import tqdm
from .tocs import TOCS
from .git import GitAcc2014, GitAcc2015 , GitAcc
from pathlib import Path
from collections import Counter
class Corpus:
    def __init__(self, name, cfg, cityfile="results/cities.txt", force=False):
        self.name=Path(name)
        self._config = cfg
        self.cityfile=cityfile

        if (not self.name.exists()) or force:
            self.run()
        else:
            self._abstracts = pd.read_parquet(self.name)



    def run(self):
        data = [(year, type, *elem) for year, tocs in TOCS.items() for type, listofelem in tocs.items() for elem in listofelem]
        self.tocs = pd.DataFrame(data , columns=["year", "type", "title", "authors" ])

        files = [
            GitAcc2014(self._config["DHd-Abstracts-2014"]).run(),
            GitAcc2015(self._config["DHd-Abstracts-2015"]).run(),
            GitAcc(self._config["DHd-Abstracts-2016"]).run(),
            GitAcc(self._config["DHd-Abstracts-2017"]).run(),
            GitAcc(self._config["DHd-Abstracts-2018"]).run(),
            GitAcc(self._config["DHd-Abstracts-2019"]).run(),
            GitAcc(self._config["DHd-Abstracts-2020"]).run(),
            GitAcc(self._config["DHd-Abstracts-2022"]).run(),
            GitAcc(self._config["DHd-Abstracts-2023"]).run()
        ]

        corpus = pd.concat(files, axis=0)
        self._abstracts = corpus
        corpus = corpus.reset_index(drop=True)
        self.extract_affiliations(cityfile=self.cityfile)


        print(corpus.isna().sum())
        print((corpus=="").sum())
        return corpus
    def get_authors(self):
        _tmp = self._abstracts.copy()
        _tmp.authors = _tmp.authors.str.split("; ")
        _tmp = _tmp.explode("authors")
        _tmp = _tmp[(_tmp.authors.map(len) > 1)]
        _tmp = _tmp.groupby(["authors"]).year.value_counts().unstack().fillna(0).astype(int)
        _tmp["overall"] = _tmp.sum(axis=1).astype(int)
        return _tmp

    def get_coauthorship(self):
        _tmp = self._abstracts.copy()
        _tmp.authors = _tmp.authors.str.replace("  ", " ")

        _tmp.authors = _tmp.authors.str.split("; ")
        _tmp.affiliation = _tmp.affiliation.str.split("; ")

        from itertools import combinations
        from collections import Counter
        def _cp(x):
            return sum([list((e,e) for e in authors) +  list(e for e in combinations(authors, 2))  for authors in x],[])
        pairs = _tmp.groupby(['year']).authors.apply(_cp)
        pairs.reset_index()

        authors = list(set(sum(_tmp.authors, [])))
        coauthorship = pd.DataFrame(index=authors, columns=authors).fillna(0).astype(int)

        for (a1,a2) in sum(pairs,[]):
            coauthorship.loc[a1, a2] += 1

        import networkx as nx
        coauthorship.drop(index=[""],columns=[""], inplace=True)
        G = nx.from_pandas_adjacency(coauthorship).to_undirected()

        nx.set_node_attributes(G, Counter(sum(_tmp.authors, [])), "overall_frequency")

        aff = pd.DataFrame(sum(_tmp[["authors", "affiliation"]].apply(lambda x: list(zip(x["authors"], x["affiliation"])), axis=1),[]))
        aff[1] = aff[1].map(lambda x: x.split(", ")[0])

        affiliation_dict = aff.groupby([0]).agg(mod=(1, lambda x: x.value_counts().index[0])).to_dict()["mod"]
        nx.set_node_attributes(G, affiliation_dict, "affiliation")

        nx.write_gexf(G,"coauthorship.gexf")
        return coauthorship

    def __getitem__(self, item):
        return self._abstracts[item]

    def extract_affiliations(self, cityfile=None):
        if cityfile is None:
            cityfile = "cities.txt"

        cityfile = Path(cityfile)
        if cityfile.exists():
            cities = [x.split(":") for x in cityfile.read_text().split("\n") if x != ""]
            cities = {x[0].lower(): x[1] if len(x) == 2 else x[0] for x in cities}


            def match(x, cities):
                import regex
                found = []
                for city in cities.keys():
                    matches = regex.findall(city, x.lower())
                    if matches:
                        found.extend([city for m in matches])
                return cities[found[0]] if len(found) > 0 else []

            self._abstracts["cities"] = self._abstracts["affiliation"].map(lambda x: [match(a, cities) for  a in x.split("; ")])
            # self._abstracts[self._abstracts.cities.map(lambda x: any(e == [] for e in x))][
            #     ["affiliation", "cities"]].values

            unmapped=set(sum(self._abstracts[self._abstracts.cities.map(lambda x: any(e == [] for e in x))][["affiliation", "cities"]].apply(lambda x: [k for k,v in zip(x["affiliation"].split("; "),x["cities"]) if v ==[]], axis=1) ,[]))
            with open("results/unmapped-institutions.txt","w")as f:
                f.write("\n".join(unmapped))
            self._abstracts["cities"] = self._abstracts["cities"].map(lambda x: "; ".join([e  if e != [] else "" for e in x]))

        else:
            cities = []

            from flair.data import Sentence
            from flair.models import SequenceTagger

            # load tagger
            tagger = SequenceTagger.load("flair/ner-german")

            affils = self._abstracts["affiliation"].map(Sentence).to_list()

            tagger.predict(affils, mini_batch_size=32, verbose=True)
            from collections import Counter

            cities = Counter([entity.text for affil in affils for entity in affil.get_spans('ner')  if entity.tag == "LOC"])
            cities = [city for city, count in cities.items() if count > 1]

            with open(cityfile, "w") as f:
                f.write("\n".join(cities))
            return


        pass
