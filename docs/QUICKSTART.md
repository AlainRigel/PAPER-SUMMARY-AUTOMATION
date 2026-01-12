# Quick Start Guide

## Web Interface (Recommended)

The easiest way to use Paper Collector is through the web interface:

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python app.py
```

### 3. Open Browser
Navigate to `http://localhost:8000`

### 4. Upload & Analyze
- Drag & drop a PDF or click to browse
- Click "Analyze Paper"
- View results and export JSON

See [web/README.md](web/README.md) for detailed web interface documentation.

## Command Line Interface

For programmatic or batch processing, use the CLI:

```bash
# Basic usage
python -m src.main ingest path/to/paper.pdf

# Save output to JSON
python -m src.main ingest paper.pdf -o output.json

# Verbose mode with detailed section breakdown
python -m src.main ingest paper.pdf -v
```
