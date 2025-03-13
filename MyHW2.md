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
