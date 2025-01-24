import osmium
import shapely.wkb as wkblib
import geopandas as gpd
from tqdm import tqdm
from pathlib import Path

wkb_factory = osmium.geom.WKBFactory()

class SimpleAreaHandler(osmium.SimpleHandler):
    def __init__(self):
        super(SimpleAreaHandler, self).__init__()
        self.green_areas = []
        self.water_areas = []
        self.progress = tqdm(desc="Verarbeite OSM-Elemente")
        
    def handle_feature(self, obj):
        try:
            # Update Progress
            self.progress.update(1)
            
            # Prüfe erst, ob es eine gültige Geometrie ist
            if isinstance(obj, osmium.osm.Area):
                geometry = wkblib.loads(wkb_factory.create_multipolygon(obj))
            else:  # Way oder Node
                try:
                    geometry = wkblib.loads(wkb_factory.create_linestring(obj))
                except:
                    return
            
            tags = dict(obj.tags)
            
            # Wasserflächen-Check
            if (tags.get('natural') == 'water' or
                'waterway' in tags or
                tags.get('landuse') in ['reservoir', 'basin'] or
                tags.get('water') in ['lake', 'river', 'pond']):
                self.water_areas.append(geometry)
            
            # Grünflächen-Check (inkl. Sport, Spiel und Friedhöfe)
            elif (tags.get('landuse') in ['grass', 'meadow', 'forest', 'greenfield', 'cemetery', 'recreation_ground'] or tags.get('leisure') in ['park', 'garden', 'playground', 'sports_centre', 'pitch', 'golf_course'] or tags.get('natural') == 'wood' or tags.get('amenity') == 'grave_yard'):
                self.green_areas.append(geometry)
                
        except Exception as e:
            print(f"Fehler bei der Verarbeitung: {e}")
    
    # Handler für verschiedene OSM-Elementtypen
    def area(self, a): self.handle_feature(a)
    def way(self, w): self.handle_feature(w)
    def node(self, n): self.handle_feature(n)
    
    def close(self):
        self.progress.close()
        print(f"Gefundene Grünflächen: {len(self.green_areas)}")
        print(f"Gefundene Wasserflächen: {len(self.water_areas)}")

def extract_berlin_areas(pbf_file):
    handler = SimpleAreaHandler()
    handler.apply_file(pbf_file)
    handler.close()
    
    # GeoDataFrames erstellen
    gdf_green = gpd.GeoDataFrame(geometry=handler.green_areas, crs="EPSG:4326")
    gdf_water = gpd.GeoDataFrame(geometry=handler.water_areas, crs="EPSG:4326")
    
    return gdf_green, gdf_water




# Verwendung:
pbf_file = Path("catchment_area/input/berlin-latest.osm.pbf")

# green_areas, water_areas = extract_berlin_areas(pbf_file)


green_areas = gpd.read_file("catchment_area/output/berlin_green_areas.geojson")
water_areas = gpd.read_file("catchment_area/output/berlin_water_areas.geojson")

# Alle Grünflächen zu einer Geometrie vereinen
green_areas = gpd.GeoDataFrame(geometry=[green_areas.union_all()], crs="EPSG:4326")

# Alle Wasserflächen zu einer Geometrie vereinen 
water_areas = gpd.GeoDataFrame(geometry=[water_areas.union_all()], crs="EPSG:4326")

green_areas.to_file(Path("catchment_area/output/berlin_green_areas.geojson"), driver="GeoJSON")
water_areas.to_file(Path("catchment_area/output/berlin_water_areas.geojson"), driver="GeoJSON")


