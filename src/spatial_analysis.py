"""
Räumliche Analysen für Berliner Kita-Standorte.

Dieses Modul führt räumliche Analysen für Kita-Standorte in Berlin durch:
- Berechnung von Isochronen (Einzugsgebiete) mit OpenRouteService API
- Extraktion von Grün- und Wasserflächen aus OpenStreetMap-Daten
- Verarbeitung und Export für weitere Analysen

Author: Silas Pignotti
Date: 2024
"""

import os
import time
from pathlib import Path
from typing import List, Tuple

import geopandas as gpd
import openrouteservice as ors
import osmium
import shapely.wkb as wkblib
from shapely.geometry import shape
from tqdm import tqdm

# Globale Konfiguration
DATA_PATHS = {
    'daycare_centers_processed': Path('data/processed/daycare_centers_processed.geojson'),
    'osm_data': Path('data/raw/berlin-latest.osm.pbf'),
    'results_dir': Path('data/results')
}

wkb_factory = osmium.geom.WKBFactory()


class OSMAreaExtractor(osmium.SimpleHandler):
    """
    Extrahiert Grün- und Wasserflächen aus OpenStreetMap-Daten.
    
    Verarbeitet OSM-Elemente und klassifiziert sie basierend auf Tags
    als Grünflächen oder Wasserflächen.
    """
    
    def __init__(self):
        super().__init__()
        self.green_areas = []
        self.water_areas = []
        self.progress = tqdm(desc="Extrahiere OSM-Flächen", unit=" Elemente")
    
    def _extract_geometry(self, element):
        """Extrahiert Geometrie aus OSM-Element."""
        try:
            if isinstance(element, osmium.osm.Area):
                return wkblib.loads(wkb_factory.create_multipolygon(element))
            else:
                return wkblib.loads(wkb_factory.create_linestring(element))
        except:
            return None
    
    def _is_water_feature(self, tags):
        """Prüft ob Element eine Wasserfläche ist."""
        return (
            tags.get('natural') == 'water' or
            'waterway' in tags or
            tags.get('landuse') in ['reservoir', 'basin'] or
            tags.get('water') in ['lake', 'river', 'pond']
        )
    
    def _is_green_feature(self, tags):
        """Prüft ob Element eine Grünfläche ist."""
        return (
            tags.get('landuse') in [
                'grass', 'meadow', 'forest', 'greenfield', 
                'cemetery', 'recreation_ground'
            ] or 
            tags.get('leisure') in [
                'park', 'garden', 'playground', 'sports_centre', 
                'pitch', 'golf_course'
            ] or 
            tags.get('natural') == 'wood' or 
            tags.get('amenity') == 'grave_yard'
        )
    
    def _process_element(self, element):
        """Verarbeitet ein einzelnes OSM-Element."""
        self.progress.update(1)
        
        geometry = self._extract_geometry(element)
        if geometry is None:
            return
        
        tags = dict(element.tags)
        
        if self._is_water_feature(tags):
            self.water_areas.append(geometry)
        elif self._is_green_feature(tags):
            self.green_areas.append(geometry)
    
    def area(self, area):
        """Handler für Area-Elemente."""
        self._process_element(area)
    
    def way(self, way):
        """Handler für Way-Elemente.""" 
        self._process_element(way)
    
    def close(self):
        """Schließt die Extraktion."""
        self.progress.close()
        print(f"✅ Grünflächen gefunden: {len(self.green_areas)}")
        print(f"✅ Wasserflächen gefunden: {len(self.water_areas)}")


class IsochroneGenerator:
    """
    Berechnet Isochronen für Kita-Standorte mit OpenRouteService API.
    
    Generiert 500m-Fußweg-Isochronen für alle Kita-Standorte und
    berücksichtigt API-Limits und Rate-Limiting.
    """
    
    def __init__(self, api_key: str):
        """
        Initialisiert den Generator.
        
        Args:
            api_key: OpenRouteService API-Schlüssel
        """
        self.client = ors.Client(key=api_key) if api_key != '-' else None
        
    def calculate_isochrones(self, daycare_file: Path, output_file: Path) -> gpd.GeoDataFrame:
        """
        Berechnet Isochronen für alle Kita-Standorte.
        
        Args:
            daycare_file: Pfad zur Kita-Datei
            output_file: Ausgabepfad für Ergebnisse
            
        Returns:
            GeoDataFrame mit berechneten Isochronen
        """
        if self.client is None:
            print("⚠️  Kein API-Schlüssel - Isochrone-Berechnung übersprungen")
            return gpd.GeoDataFrame()
        
        daycare_centers = gpd.read_file(daycare_file).to_crs('EPSG:4326')
        geometries, node_ids = [], []
        request_count = 0
        max_requests = 450  # API-Limit
        
        print(f"🚀 Berechne Isochronen für {len(daycare_centers)} Kitas...")
        
        with tqdm(total=min(len(daycare_centers), max_requests), desc="Isochronen") as pbar:
            batch_start = time.time()
            
            for idx, (_, daycare) in enumerate(daycare_centers.iterrows()):
                if request_count >= max_requests:
                    print(f"⚠️  API-Limit ({max_requests}) erreicht")
                    break
                
                try:
                    # API-Anfrage
                    result = self.client.isochrones(
                        locations=[[daycare.geometry.x, daycare.geometry.y]],
                        profile='foot-walking',
                        range=[500],
                        attributes=['area']
                    )
                    
                    geometry = shape(result['features'][0]['geometry'])
                    geometries.append(geometry)
                    node_ids.append(daycare.name)
                    request_count += 1
                    pbar.update(1)
                    
                    # Rate Limiting: 11 Requests/Minute
                    if idx % 11 == 10:
                        elapsed = time.time() - batch_start
                        if elapsed < 60:
                            time.sleep(60 - elapsed)
                        batch_start = time.time()
                
                except Exception as e:
                    print(f"❌ Fehler bei Kita {daycare.name}: {e}")
                    continue
        
        # Ergebnisse speichern
        if geometries:
            isochrones = gpd.GeoDataFrame(
                {'node_id': node_ids, 'geometry': geometries}, 
                crs='EPSG:4326'
            )
            isochrones.to_file(output_file, driver='GeoJSON')
            print(f"✅ {len(geometries)} Isochronen gespeichert: {output_file}")
            return isochrones
        
        return gpd.GeoDataFrame()


