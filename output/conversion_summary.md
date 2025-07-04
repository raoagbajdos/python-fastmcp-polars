# Actuarial Data Conversion Summary

**Conversion Date:** 2025-07-03 15:54:10

**Source:** actuarial_data.xlsx
**Output Directory:** output

## Sheets Processed

### Life_Table
- **Parquet:** `life_table.parquet`
- **CSV:** `life_table.csv`
- **JSON:** `life_table.json`
- **Schema:** `life_table_schema.json`

### Policies
- **Parquet:** `policies.parquet`
- **CSV:** `policies.csv`
- **JSON:** `policies.json`
- **Schema:** `policies_schema.json`

### Claims
- **Parquet:** `claims.parquet`
- **CSV:** `claims.csv`
- **JSON:** `claims.json`
- **Schema:** `claims_schema.json`

### Reserves
- **Parquet:** `reserves.parquet`
- **CSV:** `reserves.csv`
- **JSON:** `reserves.json`
- **Schema:** `reserves_schema.json`

## File Formats

- **Parquet:** Efficient binary format, best for data analysis
- **CSV:** Human-readable, compatible with Excel and other tools
- **JSON:** Structured format, good for web applications
- **Schema:** Metadata and statistics about each dataset

## Usage Examples

```python
import polars as pl

# Load life table data
life_table = pl.read_parquet('life_table.parquet')

# Load policy data
policies = pl.read_parquet('policies.parquet')

# Perform analysis
avg_premium = policies.select(pl.col('Annual_Premium').mean())
```
