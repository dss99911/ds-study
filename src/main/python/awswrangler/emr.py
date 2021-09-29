import awswrangler as wr
import getpass

subnet = getpass.getpass()
#%% create cluster
cluster_id = wr.emr.create_cluster(subnet)

#%% add step
step_id = wr.emr.submit_step(cluster_id, command=f"spark-submit s3://hyun.test/test.py")

#%% wait step
while wr.emr.get_step_state(cluster_id, step_id) != "COMPLETED":
    pass


#%% terminate cluster
wr.emr.terminate_cluster(cluster_id)

#%% use docker by ECR
# https://github.com/awslabs/aws-data-wrangler/blob/main/tutorials/016%20-%20EMR%20%26%20Docker.ipynb
# python library등을 emr에서 사용하려면, py-files 등을 사용하면, 번거로움이 많음
# docker에 python library를 설치해서 돌림.
# cluster를 생성할 때, docker 사용을 enabled시켜줘야 함
