#!/usr/bin/env python3
"""Runner script for actuarial data conversion example."""

import asyncio
import subprocess
import sys
from pathlib import Path


def install_dependencies():
    """Install required dependencies if not already installed."""
    print("🔧 Installing dependencies...")
    try:
        subprocess.run([
            "python3", "-m", "pip", "install", 
            "polars[xlsx]", "fastmcp", "pytest", "pytest-asyncio"
        ], check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)


def create_sample_data():
    """Create the sample actuarial Excel file."""
    print("📊 Creating sample actuarial data...")
    
    # Run the data creation script
    result = subprocess.run([
        "python3", "examples/create_actuarial_data.py"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Failed to create sample data: {result.stderr}")
        sys.exit(1)
    
    print(result.stdout)


async def run_conversion():
    """Run the Excel to Polars conversion."""
    print("🔄 Converting Excel to Polars format...")
    
    # Import and run the conversion
    sys.path.append(".")
    from examples.convert_actuarial_data import convert_excel_to_polars
    
    await convert_excel_to_polars(
        excel_path="sample_data/actuarial_data.xlsx",
        output_dir="output"
    )


def main():
    """Main runner function."""
    print("🚀 Actuarial Data Conversion Example")
    print("=" * 40)
    
    # Ensure we're in the right directory
    project_root = Path(__file__).parent
    if project_root.name != "python-mcp-excel-polars":
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Step 1: Install dependencies
    install_dependencies()
    
    # Step 2: Create sample data
    create_sample_data()
    
    # Step 3: Run conversion
    asyncio.run(run_conversion())
    
    print("\n🎉 Example completed successfully!")
    print("\n📁 Check the following directories:")
    print("   - sample_data/: Contains the generated Excel file")
    print("   - output/: Contains the converted Polars files")
    print("\n📋 Output formats:")
    print("   - .parquet: Efficient binary format for data analysis")
    print("   - .csv: Human-readable format")
    print("   - .json: Structured data format")
    print("   - _schema.json: Metadata and statistics")
    print("   - conversion_summary.md: Detailed report")


if __name__ == "__main__":
    main()
