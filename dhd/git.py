from zipfile import ZipFile
from urllib.request import urlopen
from io import BytesIO
import xml.etree.ElementTree as ET
from PyPDF2 import PdfReader
import pandas as pd
from bs4 import BeautifulSoup

class GitAcc:
    def __init__(self, config, preferXML=False):
        self._config = config
        self.repo = config["url"]

    def get_toc(self, zipfile):
        raise NotImplementedError

    def extract_content(self, x, zipfile):
        if x.lower().endswith(".pdf"):
            pdf = PdfReader(zipfile.open(x), "r")
            r= {
                "file": x.split("/")[-1],
                "filetype": "pdf",
                "publication_type": "",
                "keywords": "",
                "topics": "",
                "text": " ".join([page.extract_text() for page in pdf.pages]),
                "bib": None}
        elif x.lower().endswith(".xml"):
            text = BeautifulSoup(zipfile.open(x).read().decode(), features="xml")
            r= {
                "file": x.split("/")[-1],
                "filetype": "xml",
                "publication_type":"; ".join( [x.getText().strip().lower() for x in text.findAll("keywords", scheme="ConfTool", n="category")]),
                "keywords":"; ".join([x.getText() for e in text.findAll("keywords", scheme="ConfTool", n="keywords") for x in e.findAll("term")]),
                "topics":"; ".join([x.getText() for e in text.findAll("keywords", scheme="ConfTool", n="topics") for x in e.findAll("term")]),
                "text": text.title.getText().strip() +"\n\n" + text.body.getText().strip(),
                "bib": [x.getText().strip().replace("\n", "") for x in text.find_all("bibl")]
            }
            test = r["keywords"]
        return r
    def read_files(self, zipfile):
        files = [x.filename for x in zipfile.filelist if self._config["files"] in x.filename and (x.filename.endswith(".pdf") or x.filename.endswith(".xml"))]
        content = [self.extract_content(x, zipfile) for x in files]
        return pd.DataFrame(content, columns=["file", "filetype",  "publication_type","keywords", "topics", "text", "bib"])

    def _read_meta_manually(self, zipfile):
        _meta_xml = [x.filename for x in zipfile.filelist for f in self._config["meta"] if
                     x.filename.endswith(f)][0]
        import xml
        f = xml.dom.minidom.parse(zipfile.open(_meta_xml))
        authors = [
            "; ".join([n.getElementsByTagName("name")[0].firstChild.data for n in x.getElementsByTagName("creator")])
            for x in f.getElementsByTagName("creators")]
        affiliation = [
            "; ".join([[x.firstChild.data if x.firstChild else None for x in n.getElementsByTagName("affiliation")][0] for n in
             x.getElementsByTagName("creator")]) for x in f.getElementsByTagName("creators")]
        title = [x.firstChild.data for x in f.getElementsByTagName("title")]
        keywords = "; ".join([x.firstChild.data for x in f.getElementsByTagName("keywords")])
        toc = pd.DataFrame(zip(title, authors, affiliation, ),
                           columns=["title", "authors", "affiliation"])
        return toc

    def _read_meta(self, zipfile):
        content = []
        self._meta_xml = [x.filename for x in zipfile.filelist for f in self._config["meta"] if
                          x.filename.endswith(f)]
        content.extend([pd.read_xml(zipfile.open(f, encoding="utf8"), parser="etree") for f in self._meta_xml])
        toc = pd.concat(content, axis=0)
        return toc

    def _read_package(self, zipfile):
        content = []
        self._meta_package = [x.filename for x in zipfile.filelist for f in self._config["package"] if
                              x.filename.endswith(f)]
        if self.repo.endswith("2022"):
            content.extend([pd.read_csv(zipfile.open(f), sep=";", encoding='latin1') for f in self._meta_package])
        else:
            content.extend([pd.read_csv(zipfile.open(f), encoding='utf8') for f in self._meta_package])
        toc = pd.concat(content, axis=0)
        return toc

    def get_authors(self):
        return
    def run(self):
        http_response = urlopen(self.repo + "/archive/refs/heads/main.zip")
        zipfile = ZipFile(BytesIO(http_response.read()))
        toc = self.get_toc(zipfile)
        content = self.read_files(zipfile)
        self._abstracts = self.merge(toc, content)
        zipfile.close()
        self._abstracts["year"] = self.repo.split("-")[-1]
        return self._abstracts

class GitAcc2014(GitAcc):
    def __init__(self, config):
        super().__init__(config)

    def get_toc(self, zipfile):
        _meta_xml = [x.filename for x in zipfile.filelist for f in self._config["meta"] if
                          x.filename.endswith(f)][0]
        import xml
        f = xml.dom.minidom.parse(zipfile.open(_meta_xml))
        authors = ["; ".join([n.getElementsByTagName("name")[0].firstChild.data for n in x.getElementsByTagName("creator")]) for x in f.getElementsByTagName("creators")]
        affiliation = ["; ".join([n.getElementsByTagName("affiliation")[0].firstChild.data for n in x.getElementsByTagName("creator")]) for x in f.getElementsByTagName("creators")]
        title = [x.firstChild.data for x in f.getElementsByTagName("title")]
        publication_type = [x.firstChild.data for x in f.getElementsByTagName("publication_type")]
        toc = pd.DataFrame(zip(title, authors, affiliation, publication_type), columns=["title", "authors", "affiliation", "publication_type"])
        return toc

    def merge(self, toc, content):
        import regex
        del content["publication_type"]
        def _title_in_text(x, y):
            c = (x["authors"].split("; ")[0].replace(", ","_") + "_" + x["title"][:5].replace(" ","_")).lower()
            r = [ t for t in y["file"]  if bool(regex.match(f"({c}){{e<=6}}", (t).lower()[:len(c)]))]
            return r[0] if len(r) > 0 else None
        toc["file"] = toc.apply(lambda x: _title_in_text(x, content), axis=1)
        return pd.merge(toc, content, on="file", how="left")


