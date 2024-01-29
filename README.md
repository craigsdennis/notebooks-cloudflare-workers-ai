# Jupyter Notebooks


## Installation

```bash
python -m venv venv
source ./venv/bin/activate
python -m pip install -r requirements.txt
```


## Output 

Extract to Markdown with images inlined.

```bash
jupyter nbconvert --to=markdown --ExtractOutputPreprocessor.enabled=False cloudflare-workers-ai.ipynb
```