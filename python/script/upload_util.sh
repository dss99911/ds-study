S3_PATH=s3://hyun/common-utils.zip

set -e
cd ..

zip -r "common-utils.zip" . -x .idea/\* .git/\* build/\* dist/\* script/\* setup.py data/\* pipeline/\* program/\*

aws s3 cp common-utils.zip "$S3_PATH"
rm common-utils.zip