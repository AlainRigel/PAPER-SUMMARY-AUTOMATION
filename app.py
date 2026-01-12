"""
Web application for Paper Collector.
FastAPI backend serving the web interface.
"""

from pathlib import Path
from typing import Optional
import json
import tempfile
import shutil

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.ingestion import SimplePDFParser
from src.models.paper import Paper

app = FastAPI(
    title="Paper Collector",
    description="Academic Research Cognitive Amplifier",
    version="0.1.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/web", StaticFiles(directory="web"), name="web")

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML interface."""
    html_file = Path("web/index.html")
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>Paper Collector</h1><p>Web interface not found. Please ensure web/index.html exists.</p>")


@app.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload and parse a PDF file.
    
    Returns the parsed Paper object as JSON.
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Save uploaded file temporarily
    temp_file = UPLOAD_DIR / file.filename
    
    try:
        # Save the uploaded file
        with temp_file.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Parse the PDF
        parser = SimplePDFParser()
        paper = parser.parse(temp_file)
        
        # Convert to dict for JSON response
        paper_dict = paper.model_dump(mode='json')
        
        return JSONResponse(content={
            "success": True,
            "paper": paper_dict,
            "filename": file.filename
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing PDF: {str(e)}")
    
    finally:
        # Clean up temporary file
        if temp_file.exists():
            temp_file.unlink()



@app.post("/api/analyze")
async def analyze_paper(file: UploadFile = File(...)):
    """
    Upload, parse, and perform academic analysis on a PDF file.
    
    Returns both the parsed Paper object and deep Academic Analysis.
    """
    from src.analysis import AcademicAnalyzer
    
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Save uploaded file temporarily
    temp_file = UPLOAD_DIR / file.filename
    
    try:
        # Save the uploaded file
        with temp_file.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Parse the PDF
        parser = SimplePDFParser()
        paper = parser.parse(temp_file)
        
        # Perform academic analysis with NLP
        analyzer = AcademicAnalyzer(use_nlp=True)
        analysis = analyzer.analyze(paper)
        
        # Convert to dicts for JSON response
        paper_dict = paper.model_dump(mode='json')
        analysis_dict = analysis.model_dump(mode='json')
        
        return JSONResponse(content={
            "success": True,
            "paper": paper_dict,
            "analysis": analysis_dict,
            "filename": file.filename
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing PDF: {str(e)}")
    
    finally:
        # Clean up temporary file
        if temp_file.exists():
            temp_file.unlink()


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "0.1.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
