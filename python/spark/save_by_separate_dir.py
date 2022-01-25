import json
import boto3
import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta
import uuid
from util.util import *

# 목적 : 특정 id의 값을 가져와서 처리하기 위해, 비용이 작은 s3를 서빙용으로 사용하기
#   - 요청시 바로 응답해야 하는 실시간 서빙에는 어렵고, 피쳐 생성등, 완전 실시간이 아닌, streaming으로 단기 배치 처리로 가능한 경우 사용.

# 이런 방식을 사용하는 이유
# - spark는 파티션별로 저장하는데 시간이 많이 걸린다.
# - 실제 사용할 때도, 파티션이 많으면 쿼리 시간이 엄청 오래 걸림.
# - bucketing은 실제 서빙에서는 사용하기에 시간이 오래 걸림.
# - 서빙시 각 파티션 값 별 dir을 직접 호출하기 때문에, 호출이 빠름
#
# need to install pandas, numpy, boto3 if it's not installed

BUCKET = "hyun"
PATH = f"s3://{BUCKET}/some_data"
PATH_PARTITION_COL = "dt"

NEW_PATH = "some_new_path" # without s3 bucket
NEW_PARTITION_COL = "id"
SORT_COL = "time"
start = datetime.strptime(get_argv(0), '%Y-%m-%d')
end = get_argv(1)
if end is None:
    end = start + timedelta(days=1)
else:
    end = datetime.strptime(end, '%Y-%m-%d')

spark = create_spark_session("save_by_separate_dir")

def create_file_by_id(i, uuid_str):
    id = i[0][NEW_PARTITION_COL]
    local_file = f"{id}-{uuid_str}.parquet"
    # 데이터가 많으면 파일 분리하기.
    # 중복 제거 고려
    data_dict = list(map(lambda r: r.asDict(), i))
    df = pd.DataFrame(data_dict)
    df = df.sort_values(by=SORT_COL)
    df.to_parquet(local_file)

    boto3.client('s3').upload_file(local_file, BUCKET, f"{NEW_PATH}/{id}/{id}-{uuid_str}.parquet")
    os.remove(local_file)


def create_file(spark, dt, uuid_str):
    spark.read.parquet(f"{PATH}/{PATH_PARTITION_COL}={dt}").repartition(NEW_PARTITION_COL).foreachPartition(lambda i: create_file_by_id(list(i), uuid_str))


while start < end:
    uuid_str = uuid.uuid1()
    create_file(spark, start.strftime("%Y-%m-%d"), uuid_str)
    print(start)
    start = start + timedelta(days=1)
