# ReleaseRank Backend

Python FastAPI backend for ReleaseRank.

## Setup

### Prerequisites
- Python 3.11+
- pip or poetry

### Installation

```bash
cd backend
pip install -r requirements.txt
```

### Development

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── routes/       # API endpoint definitions
│   │   └── __init__.py
│   ├── core/
│   │   ├── config.py     # Configuration settings
│   │   └── __init__.py
│   ├── models/
│   │   ├── schemas.py    # Pydantic schemas
│   │   └── __init__.py
│   ├── services/         # Business logic services
│   ├── main.py           # FastAPI app initialization
│   └── __init__.py
├── uploads/              # Temporary audio file storage
├── requirements.txt
├── .env.example
└── README.md
```