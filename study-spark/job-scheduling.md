[Job Scheduling](https://spark.apache.org/docs/latest/job-scheduling.html): scheduling resources across and within Spark applications

## 여러 application들에 cluster자원 할당 방법
###static partitioning of resources
- 각 application에 고정된 자원을 할당함(자원이 할당되어 있으면, 해당 application이 종료되기 전까지는 다른 application에서 해당 자원 사용 불가)
- standalone, YARN, coarse-grained Mesos mode에서 사용되는 방식
- 각 cluster type별로, node 제한 및 executer, memory제한을 둘 수 있음(config 명이 좀 다름)


### dynamic sharing of CPU cores(available on Mesos)
- 각 application은 여전히 고정된 메모리를 할당 받음
- 하지만, 다른 application이 해당 node에 돌아가는 task가 없다면, 다른 application이 해당 core에서 돌아갈 수 있음.
- application은 많은데, 사용을 지속적으로 많이하는 application이 별로 없다면, 이 방식을 써도 좋다고.. (shell session을 여러 유저에게 제공할 경우)

### Dynamic Resource Allocation
- 여러 application에서 자원을 공유함
- 기본적으로 disabled됨
-  standalone mode, YARN mode, and Mesos coarse-grained mode에서 사용 가능


## 한 application내의 Scheduling

### FIFO(Default)
- 첫 job이 cluster 전체를 쓰고 있다면, 두번째 job은 대기를 타야함
- 첫 job이 cluster의 일부를 쓰고 있다면, 두번째 job은 바로 시작됨
### Round Robin (Fair scheduling)
- 각 job에 동일한 자원 분배
- 첫 job이 아무리 heavy해도, 두번째 job이 바로 시작할 수 있어서, FIFO와 같은 문제점이 없음
### Fair Schedule Pool
- pool을 나눠서, 우선순위가 높은 pool과 낮은 pool을 정할 수 있음