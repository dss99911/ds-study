https://docs.dask.org/en/stable/install.html
```shell
pip install "dask[complete]"
```



## submit
https://yarn.dask.org/en/latest/submit.html#submitting-an-application
```python
# Replace this
cluster = YarnCluster(...)

# with this
cluster = YarnCluster.from_current()

```
```shell
# Submit `myscript.py` to run on a dask cluster with 8 workers,
# each with 2 cores and 4 GiB
$ dask-yarn submit \
  --environment my_env.tar.gz \
  --worker-count 8 \
  --worker-vcores 2 \
  --worker-memory 4GiB \
  myscript.py

application_1538148161343_0051

$ dask-yarn status application_1538148161343_0051

$ dask-yarn kill application_1538148161343_0051

$ yarn logs -applicationId application_1538148161343_0051
```

## EMR
https://yarn.dask.org/en/latest/aws-emr.html
### bootstrap
- https://yarn.dask.org/en/latest/aws-emr.html#add-a-bootstrap-action
- use conda pack to install on task node. instead of installing on each task instance
- it guides to install by conda. but, it takes very long time on emr cluster(not sure the reason. so, I used venv-pack instead)
- install 
```shell
python3 -m venv test-env
source test-env/bin/activate
python3 -m pip install "dask[complete]"
python3 -m pip install dask-yarn
python3 -m pip install pyarrow s3fs venv-pack tornado
venv-pack
# use test-env.tar.gz venv-pack file.
```


## TODO
python a.py 로 실행하면 성공
    - 분산 처리도 되는 건지 확인
dask-yarn submit 으로 실행시키면 실패.
    - Failure in service dask.scheduler, see logs for more information.
    - dask dashboard에서 확인해봐야 할 것 같음. yarn log에는 별다른 내용이 없음. 
