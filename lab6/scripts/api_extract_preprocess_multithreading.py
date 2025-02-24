from secrets_import import *
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing
from tqdm import tqdm
import time

from api_extract_preprocess_helper import *


def process_well_batch(wells, batch_size=10):
    with ThreadPoolExecutor(max_workers=batch_size) as executor:
        futures = []
        for well in wells:
            futures.append(
                executor.submit(
                    get_well_details,
                    well_name=well["well_name"],
                    api_number=well["api_number"]
                )
            )
        return [future.result() for future in futures]

def update_well_data_batch(well_data_batch):
    conn = connect_db()
    with conn.cursor() as cursor:
        update_query = f"""
        UPDATE {TABLE_NAME} SET
            well_status = %s,
            well_type = %s,
            closest_city = %s,
            barrels_of_oil_produced = %s,
            mcf_of_gas_produced = %s
        WHERE api_number = %s;
        """
        cursor.executemany(update_query, [
            (
                data["well_status"],
                data["well_type"],
                data["closest_city"],
                data["barrels_of_oil_produced"],
                data["mcf_of_gas_produced"],
                data["api_number"]
            )
            for data in well_data_batch
        ])
        conn.commit()
    conn.close()

def process_wells_parallel(well_list, batch_size=50):
    
    num_processes = min(multiprocessing.cpu_count(), len(well_list) // batch_size + 1)
    
    
    well_batches = [
        well_list[i:i + batch_size]
        for i in range(0, len(well_list), batch_size)
    ]
    
    with ProcessPoolExecutor(max_workers=num_processes) as process_executor:
        
        futures = [
            process_executor.submit(process_well_batch, batch)
            for batch in well_batches
        ]
        

        with tqdm(total=len(well_list), desc="Processing wells") as pbar:
            for future in futures:
                well_data_batch = future.result()
                update_well_data_batch(well_data_batch)
                pbar.update(len(well_data_batch))

if __name__ == "__main__":
    start_time = time.time()
    print("Starting well data extraction and update...")
    
 
    check_and_create_columns()
    

    well_list = get_well_list_from_db()
    print(f"Found {len(well_list)} wells to process")
    
  
    process_wells_parallel(well_list)
    
    end_time = time.time()
    print(f"Processing completed in {end_time - start_time:.2f} seconds")