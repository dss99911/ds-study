https://jaemunbro.medium.com/apache-spark-partition-%EA%B0%9C%EC%88%98%EC%99%80-%ED%81%AC%EA%B8%B0-%EC%A0%95%ED%95%98%EA%B8%B0-3a790bd4675d

파티션 수 조절하기

파티션이 많은 경우
- driver prgram에서 스케줄링이 버거워짐. driver OOM
- 작은 파일들을 생성하는 I/O
- executor의 OOM을 예방(한 파티션에 데이터가 많으면 OOM발생)
- 일반적으로 적은 것보단 많은게 좋음
- 메모리가 허용하는 한에서는 파티션이 적은게 좋음. 메모리 한도를 잘 모르기에, 처음엔 많이 설정해보고, 점차 줄여보기.