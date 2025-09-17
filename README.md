# Auto PPT

Auto PPT is an application designed to automate the creation of PowerPoint presentations using AI. It features a backend API (FastAPI) for slide generation and a frontend (Streamlit) for user interaction. The system leverages AI agents to generate content and images for slides, streamlining the process of making professional presentations.

## Features
- Automated slide content generation
- AI-powered image creation for slides
- RESTful API for integration
- User-friendly frontend interface

---

## Getting Started

### Prerequisites
- Python 3.10+
- pip (Python package manager)

### 1. Install Dependencies
Navigate to the project root and run:

```bash
pip install -r requirements.txt
```

### 2. Start the Backend Server
Navigate to the `Backend` directory and run:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The backend server will be available at [http://localhost:8000](http://localhost:8000).

### 3. Start the Frontend Server
Navigate to the `Frontend` directory and run:

```bash
streamlit run app.py
```

The frontend will be available at the URL provided in the terminal (typically [http://localhost:8501](http://localhost:8501)).

---

## API Documentation

The backend API is built with FastAPI. Once the backend server is running, interactive API documentation is available at:
- [http://localhost:8000/]


### Main Endpoints

#### `POST /generate_ppt`
- **Description:** Generates a PowerPoint presentation based on user input.
- **Request Body:**
  - `topic` (string): The topic for the presentation.
  - `num_slides` (int): Number of slides to generate.
- **Response:**
  - Returns a downloadable PPTX file or a link to the generated file.

#### `GET /slides/{slide_id}`
- **Description:** Retrieves information or images for a specific slide.
- **Path Parameter:**
  - `slide_id` (string): The ID of the slide.
- **Response:**
  - Slide content and associated images.

#### `GET /images/{image_name}`
- **Description:** Serves generated images for slides.
- **Path Parameter:**
  - `image_name` (string): The filename of the image.
- **Response:**
  - Image file (PNG/JPG).

#### `GET /health`
- **Description:** Health check endpoint to verify the backend is running.
- **Response:**
  - JSON status message.

---

## Notes
- For more details, refer to the code in the `Backend` and `Frontend` directories.
- API endpoints and request/response formats may evolve as the project develops.
