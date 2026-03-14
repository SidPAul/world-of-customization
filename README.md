# Print Pop Project Setup

This guide will help you run the Print Pop project on your local machine.

## Prerequisites
- Python installed (use `py` command on Windows)

## Setup Instructions

### 1. Create a Virtual Environment (Recommended)
```bash
py -m venv venv
```

### 2. Activate the Virtual Environment
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
py manage.py migrate
```

### 5. Start the Development Server
```bash
py manage.py runserver
```

Once the server is running, you can access the landing page at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
