"""
Einzugsgebiets-Berechnung für Kindertagesstätten in Berlin.

Dieses Modul berechnet Isochronen (Fußläufige Erreichbarkeitsbereiche) für Kita-Standorte
unter Verwendung der OpenRouteService API. Die Ergebnisse werden als GeoJSON gespeichert
und können für weitere räumliche Analysen verwendet werden.

Author: Silas Pignotti
Date: 2024
"""

import logging
import os
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import geopandas as gpd
import openrouteservice as ors
from shapely.geometry import shape
from tqdm import tqdm


class IsochroneCalculator:
    """
    Berechnet Isochronen für Kita-Standorte basierend auf Fußläufiger Erreichbarkeit.
    
    Diese Klasse verwendet die OpenRouteService API um 500m Isochronen für alle
    Kita-Standorte zu berechnen. Die Ergebnisse werden schrittweise gespeichert
    um Datenverlust bei API-Limits zu vermeiden.
    
    Attributes:
        input_file (str): Pfad zur Eingabedatei mit Kita-Standorten
        output_dir (str): Ausgabeverzeichnis für Ergebnisse
        client (ors.Client): OpenRouteService API Client
        output_file (str): Pfad zur Ausgabedatei
    """
    
    def __init__(self, input_file: str, output_dir: str, api_key: str) -> None:
        """
        Initialisiert den IsochroneCalculator.
        
        Args:
            input_file: Pfad zur GeoJSON-Datei mit Kita-Standorten
            output_dir: Verzeichnis für Ausgabedateien
            api_key: OpenRouteService API-Schlüssel
        """
        self.input_file = input_file
        self.output_dir = output_dir
        self.client = ors.Client(key=api_key)
        
        # Erstelle Ausgabeverzeichnis
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Setup Logging
        self._setup_logging()
        
        self.output_file = os.path.join(output_dir, 'isochrones.geojson')
    
    def _setup_logging(self) -> None:
        """Konfiguriert das Logging für die Isochronen-Berechnung."""
        log_file = os.path.join(
            self.output_dir, 
            f'isochrones_{datetime.now():%Y%m%d_%H%M}.log'
        )
        
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def get_start_index(self) -> int:
        """
        Bestimmt den Startindex für die Verarbeitung.
        
        Falls bereits Ergebnisse existieren, wird von dort fortgesetzt.
        
        Returns:
            Index ab dem die Verarbeitung fortgesetzt werden soll
        """
        if os.path.exists(self.output_file):
            existing_isochrones = gpd.read_file(self.output_file)
            return len(existing_isochrones)
        return 0
    
    def calculate_isochrones(self) -> gpd.GeoDataFrame:
        """
        Berechnet Isochronen für alle Kita-Standorte.
        
        Die Methode verarbeitet alle Standorte schrittweise und speichert
        Zwischenergebnisse alle 10 Berechnungen. API-Limits werden beachtet.
        
        Returns:
            GeoDataFrame mit allen berechneten Isochronen
            
        Raises:
            Exception: Bei Fehlern in der API-Verarbeitung
        """
        nodes = gpd.read_file(self.input_file).to_crs('EPSG:4326')
        start_idx = self.get_start_index()
        request_count = 0
        
        geometries: List = []
        node_ids: List = []
        
        # Lade existierende Ergebnisse falls vorhanden
        if os.path.exists(self.output_file):
            existing_data = gpd.read_file(self.output_file)
            geometries.extend(existing_data.geometry.tolist())
            node_ids.extend(existing_data.node_id.tolist())
        
        logging.info(f"Starting processing from index {start_idx}")
        
        try:
            with tqdm(total=len(nodes), initial=start_idx) as pbar:
                batch_start_time = time.time()
                
                for idx, row in nodes.iloc[start_idx:].iterrows():
                    if request_count >= 450:  # API-Limit
                        logging.info("Session limit (450) reached")
                        break
                    
                    # Berechne Isochrone für aktuellen Standort
                    result = self.client.isochrones(
                        locations=[[row.geometry.x, row.geometry.y]],
                        profile='foot-walking',
                        range=[500],  # 500m Radius
                        attributes=['area']
                    )
                    
                    # Extrahiere Geometrie und speichere
                    isochrone_geom = shape(result['features'][0]['geometry'])
                    geometries.append(isochrone_geom)
                    node_ids.append(row.name)
                    
                    request_count += 1
                    pbar.update(1)
                    
                    # Speichere Zwischenergebnisse alle 10 Berechnungen
                    if len(geometries) % 10 == 0:
                        self._save_temp_results(geometries, node_ids)
                    
                    # Rate Limiting: Max 11 Requests pro Minute
                    elapsed = time.time() - batch_start_time
                    if idx % 11 == 10 and elapsed < 60:
                        time.sleep(60 - elapsed)
                        batch_start_time = time.time()
                            
        except Exception as e:
            logging.error(f"Error processing node {row.name}: {str(e)}")
            raise
        
        # Finale Speicherung
        isochrones_gdf = gpd.GeoDataFrame(
            {'node_id': node_ids, 'geometry': geometries},
            crs='EPSG:4326'
        )
        
        isochrones_gdf.to_file(self.output_file, driver='GeoJSON')
        logging.info(f"Processing completed. Processed {request_count} nodes.")
            
        return isochrones_gdf
    
    def _save_temp_results(self, geometries: List, node_ids: List) -> None:
        """
        Speichert temporäre Ergebnisse als GeoJSON.
        
        Args:
            geometries: Liste der berechneten Geometrien
            node_ids: Liste der zugehörigen Node-IDs
        """
        temp_gdf = gpd.GeoDataFrame(
            {'node_id': node_ids, 'geometry': geometries},
            crs='EPSG:4326'
        )
        temp_gdf.to_file(self.output_file, driver='GeoJSON')


