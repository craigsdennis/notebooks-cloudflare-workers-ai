# Jupyter Notebooks


<iframe width="560" height="315" src="https://www.youtube.com/embed/1AnBEBhfnic?si=13UuhL1FzNu5ZofX" title="Exploring Cloudflare Workers AI API in a Jupyter Notebook" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

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