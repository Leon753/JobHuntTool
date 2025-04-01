# JobHuntTool
Automated Job Tracker to help you get your next job. 

<img width="1710" alt="image" src="https://github.com/user-attachments/assets/9919b852-cdef-450d-9b0a-1f010919624f" />


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
poetry install --no-root
```

### 4. Run Server
```bash 
poetry run python -m uvicorn main:app --port 8080 --reload
```