def remove_overlapping_areas(isochrones_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Entfernt überlappende Bereiche aus den Isochronen.
    
    Diese Funktion verhindert, dass sich Einzugsgebiete überschneiden,
    indem sie die Überlappungen von der ersten Geometrie abzieht.
    
    Args:
        isochrones_gdf: GeoDataFrame mit Isochronen
        
    Returns:
        GeoDataFrame mit überlappungsfreien Isochronen
    """
    all_geoms = list(isochrones_gdf.geometry)
    
    # Entferne Überlappungen zwischen allen Geometrien
    for i in range(len(all_geoms)):
        for j in range(i + 1, len(all_geoms)):
            if all_geoms[i].intersects(all_geoms[j]):
                all_geoms[i] = all_geoms[i].difference(all_geoms[j])
    
    # Erstelle neues GeoDataFrame mit bereinigten Geometrien
    result_gdf = isochrones_gdf.copy()
    result_gdf.geometry = all_geoms
    
    return result_gdf


def main() -> None:
    """Hauptfunktion für die Isochronen-Berechnung."""
    config = {
        'input_file': 'input/kitas_processed.geojson',
        'output_dir': 'catchment_area/output',
        'api_key': '-'  # API-Schlüssel hier eintragen
    }
    
    # Berechne Isochronen (auskommentiert für Demo)
    # calculator = IsochroneCalculator(**config)
    # isochrones = calculator.calculate_isochrones()
    
    # Entferne überlappende Bereiche
    isochrones = gpd.read_file(f"{config['output_dir']}/isochrones.geojson")
    isochrones_clean = remove_overlapping_areas(isochrones)
    
    # Speichere bereinigte Ergebnisse
    output_file = f"{config['output_dir']}/isochrones_overlapping.geojson"
    isochrones_clean.to_file(output_file, driver='GeoJSON')
    logging.info(f"Überlappungsfreie Isochrone wurden in {output_file} gespeichert")


if __name__ == "__main__":
    main()
