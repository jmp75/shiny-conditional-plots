
This is a material for a blog post at https://jmp75.github.io/work-blog/.  


I ended up setting up a virtual env with [`uv`](https://docs.astral.sh/uv/getting-started/installation/).

```sh
cd ~/src/shiny-conditional-plots
uv venv --python 3.11
source .venv/bin/activate
uv pip install shiny shinywidgets
```
