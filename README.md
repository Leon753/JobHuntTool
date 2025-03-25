# JobHuntTool

# Project Setup Instructions

## Prerequisites

- **Python 3.12**: Ensure Python 3.12 is installed on your machine.
- **Git**: Required for cloning the repository (if applicable).

## Steps to Set Up and Run the Project

### 1. Clone the Repository (if needed)

If you haven't already cloned the project repository, run:

```bash
git clone <repository_url>
cd <repository_directory>/backend

```
### 2. Create & activate Virtual Enviroment
```bash
python3.12 -m venv venv
source venv/bin/activate
```

### 3. Install Poetry 

```bash
pip install poetry
```


### 3. Install Project Dependencies
```bash
poetry install
```

### 4. Run Server
```bash 
poetry run python -m uvicorn main:app --port 8080 --reload
```

