# Setup Instructions

Install Python pre-requisites

```bash
sudo apt install python3-pip ipython3
```

Create .env file:

```config
OPENAI_API_KEY='<api-key>'
```

Create Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run flask app:

```bash
python app.py
```
