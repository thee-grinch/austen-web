# FastAPI Server Installation Guide

Follow these steps to install and run the FastAPI server located in the `/app` directory.

## Prerequisites

- Python 3.7+
- `pip` (Python package installer)

## Installation

1. **Clone the repository** (if you haven't already):

    ```bash
    git clone https://github.com/thee-grinch/austen-web.git
    cd austen-web
    ```

2. **Navigate to the `/app` directory**:

    ```bash
    cd app
    ```

3. **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Server

1. **Start the FastAPI server**:

    ```bash
    uvicorn main:app --reload
    ```

    - The `--reload` flag will auto-reload the server upon code changes.

2. **Access the API documentation**:

    - Open your web browser and go to `http://127.0.0.1:8000/docs` for the interactive Swagger UI.
    - Alternatively, visit `http://127.0.0.1:8000/redoc` for the ReDoc documentation.

## Additional Information

- For more details on FastAPI, visit the [FastAPI documentation](https://fastapi.tiangolo.com/).
- Ensure your `requirements.txt` includes all necessary dependencies for the FastAPI server.

## on the signup use the following
username: admin@admin.ke
password: admin

to access admin dashboard or go to /admin endpoint
