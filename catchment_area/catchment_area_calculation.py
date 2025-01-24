import openrouteservice as ors
import geopandas as gpd
import time
from datetime import datetime
import os
import logging
from tqdm import tqdm
from shapely.geometry import shape

class IsochroneCalculator:
    def __init__(self, input_file, output_dir, api_key):
        self.input_file = input_file
        self.output_dir = output_dir
        self.client = ors.Client(key=api_key)
        
        os.makedirs(output_dir, exist_ok=True)
        
        logging.basicConfig(
            filename=os.path.join(output_dir, f'isochrones_{datetime.now():%Y%m%d_%H%M}.log'),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        self.output_file = os.path.join(output_dir, 'isochrones.geojson')

    def get_start_index(self):
        if os.path.exists(self.output_file):
            existing_isochrones = gpd.read_file(self.output_file)
            return len(existing_isochrones)
        return 0

    def calculate_isochrones(self):
        nodes = gpd.read_file(self.input_file).to_crs('EPSG:4326')
        start_idx = self.get_start_index()
        request_count = 0
        
        geometries = []
        node_ids = []
        
        if os.path.exists(self.output_file):
            existing_data = gpd.read_file(self.output_file)
            geometries.extend(existing_data.geometry.tolist())
            node_ids.extend(existing_data.node_id.tolist())
        
        logging.info(f"Starting processing from index {start_idx}")
        
        try:
            with tqdm(total=len(nodes), initial=start_idx) as pbar:
                batch_start_time = time.time()
                
                for idx, row in nodes.iloc[start_idx:].iterrows():
                    if request_count >= 450:
                        logging.info("Session limit (450) reached")
                        break
                    
                    result = self.client.isochrones(
                        locations=[[row.geometry.x, row.geometry.y]],
                        profile='foot-walking',
                        range=[500],
                        attributes=['area']
                    )
                    
                    isochrone_geom = shape(result['features'][0]['geometry'])
                    geometries.append(isochrone_geom)
                    node_ids.append(row.name)
                    
                    request_count += 1
                    pbar.update(1)
                    
                    if len(geometries) % 10 == 0:
                        temp_gdf = gpd.GeoDataFrame(
                            {'node_id': node_ids, 'geometry': geometries},
                            crs='EPSG:4326'
                        )
                        temp_gdf.to_file(self.output_file, driver='GeoJSON')
                    
                    elapsed = time.time() - batch_start_time
                    if idx % 11 == 10 and elapsed < 60:
                        time.sleep(60 - elapsed)
                        batch_start_time = time.time()
                            
        except Exception as e:
            logging.error(f"Error processing node {row.name}: {str(e)}")
            raise
        
        isochrones_gdf = gpd.GeoDataFrame(
            {'node_id': node_ids, 'geometry': geometries},
            crs='EPSG:4326'
        )
        
        isochrones_gdf.to_file(self.output_file, driver='GeoJSON')
        logging.info(f"Processing completed. Processed {request_count} nodes.")
            
        return isochrones_gdf

if __name__ == "__main__":
    config = {
        'input_file': 'input/kitas_processed.geojson',
        'output_dir': 'catchment_area/output',
        'api_key': '-'
    }
    
#    calculator = IsochroneCalculator(**config)
#    isochrones = calculator.calculate_isochrones()

    # Überlappende Flächen entfernen
    isochrones = gpd.read_file(f"{config['output_dir']}/isochrones.geojson")
    
    # Alle Geometrien in eine Liste konvertieren
    all_geoms = list(isochrones.geometry)
    
    # Für jede Geometrie die Überlappungen mit nachfolgenden Geometrien entfernen
    for i in range(len(all_geoms)):
        for j in range(i + 1, len(all_geoms)):
            if all_geoms[i].intersects(all_geoms[j]):
                # Überlappenden Bereich von der ersten Geometrie abziehen
                all_geoms[i] = all_geoms[i].difference(all_geoms[j])
    
    # Aktualisierte Geometrien zurück ins GeoDataFrame schreiben
    isochrones.geometry = all_geoms
    
    # Ergebnisse speichern
    output_file = f"{config['output_dir']}/isochrones_overlapping.geojson"
    isochrones.to_file(output_file, driver='GeoJSON')
    logging.info(f"Überlappungsfreie Isochrone wurden in {output_file} gespeichert")
