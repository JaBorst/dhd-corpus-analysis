
# Wer mit Wem... und Wo?

In diesem Repository liegen Code und Daten für die Analyse der DHd-Abstracts 2014 - 2023.


## Ergebnisse
**Ko-Autorenschaft: wer mit wem?**
 - `results/coauthorship.xslx`: Adjacency-Matrix der AutorInnen
 - `results/coauthorship.gexf`: Gephi-lesbares Format

**..und wo?**
- `results/city-frequencies.xlsx`: Orte, mit der zugehörigen Publikationshäufigkeit pro Jahr, (*_per_year.xlsx listet Publikationshäufigkeiten pro Jahr, *_overall.xlsx sind aggregierte Zahlen)
- `results/cocityship.xlsx`: Ko-Ortschaft: welche Orte publizieren häufig zusammen (insgesamt)
 - `results/cocityship.gexf`: Selbe Ergebnisse als als Gephi-lesbares Format´.
 - `results/geodata_publication.geojson`: (geopandas, geodata encoded)
   
**Zitationen**
 - `results/top_external_citation.xlsx`
   


## Visualisierungen
 - Graphvisualisierungen für gemeinsame Autorenschaft wurden in [Gephi](https://gephi.org/) erzeugt.
 - `notebook/topcitations.ipnyb`: Einlicke in meistzitierte Arbeiten, welche 10-20 Papers werden insgesamt am häufigsten zitiert?
 - `notebook/Cities and GeoVis.ipnyb`: Beispiele für Kartenvisualisierungen für AutorInnen-Netzwerke.

## Code

 - `main.py`: Der Code in `dhd` kann verwendet werden um das Korpus der Abstracts neu zu erstellen. Das Ausführen von `main.py` lädt die URLs aus CONFIG.yaml und extrahiert die Abstracts aus dem jeweiligen github Repository. Vielen Dank an https://github.com/DHd-Verband für das Bereitstellen der Abstracts.
 - `requirements.txt`: Eine Liste der verwendeten Pakete, kann mit conda verwendet werden um ein zur Ausführung von main.py passendes Environment zu erzeugen.

## Additional Files
 - `results/cities.txt`: Liste von Städten, Mapping für die Affiliationen in den Daten mit alternativen Schreibweisen.
 - `unmapped_institions.txt`: Liste von Affiliationen und Institutionen die weder automatisch gemappt werden konnten noch in cities.txt explizit erscheinen.

## Referenz
 
 Die Ergebnisse aus diesem Repository wurden auf der DHd 2024 als Poster präsentiert.
 `
J. Borst, M. Burghardt, V. Piontkowitz and J. Klähn, ‘Wer mit wem … und wo? Eine szientometrische Analyse der DHd-Abstracts 2014 - 2022’, presented at the DHd 2024 Quo Vadis DH (DHd2024), Passau, Deutschland, Feb. 2024. doi: 10.5281/zenodo.10698254. 
 `
 
 ```
 @InProceedings{borstWermitwem2024,
  author    = {Borst, Janos and Burghardt, Manuel and Piontkowitz, Vera and Klähn, Jannis},
  booktitle = {DHd 2024 Quo Vadis DH (DHd2024)},
  title     = {Wer mit wem … und wo? Eine szientometrische Analyse der DHd-Abstracts 2014 - 2022},
  year      = {2024},
  address   = {Passau, Deutschland.},
  publisher = {Zenodo},
  copyright = {Creative Commons Attribution 4.0 International},
  doi       = {10.5281/zenodo.10698253},
  keywords  = {DHd2024, Paper, Posterpräsentation, Szientometrie, Koautorenschaftsanalyse, Wissenschaftsforschung, Räumliche Analyse, Netzwerkanalyse, Visualisierung, Forschungsprozess, Text},
}
```
