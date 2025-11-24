# FilmGrain App

A web application that adds realistic film grain to your photos using the [filmgrainer](https://github.com/larspontoppidan/filmgrainer) library.

## Features

-   **Film Grain Simulation**: Adds realistic grain based on physical film characteristics.
-   **Format Support**: Supports PNG, JPG, and HEIC input formats.
-   **Customizable Controls**: Adjust grain power, scale, shadows, highlights, saturation, and sharpness.
-   **Grayscale Mode**: Option to force grayscale output.
-   **Responsive UI**: Mobile-friendly interface built with React.
-   **Dockerized**: Easy deployment with Docker Compose.

## Tech Stack

-   **Backend**: FastAPI (Python 3.11)
-   **Frontend**: React (Vite)
-   **Image Processing**: `filmgrainer`, `Pillow`, `pillow-heif`
-   **Infrastructure**: Docker, Nginx

## Prerequisites

-   Docker
-   Docker Compose

## Getting Started

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd FilmGrain
    ```

2.  **Start the application**:
    ```bash
    docker-compose up --build
    ```

3.  **Access the App**:
    -   **Frontend**: Open [http://localhost:3000](http://localhost:3000) in your browser.
    -   **Backend API Docs**: Available at [http://localhost:8000/docs](http://localhost:8000/docs).

## Usage

1.  Click "Choose Image" to upload a photo (PNG, JPG, or HEIC).
2.  Use the sliders to adjust the grain effect:
    -   **Grain Power**: Overall intensity of the grain.
    -   **Scale**: Scale of the grain relative to the image.
    -   **Shadows/Highs**: Grain intensity in shadows and highlights.
    -   **Saturation**: Color saturation of the grain.
3.  Toggle "Force Grayscale" for a black-and-white film look.
4.  Click "Apply Grain" to process the image.
5.  Once processed, click "Download" to save the result.

## Development

### Backend
The backend is located in the `backend/` directory. It uses `pip` for dependency management.
-   **Main entry point**: `app/main.py`
-   **Grain logic**: `app/grain.py`

### Frontend
The frontend is located in the `frontend/` directory. It is a standard Vite React app.
-   **Install dependencies**: `npm install`
-   **Run locally**: `npm run dev`

## License

This project uses `filmgrainer` which is licensed under the MIT License.
