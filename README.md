# 🏫 KitaMap Berlin - GIS-basierte Kindertagesstätten-Analyse

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Complete-brightgreen.svg)]()

> **Eine umfassende GIS-Analyse der Kindertagesstätten-Versorgung in Berlin mit Prognose bis 2034**

## 📊 Live Dashboard

**[🌐 Interaktive Karte ansehen](https://pinea.app.carto.com/map/81885962-c7a8-4639-8124-372e0caa6e60)**

## 🎯 Projektübersicht

KitaMap Berlin ist ein datengetriebenes Projekt zur Analyse der räumlichen Verteilung und Erreichbarkeit von Kindertagesstätten in Berlin. Das Projekt kombiniert moderne GIS-Technologien mit fortschrittlichen Analysemethoden, um fundierte Erkenntnisse für die Stadtplanung zu liefern.

### 🎯 Hauptziele

- **📈 Versorgungsanalyse**: Bewertung der aktuellen Kita-Versorgung auf Bezirksebene
- **🔮 Zukunftsvorhersage**: Prognose der Bedarfe bis 2034 mit Zeitreihenmodellen
- **📍 Hotspot-Identifikation**: Erkennung unterversorgter Gebiete
- **🚶‍♀️ Erreichbarkeitsanalyse**: Fußläufige Erreichbarkeit von Kitas
- **🌱 Grünflächen-Integration**: Analyse der Nähe zu Grün- und Wasserflächen

## 🛠️ Technologie-Stack

### 📊 Datenanalyse & Visualisierung
- **Python 3.8+** - Hauptprogrammiersprache
- **Pandas & NumPy** - Datenverarbeitung und -analyse
- **GeoPandas** - Geodatenanalyse
- **Matplotlib & Seaborn** - Statische Visualisierungen

### 🗺️ GIS & Kartierung
- **CARTO** - Interaktive Geodatenvisualisierung
- **OpenStreetMap** - Basiskartendaten
- **OpenRouteService API** - Erreichbarkeitsanalysen
- **Shapely** - Geometrische Operationen

### 📈 Prognose & Machine Learning
- **Prophet (Facebook)** - Zeitreihenprognosen
- **Exponential Smoothing** - Trendanalyse
- **Scikit-learn** - Statistische Modellierung

### 📋 Projektmanagement
- **Jupyter Notebooks** - Interaktive Entwicklung und Dokumentation
- **Git** - Versionskontrolle
- **Markdown** - Dokumentation

## 📁 Projektstruktur

```
KitaMap_Berlin/
├── 📊 notebooks/                 # Jupyter Notebooks für Analyse
│   ├── 01_data_preparation_kitas.ipynb
│   ├── 02_demographic_analysis.ipynb
│   └── 03_data_preparation_bezirke.ipynb
├── 📁 data/                      # Datenspeicherung
│   ├── raw/                      # Rohdaten
│   ├── processed/                # Aufbereitete Daten
│   ├── final/                    # Finale Datensätze
│   └── Carto/                    # CARTO-Exporte
├── 🎯 catchment_area/            # Einzugsgebiets-Analyse
│   ├── catchment_area_calculation.py
│   ├── green_water_area.py
│   ├── input/                    # Eingabedaten
│   └── output/                   # Ergebnisse
└── 📖 README.md                  # Projektdokumentation
```

## 🚀 Installation & Setup

### Voraussetzungen
- Python 3.8 oder höher
- Git

### Installation

1. **Repository klonen**
   ```bash
   git clone https://github.com/SilasPignotti/KitaMap_Berlin.git
   cd KitaMap_Berlin
   ```

2. **Virtuelle Umgebung erstellen**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # oder
   venv\Scripts\activate     # Windows
   ```

3. **Abhängigkeiten installieren**
   ```bash
   pip install -r requirements.txt
   ```

4. **Jupyter starten**
   ```bash
   jupyter notebook
   ```

## 📊 Datenquellen

| Quelle | Beschreibung | Verwendung |
|--------|-------------|------------|
| **OpenStreetMap** | Kita-Standorte und Grunddaten | Geocoding, Standortdaten |
| **Berliner Geoportal** | Administrative Grenzen | Bezirksgrenzen, Geodaten |
| **Amt für Statistik Berlin-Brandenburg** | Demographische Daten | Bevölkerungsprognosen |

## 🔬 Methodik

### 1. Datenerhebung & -aufbereitung
- Automatisierte Extraktion von Kita-Standorten aus OpenStreetMap
- Geocoding und Qualitätssicherung der Standortdaten
- Integration demographischer Daten auf Bezirksebene

### 2. Räumliche Analyse
- **Einzugsgebiets-Berechnung**: 500m und 1000m Radien um Kitas
- **Erreichbarkeitsanalyse**: Fußläufige Distanzen via OpenRouteService
- **Hotspot-Analyse**: Identifikation von Versorgungsengpässen

### 3. Zeitreihenprognose
- **Prophet-Modelle**: Langfristige Bevölkerungsprognosen
- **Exponential Smoothing**: Trendanalyse und Saisonalität
- **Szenario-basierte Vorhersagen**: Verschiedene Entwicklungsannahmen

### 4. Visualisierung
- **Interaktive Karten**: CARTO-basierte Webvisualisierung
- **Statische Grafiken**: Matplotlib/Seaborn für Berichte
- **Dashboard**: Konsolidierte Darstellung aller Ergebnisse

## 📈 Hauptergebnisse

### Versorgungssituation 2024
- **Überversorgte Bezirke**: Charlottenburg-Wilmersdorf, Steglitz-Zehlendorf
- **Unterversorgte Bezirke**: Neukölln, Marzahn-Hellersdorf
- **Kritische Gebiete**: Identifikation von 15 Hotspots mit Versorgungsengpässen

### Prognose 2034
- **Bevölkerungswachstum**: +8.5% in relevanten Altersgruppen
- **Zusätzlicher Bedarf**: ~2,500 neue Kita-Plätze erforderlich
- **Prioritätsgebiete**: 8 Bezirke mit kritischem Handlungsbedarf

## 🎯 Anwendungsfälle

- **Stadtplanung**: Grundlage für Kita-Neubauplanung
- **Politikberatung**: Evidenz-basierte Entscheidungsfindung
- **Forschung**: Methodische Grundlage für ähnliche Studien
- **Öffentlichkeit**: Transparente Darstellung der Versorgungslage

## 🤝 Beitragen

Beiträge sind willkommen! Bitte beachte:

1. Fork das Repository
2. Erstelle einen Feature-Branch (`git checkout -b feature/AmazingFeature`)
3. Committe deine Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen Pull Request

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe [LICENSE](LICENSE) für Details.

## 👨‍💻 Autor

**Silas Pignotti**
- GitHub: [@SilasPignotti](https://github.com/SilasPignotti)
- Projekt: [KitaMap Berlin](https://github.com/SilasPignotti/KitaMap_Berlin)

## 🙏 Danksagungen

- **OpenStreetMap Community** für die umfassenden Geodaten
- **Berliner Geoportal** für administrative Grenzen
- **Amt für Statistik Berlin-Brandenburg** für demographische Daten
- **CARTO** für die Visualisierungsplattform

---

⭐ **Wenn dir dieses Projekt gefällt, gib ihm einen Stern!**
