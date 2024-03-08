
# Results und Notebooks

**Ko-Autorenschaft: wer mit wem?**
 - `results/coauthorship.xslx` (Adjacency Matrix der AutorInnen)
 - `results/coauthorship.gexf` (Gephi - readable)
Graphvisualisierungen für gemeinsame Autorenschaft wurden in gephi erzeugt.


**`notebook/External Bibliographies (Citations Frequency and Recency).ipnyb`**
- Einlicke in meistzitierte Werke
- Welche 10-20 Papers werden insgesamt am häufigsten zitiert?
    - `results/top_external_citation.xlsx`


**`notebook/Cities and GeoVis.ipnyb`**
- `results/city-frequencies.xlsx`: Orte, wo wird am meisten publiziert 
- `results/cocityship.xlsx`: Ko-Ortschaft: welche Orte publizieren häufig zusammen (je Jahr / insgesamt)
 - Ergebnisse auch als .gephi: `results/cocityship.gexf` (Gephi)
 - `results/geodata_publication.geojson` (geopandas, geodata encoded)

Kartenvisualisierungen für AutorInnennetzwerke im Notebook.



**Additional Files**
 - cities.txt : Liste von Städten, Lookup für die Affiliationen in then Daten mit alternativen Schreibweisen.
 - unmapped_institions.txt: A list of affiliations and institutions that could neither be automatically mapped nor was present in cities.txt.



 # Referenz
 
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
