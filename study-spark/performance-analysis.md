# 성능 분석

1. 작업 partition, shuffle partition 설정
   - ganglia에서 core들이 쉬는 시간이 많은지 체크 (한 코어가 3개는 처리할 수 있게 해야, 일찍 끝난 코어가 놀지 않음)

2. memory 설정
   - gc시간이얼마나 걸리는지 파악하고(ganglia나 spark ui에서 확인), memory가 큰 instance를 써야 하는지 파악하기.