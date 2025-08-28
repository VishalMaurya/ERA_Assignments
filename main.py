from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os
from pathlib import Path

app = FastAPI(title="Animal & File Upload App")

# Create static and templates directories if they don't exist
Path("static").mkdir(exist_ok=True)
Path("static/images").mkdir(exist_ok=True)
Path("templates").mkdir(exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main HTML page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/animal/{animal_name}")
async def get_animal_image(animal_name: str):
    """Return animal image based on selection"""
    valid_animals = ["cat", "dog", "elephant"]
    
    if animal_name.lower() not in valid_animals:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    image_path = f"static/images/{animal_name.lower()}.svg"
    
    if os.path.exists(image_path):
        return FileResponse(image_path)
    else:
        raise HTTPException(status_code=404, detail="Image not found")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Handle file upload and return file information"""
    
    # Get file size by reading the file
    contents = await file.read()
    file_size = len(contents)
    
    # Reset file pointer for potential future use
    await file.seek(0)
    
    return {
        "filename": file.filename,
        "size": file_size,
        "type": file.content_type,
        "size_formatted": format_file_size(file_size)
    }

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
