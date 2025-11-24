from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
import tempfile
import json
from app.grain import apply_grain

app = FastAPI(title="FilmGrain API")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/process")
async def process_endpoint(
    file: UploadFile = File(...),
    scale: float = Form(1.0),
    src_type: int = Form(1),
    grain_power: float = Form(1.0),
    shadows: float = Form(0.5),
    highs: float = Form(0.5),
    grain_type: int = Form(1),
    grain_sat: float = Form(0.5),
    sharpen: int = Form(0),
    gray: bool = Form(False)
):
    # Create temp file for upload
    fd, input_path = tempfile.mkstemp(suffix=os.path.splitext(file.filename)[1])
    os.close(fd)
    
    try:
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Prepare params
        params = {
            "scale": scale,
            "src_type": src_type,
            "grain_power": grain_power,
            "shadows": shadows,
            "highs": highs,
            "grain_type": grain_type,
            "grain_sat": grain_sat,
            "sharpen": sharpen,
            "gray": gray
        }
        
        # Process
        output_path = apply_grain(input_path, params)
        
        # Return file
        return FileResponse(output_path, media_type="image/png", filename="grained.png")
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error processing image: {e}", flush=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup input file
        if os.path.exists(input_path):
            os.remove(input_path)
        # Note: Output file is returned, FastAPI handles closing, but we might need a background task to delete it later.
        # For now, we rely on OS temp cleanup or container restart for simplicity, 
        # or we could use BackgroundTasks to delete after sending.

