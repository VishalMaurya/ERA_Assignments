# Animal & File Upload App

A full-stack web application built with FastAPI backend and HTML/CSS/JS frontend featuring animal selection and file upload functionality.

## Features

### Animal Selection Box
- Three checkboxes for selecting animals: Cat, Dog, Elephant
- Displays corresponding animal images when selected
- Only one animal can be selected at a time (radio button behavior)

### File Upload Box  
- Drag-and-drop file upload functionality
- Click to select files
- Displays file information including:
  - File name
  - File size (formatted and in bytes)
  - File type/MIME type

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **File Handling**: Python multipart support
- **Static Files**: SVG images for animal placeholders
- **Package Manager**: uv (ultra-fast Python package installer)
- **Environment**: Virtual environment with uv

## Setup Instructions

### Option 1: Automated Setup (Recommended)

```bash
python run.py
```

This script will automatically:
- Install `uv` if not present
- Create a virtual environment
- Install all dependencies
- Start the application

### Option 2: Manual Setup

#### 1. Install uv (if not already installed)

```bash
pip install uv
```

#### 2. Create Virtual Environment

```bash
uv venv venv
```

#### 3. Activate Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

#### 4. Install Dependencies

```bash
uv pip install -r requirements.txt
```

#### 5. Run the Application

```bash
python main.py
```

The application will start on `http://localhost:8000`

### 3. Access the Application

Open your web browser and navigate to:
```
http://localhost:8000
```

## File Structure

```
Session2_Assignment/
├── main.py                 # FastAPI backend application
├── run.py                  # Automated setup and run script
├── check_setup.py          # Setup status checker
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore             # Git ignore patterns
├── venv/                  # Virtual environment (created by uv)
├── templates/
│   └── index.html         # Frontend HTML template
└── static/
    └── images/
        ├── cat.svg        # Cat placeholder image
        ├── dog.svg        # Dog placeholder image
        └── elephant.svg   # Elephant placeholder image
```

## API Endpoints

- `GET /` - Serves the main HTML page
- `GET /animal/{animal_name}` - Returns animal image (cat, dog, elephant)
- `POST /upload` - Handles file upload and returns file information

## Customization

### Adding Real Animal Images

To replace the placeholder SVG images with real photos:

1. Add your images to the `static/images/` folder
2. Name them `cat.jpg`, `dog.jpg`, `elephant.jpg` (or any supported image format)
3. Update the file extension in `main.py` line 35:
   ```python
   image_path = f"static/images/{animal_name.lower()}.jpg"  # Change .svg to .jpg
   ```

### Styling

The frontend uses modern CSS with:
- Gradient background
- Card-based layout
- Hover effects
- Responsive design
- Drag-and-drop visual feedback

## Browser Support

- Modern browsers with ES6+ support
- Chrome, Firefox, Safari, Edge
- Mobile responsive design

## Development

### Using uv environment

1. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate     # Windows
   ```

2. Run in development mode with auto-reload:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Adding new dependencies

```bash
# Add new package
uv pip install package_name

# Update requirements.txt
uv pip freeze > requirements.txt
```

## Why uv?

- **Fast**: uv is 10-100x faster than pip
- **Reliable**: Better dependency resolution
- **Modern**: Built in Rust with modern Python tooling
- **Compatible**: Drop-in replacement for pip

## Additional Utilities

### Setup Status Checker

```bash
python check_setup.py
```

This utility checks:
- ✅ uv installation and version
- ✅ Virtual environment status
- ✅ Dependencies installation
- 🎯 Overall setup health

### Project Structure

The project is now organized with:
- **Automated Setup**: `run.py` handles everything
- **Health Checks**: `check_setup.py` verifies configuration
- **Clean Environment**: Virtual environment isolation
- **Git Ready**: Proper `.gitignore` for Python projects
