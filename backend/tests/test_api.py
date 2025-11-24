import pytest
from fastapi.testclient import TestClient
from app.main import app
import os
from PIL import Image
import io

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_process_image_png():
    # Create a dummy image
    img = Image.new('RGB', (100, 100), color = 'red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    files = {'file': ('test.png', img_byte_arr, 'image/png')}
    data = {
        'scale': 1.0,
        'grain_power': 0.5
    }
    
    # Mocking apply_grain would be ideal, but for integration test we might want to see if it runs.
    # However, filmgrainer might not be installed in the test environment.
    # So we should mock app.grain.apply_grain if we want to test the API layer only.
    
    # For this test, we assume the environment might not have filmgrainer, so we expect a 500 or we mock.
    # Let's mock it to verify API logic.
    
    from unittest.mock import patch
    with patch('app.main.apply_grain') as mock_apply:
        mock_apply.return_value = "/tmp/mock_output.png"
        # Create dummy output file
        with open("/tmp/mock_output.png", "wb") as f:
            f.write(b"fake png content")
            
        response = client.post("/process", files=files, data=data)
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
