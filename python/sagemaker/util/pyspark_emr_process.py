
# todo modify path properly.
#from util.pandas_util import *
from pandas_util import *
import sys


def process(schema_path, py_path, instance_type, instance_count, volume_size, args):
    name = f"{py_path.split('/')[-1].split('.')[0]}"
    run_emr_spark_job(
        name=name,
        steps=[
            create_emr_pyspark_step(schema_path, py_path, args)
        ],
        instance_type_core=instance_type,
        instance_num_on_demand_core=int(instance_count),
        instance_ebs_size_core=int(volume_size),
        instance_ebs_size_task=int(volume_size),
        logging_s3_path=f"{schema_path}/log/{name}"
    )


if __name__ == '__main__':
    process(
        get_args_schema_path(),
        get_args("py_path"),
        get_args("instance_type"),
        get_args("instance_count"),
        get_args("volume_size"),
        sys.argv[1:]
    )