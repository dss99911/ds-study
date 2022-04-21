# Jupyter
## Install
```shell
conda install -c conda-forge notebook
```

## Run notebook
```shell
jupyter notebook
```

## Difference with scientific mode
### scientific mode
- no need jupyter server
- able to call cell from various python files
- able to refer other python files. 
- result is not saved

### Jupyter
- result is saved
  https://github.com/dss99911/spark-study/blob/master/src/main/python/jupyter/matplot.ipynb


View the notebooks online:
[![nbviewer](https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg)](https://nbviewer.jupyter.org/github/dss99911/spark-study/blob/master/python/jupyter)


Excecute the notebooks in Binder:
  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/dss99911/spark-study/HEAD)

## Jupyter Enterprise Gateway
https://jupyter-enterprise-gateway.readthedocs.io/en/latest/
- EMR에서 지원함.
- 여러 유저가 리소스를 여러 노트북에서 사용할 때, 더 효과적이라고 함.