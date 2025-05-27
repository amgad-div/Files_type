
# File Types, Reading Speed, and Size

## Overview
This project benchmarks the writing and reading speeds of various file formats when handling large datasets. It also compares file sizes to evaluate storage efficiency. The goal is to understand the trade-offs between speed, size, and compatibility.

## Dataset
The dataset contains **1,000,000** rows with the following columns:
- `id`: Unique identifier.
- `name`: User-generated names.
- `value_a`: A numerical value with a floating-point format.
- `category`: Categorical classification for grouping.
- `description`: A long textual description.

## File Formats Tested
The dataset is saved in the following formats:
1. **CSV** - Common text-based format, readable in spreadsheets.
2. **JSON** - Structured format, useful for web applications.
3. **Parquet** - Columnar format optimized for analytics.
4. **ORC** - Binary format optimized for large-scale processing.
5. **Feather** - Fast binary format for Python.
6. **Pickle** - Python-native serialization.
7. **Avro** - Binary format with schema enforcement.

## Write Speed & File Size
Below are the measured write speeds and file sizes:

| Format  | Write Time (s) | File Size (MB) |
|---------|--------------|----------------|
| **CSV** | 5.4         | 78.13          |
| **JSON** | 2.8        | 130.58         |
| **Parquet** | 0.75    | 18.24          |
| **ORC** | 0.96         | 67.56         |
| **Feather** | 0.43     | 28.41         |
| **Pickle** | 1.73      | 83.73         |
| **Avro** | 9.31       | 68.82          |

## Read Speed
Below are the measured read speeds:

| Format  | Read Time (s) |
|---------|--------------|
| **CSV** | 2.8         |
| **JSON** | 9.3         |
| **Parquet** | 1.1      |
| **ORC** | 0.9         |
| **Feather** | 0.8     |
| **Pickle** | 1.4      |
| **Avro** | 4.7       |


## Why is Parquet Faster?
Parquet is optimized for analytical workloads due to its **columnar storage format**:
- **Columnar compression**: It stores columns separately, leading to better compression and smaller file sizes.
- **Efficient retrieval**: Only the required columns are loaded instead of reading the entire dataset, reducing I/O overhead.
- **Binary storage**: Unlike CSV or JSON, Parquet does not require complex parsing.
- **Optimized for parallelism**: It supports multi-threaded processing, making it ideal for big data workloads.

Parquet significantly reduces both storage space and read time, making it a preferred choice for **large datasets and analytical processing**.

## Usage
### Installation
Ensure dependencies are installed before running the script:
```sh
pip install fastavro pyarrow pandas
```

### Execution
Run the script to generate data, save files, and test read speeds:
```sh
python file_types.ipynb
```

Let me know if you need further refinements! 🚀
