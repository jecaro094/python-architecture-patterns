# python-architecture-patterns
Repository to apply principles in `Architecture Patterns with Python` book

## Dependencies

Install dependencies using this command:

In order to create and activate a virtual environment:

```bash
python3 -m venv .venv   # Create virtual environment
source .venv/bin/activate   # Activate virtual environment
```

And, in order to install pip dependencies from requirements file:

```bash
pip install -r requirements.txt
```

## Execute locally

Run this command to execute fastapi application:

```bash
uvicorn application:app --reload
```

And access swagger trough this endpoint:

```bash
localhost:8000/docs
```

## Pre-commit

To standardize lint, types, etc... we use this command to apply `pre-commit`, from the root folder in the repo:

```bash
pre-commit run --files *.py
```

## Execute tests

```bash
pytest  # Test configuration in `pyproject.toml` file
```

## Database Script

Execute python script so that you can populate / manipulate local sqlite database used for the example:

```bash
python3 ./script_db.py
```

You can connect to database using a tool like dbeaver. Connect to sqlite database, and use folder location (path) to access the database (`mydb.sqlite` in my case, in my github repo path).