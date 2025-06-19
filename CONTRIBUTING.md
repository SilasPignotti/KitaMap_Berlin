# 🤝 Beitragen zu KitaMap Berlin

Vielen Dank für Ihr Interesse an der Verbesserung von KitaMap Berlin! 

## 📋 Übersicht

KitaMap Berlin ist ein Open-Source-Projekt zur GIS-basierten Analyse der Kindertagesstätten-Versorgung in Berlin. Wir freuen uns über alle Arten von Beiträgen:

- 🐛 Bug Reports
- 💡 Feature Requests  
- 📝 Dokumentation
- 🔧 Code-Verbesserungen
- 🧪 Tests
- 🌍 Übersetzungen

## 🚀 Erste Schritte

### Voraussetzungen

- Python 3.8 oder höher
- Git
- Grundkenntnisse in Python und GIS

### Setup

1. **Repository forken**
   ```bash
   # Fork das Repository auf GitHub
   # Dann klone deinen Fork
   git clone https://github.com/YOUR_USERNAME/KitaMap_Berlin.git
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
   pip install -e .[dev]  # Für Entwicklungsabhängigkeiten
   ```

4. **Branch erstellen**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📝 Entwicklungsrichtlinien

### Code-Stil

Wir verwenden moderne Python-Best-Practices:

- **Black** für Code-Formatierung
- **Ruff** für Linting
- **MyPy** für Type Checking
- **PEP 8** Konformität

```bash
# Code formatieren
black .

# Linting
ruff check .

# Type Checking
mypy .
```

### Commit-Messages

Verwende aussagekräftige Commit-Messages im Format:

```
type(scope): description

[optional body]

[optional footer]
```

Beispiele:
- `feat(analysis): add new demographic analysis function`
- `fix(catchment): resolve overlapping area calculation bug`
- `docs(readme): update installation instructions`

### Pull Request Prozess

1. **Feature Branch erstellen**
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Änderungen committen**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

3. **Branch pushen**
   ```bash
   git push origin feature/amazing-feature
   ```

4. **Pull Request erstellen**
   - Gehe zu deinem Fork auf GitHub
   - Klicke auf "New Pull Request"
   - Wähle den `main` Branch als Ziel
   - Beschreibe deine Änderungen detailliert

### Pull Request Checklist

- [ ] Code folgt den Style-Richtlinien
- [ ] Tests wurden hinzugefügt/aktualisiert
- [ ] Dokumentation wurde aktualisiert
- [ ] Commit-Messages sind aussagekräftig
- [ ] Änderungen sind getestet
- [ ] Keine sensiblen Daten enthalten

## 🧪 Testing

### Tests ausführen

```bash
# Alle Tests
pytest

# Mit Coverage
pytest --cov=kitamap

# Spezifische Tests
pytest tests/test_analysis.py
```

### Neue Tests schreiben

- Tests gehören in den `tests/` Ordner
- Verwende beschreibende Test-Namen
- Teste sowohl positive als auch negative Fälle
- Ziel: >80% Code-Coverage

## 📊 Projektstruktur

```
KitaMap_Berlin/
├── 📊 notebooks/           # Jupyter Notebooks
├── 📁 data/               # Datenspeicherung
├── 🎯 catchment_area/     # Einzugsgebiets-Analyse
├── 🧪 tests/              # Tests (zu erstellen)
├── 📖 docs/               # Dokumentation (zu erstellen)
└── 📄 config/             # Konfigurationsdateien
```

## 🐛 Bug Reports

Bei Bug Reports bitte folgende Informationen angeben:

1. **Betriebssystem und Python-Version**
2. **Schritt-für-Schritt Reproduktion**
3. **Erwartetes vs. tatsächliches Verhalten**
4. **Screenshots/Logs** (falls relevant)
5. **Mögliche Ursachen** (falls bekannt)

## 💡 Feature Requests

Für neue Features:

1. **Problem beschreiben** - Was soll gelöst werden?
2. **Lösungsansatz vorschlagen** - Wie könnte es implementiert werden?
3. **Alternativen diskutieren** - Gibt es andere Ansätze?
4. **Priorität angeben** - Wie wichtig ist das Feature?

## 📚 Dokumentation

### Docstrings

Verwende Google-Style Docstrings:

```python
def calculate_isochrones(self, radius: int = 500) -> gpd.GeoDataFrame:
    """Berechnet Isochronen für Kita-Standorte.
    
    Args:
        radius: Radius in Metern für die Isochronen-Berechnung.
               Standard: 500m.
    
    Returns:
        GeoDataFrame mit berechneten Isochronen.
        
    Raises:
        ValueError: Wenn radius <= 0.
        APIError: Bei Fehlern der OpenRouteService API.
    """
```

### README Updates

- Halte die README aktuell
- Füge Beispiele für neue Features hinzu
- Dokumentiere Breaking Changes

## 🔒 Sicherheit

- **Keine API-Keys** in Code committen
- Verwende `.env` Dateien für Konfiguration
- Melde Sicherheitslücken privat an den Maintainer

## 🏷️ Labels

Wir verwenden folgende Labels für Issues:

- `bug` - Fehler im Code
- `enhancement` - Neue Features
- `documentation` - Dokumentationsverbesserungen
- `good first issue` - Gut für Anfänger
- `help wanted` - Benötigt Hilfe
- `question` - Fragen/Diskussionen

## 📞 Support

Bei Fragen:

1. **Issues** - Für Bugs und Feature Requests
2. **Discussions** - Für allgemeine Fragen
3. **Email** - Für private Angelegenheiten

## 🎉 Anerkennung

Alle Beiträge werden in der README und Release Notes anerkannt.

---

**Vielen Dank für deine Beiträge! 🚀** 