class GitAcc2015(GitAcc):
    def __init__(self, config):
        super().__init__(config)

    def get_toc(self, zipfile):
        _meta_xml = [x.filename for x in zipfile.filelist for f in self._config["meta"] if
                     x.filename.endswith(f)][0]
        import xml
        f = xml.dom.minidom.parse(zipfile.open(_meta_xml))
        authors = [
            "; ".join([n.getElementsByTagName("name")[0].firstChild.data for n in x.getElementsByTagName("creator")])
            for x in f.getElementsByTagName("creators")]
        affiliation = [[[x.firstChild.data if x.firstChild else None for x in n.getElementsByTagName("affiliation")][0] for n in x.getElementsByTagName("creator")] for x in f.getElementsByTagName("creators")]
        affiliation = ["; ".join([a for a in x if a]) for x in affiliation if x]
        title = [x.firstChild.data for x in f.getElementsByTagName("title")]
        publication_type = [x.firstChild.data for x in f.getElementsByTagName("publication_type")]
        toc = pd.DataFrame(zip(title, authors, affiliation, publication_type),
                           columns=["title", "authors", "affiliation", "publication_type"])
        return toc


    def merge(self, toc, content):
        import regex
        def _title_in_text(x, y):
            authors = "|".join([n.split(" ")[0]  for a in x["authors"].split("; ") for n in a.split(", ")]) + "|" + x["authors"].split("; ")[0].replace(", ","_")
            c =(  "(" + authors+ ")-" + x["title"][:15].replace(" ","_").replace("DFG-Projekt","")).lower()
            r = [ t for t in y["file"]  if bool(regex.findall(f"({c}){{e<=4}}", (t).lower()))]
            return r[0] if len(r) > 0 else None
        toc["file"] = toc.apply(lambda x: _title_in_text(x, content), axis=1)

        toc.loc[toc["file"].isna(), "file"] =         ["150225_Philologie_III_3_de_Kok-WebLicht-1151162.pdf",
         "150226_Panel_III_Sahle-Panel_der_AG_Datenzentren_im_Verband_DHd-1131158.pdf",
         "150226_Philologie_VIII_1_Wandl-Vogt-Transformation_Perspektiven_am_Beispiel_eines_lexikographischen_Jahrhundertprojekts-841120.pdf",
         "150227_Philologie_IX_1_Ivanovic-Digitale_Korpusanalyse_in_der_Literaturwissenschaft_am_Beispiel_von_Ilse_Aichinger-1761194.pdf",
         "BARZEN_Johanna_Muster_in_den_Geisteswissenschaften.pdf",
         "CAPELLE_Irmlind_Entwicklung_eines_MEI_und_TEI_basierten_Modells_kontextueller_Tiefenerschlieįung_von_Musikalienbeständen_am_Beispiel_des_Detmolder_Hoftheaters_im_19._Jahrhunderts.pdf",
          "KRÖGER_Barbara_Germania_Sacra_Online_Das_Forschungsportal_für_kirchliche_Personen_und_Institutionen_bis_1810.pdf",
        "POURTSKHVANIDZE_Zakharia_Visualisierung_von_Informationsgliederungen.pdf",
         "RIPPERGER_Hannah_Virtuelle_Rekonstruktion_des_Regensburger_Ballhauses.pdf"
         ]
        del content["publication_type"]
        r = pd.merge(toc, content, on="file", how="left")
        return r

class GitAcc(GitAcc):
    def __init__(self, config):
        super().__init__(config)

    def get_toc(self, zipfile):
        toc= []
        return toc

    def merge(self, toc, content):
        return content

    def extract_content(self, x, zipfile):
        text = BeautifulSoup(zipfile.open(x).read().decode(), features="xml")
        r = {
            "file": x.split("/")[-1],
            "filetype": "xml",
            "title": text.title.getText().strip(),
            "authors": "; ".join(
                [f"{x.find('surname').getText()}, {x.find('forename').getText()}" for x in text.findAll("name")] + [
                    f"{x.find('surname').getText()}, {x.find('forename').getText()}" for x in
                    text.findAll("persName")]),
            "affiliation": "; ".join([x.getText().strip() for x in text.findAll("affiliation")]),
            "publication_type": "; ".join(
                [x.getText().strip().lower() for x in text.findAll("keywords", scheme="ConfTool", n="category")]),
            "subcategory": "; ".join(
                [x.getText() for e in text.findAll("keywords", scheme="ConfTool", n="subcategory") for x in
                 e.findAll("term")]),
            "keywords": "; ".join(
                [x.getText() for e in text.findAll("keywords", scheme="ConfTool", n="keywords") for x in
                 e.findAll("term")]),
            "topics": "; ".join([x.getText() for e in text.findAll("keywords", scheme="ConfTool", n="topics") for x in
                                 e.findAll("term")]),
            "text": text.title.getText().strip() + "\n\n" + text.body.getText().strip(),
            "bib": [x.getText().strip().replace("\n", "") for x in text.find_all("bibl")]
        }
        test = r["authors"]
        return r

    def read_files(self, zipfile):
        files = [x.filename for x in zipfile.filelist if self._config["files"] in x.filename and (x.filename.endswith(".pdf") or x.filename.endswith(".xml"))]
        content = [self.extract_content(x, zipfile) for x in files]
        return  pd.DataFrame(content, columns=["file", "filetype","title", "authors", "affiliation",  "publication_type","keywords", "subcategory", "topics", "text", "bib",])
