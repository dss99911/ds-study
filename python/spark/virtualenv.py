# https://aws.amazon.com/ko/blogs/korea/install-python-libraries-on-a-running-cluster-with-emr-notebooks/

# { "conf":{
#           "spark.pyspark.virtualenv.enabled": "true",
#           "spark.pyspark.virtualenv.type":"native",
#           "spark.pyspark.virtualenv.bin.path":"/usr/bin/virtualenv"
#          }
# }


#가상환경에 설치하는 방식, 세션이 끝나면, 자동삭제됨
sc.list_packages()
sc.install_pypi_package("pandas==0.25.1") #Install pandas version 0.25.1
sc.install_pypi_package("matplotlib", "https://pypi.org/simple") #Install matplotlib from given PyPI repository