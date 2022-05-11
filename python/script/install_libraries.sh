cd ..
pip install -r requirements.txt
pip install pyspark-stubs==3.0.0.post3 --no-deps

# sagemaker's pyspark version is not matched with latest pyspark version
pip install sagemaker-pyspark==1.4.2 --no-deps
pip install sagemaker==2.89.0