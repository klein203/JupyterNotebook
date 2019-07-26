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

# Decision Tree Notes
## Decision Tree Classifier
- ID3: min(info_gain)
- C4.5: min(info_gain_rate)
- CART: min(gini)

## Ensemble Classifier
- Random Forest: bagging, majority of nDTs prediction, DT={ID3, C4.5, CART ...}
- Extra Trees: bagging, majority of nDTs prediction, DT={random_feature}
- AdaBoost: boosting, 
- XgBoost

## Decision Tree Regression
- Decision Tree Regressor: min(sigma(R_l) + sigm(R_r))