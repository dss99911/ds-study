[What is Job, Stage, Task](https://rtfmplz.github.io/2017/05/02/what-is-job-stage-task-in-spark)
[DagScheduler](https://mallikarjuna_g.gitbooks.io/spark/content/spark-dagscheduler.html)

Action : collect, show, reduce, count 등 실제로 job을 실행시키는 메서드

Job
- Stage로 분할된 계산들의 조합
- map, filter등 여러 변환, 처리 등을 한 후, action이 호출되면, job이 만들어지고, job이 실행된다.

Stage
- Parallel Tasks의 집합
- join, repartition등 shuffle dependencies가 job에서 stage를 분리시키는 요소로 작용한다.
- 병렬 처리가 가능한 한 task의 집합

Task
- 개별 파티션에 대한 연산을 처리하는 작업, JVM에 의해 실행
- 데이터는 여러 파티션에 존재할 수 있다. 한 파티션에 대한 연산을 처리함.


