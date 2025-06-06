# -*- coding: utf-8 -*-
"""file_types.ipynb


#Files type, Readind speed and size
"""

!pip install fastavro

import pandas as pd
import os
import time
import pickle
import fastavro
import pyarrow.orc as orc
import pyarrow.feather as feather


# Generating large dataset (1000000)
print("Generating large dataset...")
num_rows = 1000000
data = {
    'id': range(num_rows),
    'name': [f'User_{i}' for i in range(num_rows)],
    'value_a': [float(i * 1.5) for i in range(num_rows)],
    'category': [f'Category_{i % 10}' for i in range(num_rows)],
    'description': [f'This is a long description for item {i}' for i in range(num_rows)]
}
df = pd.DataFrame(data)
print(f"Dataset generated with {len(df)} rows and {len(df.columns)} columns.")

print(df.head(5))

"""## Testing Write Speed and File Size"""

# Make path for data
output_dir = 'data_speed_test'
os.makedirs(output_dir, exist_ok=True)

csv_file = os.path.join(output_dir, 'large_data.csv')
json_file = os.path.join(output_dir, 'large_data.json')
parquet_file = os.path.join(output_dir, 'large_data.parquet')
pickle_file = os.path.join(output_dir, 'large_data.pkl')
avro_file = os.path.join(output_dir, 'large_data.avro')
orc_file = os.path.join(output_dir, 'large_data.orc')
feather_file = os.path.join(output_dir, 'large_data.feather')

print("\n--- Testing Write Speed and File Size ---")

# Writing in CSV file
start_time = time.time()
df.to_csv(csv_file, index=False)
end_time = time.time()
print(f"CSV Write Time: {end_time - start_time:.4f} seconds")
print(f"CSV File Size: {os.path.getsize(csv_file) / (1024 * 1024):.2f} MB")

print("- - -"*10)
# Writing in JSON file
start_time = time.time()
df.to_json(json_file, orient='records', lines=True)  # lines=True makes it JSONL (JSON Lines)
end_time = time.time()
print(f"JSON Write Time: {end_time - start_time:.4f} seconds")
print(f"JSON File Size: {os.path.getsize(json_file) / (1024 * 1024):.2f} MB")

print("- - -"*10)
# Writing in Parquet file
start_time = time.time()
df.to_parquet(parquet_file, engine='pyarrow', index=False)
end_time = time.time()
print(f"Parquet Write Time: {end_time - start_time:.4f} seconds")
print(f"Parquet File Size: {os.path.getsize(parquet_file) / (1024 * 1024):.2f} MB")

print("- - -"*10)
# Writing in ORC file
start_time = time.time()
df.to_orc(orc_file, engine='pyarrow')
end_time = time.time()
print(f"ORC Write Time: {end_time - start_time:.4f} seconds")
print(f"ORC File Size: {os.path.getsize(orc_file) / (1024 * 1024):.2f} MB")

print("- - -"*10)
# Writing in Feather file
start_time = time.time()
df.to_feather(feather_file)
end_time = time.time()
print(f"Feather Write Time: {end_time - start_time:.4f} seconds")
print(f"Feather File Size: {os.path.getsize(feather_file) / (1024 * 1024):.2f} MB")

print("- - -"*10)
# Writing in Pickle file
start_time = time.time()
with open(pickle_file, 'wb') as f:
    pickle.dump(df, f)
end_time = time.time()
print(f"Pickle Write Time: {end_time - start_time:.4f} seconds")
print(f"Pickle File Size: {os.path.getsize(pickle_file) / (1024 * 1024):.2f} MB")

print("- - -"*10)
# Writing in Avro file
schema = {
    "type": "record",
    "name": "DataFrame",
    "fields": [{"name": col, "type": "string" if df[col].dtype == 'object' else "int"} for col in df.columns]
}

start_time = time.time()
with open(avro_file, 'wb') as f:
    writer = fastavro.writer(f, schema, df.to_dict(orient="records"))
end_time = time.time()
print(f"Avro Write Time: {end_time - start_time:.4f} seconds")
print(f"Avro File Size: {os.path.getsize(avro_file) / (1024 * 1024):.2f} MB")

print("\n--- Testing Read Speed ---")

"""## Testing Reading Speed"""

# Reading from csv file
start_time = time.time()
df_csv = pd.read_csv(csv_file)
end_time = time.time()
print(f"CSV Read Time: {end_time - start_time:.4f} seconds")

# Reading from JSON file
start_time = time.time()
df_json = pd.read_json(json_file, orient='records', lines=True)
end_time = time.time()
print(f"JSON Read Time: {end_time - start_time:.4f} seconds")

# Reading from Parquet file (all columns)
start_time = time.time()
df_parquet = pd.read_parquet(parquet_file, engine='pyarrow')
end_time = time.time()
print(f"Parquet Read All Columns Time: {end_time - start_time:.4f} seconds")

# Reading from ORC file
start_time = time.time()
df_orc = pd.read_orc(orc_file) 
end_time = time.time()
print(f"ORC Read Time: {end_time - start_time:.4f} seconds")

# Reading from Feather file
start_time = time.time()
df_feather = pd.read_feather(feather_file)
end_time = time.time()
print(f"Feather Read Time: {end_time - start_time:.4f} seconds")

# Reading from Pickle file
start_time = time.time()
with open(pickle_file, 'rb') as f:
    df_pickle = pickle.load(f)
end_time = time.time()
print(f"Pickle Read Time: {end_time - start_time:.4f} seconds")

# Reading from Avro file
start_time = time.time()
with open(avro_file, 'rb') as f:
    reader = fastavro.reader(f)
    df_avro = pd.DataFrame(list(reader))
end_time = time.time()
print(f"Avro Read Time: {end_time - start_time:.4f} seconds")

# Reading from Parquet file (only one row)
print("\n--- Testing Parquet Read Speed ---")
start_time = time.time()
df_parquet_col = pd.read_parquet(parquet_file, engine='pyarrow', columns=['value_a'])
end_time = time.time()
print(f"Parquet Read 'value_a' Column Only Time: {end_time - start_time:.4f} seconds")

