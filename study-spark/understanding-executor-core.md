Executor : driver한테서 application code를 받아서, 각 core에 task를 할당함.
Core : 노드의 cpu core와 일치하는 개념. executor 가 각 core를 담당.

- config에 executor, core, memory 값들을 설정하는게 중요.
- core갯수를 크게 설정하면, executor갯수가 작아지고, 병렬성이 낮아짐(TODO 왜 낮아지지?)
- core갯수가 작으면, executor수가 많아지고, I/O operator 양이 많아진다고(TODO 이해안됨..driver node와 통신하는 데이터가 많아진다는 건가? executor가 병목이 될 수 있다는 의미 인 듯. 그런데, cpu처리량이 많은 작업이라면, executor가 적은게 좋은듯.)
- [reference](https://aws.amazon.com/blogs/big-data/best-practices-for-successfully-managing-memory-for-apache-spark-applications-on-amazon-emr/)