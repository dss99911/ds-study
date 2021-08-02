# Spark Conf

https://spark.apache.org/docs/latest/configuration.html



## default conf
search file named `spark-defaults.conf`


## Python Package Management 
- Use python packages for executors
- https://spark.apache.org/docs/latest/api/python/user_guide/python_packaging.html
- https://databricks.com/blog/2020/12/22/how-to-manage-python-dependencies-in-pyspark.html
- use conf `spark.submit.pyFiles` or `spark.archives`

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
