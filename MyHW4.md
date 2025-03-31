#### Couchbase

### Установка

Установка производилась на VM в Docker. При установке возникли проблемы с ресурсами, поэтому установку и натсройку производил по частям. Ниже команды по установке.
```
daemom@OVMCOUCH:~$  sudo docker run -d --name db3 -p 8091-8096:8091-8096 -p 11210-11211:11210-11211 couchbase
Unable to find image 'couchbase:latest' locally
latest: Pulling from library/couchbase
9cb31e2e37ea: Pull complete
f93d27079563: Pull complete
823613d60730: Pull complete
094dda71641f: Pull complete
16402788a899: Pull complete
4b036622c75a: Pull complete
2e5a6250533c: Pull complete
095ce9448d87: Pull complete
7a64793937a5: Pull complete
b2efc41046c9: Pull complete
4f4fb700ef54: Pull complete
133bd0212703: Pull complete
Digest: sha256:2c1ec01cdf6cb2142bd8219ae191a7b039e7353d51868e9bf6807d3ec629750d
Status: Downloaded newer image for couchbase:latest
2396c8a6a08597fda93a0fd797860cd92778d6e4d3d6c7f9db1df2dbde08bd3c
daemom@OVMCOUCH:~$ sudo docker run -d --name db2 couchbase
405834df81ca2e696c5d678d7f55c83c2a0258e926f5db938f8fa27aa0866934
daemom@OVMCOUCH:~$ sudo docker run -d --name db2 couchbase
77d8133557a19e71ffb0f94c0e3cec162fca7132092e0d8a08900d7bbf9d28e1
```
Узнаем IP адреса для добавления в кластер:
```
daemom@OVMCOUCH:~$ sudo docker inspect --format '{{ .NetworkSettings.IPAddress }}' db1
172.17.0.3
daemom@OVMCOUCH:~$ sudo docker inspect --format '{{ .NetworkSettings.IPAddress }}' db2
172.17.0.4
````
### Настройка

Настройка производилась через веб интерфейс. В итоге пришлось убрать часть сервисов и урезать ресурсы.  
Итоговый кластер:   
![CLASTER](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/claster.jpg?raw=true)  
Выделение ресурсов:    
![SETINGS](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/settinggs.jpg?raw=true)  
Загружаем данные:  
![DATA](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/data.jpg?raw=true)  
Выполним запрос:
![QUERY](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/query.jpg?raw=true)  

### Отказоустойчивость

Отключаем одну ноду:
```
daemom@OVMCOUCH:~$ sudo docker stop db2
db2
```
Видим что в класере нода недоступна:
![FAIL](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/stop1.jpg?raw=true)  
Выполняем запрос:
![QUERY2](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/qw2.jpg?raw=true)  
Так же в атомате запустилась ребалансировка и проблем с запросами не было. Можно сделать вывод, что кластер в случае отключения однй из нод при должной настройке не потеряет в произвоительности и не допустит потери данных, т.к. произойдет дополнительное реплицирование.
