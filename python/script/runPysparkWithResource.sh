set -e
cd ..

PY_NAME="$1" # python file path. ex) spark/read.py

zip -r -X "python.zip" *
#aws s3 cp python.zip s3://hyun/python.zip
#aws s3 cp "$PY_NAME" "s3://hyun/$PY_NAME"
rm python.zip

spark-submit --packages io.delta:delta-core_2.12:0.8.0 --py-files s3://hyun/python.zip main.py dev
