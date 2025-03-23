## MongoDB 2

### Настройка стенда:
Установил в docker кластер:
```
daemom@OVMMNG:/usr/src/mongodb$ sudo docker ps
CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS          PORTS                                                      NAMES
4d95c72185ed   mongo:4.4.18   "docker-entrypoint.s…"   58 seconds ago   Up 38 seconds   27017/tcp, 0.0.0.0:40001->40001/tcp, :::40001->40001/tcp   mongo-configsvr-1
54f5e1733bab   mongo:4.4.18   "docker-entrypoint.s…"   58 seconds ago   Up 45 seconds   27017/tcp, 0.0.0.0:40011->40011/tcp, :::40011->40011/tcp   mongo-shard-1-rs-1
2a8ab654572a   mongo:4.4.18   "docker-entrypoint.s…"   58 seconds ago   Up 43 seconds   27017/tcp, 0.0.0.0:40022->40022/tcp, :::40022->40022/tcp   mongo-shard-2-rs-2
98d22eb910de   mongo:4.4.18   "docker-entrypoint.s…"   58 seconds ago   Up 32 seconds   27017/tcp, 0.0.0.0:40012->40012/tcp, :::40012->40012/tcp   mongo-shard-1-rs-2
59bf34472424   mongo:4.4.18   "docker-entrypoint.s…"   58 seconds ago   Up 34 seconds   27017/tcp, 0.0.0.0:40023->40023/tcp, :::40023->40023/tcp   mongo-shard-2-rs-3
b527555e87a4   mongo:4.4.18   "docker-entrypoint.s…"   58 seconds ago   Up 46 seconds   27017/tcp, 0.0.0.0:40013->40013/tcp, :::40013->40013/tcp   mongo-shard-1-rs-3
23739f422047   mongo:4.4.18   "docker-entrypoint.s…"   58 seconds ago   Up 40 seconds   0.0.0.0:40100->27017/tcp, :::40100->27017/tcp              mongos-shard
f4d147fe1dfe   mongo:4.4.18   "docker-entrypoint.s…"   58 seconds ago   Up 32 seconds   27017/tcp, 0.0.0.0:40021->40021/tcp, :::40021->40021/tcp   mongo-shard-2-rs-1
7ca11feb2053   mongo:4.4.18   "docker-entrypoint.s…"   58 seconds ago   Up 44 seconds   27017/tcp, 0.0.0.0:40003->40003/tcp, :::40003->40003/tcp   mongo-configsvr-3
334e2e1ca162   mongo:4.4.18   "docker-entrypoint.s…"   58 seconds ago   Up 34 seconds   27017/tcp, 0.0.0.0:40002->40002/tcp, :::40002->40002/tcp   mongo-configsvr-2
```
Настройка:
```
daemom@OVMMNG:/usr/src/mongodb$ mongosh --port 40001
rs.initiate({
figsvr-3:40003" }
  ]
...   "_id" : "config-replica-set",
...   members : [
...     {"_id" : 0, host : "mongo-configsvr-1:40001"},
...     {"_id" : 1, host : "mongo-configsvr-2:40002"},
...     {"_id" : 2, host : "mongo-configsvr-3:40003" }
...   ]
... });
{
  ok: 1,
  '$gleStats': {
    lastOpTime: Timestamp({ t: 1742737183, i: 1 }),
    electionId: ObjectId('000000000000000000000000')
  },
  lastCommittedOpTime: Timestamp({ t: 0, i: 0 })
}
```
```
daemom@OVMMNG:/usr/src/mongodb$ mongosh --port 40011
test> rs.initiate({
...   "_id" : "shard-replica-set-1",
...   members : [
...     {"_id" : 0, host : "mongo-shard-1-rs-1:40011"},
...     {"_id" : 1, host : "mongo-shard-1-rs-2:40012"},
...     {"_id" : 2, host : "mongo-shard-1-rs-3:40013" }
...   ]
... });
{ ok: 1 }
```
```
daemom@OVMMNG:/usr/src/mongodb$ mongosh --port 40021
test> rs.initiate({
...   "_id" : "shard-replica-set-2",
...   members : [
...     {"_id" : 0, host : "mongo-shard-2-rs-1:40021"},
...     {"_id" : 1, host : "mongo-shard-2-rs-2:40022"},
...     {"_id" : 2, host : "mongo-shard-2-rs-3:40023" }
...   ]
... });
{ ok: 1 }
```
```
root@mongos-shard:/# mongo
mongos> sh.addShard("shard-replica-set-1/mongo-shard-1-rs-1:40011,mongo-shard-1-rs-2:40012,mongo-shard-1-rs-3:40013")
{
        "shardAdded" : "shard-replica-set-1",
        "ok" : 1,
        "operationTime" : Timestamp(1742737810, 4),
        "$clusterTime" : {
                "clusterTime" : Timestamp(1742737810, 4),
                "signature" : {
                        "hash" : BinData(0,"AAAAAAAAAAAAAAAAAAAAAAAAAAA="),
                        "keyId" : NumberLong(0)
                }
        }
}
mongos> sh.addShard("shard-replica-set-2/mongo-shard-2-rs-1:40021,mongo-shard-2-rs-2:40022,mongo-shard-2-rs-3:40023")
{
        "shardAdded" : "shard-replica-set-2",
        "ok" : 1,
        "operationTime" : Timestamp(1742738007, 3),
        "$clusterTime" : {
                "clusterTime" : Timestamp(1742738007, 3),
                "signature" : {
                        "hash" : BinData(0,"AAAAAAAAAAAAAAAAAAAAAAAAAAA="),
                        "keyId" : NumberLong(0)
                }
        }
}
```
```
mongos> sh.status()
--- Sharding Status ---
  sharding version: {
        "_id" : 1,
        "minCompatibleVersion" : 5,
        "currentVersion" : 6,
        "clusterId" : ObjectId("67e00f2b8ad1a7f6cabe46ca")
  }
  shards:
        {  "_id" : "shard-replica-set-1",  "host" : "shard-replica-set-1/mongo-shard-1-rs-1:40011,mongo-shard-1-rs-2:40012,mongo-shard-1-rs-3:40013",  "state" : 1 }
        {  "_id" : "shard-replica-set-2",  "host" : "shard-replica-set-2/mongo-shard-2-rs-1:40021,mongo-shard-2-rs-2:40022,mongo-shard-2-rs-3:40023",  "state" : 1 }
  active mongoses:
        "4.4.18" : 1
  autosplit:
        Currently enabled: yes
  balancer:
        Currently enabled:  yes
        Currently running:  yes
        Collections with active migrations:
                config.system.sessions started at Sun Mar 23 2025 14:25:17 GMT+0000 (UTC)
        Failed balancer rounds in last 5 attempts:  0
        Migration Results for the last 24 hours:
                456 : Success
  databases:
        {  "_id" : "config",  "primary" : "config",  "partitioned" : true }
                config.system.sessions
                        shard key: { "_id" : 1 }
                        unique: false
                        balancing: true
                        chunks:
                                shard-replica-set-1     568
                                shard-replica-set-2     456
                        too many chunks to print, use verbose if you want to force print
```
Создаем индекс:
```
mongos> db.tickets.createIndex({amount:1})
{
        "raw" : {
                "shard-replica-set-2/mongo-shard-2-rs-1:40021,mongo-shard-2-rs-2:40022,mongo-shard-2-rs-3:40023" : {
                        "createdCollectionAutomatically" : false,
                        "numIndexesBefore" : 1,
                        "numIndexesAfter" : 2,
                        "commitQuorum" : "votingMembers",
                        "ok" : 1
                }
        },
        "ok" : 1,
        "operationTime" : Timestamp(1742746025, 5),
        "$clusterTime" : {
                "clusterTime" : Timestamp(1742746025, 5),
                "signature" : {
                        "hash" : BinData(0,"AAAAAAAAAAAAAAAAAAAAAAAAAAA="),
                        "keyId" : NumberLong(0)
                }
        }
}
```
#### Делаем шардирование:
```
mongos> use admin
switched to db admin
mongos> db.runCommand({shardCllection: "test:tickets", key: {amount: 1}})
{
        "ok" : 0,
        "errmsg" : "no such cmd: shardCllection",
        "code" : 59,
        "codeName" : "CommandNotFound",
        "operationTime" : Timestamp(1742746327, 1),
        "$clusterTime" : {
                "clusterTime" : Timestamp(1742746327, 1),
                "signature" : {
                        "hash" : BinData(0,"AAAAAAAAAAAAAAAAAAAAAAAAAAA="),
                        "keyId" : NumberLong(0)
                }
        }
}
```
Процесс шардирования:
```
mongos> db.tickets.getShardDistribution()

Shard shard-replica-set-2 at shard-replica-set-2/mongo-shard-2-rs-1:40021,mongo-shard-2-rs-2:40022,mongo-shard-2-rs-3:40023
 data : 67.7MiB docs : 1000000 chunks : 6
 estimated data per chunk : 11.28MiB
 estimated docs per chunk : 166666

Shard shard-replica-set-1 at shard-replica-set-1/mongo-shard-1-rs-1:40011,mongo-shard-1-rs-2:40012,mongo-shard-1-rs-3:40013
 data : 15.64MiB docs : 231090 chunks : 1
 estimated data per chunk : 15.64MiB
 estimated docs per chunk : 231090

Totals
 data : 83.35MiB docs : 1231090 chunks : 7
 Shard shard-replica-set-2 contains 81.22% data, 81.22% docs in cluster, avg obj size on shard : 71B
 Shard shard-replica-set-1 contains 18.77% data, 18.77% docs in cluster, avg obj size on shard : 71B
```
Остановим один инстанс:
```
daemom@OVMMNG:/usr/src/mongodb$ sudo docker stop mongo-shard-2-rs-1
mongo-shard-2-rs-1
```
Смотрим результат:
До:  
```
mongos> db.tickets.getShardDistribution()

Shard shard-replica-set-2 at shard-replica-set-2/mongo-shard-2-rs-1:40021,mongo-shard-2-rs-2:40022,mongo-shard-2-rs-3:40023
 data : 67.7MiB docs : 1000000 chunks : 4
 estimated data per chunk : 16.92MiB
 estimated docs per chunk : 250000

Shard shard-replica-set-1 at shard-replica-set-1/mongo-shard-1-rs-1:40011,mongo-shard-1-rs-2:40012,mongo-shard-1-rs-3:40013
 data : 29.84MiB docs : 440823 chunks : 3
 estimated data per chunk : 9.94MiB
 estimated docs per chunk : 146941

Totals
 data : 97.55MiB docs : 1440823 chunks : 7
 Shard shard-replica-set-2 contains 69.4% data, 69.4% docs in cluster, avg obj size on shard : 71B
 Shard shard-replica-set-1 contains 30.59% data, 30.59% docs in cluster, avg obj size on shard : 71B

mongos>
mongos> db.tickets.getShardDistribution()

Shard shard-replica-set-1 at shard-replica-set-1/mongo-shard-1-rs-1:40011,mongo-shard-1-rs-2:40012,mongo-shard-1-rs-3:40013
 data : 29.84MiB docs : 440823 chunks : 3
 estimated data per chunk : 9.94MiB
 estimated docs per chunk : 146941

Shard shard-replica-set-2 at shard-replica-set-2/mongo-shard-2-rs-1:40021,mongo-shard-2-rs-2:40022,mongo-shard-2-rs-3:40023
 data : 67.7MiB docs : 1000000 chunks : 4
 estimated data per chunk : 16.92MiB
 estimated docs per chunk : 250000

Totals
 data : 97.55MiB docs : 1440823 chunks : 7
 Shard shard-replica-set-1 contains 30.59% data, 30.59% docs in cluster, avg obj size on shard : 71B
 Shard shard-replica-set-2 contains 69.4% data, 69.4% docs in cluster, avg obj size on shard : 71B
```
После:  
```
mongos> db.tickets.getShardDistribution()

Shard shard-replica-set-1 at shard-replica-set-1/mongo-shard-1-rs-1:40011,mongo-shard-1-rs-2:40012,mongo-shard-1-rs-3:40013
 data : 29.84MiB docs : 440823 chunks : 3
 estimated data per chunk : 9.94MiB
 estimated docs per chunk : 146941

Shard shard-replica-set-2 at shard-replica-set-2/mongo-shard-2-rs-1:40021,mongo-shard-2-rs-2:40022,mongo-shard-2-rs-3:40023
 data : 67.7MiB docs : 1000000 chunks : 4
 estimated data per chunk : 16.92MiB
 estimated docs per chunk : 250000

Totals
 data : 97.55MiB docs : 1440823 chunks : 7
 Shard shard-replica-set-1 contains 30.59% data, 30.59% docs in cluster, avg obj size on shard : 71B
 Shard shard-replica-set-2 contains 69.4% data, 69.4% docs in cluster, avg obj size on shard : 71B
```
Запустим предыдущий, остановим другой:
```
daemom@OVMMNG:/usr/src/mongodb$ sudo docker start mongo-shard-2-rs-1
mongo-shard-2-rs-1
daemom@OVMMNG:/usr/src/mongodb$ sudo docker stop mongo-shard-1-rs-1
mongo-shard-1-rs-1
daemom@OVMMNG:/usr/src/mongodb$
```
Смотрим статус:
```
mongos> db.tickets.getShardDistribution()

Shard shard-replica-set-1 at shard-replica-set-1/mongo-shard-1-rs-1:40011,mongo-shard-1-rs-2:40012,mongo-shard-1-rs-3:40013
 data : 29.84MiB docs : 440823 chunks : 3
 estimated data per chunk : 9.94MiB
 estimated docs per chunk : 146941

Shard shard-replica-set-2 at shard-replica-set-2/mongo-shard-2-rs-1:40021,mongo-shard-2-rs-2:40022,mongo-shard-2-rs-3:40023
 data : 67.7MiB docs : 1000000 chunks : 4
 estimated data per chunk : 16.92MiB
 estimated docs per chunk : 250000

Totals
 data : 97.55MiB docs : 1440823 chunks : 7
 Shard shard-replica-set-1 contains 30.59% data, 30.59% docs in cluster, avg obj size on shard : 71B
 Shard shard-replica-set-2 contains 69.4% data, 69.4% docs in cluster, avg obj size on shard : 71B

mongos>
```
При падении происходит ребалансировка шардинга и процессов репликации,происходит голосавание, меняются master, secondary. Поэтому мы и видим новую картину при проверке статуса.

