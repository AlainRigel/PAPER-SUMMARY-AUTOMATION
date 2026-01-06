# Web Interface

Modern web interface for Paper Collector with drag-and-drop PDF upload and real-time analysis.

## Features

- 🎨 **Premium Dark Theme** - Beautiful, modern UI with smooth animations
- 📤 **Drag & Drop Upload** - Easy file upload with visual feedback
- ⚡ **Real-time Processing** - Instant PDF analysis and parsing
- 📊 **Rich Visualizations** - Detailed breakdown of paper structure
- 💾 **JSON Export** - Download parsed data for further analysis
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Server

```bash
python app.py
```

The server will start at `http://localhost:8000`

### 3. Open in Browser

Navigate to `http://localhost:8000` in your web browser.

## Usage

1. **Upload PDF**: Click the upload zone or drag & drop a PDF file
2. **Analyze**: Click "Analyze Paper" to process the document
3. **View Results**: See extracted metadata, sections, and content
4. **Export**: Download the parsed data as JSON

## API Endpoints

### `GET /`
Serves the web interface

### `POST /api/upload`
Upload and parse a PDF file

**Request**: Multipart form data with `file` field
**Response**: JSON with parsed paper data

```json
{
  "success": true,
  "paper": {
    "title": "Paper Title",
    "authors": [...],
    "sections": [...],
    ...
  },
  "filename": "paper.pdf"
}
```

### `GET /api/health`
Health check endpoint

**Response**: 
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

## File Structure

```
web/
├── index.html    # Main HTML interface
├── style.css     # Styling and theme
└── script.js     # Interactive functionality
```

## Customization

### Theme Colors

Edit CSS variables in `web/style.css`:

```css
:root {
    --primary: #6366f1;
    --secondary: #8b5cf6;
    --accent: #ec4899;
    /* ... */
}
```

### Server Configuration

Edit `app.py` to change host/port:

```python
uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Troubleshooting

### Server not starting
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check if port 8000 is available

### Upload fails
- Verify PDF file is valid and under 50MB
- Check server logs for errors

### CORS errors
- Server allows all origins by default
- Modify CORS settings in `app.py` if needed

## Development

To run in development mode with auto-reload:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Production Deployment

For production, use a production ASGI server:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

Or use Gunicorn with Uvicorn workers:

```bash
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```
