"""
Grün- und Wasserflächen-Extraktion aus OpenStreetMap Daten.

Dieses Modul extrahiert Grünflächen und Wasserflächen aus OSM-Daten für Berlin
und bereitet sie für die räumliche Analyse der Kita-Standorte vor.

Author: Silas Pignotti
Date: 2024
"""

from pathlib import Path
from typing import List, Tuple

import geopandas as gpd
import osmium
import shapely.wkb as wkblib
from tqdm import tqdm

# WKB Factory für Geometrie-Konvertierung
wkb_factory = osmium.geom.WKBFactory()


class SimpleAreaHandler(osmium.SimpleHandler):
    """
    OSM-Handler für die Extraktion von Grün- und Wasserflächen.
    
    Diese Klasse verarbeitet OSM-Elemente und extrahiert relevante
    Grünflächen (Parks, Spielplätze, etc.) und Wasserflächen (Seen, Flüsse, etc.)
    basierend auf OSM-Tags.
    
    Attributes:
        green_areas (List): Liste der gefundenen Grünflächen-Geometrien
        water_areas (List): Liste der gefundenen Wasserflächen-Geometrien
        progress (tqdm): Fortschrittsanzeige
    """
    
    def __init__(self) -> None:
        """Initialisiert den AreaHandler."""
        super(SimpleAreaHandler, self).__init__()
        self.green_areas: List = []
        self.water_areas: List = []
        self.progress = tqdm(desc="Verarbeite OSM-Elemente")
        
    def handle_feature(self, obj) -> None:
        """
        Verarbeitet ein einzelnes OSM-Element.
        
        Args:
            obj: OSM-Element (Area, Way oder Node)
        """
        try:
            # Update Progress
            self.progress.update(1)
            
            # Extrahiere Geometrie basierend auf Elementtyp
            geometry = self._extract_geometry(obj)
            if geometry is None:
                return
            
            tags = dict(obj.tags)
            
            # Klassifiziere Element basierend auf Tags
            if self._is_water_area(tags):
                self.water_areas.append(geometry)
            elif self._is_green_area(tags):
                self.green_areas.append(geometry)
                
        except Exception as e:
            print(f"Fehler bei der Verarbeitung: {e}")
    
    def _extract_geometry(self, obj) -> object:
        """
        Extrahiert Geometrie aus OSM-Element.
        
        Args:
            obj: OSM-Element
            
        Returns:
            Shapely-Geometrie oder None bei Fehlern
        """
        try:
            if isinstance(obj, osmium.osm.Area):
                return wkblib.loads(wkb_factory.create_multipolygon(obj))
            else:  # Way oder Node
                return wkblib.loads(wkb_factory.create_linestring(obj))
        except:
            return None
    
    def _is_water_area(self, tags: dict) -> bool:
        """
        Prüft ob ein Element eine Wasserfläche ist.
        
        Args:
            tags: OSM-Tags des Elements
            
        Returns:
            True wenn es sich um eine Wasserfläche handelt
        """
        return (
            tags.get('natural') == 'water' or
            'waterway' in tags or
            tags.get('landuse') in ['reservoir', 'basin'] or
            tags.get('water') in ['lake', 'river', 'pond']
        )
    
    def _is_green_area(self, tags: dict) -> bool:
        """
        Prüft ob ein Element eine Grünfläche ist.
        
        Args:
            tags: OSM-Tags des Elements
            
        Returns:
            True wenn es sich um eine Grünfläche handelt
        """
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
    
    # Handler für verschiedene OSM-Elementtypen
    def area(self, a) -> None:
        """Handler für Area-Elemente."""
        self.handle_feature(a)
    
    def way(self, w) -> None:
        """Handler für Way-Elemente."""
        self.handle_feature(w)
    
    def node(self, n) -> None:
        """Handler für Node-Elemente."""
        self.handle_feature(n)
    
    def close(self) -> None:
        """Schließt den Handler und zeigt Statistiken."""
        self.progress.close()
        print(f"Gefundene Grünflächen: {len(self.green_areas)}")
        print(f"Gefundene Wasserflächen: {len(self.water_areas)}")


def extract_berlin_areas(pbf_file: Path) -> Tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """
    Extrahiert Grün- und Wasserflächen aus OSM-Daten.
    
    Args:
        pbf_file: Pfad zur OSM-PBF-Datei
        
    Returns:
        Tuple aus (Grünflächen-GeoDataFrame, Wasserflächen-GeoDataFrame)
    """
    handler = SimpleAreaHandler()
    handler.apply_file(pbf_file)
    handler.close()
    
    # Erstelle GeoDataFrames
    gdf_green = gpd.GeoDataFrame(geometry=handler.green_areas, crs="EPSG:4326")
    gdf_water = gpd.GeoDataFrame(geometry=handler.water_areas, crs="EPSG:4326")
    
    return gdf_green, gdf_water


def merge_geometries(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Vereinigt alle Geometrien in einem GeoDataFrame zu einer einzigen.
    
    Args:
        gdf: GeoDataFrame mit mehreren Geometrien
        
    Returns:
        GeoDataFrame mit einer vereinigten Geometrie
    """
    if len(gdf) == 0:
        return gdf
    
    unified_geometry = gdf.union_all()
    return gpd.GeoDataFrame(geometry=[unified_geometry], crs=gdf.crs)


def main() -> None:
    """Hauptfunktion für die Grün- und Wasserflächen-Verarbeitung."""
    # Pfade definieren
    pbf_file = Path("catchment_area/input/berlin-latest.osm.pbf")
    output_dir = Path("catchment_area/output")
    
    # Extrahiere Flächen aus OSM (auskommentiert für Demo)
    # green_areas, water_areas = extract_berlin_areas(pbf_file)
    
    # Lade bereits extrahierte Daten
    green_areas = gpd.read_file(output_dir / "berlin_green_areas.geojson")
    water_areas = gpd.read_file(output_dir / "berlin_water_areas.geojson")
    
    # Vereinige alle Grünflächen zu einer Geometrie
    green_areas_unified = merge_geometries(green_areas)
    
    # Vereinige alle Wasserflächen zu einer Geometrie 
    water_areas_unified = merge_geometries(water_areas)
    
    # Speichere vereinigte Ergebnisse
    green_areas_unified.to_file(
        output_dir / "berlin_green_areas.geojson", 
        driver="GeoJSON"
    )
    water_areas_unified.to_file(
        output_dir / "berlin_water_areas.geojson", 
        driver="GeoJSON"
    )
    
    print("Grün- und Wasserflächen erfolgreich verarbeitet und gespeichert.")


if __name__ == "__main__":
    main()


