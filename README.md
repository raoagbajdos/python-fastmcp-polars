# Excel to Polars MCP Server

A Model Context Protocol (MCP) server that converts Excel files to Polars DataFrames using FastMCP. Includes comprehensive actuarial data examples and advanced analytics capabilities.

## Features

- Convert Excel files (.xlsx, .xls) to Polars DataFrames
- Support for multiple sheets with automatic detection
- Configurable data type inference and schema validation
- Memory-efficient processing using Polars
- Multiple output formats: Parquet, CSV, JSON
- Schema generation with statistics and metadata
- Professional actuarial data examples
- Advanced Polars analytics and reporting
- Comprehensive test suite with realistic data

## Installation

This project uses `uv` for dependency management. Make sure you have `uv` installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then install the project:

```bash
uv sync
```

## Usage

### Running the MCP Server

```bash
uv run excel-polars-mcp
```

## Available MCP Tools

- `read_excel`: Convert an Excel file to Polars DataFrame with configurable options
- `list_sheets`: List all sheet names in an Excel file
- `read_excel_sheet`: Read a specific sheet from an Excel file

## API Usage

```python
import polars as pl

# Load converted actuarial data
life_table = pl.read_parquet('output/life_table.parquet')
policies = pl.read_parquet('output/policies.parquet')
claims = pl.read_parquet('output/claims.parquet')
reserves = pl.read_parquet('output/reserves.parquet')

# Perform actuarial analysis
loss_ratios = policies.join(claims, on='Policy_ID').group_by('Policy_Type').agg([
    pl.col('Claim_Amount').sum() / pl.col('Face_Amount').sum() * 100
])

# High-value claims analysis
high_value_claims = claims.filter(pl.col('Claim_Amount') > 400000)

# Mortality analysis
high_mortality = life_table.filter(pl.col('Mortality_Rate_qx') > 0.1)
```

## Output Formats

Each Excel sheet is converted to multiple formats:

| Format | Use Case | File Extension |
|--------|----------|----------------|
| **Parquet** | High-performance analytics, data science | `.parquet` |
| **CSV** | Human-readable, Excel compatibility | `.csv` |
| **JSON** | Web APIs, structured data exchange | `.json` |
| **Schema** | Metadata, statistics, data validation | `_schema.json` |

## Sample Data

The project includes comprehensive actuarial datasets:

| Dataset | Records | Description |
|---------|---------|-------------|
| **Life Table** | 101 | Mortality rates, survival probabilities by age (0-100) |
| **Policies** | 1,000 | Insurance policies with demographics and financial data |
| **Claims** | 150 | Insurance claims with amounts, status, and investigation data |
| **Reserves** | 25 | Financial reserves by product type and valuation year |

## Examples

### Basic Usage
```bash
python3 examples/demo.py
```

### Actuarial Data Example
A comprehensive example that creates sample actuarial data and converts it to Polars format:

```bash
python3 run_actuarial_example.py
```

This example:
1. **Generates** a multi-sheet Excel file with realistic actuarial data:
   - **Life tables** with mortality rates, survival probabilities, and life expectancy (101 ages)
   - **Insurance policies** with demographics, premiums, face amounts (1,000 policies)
   - **Claims data** with types, amounts, status, and investigation times (150 claims)
   - **Reserve calculations** by product type and valuation year (25 records)

2. **Converts** each sheet to multiple formats:
   - **Parquet** files for efficient data analysis
   - **CSV** files for human readability and Excel compatibility
   - **JSON** files for web applications and APIs
   - **Schema** files with metadata, statistics, and data types

3. **Generates** comprehensive analytics:
   - Summary statistics and data quality reports
   - Loss ratio analysis by policy type
   - Mortality analysis and high-risk identification
   - Reserve adequacy and trend analysis

### Advanced Analytics Example
Perform comprehensive actuarial analysis on the converted data:

```bash
python3 analyze_polars_data.py
```

Features include:
- **Claims Analysis**: By status, type, and high-value claims
- **Policy Analysis**: Premium rates, face amounts, and status distribution  
- **Mortality Analysis**: High mortality ages and life expectancy statistics
- **Reserve Analysis**: Trends by year and product type
- **Loss Ratios**: Policy-to-claim analysis with advanced joins
- **Data Export**: Filtered datasets and summary reports

## Project Structure

```
├── excel_polars_mcp/          # Core MCP server implementation
│   ├── __init__.py
│   └── server.py              # FastMCP server with Excel conversion tools
├── examples/                  # Example scripts and demos
│   ├── demo.py               # Basic usage demonstration
│   ├── create_actuarial_data.py  # Generate sample actuarial Excel file
│   └── convert_actuarial_data.py # Convert Excel to Polars formats
├── sample_data/               # Generated sample data
│   └── actuarial_data.xlsx   # Multi-sheet actuarial Excel file
├── output/                    # Converted data in multiple formats
│   ├── *.parquet             # Efficient binary format
│   ├── *.csv                 # Human-readable format
│   ├── *.json                # Structured data format
│   ├── *_schema.json         # Metadata and statistics
│   └── conversion_summary.md  # Detailed conversion report
├── tests/                     # Comprehensive test suite
├── run_actuarial_example.py  # One-command actuarial demo
├── analyze_polars_data.py    # Advanced analytics demonstration
├── view_actuarial_data.py    # Data inspection utility
└── pyproject.toml            # Project configuration with uv

## Development

Install development dependencies:

```bash
uv sync --dev
```

Run tests:

```bash
uv run pytest
```

Format code:

```bash
uv run black .
uv run ruff check --fix .
```

Type checking:

```bash
uv run mypy .
```

## Quick Start

1. **Clone and setup**:
   ```bash
   git clone <repository>
   cd python-mcp-excel-polars
   uv sync
   ```

2. **Run the actuarial example**:
   ```bash
   python3 run_actuarial_example.py
   ```

3. **Analyze the results**:
   ```bash
   python3 analyze_polars_data.py
   ```

4. **Explore the data**:
   ```bash
   python3 view_actuarial_data.py
   ```

## Dependencies

- **Polars**: High-performance DataFrames
- **FastMCP**: Model Context Protocol implementation
- **openpyxl**: Excel file reading/writing
- **xlsxwriter**: Multi-sheet Excel creation
- **fastexcel**: Optimized Excel processing

## Use Cases

- **Actuarial Analysis**: Life tables, mortality studies, reserve calculations
- **Insurance Analytics**: Policy analysis, claims processing, loss ratios
- **Data Migration**: Excel to modern data formats (Parquet, JSON)
- **Financial Modeling**: Risk assessment, statistical analysis
- **Business Intelligence**: Automated reporting and data transformation

## License

MIT License - see LICENSE file for details.