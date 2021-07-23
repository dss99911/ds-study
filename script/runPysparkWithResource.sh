
cd ..

mkdir -p build
if [ -d "build/python" ]; then
  rm -r build/python
fi
cp -r src/main/python build/python
cd build/python
zip -r -X "../python.zip" *
cd ../..

spark-submit --packages io.delta:delta-core_2.12:0.8.0 --py-files build/python.zip src/main/python/spark/main.py dev
