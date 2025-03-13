## MongoDB

### Установка MongoDB

При установке на виртиуальную машину столкнулся с проблемой, что новые версии MongoDB требуют поддержку AVX, которо у меня нет. Поэтому устновил последнюю версию, которая работает без этой поддержки: 4.4.18:
```
daemom@OVMMNG:~$ curl -fsSL https://pgp.mongodb.com/server-7.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
daemom@OVMMNG:~$ sudo apt update
daemom@OVMMNG:~$ sudo apt-get install mongodb-org=4.4.18 mongodb-org-server=4.4.18 mongodb-org-shell=4.4.18 mongodb-org-mongos=4.4.18 mongodb-org-tools=4.4.18
```
Проверяем:
```
daemom@OVMMNG:~$ mongod --version
db version v4.4.18
Build Info: {
    "version": "4.4.18",
    "gitVersion": "8ed32b5c2c68ebe7f8ae2ebe8d23f36037a17dea",
    "openSSLVersion": "OpenSSL 1.1.1f  31 Mar 2020",
    "modules": [],
    "allocator": "tcmalloc",
    "environment": {
        "distmod": "ubuntu2004",
        "distarch": "x86_64",
        "target_arch": "x86_64"
    }
}
```
```
daemom@OVMMNG:~$ sudo service mongod status
● mongod.service - MongoDB Database Server
     Loaded: loaded (/usr/lib/systemd/system/mongod.service; disabled; preset: enabled)
     Active: active (running) since Thu 2025-03-13 12:17:19 UTC; 4s ago
 Invocation: 2a897fc741b543358ce0f23fb40c6ea3
       Docs: https://docs.mongodb.org/manual
   Main PID: 28742 (mongod)
     Memory: 157.4M (peak: 250.3M)
        CPU: 1.582s
     CGroup: /system.slice/mongod.service
             └─28742 /usr/bin/mongod --config /etc/mongod.conf

Mar 13 12:17:19 OVMMNG systemd[1]: Started mongod.service - MongoDB Database Server.
```
### Загрузка данных:

В качестве данных я использовал набор: https://github.com/ivylabs/mongodb-databases-sample.
```
daemom@OVMMNG:~$ git clone https://github.com/ivylabs/mongodb-databases-sample.git
Cloning into 'mongodb-databases-sample'...
remote: Enumerating objects: 58, done.
remote: Total 58 (delta 0), reused 0 (delta 0), pack-reused 58 (from 1)
Receiving objects: 100% (58/58), 7.25 MiB | 3.37 MiB/s, done.
Resolving deltas: 100% (22/22), done.
daemom@OVMMNG:~$ cd mongodb-databases-sample
sudo mongorestore --host=127.0.0.1 --port=27017  foodmart/MainTables-to-collections/
2025-03-13T18:25:00.632+0000    328035 document(s) restored successfully. 0 document(s) failed to restore.
```

### Выборка данных:  

Переходим в бд:
```
> use foodmart;
switched to db foodmart
```
Первая выборка:
```
> db.category.find();
{ "_id" : ObjectId("53c7c973ccf26e6de850ba3d"), "category_id" : "ACTUAL", "category_description" : "Current Year's Actuals" }
{ "_id" : ObjectId("53c7c973ccf26e6de850ba3e"), "category_id" : "ADJUSTMENT", "category_description" : "Adjustment for Budget input" }
{ "_id" : ObjectId("53c7c973ccf26e6de850ba3f"), "category_id" : "BUDGET", "category_description" : "Current Year's Budget" }
{ "_id" : ObjectId("53c7c973ccf26e6de850ba40"), "category_id" : "FORECAST", "category_description" : "Forecast" }
```
Вторая выборка:
```
> db.department.find();
{ "_id" : ObjectId("53c7c972ccf26e6de850ba1a"), "department_id" : NumberLong(1), "department_description" : "HQ General Management" }
{ "_id" : ObjectId("53c7c972ccf26e6de850ba1c"), "department_id" : NumberLong(2), "department_description" : "HQ Information Systems" }
{ "_id" : ObjectId("53c7c972ccf26e6de850ba1e"), "department_id" : NumberLong(3), "department_description" : "HQ Marketing" }
{ "_id" : ObjectId("53c7c972ccf26e6de850ba20"), "department_id" : NumberLong(4), "department_description" : "HQ Human Resources" }
{ "_id" : ObjectId("53c7c972ccf26e6de850ba22"), "department_id" : NumberLong(5), "department_description" : "HQ Finance and Accounting" }
{ "_id" : ObjectId("53c7c972ccf26e6de850ba24"), "department_id" : NumberLong(11), "department_description" : "Store Management" }
{ "_id" : ObjectId("53c7c972ccf26e6de850ba25"), "department_id" : NumberLong(14), "department_description" : "Store Information Systems" }
{ "_id" : ObjectId("53c7c972ccf26e6de850ba26"), "department_id" : NumberLong(15), "department_description" : "Store Permanent Checkers" }
{ "_id" : ObjectId("53c7c972ccf26e6de850ba27"), "department_id" : NumberLong(16), "department_description" : "Store Temporary Checkers" }
{ "_id" : ObjectId("53c7c972ccf26e6de850ba28"), "department_id" : NumberLong(17), "department_description" : "Store Permanent Stockers" }
{ "_id" : ObjectId("53c7c972ccf26e6de850ba29"), "department_id" : NumberLong(18), "department_description" : "Store Temporary Stockers" }
{ "_id" : ObjectId("53c7c972ccf26e6de850ba2a"), "department_id" : NumberLong(19), "department_description" : "Store Permanent Butchers" }
```
Третья выборка:
```
> db.department.find({department_description:'Store Information Systems'});
{ "_id" : ObjectId("53c7c972ccf26e6de850ba25"), "department_id" : NumberLong(14), "department_description" : "Store Information Systems" }
```

### Изменение данных:  

Смотрим что есть:  
```
> db.warehouse_class.find();
{ "_id" : ObjectId("53c7c972ccf26e6de850ba19"), "warehouse_class_id" : NumberLong(1), "description" : "Small Independent" }
{ "_id" : ObjectId("53c7c972ccf26e6de850ba1b"), "warehouse_class_id" : NumberLong(2), "description" : "Medium Independent" }
{ "_id" : ObjectId("53c7c972ccf26e6de850ba1d"), "warehouse_class_id" : NumberLong(3), "description" : "Large Independent" }
{ "_id" : ObjectId("53c7c972ccf26e6de850ba1f"), "warehouse_class_id" : NumberLong(4), "description" : "Small Owned" }
{ "_id" : ObjectId("53c7c972ccf26e6de850ba21"), "warehouse_class_id" : NumberLong(5), "description" : "Medium Owned" }
{ "_id" : ObjectId("53c7c972ccf26e6de850ba23"), "warehouse_class_id" : NumberLong(6), "description" : "Large Owned" }
```
Меняем:  
```
> db.warehouse_class.updateOne({ warehouse_class_id: 4 }, { $set: { description: "Super Small"} });
{ "acknowledged" : true, "matchedCount" : 1, "modifiedCount" : 1 }
```
Проверяем:
```
> db.warehouse_class.find({ warehouse_class_id: 4 });
{ "_id" : ObjectId("53c7c972ccf26e6de850ba1f"), "warehouse_class_id" : NumberLong(4), "description" : "Super Small" }
```
