# Zeppelin

## Install
- https://zeppelin.apache.org/docs/0.9.0/quickstart/install.html
- apache/zeppelin dockerhub 이미지는 [Zeppelin interpreter](https://zeppelin.apache.org/docs/0.9.0/quickstart/docker.html)를 위한 것으로, Zeppelin UI설치를 위한 것은 아닌 것 같음. (anonymous로 작동하긴 하지만, shiro authentication file을 적용하면 에러남)
- binary로 설치하거나, 설정해야 할게 많으므로, AWS EMR cluster에 있는 zeppelin을 사용하거나 하면 좋을 듯.

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

## Authentication
refer to [this](https://zeppelin.apache.org/docs/latest/setup/security/shiro_authentication.html#overview)

- **Shiro-based** authentication for testing and informal use
- **LDAP and Active Directory** authentication for production use

### Find Shiro.ini file
```
find / -name shiro.ini.template
```

### copy shiro.ini file
```shell
cp /opt/zeppelin/conf/shiro.ini.template /opt/zeppelin/conf/shiro.ini
```

### change users on [users] tab on shiro.ini

### restart zeppelin
- it's different depends on environment

AWS EMR
```shell
sudo service zeppelin stop
sudo service zeppelin start
```

## Git Repo
https://zeppelin.apache.org/docs/0.8.0/setup/storage/storage.html
- S3 에 저장 가능.(version control 기능 사용 불가)
- loca git, remote git 사용 가능

## Sql
input 값을 받을 수 있음. 
- single value : `${maxAge=30}`
- list value : ${marital=single,single|divorced|married}
```sql
select age, count(1) value 
from bank 
where age < ${maxAge=30} 
group by age 
order by age
```

