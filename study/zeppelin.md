# Zeppelin

## Ztools
- [Ztools](https://blog.jetbrains.com/idea/2020/10/ztools-for-apache-zeppelin/)
- Schema autocomplete
- Variable Explorer
-  

## Publish Paragraph result
- https://zeppelin.apache.org/docs/0.6.1/manual/publish.html
- use something like the below on markdown paragraph.
```html
<iframe src="/#/notebook/2G4YMMBWU/paragraph/paragraph_1617676140706_-858949505?asIframe" width="100%"></iframe>ㅓㅐ
```

## log 보기
`/var/log/zeppelin` 에 `zeppelin-interpreter-spark-hyun.kim-zeppelin-ip-10-50-7-46.log` 와 같이 유저 이름과 함께 로그가 남음.

## Scheduling
- 특정 노트를 스케줄링 하기
https://zeppelin.apache.org/docs/0.8.0/usage/other_features/cron_scheduler.html
- 서버가 안정적이어야 쓰기 좋을 것 같고,
- 스케줄링 필요하면, 젠킨스에서 쓰는게 나을듯.

## Interpreter Binding Mode
https://zeppelin.apache.org/docs/0.9.0-preview1/usage/interpreter/interpreter_binding_mode.html
- per user로 설정하면, 유저별로, 다른 노트에 있는 변수, 함수도 참조 가능함.
- per user로 설정하면, 노트 내에서 interpret 재시작시, 유저별로, interpreter재시작되서, 다른 사용자에게 영향이 없음.(하지만, 노트에서 재시작해야함. interpreter세팅에서 재시작 하면, 전체 재시작)

## Version control of Zeppelin
https://zeppelin.apache.org/docs/0.8.0/setup/storage/storage.html#notebook-storage-in-github