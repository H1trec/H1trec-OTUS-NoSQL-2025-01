### Cassandra

#### Установка в Docker

Доке на моей VM уже был установлен. Поднимаем Cassandra при помощи файла docker-compose.yml
```
daemom@OVMCOUCH:/usr/src/cas$ sudo docker compose up -d
```

Проверяем после установки:  
```
daemom@OVMCOUCH:/usr/src/cas$ sudo docker ps
CONTAINER ID   IMAGE              COMMAND                  CREATED          STATUS          PORTS                                         NAMES
18947ec6d3e9   cassandra:latest   "docker-entrypoint.s…"   12 seconds ago   Up 10 seconds   7000-7001/tcp, 7199/tcp, 9042/tcp, 9160/tcp   cas-cassandra2-1
99c71770380b   cassandra:latest   "docker-entrypoint.s…"   12 seconds ago   Up 10 seconds   7000-7001/tcp, 7199/tcp, 9042/tcp, 9160/tcp   cas-cassandra1-1
45e58b869dd6   cassandra:latest   "docker-entrypoint.s…"   15 seconds ago   Up 11 seconds   7000-7001/tcp, 7199/tcp, 9042/tcp, 9160/tcp   cas-cassandra-seed-1
a1527374afb0   zookeeper:latest   "/docker-entrypoint.…"   3 minutes ago    Up 3 minutes    2181/tcp, 2888/tcp, 3888/tcp, 8080/tcp        cas-zoo1-1
```

#### Работа с Cassandra

Создаем KEYSPACE:  
```
daemom@OVMCOUCH:/usr/src/cas$ sudo docker exec -ti cas-cassandra-seed-1 bash
root@45e58b869dd6:/# cqlsh
Connected to Test Cluster at 127.0.0.1:9042
[cqlsh 6.2.0 | Cassandra 5.0.4 | CQL spec 3.4.7 | Native protocol v5]
Use HELP for help.
cqlsh> CREATE KEYSPACE IF NOT EXISTS test WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '2' };
cqlsh> describe keyspaces;

system       system_distributed  system_traces  system_virtual_schema
system_auth  system_schema       system_views   test
cqlsh> use test;
cqlsh:test>
```

Создаем первую таблицу добавляем данные:
```
CREATE TABLE IF NOT EXISTS shopping_cart (
userid text PRIMARY KEY,
item_count int,
last_update_timestamp timestamp
);
INSERT INTO shopping_cart
(userid, item_count, last_update_timestamp)
VALUES ('9876', 2, toTimeStamp(now()));
INSERT INTO shopping_cart
(userid, item_count, last_update_timestamp)
VALUES ('1234', 5, toTimeStamp(now()));
INSERT INTO shopping_cart
(userid, item_count, last_update_timestamp)
VALUES ('1454', 7, toTimeStamp(now()));
INSERT INTO shopping_cart
(userid, item_count, last_update_timestamp)
VALUES ('1444', 9, toTimeStamp(now()));

cqlsh:test> SELECT * FROM shopping_cart;

 userid | item_count | last_update_timestamp
--------+------------+---------------------------------
   1444 |          9 | 2025-04-12 18:50:44.664000+0000
   1454 |          7 | 2025-04-12 18:50:42.337000+0000
   1234 |          5 | 2025-04-12 18:50:42.276000+0000
   9876 |          2 | 2025-04-12 18:50:42.182000+0000

(4 rows)
```

Создаем вторую таблицу с составным Partition key:
```
CREATE TABLE IF NOT EXISTS shopping_cart2 (
userid text,
item_count int,
date_created date,
last_update_timestamp timestamp,
PRIMARY KEY ((userid, date_created), last_update_timestamp)
);

INSERT INTO shopping_cart2
(userid, item_count, date_created, last_update_timestamp)
VALUES ('9876', 2, '2023-05-03', toTimeStamp(now()));
INSERT INTO shopping_cart2
(userid, item_count, date_created,  last_update_timestamp)
VALUES ('1234', 5, '2023-05-02', toTimeStamp(now()));
INSERT INTO shopping_cart2
(userid, item_count, date_created, last_update_timestamp)
VALUES ('1454', 7, '2023-05-03', toTimeStamp(now()));
INSERT INTO shopping_cart2
(userid, item_count, date_created,  last_update_timestamp)
VALUES ('1444', 9, '2023-05-02', toTimeStamp(now()));
cqlsh:test>  SELECT * FROM shopping_cart2;

 userid | date_created | last_update_timestamp           | item_count
--------+--------------+---------------------------------+------------
   1454 |   2023-05-03 | 2025-04-12 18:53:18.225000+0000 |          7
   1234 |   2023-05-02 | 2025-04-12 18:53:18.208000+0000 |          5
   9876 |   2023-05-03 | 2025-04-12 18:53:18.165000+0000 |          2
   1444 |   2023-05-02 | 2025-04-12 18:53:19.867000+0000 |          9

(4 rows)
```

Выполняем запросы WHERE:   
```
cqlsh:test> SELECT * FROM shopping_cart2 WHERE userid = '1234' AND date_created = '2023-05-02';

 userid | date_created | last_update_timestamp           | item_count
--------+--------------+---------------------------------+------------
   1234 |   2023-05-02 | 2025-04-12 18:53:18.208000+0000 |          5

(1 rows)


cqlsh:test> SELECT * FROM shopping_cart2 WHERE userid = '1234' AND date_created = '2023-05-02' AND last_update_timestamp > '2023-05-03 18:13:16.640000+0000';

 userid | date_created | last_update_timestamp           | item_count
--------+--------------+---------------------------------+------------
   1234 |   2023-05-02 | 2025-04-12 18:53:18.208000+0000 |          5

(1 rows)
```

Создаем индекс:  
```
cqlsh:test> CREATE INDEX idx1 ON test.shopping_cart (last_update_timestamp);
cqlsh:test>
```
