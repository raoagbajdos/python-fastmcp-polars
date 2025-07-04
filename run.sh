#!/bin/bash

# Excel to Polars MCP Server Setup and Run Script

set -e

echo "🚀 Setting up Excel to Polars MCP Server..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "✅ uv installed successfully"
fi

# Install dependencies
echo "📦 Installing dependencies with uv..."
uv sync

# Run type checking
echo "🔍 Running type checks..."
uv run mypy excel_polars_mcp/ --ignore-missing-imports || echo "⚠️  Type check warnings found"

# Run linting
echo "🧹 Running code formatting and linting..."
uv run black excel_polars_mcp/ tests/ examples/
uv run ruff check excel_polars_mcp/ tests/ examples/ --fix || echo "⚠️  Linting warnings found"

# Run tests
echo "🧪 Running tests..."
uv run pytest tests/ -v

# Start the server
echo "🎯 Starting MCP server..."
echo "Server will be available for MCP connections..."
uv run excel-polars-mcp