def remove_overlapping_areas(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Entfernt Überlappungen zwischen Isochronen.
    
    Args:
        gdf: GeoDataFrame mit Isochronen
        
    Returns:
        GeoDataFrame ohne Überlappungen
    """
    if len(gdf) == 0:
        return gdf
    
    print("🔧 Entferne Überlappungen...")
    geometries = list(gdf.geometry)
    
    for i in tqdm(range(len(geometries)), desc="Überlappungen"):
        for j in range(i + 1, len(geometries)):
            if geometries[i].intersects(geometries[j]):
                geometries[i] = geometries[i].difference(geometries[j])
    
    result = gdf.copy()
    result.geometry = geometries
    return result


def merge_geometries(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Vereinigt alle Geometrien zu einer einzigen."""
    if len(gdf) == 0:
        return gdf
    
    unified_geometry = gdf.union_all()
    return gpd.GeoDataFrame(geometry=[unified_geometry], crs=gdf.crs)


def extract_osm_areas(osm_file: Path, output_dir: Path) -> Tuple[Path, Path]:
    """
    Extrahiert Grün- und Wasserflächen aus OSM-Daten.
    
    Args:
        osm_file: Pfad zur OSM-PBF-Datei
        output_dir: Ausgabeverzeichnis
        
    Returns:
        Tuple aus (Grünflächen-Pfad, Wasserflächen-Pfad)
    """
    print(f"📊 Extrahiere Flächen aus {osm_file}...")
    
    extractor = OSMAreaExtractor()
    extractor.apply_file(str(osm_file))
    extractor.close()
    
    # Erstelle GeoDataFrames
    green_gdf = gpd.GeoDataFrame(geometry=extractor.green_areas, crs="EPSG:4326")
    water_gdf = gpd.GeoDataFrame(geometry=extractor.water_areas, crs="EPSG:4326")
    
    # Vereinige und speichere
    output_dir.mkdir(parents=True, exist_ok=True)
    
    green_path = output_dir / 'berlin_green_areas.geojson'
    water_path = output_dir / 'berlin_water_areas.geojson'
    
    if len(green_gdf) > 0:
        green_unified = merge_geometries(green_gdf)
        green_unified.to_file(green_path, driver="GeoJSON")
        print(f"✅ Grünflächen gespeichert: {green_path}")
    
    if len(water_gdf) > 0:
        water_unified = merge_geometries(water_gdf)
        water_unified.to_file(water_path, driver="GeoJSON")
        print(f"✅ Wasserflächen gespeichert: {water_path}")
    
    return green_path, water_path


def generate_isochrones(api_key: str = None) -> Path:
    """
    Generiert Isochronen für Kita-Standorte.
    
    Args:
        api_key: OpenRouteService API-Schlüssel (optional)
        
    Returns:
        Pfad zur Isochrone-Datei
    """
    if api_key is None:
        api_key = os.getenv('OPENROUTESERVICE_API_KEY', '-')
    
    generator = IsochroneGenerator(api_key)
    output_file = DATA_PATHS['results_dir'] / 'isochrones.geojson'
    
    # Berechne Isochronen
    isochrones = generator.calculate_isochrones(
        DATA_PATHS['daycare_centers_processed'], 
        output_file
    )
    
    # Entferne Überlappungen falls Daten vorhanden
    if len(isochrones) > 0:
        clean_isochrones = remove_overlapping_areas(isochrones)
        clean_output = DATA_PATHS['results_dir'] / 'isochrones_overlapping.geojson'
        clean_isochrones.to_file(clean_output, driver='GeoJSON')
        print(f"✅ Bereinigte Isochronen: {clean_output}")
        
        return clean_output
    
    return output_file


def run_full_analysis(api_key: str = None):
    """
    Führt die komplette räumliche Analyse durch.
    
    Args:
        api_key: OpenRouteService API-Schlüssel (optional)
    """
    print("🎯 Starte räumliche Analyse für Berliner Kitas\n")
    
    # 1. OSM-Flächen extrahieren
    print("1️⃣ Extrahiere Grün- und Wasserflächen...")
    green_path, water_path = extract_osm_areas(
        DATA_PATHS['osm_data'],
        DATA_PATHS['results_dir']
    )
    
    print("\n2️⃣ Generiere Isochronen...")
    isochrones_path = generate_isochrones(api_key)
    
    print(f"\n✨ Analyse abgeschlossen! Ergebnisse in: {DATA_PATHS['results_dir']}")
    print(f"   📍 Grünflächen: {green_path.name}")
    print(f"   📍 Wasserflächen: {water_path.name}")  
    print(f"   📍 Isochronen: {isochrones_path.name}")


if __name__ == "__main__":
    # Vollständige Analyse durchführen
    # API-Schlüssel als Umgebungsvariable oder hier eintragen
    run_full_analysis()