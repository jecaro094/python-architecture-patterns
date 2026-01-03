# python-architecture-patterns
Repository to apply principles in `Architecture Patterns with Python` book

## Dependencies

Install dependencies using this command:

```bash
python3 -m venv .venv   # Create virtual environment
source .venv/bin/activate   # Activate virtual environment
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

## Execute tests

```bash
pytest  # Test configuration in `pyproject.toml` file
```

## Database Script

Execute python script so that you can populate / manipulate local sqlite database used for the example:

```bash
python3 db_script.py
```

You can connect to database using a tool like dbeaver. Connect to sqlite database, and use folder location (path) to access the database (`mydb.sqlite` in my case, in my github repo path).