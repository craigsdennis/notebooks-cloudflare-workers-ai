# Jupyter Notebooks

[<img src="https://i.ytimg.com/vi/1AnBEBhfnic/maxresdefault.jpg" width="50%">](https://www.youtube.com/watch?v=1AnBEBhfnic "Exploring Cloudflare Workers AI API in a Jupyter Notebook")

## Installation

```bash
python -m venv venv
source ./venv/bin/activate
python -m pip install -r requirements.txt
```

## Open the viewer

```bash
jupyter notebook 
```

Choose your IPython Notebook (*.ipynb)


## Output 

Extract to Markdown with images inlined.

```bash
jupyter nbconvert --to=markdown --ExtractOutputPreprocessor.enabled=False cloudflare-workers-ai.ipynb
```