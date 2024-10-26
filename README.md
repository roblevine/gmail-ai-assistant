# Setup Instructions

Install Python pre-requisites

```bash
sudo apt install python3-pip ipython3
```

Create .env file:

```config
OPENAI_API_KEY='<openia-api-key>'
ANTHROPIC_API_KEY='<anthropic-api-key>'
OLLAMA_URL='http://<hostname>:11434'
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

# Accessing Ollama on the host from inside a container

Ensure Ollama on the host is set to listen on relevant interfaces (not just loopback)

### Powershell

```powershell
$env:OLLAMA_HOST="0.0.0.0"
ollama serve
```