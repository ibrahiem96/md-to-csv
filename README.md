# Markdown to CSV

Web service that converts markdown tables to CSV tables (friendly for excel).

## Requirements

- Python3
- Pip

## Run in Debug Mode

```bash
pip3 install -r requirements.txt
python3 app.py
```

## Run in Docker

```bash
docker build -t md-to-csv .
docker run -p 5000:5000 md-to-csv
```