import React, { useState } from 'react';
import axios from 'axios';
import './index.css';

function App() {
    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [processedImage, setProcessedImage] = useState(null);
    const [loading, setLoading] = useState(false);
    const [params, setParams] = useState({
        scale: 1.0,
        src_type: 1,
        grain_power: 0.75,
        shadows: 0.1,
        highs: 0.1,
        grain_type: 1,
        grain_sat: 0.6,
        sharpen: 0,
        gray: false
    });

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            setFile(selectedFile);
            setPreview(URL.createObjectURL(selectedFile));
            setProcessedImage(null);
        }
    };

    const handleParamChange = (e) => {
        const { name, value } = e.target;
        setParams(prev => ({ ...prev, [name]: parseFloat(value) }));
    };

    const processImage = async () => {
        if (!file) return;
        setLoading(true);

        const formData = new FormData();
        formData.append('file', file);
        Object.keys(params).forEach(key => {
            formData.append(key, params[key]);
        });

        try {
            const response = await axios.post('/process', formData, {
                responseType: 'blob'
            });
            const url = URL.createObjectURL(response.data);
            setProcessedImage(url);
        } catch (error) {
            console.error("Error processing image:", error);
            alert("Failed to process image.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container">
            <header>
                <h1>FilmGrain</h1>
                <p>Add realistic film grain to your photos.</p>
            </header>

            <main>
                <div className="controls">
                    <div className="upload-section">
                        <label htmlFor="file-upload" className="custom-file-upload">
                            Choose Image
                        </label>
                        <input id="file-upload" type="file" accept="image/*,.heic" onChange={handleFileChange} />
                        {file && <span className="filename">{file.name}</span>}
                    </div>

                    <div className="sliders">
                        <div className="control-group">
                            <label>Grain Power ({params.grain_power})</label>
                            <input type="range" name="grain_power" min="0" max="5" step="0.1" value={params.grain_power} onChange={handleParamChange} />
                        </div>
                        <div className="control-group">
                            <label>Scale ({params.scale})</label>
                            <input type="range" name="scale" min="0.1" max="5" step="0.1" value={params.scale} onChange={handleParamChange} />
                        </div>
                        <div className="control-group">
                            <label>Shadows ({params.shadows})</label>
                            <input type="range" name="shadows" min="0" max="1" step="0.1" value={params.shadows} onChange={handleParamChange} />
                        </div>
                        <div className="control-group">
                            <label>Highs ({params.highs})</label>
                            <input type="range" name="highs" min="0" max="1" step="0.1" value={params.highs} onChange={handleParamChange} />
                        </div>
                        <div className="control-group">
                            <label>Saturation ({params.grain_sat})</label>
                            <input type="range" name="grain_sat" min="0" max="1" step="0.1" value={params.grain_sat} onChange={handleParamChange} />
                        </div>
                    </div>

                    <div className="control-group">
                        <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
                            <input
                                type="checkbox"
                                name="gray"
                                checked={params.gray}
                                onChange={(e) => setParams(prev => ({ ...prev, gray: e.target.checked }))}
                                style={{ width: 'auto', accentColor: 'var(--primary-color)' }}
                            />
                            Force Grayscale
                        </label>
                    </div>

                    <button className="process-btn" onClick={processImage} disabled={!file || loading}>
                        {loading ? 'Processing...' : 'Apply Grain'}
                    </button>
                </div>

                <div className="preview-area">
                    <div className="image-container">
                        <h3>Original</h3>
                        {preview ? <img src={preview} alt="Original" /> : <div className="placeholder">No image selected</div>}
                    </div>
                    <div className="image-container">
                        <h3>Processed</h3>
                        {processedImage ? (
                            <>
                                <img src={processedImage} alt="Processed" />
                                <a href={processedImage} download="grained.png" className="download-btn">Download</a>
                            </>
                        ) : (
                            <div className="placeholder">{loading ? 'Processing...' : 'Waiting for result'}</div>
                        )}
                    </div>
                </div>
            </main>
        </div>
    );
}

export default App;
