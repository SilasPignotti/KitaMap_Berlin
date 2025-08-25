#!/usr/bin/env python3
"""
Kommandozeilen-Tool für die räumliche Analyse der Berliner Kitas.

Führt die komplette räumliche Analyse durch oder einzelne Schritte.

Verwendung:
    python run_analysis.py                    # Vollständige Analyse
    python run_analysis.py --osm-only        # Nur OSM-Extraktion
    python run_analysis.py --isochrones-only # Nur Isochronen
"""

import argparse
import os
import sys
from pathlib import Path

# Füge src/ zum Python-Pfad hinzu
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from spatial_analysis import run_full_analysis, extract_osm_areas, generate_isochrones, DATA_PATHS


def main():
    """Hauptfunktion für das CLI."""
    parser = argparse.ArgumentParser(
        description="Räumliche Analyse für Berliner Kita-Standorte",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--api-key', 
        type=str, 
        default=None,
        help='OpenRouteService API-Schlüssel (oder OPENROUTESERVICE_API_KEY env var)'
    )
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--osm-only', 
        action='store_true',
        help='Nur OSM-Flächen extrahieren'
    )
    group.add_argument(
        '--isochrones-only', 
        action='store_true',
        help='Nur Isochronen berechnen'
    )
    
    args = parser.parse_args()
    
    # API-Schlüssel aus Argumenten oder Umgebungsvariable
    api_key = args.api_key or os.getenv('OPENROUTESERVICE_API_KEY')
    
    print("🏫 KitaMap Berlin - Räumliche Analyse")
    print("=" * 40)
    
    try:
        if args.osm_only:
            print("📊 Extrahiere nur OSM-Flächen...")
            extract_osm_areas(DATA_PATHS['osm_data'], DATA_PATHS['results_dir'])
            
        elif args.isochrones_only:
            print("📍 Berechne nur Isochronen...")
            if not api_key:
                print("⚠️  Warnung: Kein API-Schlüssel gefunden")
                print("   Setze OPENROUTESERVICE_API_KEY Umgebungsvariable")
                print("   oder verwende --api-key DEIN_SCHLUESSEL")
            generate_isochrones(api_key)
            
        else:
            print("🎯 Führe vollständige Analyse durch...")
            if not api_key:
                print("⚠️  Kein API-Schlüssel - Isochronen werden übersprungen")
                print("   Für vollständige Analyse: OPENROUTESERVICE_API_KEY setzen")
            run_full_analysis(api_key)
        
        print("\n✅ Fertig!")
        
    except KeyboardInterrupt:
        print("\n❌ Analyse abgebrochen")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fehler: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()