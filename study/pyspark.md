# Pyspark

## [Install](https://spark.apache.org/docs/latest/api/python/getting_started/install.html)

```shell
conda create -n pyspark_env
conda activate -n pyspark_env
pip install pyspark

# setopt nonomatch # if use zsh
pip install pyspark[sql] # install extra dependencies
```

## environment file
```shell
conda env export > environment.yml
conda env create -f environment.yml
```

