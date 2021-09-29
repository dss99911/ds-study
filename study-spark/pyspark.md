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



## Python Package Management
- Use python packages for executors
- https://spark.apache.org/docs/latest/api/python/user_guide/python_packaging.html
- https://databricks.com/blog/2020/12/22/how-to-manage-python-dependencies-in-pyspark.html
- use conf `spark.submit.pyFiles` or `spark.archives`
- archives방식은 시도해봤지만, 무슨 이유에선가 안됨
- site-packages 를 zip으로 압축하여, pyFiles에 추가하는 방식으로 처리. spark-defaults.conf에 추가하면 별도로 추가할 필요가 없음. 하지만 별도의 python file을 추가할 경우. --py-files {a-path},{b-path} 와 같은 식으로, 둘다 추가해줘야 함. conf파일에 등록되어 있어도 --py-files를 추가하면, overwrite됨.
- 다른 방법 : EMR Bootstrap Actions에 설정해놓으면, 전체 클러스터에 설치해준다.
    - 단점 : 처음 cluster설정시에만 설정가능하고, 추가 설치를 못한다.
- 다른 방법2 : docker를 이용. 아래와 같이 step을 추가할 때, docker image를 추가하면, 해당 step을 실행할 때, image를 실행시킨 후에 처리하는 듯.
  - docker image에 python library들을 설치한 후에 사용하는 방식임
  - https://github.com/awslabs/aws-data-wrangler/blob/main/tutorials/016%20-%20EMR%20%26%20Docker.ipynb
```python
DOCKER_IMAGE = f"{wr.get_account_id()}.dkr.ecr.us-east-1.amazonaws.com/emr-wrangler:emr-wrangler"

step_id = wr.emr.submit_spark_step(
    cluster_id,
    f"s3://{bucket}/test_docker.py",
    docker_image=DOCKER_IMAGE
)
```

### Using Virtualenv
- 동일한 python interpreter가 executor에 있어야 한다고 함.
- https://spark.apache.org/docs/latest/api/python/user_guide/python_packaging.html#using-virtualenv
- Error : ModuleNotFoundError: No module named 'Cython' -> use `pip3 install pyarrow pandas`

## Environment Variable
- https://spark.apache.org/docs/latest/configuration.html#environment-variables
- conf/spark-env.sh
- python path
    ```shell
    export PYTHONPATH=$PYTHONPATH:/var/lib/zeppelin/local-repo/graphframes/graphframes/0.8.1-spark3.0-s_2.12/graphframes-0.8.1-spark3.0-s_2.12.jar
    ```

### Python path
```python
import os
os.environ['PYSPARK_PYTHON'] # python location
os.environ['PYTHONPATH'] # python package paths
```

### find library installed path
``` python
import requests
requests
```
위의 코드 호출하면, 아래와 같이 위치가 나옴.

```
/usr/local/lib/python3.7/site-packages/requests/__init__.py:91: RequestsDependencyWarning: urllib3 (1.26.5) or chardet (3.0.4) doesn't match a supported version!
  RequestsDependencyWarning)
<module 'requests' from '/usr/local/lib/python3.7/site-packages/requests/__init__.py'>
```
