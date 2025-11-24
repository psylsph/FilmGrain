import subprocess
import tempfile
import os
import shutil
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

def convert_to_png(input_path: str) -> str:
    """Converts input image to PNG if it's not already, handling HEIC."""
    try:
        img = Image.open(input_path)
        # Create a temp file for the PNG
        fd, output_path = tempfile.mkstemp(suffix=".png")
        os.close(fd)
        img.save(output_path, format="PNG")
        return output_path
    except Exception as e:
        raise ValueError(f"Failed to convert image: {e}")

def apply_grain(image_path: str, grain_params: dict) -> str:
    """
    Applies film grain using filmgrainer CLI.
    Returns path to the processed image.
    """
    # First ensure we have a PNG/JPG (filmgrainer might need specific inputs, but PIL handles most)
    # We convert to PNG to be safe and standardized
    png_path = convert_to_png(image_path)
    
    # Create output path
    fd, output_path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    
    # Construct command
    # filmgrainer usage: filmgrainer [options] -o output input
    
    cmd = ["filmgrainer"]
    
    # Map params to CLI args
    if "scale" in grain_params:
        cmd.extend(["--scale", str(grain_params["scale"])])
    
    if "grain_type" in grain_params:
        cmd.extend(["--type", str(grain_params["grain_type"])])
        
    if "grain_sat" in grain_params:
        cmd.extend(["--sat", str(grain_params["grain_sat"])])
        
    if "sharpen" in grain_params:
         cmd.extend(["--sharpen", str(grain_params["sharpen"])])

    if grain_params.get("gray"):
        cmd.append("--gray")

    # Construct power string from grain_power, shadows, highs
    # User provided usage: --power <overall>,<highlights>,<shadows>
    p_global = grain_params.get("grain_power", 1.0)
    p_shadows = grain_params.get("shadows", 0.5)
    p_highs = grain_params.get("highs", 0.5)
    power_str = f"{p_global},{p_highs},{p_shadows}"
    cmd.extend(["--power", power_str])

    # Output and Input
    cmd.extend(["-o", output_path])
    cmd.append(png_path)

    # Run command
    print(f"Running command: {' '.join(cmd)}", flush=True)
    try:
        # Capture both stdout and stderr
        result = subprocess.run(cmd, check=True, capture_output=True)
        print(f"Command output: {result.stdout.decode()}", flush=True)
    except subprocess.CalledProcessError as e:
        # Clean up temp files if failed
        if os.path.exists(png_path) and png_path != image_path:
            os.remove(png_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        
        stdout_msg = e.stdout.decode()
        stderr_msg = e.stderr.decode()
        print(f"Filmgrainer failed. Exit code: {e.returncode}", flush=True)
        print(f"STDOUT: {stdout_msg}", flush=True)
        print(f"STDERR: {stderr_msg}", flush=True)
        
        raise RuntimeError(f"Filmgrainer failed (Exit {e.returncode}): {stderr_msg} | {stdout_msg}")
        
    # Clean up intermediate PNG if it was created from a different source
    if png_path != image_path:
        os.remove(png_path)
        
    return output_path

