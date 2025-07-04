#!/usr/bin/env python3
"""
Example script showing how to use the Excel to Polars MCP server.
This demonstrates the tools available and their usage.
"""

import asyncio
import tempfile
from pathlib import Path

import polars as pl
from excel_polars_mcp.server import (
    ListSheetsArgs,
    ReadExcelArgs,
    ReadExcelSheetArgs,
    list_sheets,
    read_excel,
    read_excel_sheet,
)


def create_sample_excel() -> str:
    """Create a sample Excel file for demonstration."""
    # Create sample data
    df1 = pl.DataFrame(
        {
            "Employee_ID": [1, 2, 3, 4, 5],
            "Name": [
                "Alice Johnson",
                "Bob Smith",
                "Charlie Brown",
                "Diana Prince",
                "Eve Wilson",
            ],
            "Department": [
                "Engineering",
                "Marketing",
                "Engineering",
                "HR",
                "Marketing",
            ],
            "Salary": [75000, 65000, 80000, 70000, 68000],
            "Start_Date": [
                "2022-01-15",
                "2021-03-10",
                "2020-06-01",
                "2023-02-20",
                "2022-11-05",
            ],
        }
    )

    # Create temporary Excel file
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        df1.write_excel(tmp.name, worksheet="Employees")
        return tmp.name


async def demonstrate_tools():
    """Demonstrate all available MCP tools."""
    print("🔧 Excel to Polars MCP Server Demo")
    print("=" * 40)

    # Create sample file
    sample_file = create_sample_excel()
    print(f"📁 Created sample Excel file: {sample_file}")

    try:
        # 1. List sheets in the Excel file
        print("\n1. 📋 Listing sheets in Excel file...")
        list_args = ListSheetsArgs(file_path=sample_file)
        sheets_result = await list_sheets(list_args)

        if sheets_result.get("success"):
            print(f"   Found sheets: {sheets_result['sheets']}")
        else:
            print(f"   ❌ Error: {sheets_result.get('error')}")

        # 2. Read entire Excel file (first sheet)
        print("\n2. 📖 Reading Excel file (default sheet)...")
        read_args = ReadExcelArgs(
            file_path=sample_file, has_header=True, infer_schema_length=100
        )
        read_result = await read_excel(read_args)

        if read_result.get("success"):
            print(f"   ✅ Successfully read {read_result['shape']} DataFrame")
            print(f"   📊 Columns: {read_result['columns']}")
            print(f"   🏗️  Schema: {read_result['schema']}")
            print("   📄 First few rows:")
            data = read_result["data"]
            for i in range(min(3, len(list(data.values())[0]))):
                row = {col: data[col][i] for col in data.keys()}
                print(f"      {row}")
        else:
            print(f"   ❌ Error: {read_result.get('error')}")

        # 3. Read specific sheet (if multiple sheets exist)
        if sheets_result.get("success") and sheets_result["sheets"]:
            sheet_name = sheets_result["sheets"][0]
            print(f"\n3. 📑 Reading specific sheet: '{sheet_name}'...")

            sheet_args = ReadExcelSheetArgs(
                file_path=sample_file, sheet_name=sheet_name, has_header=True
            )
            sheet_result = await read_excel_sheet(sheet_args)

            if sheet_result.get("success"):
                print(f"   ✅ Successfully read sheet '{sheet_name}'")
                print(f"   📊 Shape: {sheet_result['shape']}")
                print(f"   🏗️  Schema: {sheet_result['schema']}")
            else:
                print(f"   ❌ Error: {sheet_result.get('error')}")

        # 4. Demonstrate error handling
        print("\n4. 🚫 Testing error handling...")
        error_args = ReadExcelArgs(file_path="nonexistent_file.xlsx")
        error_result = await read_excel(error_args)
        print(f"   Expected error: {error_result.get('error')}")

    finally:
        # Cleanup
        Path(sample_file).unlink()
        print("\n🧹 Cleaned up sample file")

    print("\n✨ Demo completed!")


if __name__ == "__main__":
    asyncio.run(demonstrate_tools())