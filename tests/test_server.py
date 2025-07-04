"""Tests for the Excel to Polars MCP server."""

import tempfile
from pathlib import Path

import polars as pl
import pytest

from excel_polars_mcp.server import (
    ListSheetsArgs,
    ReadExcelArgs,
    ReadExcelSheetArgs,
    list_sheets,
    read_excel,
    read_excel_sheet,
)


@pytest.fixture
def sample_excel_file():
    """Create a temporary Excel file for testing."""
    # Create sample data
    df = pl.DataFrame({
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [25, 30, 35],
        "City": ["New York", "London", "Tokyo"],
    })

    # Create temporary file
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        df.write_excel(tmp.name)
        yield tmp.name

    # Cleanup
    Path(tmp.name).unlink()


def create_temp_text_file() -> str:
    """Creates a temporary text file and returns its path."""
    tmp = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)
    tmp.write(b"this is not an excel file")
    tmp.close()
    return tmp.name


@pytest.mark.asyncio
async def test_read_excel_success(sample_excel_file):
    """Test successful Excel file reading."""
    args = ReadExcelArgs(file_path=sample_excel_file)
    result = await read_excel(args)

    assert result["success"] is True
    assert "data" in result
    assert "schema" in result
    assert "shape" in result
    assert result["shape"] == (3, 3)  # 3 rows, 3 columns


@pytest.mark.asyncio
async def test_read_excel_file_not_found():
    """Test reading non-existent file."""
    args = ReadExcelArgs(file_path="nonexistent.xlsx")
    result = await read_excel(args)

    assert "error" in result
    assert "File not found" in result["error"]


@pytest.mark.asyncio
async def test_read_excel_invalid_extension():
    """Test reading file with invalid extension."""
    file_path = create_temp_text_file()
    try:
        args = ReadExcelArgs(file_path=file_path)
        result = await read_excel(args)

        assert "error" in result
        assert "must be an Excel file" in result["error"]
    finally:
        # Cleanup
        Path(file_path).unlink()


@pytest.mark.asyncio
async def test_list_sheets_success(sample_excel_file):
    """Test successful sheet listing."""
    args = ListSheetsArgs(file_path=sample_excel_file)
    result = await list_sheets(args)

    assert result["success"] is True
    assert "sheets" in result
    assert isinstance(result["sheets"], list)


@pytest.mark.asyncio
async def test_read_excel_sheet_success(sample_excel_file):
    """Test reading specific sheet."""
    # First get the sheet names
    list_args = ListSheetsArgs(file_path=sample_excel_file)
    list_result = await list_sheets(list_args)

    if list_result.get("success") and list_result["sheets"]:
        sheet_name = list_result["sheets"][0]

        args = ReadExcelSheetArgs(file_path=sample_excel_file, sheet_name=sheet_name)
        result = await read_excel_sheet(args)

        assert result["success"] is True
        assert result["sheet_name"] == sheet_name
        assert "data" in result


@pytest.mark.asyncio
async def test_read_excel_with_options(sample_excel_file):
    """Test reading Excel with custom options."""
    args = ReadExcelArgs(
        file_path=sample_excel_file, has_header=True, infer_schema_length=50
    )
    result = await read_excel(args)

    assert result["success"] is True
    assert len(result["columns"]) == 3
    assert "Name" in result["columns"]