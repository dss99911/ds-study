# Spark Conf

https://spark.apache.org/docs/latest/configuration.html



## default conf
search file named `spark-defaults.conf`


## Python Package Management 
- Use python packages for executors
- https://spark.apache.org/docs/latest/api/python/user_guide/python_packaging.html
- https://databricks.com/blog/2020/12/22/how-to-manage-python-dependencies-in-pyspark.html
- use conf `spark.submit.pyFiles` or `spark.archives`
- archives방식은 시도해봤지만, 무슨 이유에선가 안됨
- site-packages 를 zip으로 압축하여, pyFiles에 추가하는 방식으로 처리. spark-defaults.conf에 추가하면 별도로 추가할 필요가 없음. 하지만 별도의 python file을 추가할 경우. --py-files {a-path},{b-path} 와 같은 식으로, 둘다 추가해줘야 함. conf파일에 등록되어 있어도 --py-files를 추가하면, overwrite됨. 

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