#### Аутентификация и многоролевой доступ

Создаем пользователя с правами root:
```
mongos> use admin
switched to db admin
mongos> db.createUser({
... user: "root",
... pwd: "strictRootPassword",
... roles: [
... { role: "root", db: "admin" }
... ]
... })
Successfully added user: {
        "user" : "root",
        "roles" : [
                {
                        "role" : "root",
                        "db" : "admin"
                }
        ]
}
```
Создадим роль и назначим ее пользователю:
```
mongos> db.createRole(
...  {
...  role: "superRoot",
...  privileges:[
...  { resource: {anyResource:true}, actions: ["anyAction"]}
...  ],
...  roles:[]
...  }
... )
mongos> db.createUser({
...  user: "companyDBA",
...  pwd: "strictSuperRootPassword",
...  roles: ["superRoot"]
... })
Successfully added user: { "user" : "companyDBA", "roles" : [ "superRoot" ] }
```
Включаем аутентификацию, перезапускаем сервис и пытаемя подключиться:
```
daemom@OVMMNG:~$ mongo -u root -p --authenticationDatabase admin
MongoDB shell version v4.4.18
Enter password:
```
Идет запрос пароля. Вводим пароль и попадем в БД:
```
connecting to: mongodb://127.0.0.1:27017/?authSource=admin&compressors=disabled&gssapiServiceName=mongodb
Implicit session: session { "id" : UUID("4bb07a65-53f8-489a-af29-cd8f7fb757ad") }
MongoDB server version: 4.4.18
```
```
