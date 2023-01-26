# https://aws.amazon.com/ko/blogs/korea/install-python-libraries-on-a-running-cluster-with-emr-notebooks/

# { "conf":{
#           "spark.pyspark.python": "python", # default: python3    
#           "spark.pyspark.virtualenv.enabled": "true",
#           "spark.pyspark.virtualenv.type":"native",
#           "spark.pyspark.virtualenv.bin.path":"/usr/bin/virtualenv"
#          }
# }

# livy에서 virtual ennv설정해놓으면, spark.createDataFrame()에서 에러남. 필요할 때만 conf변경해서 호출하는게 좋을듯.

#가상환경에 설치하는 방식, 세션이 끝나면, 자동삭제됨
sc.list_packages()
sc.install_pypi_package("pandas==0.25.1") #Install pandas version 0.25.1
sc.install_pypi_package("matplotlib", "https://pypi.org/simple") #Install matplotlib from given PyPI repository


# 아래 값을 설정하면, "spark.pyspark.python": "python" 을 안해도됨
# "PYSPARK_PYTHON": "/usr/bin/python3",
# "PYSPARK_DRIVER_PYTHON": "/usr/bin/python3"

# 처음 install_pypi_package를 할 때는 설치된 것이 바로 import안되고, 재시작 해야 함. 그 이후부터 는 바로 됨

# working directory의 .local폴더에 library가 설치됨.