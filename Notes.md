# Jupyter Notebook/Lab
## Config - default notebook location setting
- run `jupyter notebook --generate-config`
- edit config file `jupyter_notebook_config.py`
- find `#c.NotebookApp.notebook_dir = ''` and change it to `c.NotebookApp.notebook_dir = 'D:\JupyterNotebook'`
- run `jupyter notebook` and done

## Config - autocomplete
- run `ipython profile create`
- edit config file `~/.ipython/profile_default/`
- find `#c.Completer.jedi_compute_type_timeout = 400` and change it to `c.Completer.jedi_compute_type_timeout = 400` 
- find `#c.Completer.greedy = False` and change it to `c.Completer.greedy = True`
- find `#c.Completer.use_jedi = True` and change it to `c.Completer.use_jedi = True`

# Graphviz
## Setup in Conda Environment
- `conda install -c conda-forge graphviz`
- `conda install -c conda-forge python-graphviz`