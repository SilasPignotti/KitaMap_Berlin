# KitaMap Berlin
Eine GIS-basierte Analyse der Kindertagesstätten-Versorgung in Berlin mit Prognose bis 2034.
Projektbeschreibung
KitaMap Berlin analysiert die räumliche Verteilung und Erreichbarkeit von Kitaplätzen in den Berliner Bezirken. Das Projekt nutzt Open Data Quellen und GIS-Technologien, um:

* Die aktuelle Versorgungssituation auf Bezirksebene zu bewerten
* Zukünftige Bedarfe bis 2034 zu prognostizieren
* Unterversorgte Gebiete zu identifizieren
* Die fußläufige Erreichbarkeit von Kitas zu analysieren

Ein interaktives Dashboard visualisiert die Ergebnisse und ist verfügbar unter: [https://pinea.app.carto.com/map/81885962-c7a8-4639-8124-372e0caa6e60]

##Datenquellen

* OpenStreetMap: Kita-Standorte und Grunddaten
* Berliner Geoportal: Administrative Grenzen
* Amt für Statistik Berlin-Brandenburg: Demographische Daten

### Technologien

* Python für Datenverarbeitung und Analyse
* CARTO für Geodatenvisualisierung
* Prophet und Exponential Smoothing für Zeitreihenprognosen
* OpenRouteService API für Erreichbarkeitsanalysen
