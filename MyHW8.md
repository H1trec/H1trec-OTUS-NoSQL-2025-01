#### Etcd

### Установка 
```
daemom@OVMCOUCH:/usr/src/etcd$ sudo docker compose -f docker_compose.yml  up -d
[+] Running 4/4
 ✔ etcd3 Pulled                                                                                                   24.4s
 ✔ etcd1 Pulled                                                                                                   24.4s
 ✔ etcd2 Pulled                                                                                                   24.4s
   ✔ a425929bf30e Pull complete                                                                                   20.6s
[+] Running 4/4
 ✔ Network etcd_default  Created                                                                                   0.3s
 ✔ Container etcd1       Started                                                                                   6.7s
 ✔ Container etcd2       Started                                                                                   6.7s
 ✔ Container etcd3       Started
```
### Тесирование

Проверка docker:
```
daemom@OVMCOUCH:/usr/src/etcd$ sudo docker ps
CONTAINER ID   IMAGE                 COMMAND                  CREATED         STATUS         PORTS                                                   NAMES
4109069695bd   bitnami/etcd:latest   "/opt/bitnami/script…"   3 minutes ago   Up 3 minutes   2380/tcp, 0.0.0.0:2382->2379/tcp, [::]:2382->2379/tcp   etcd2
a9cd5abe9feb   bitnami/etcd:latest   "/opt/bitnami/script…"   3 minutes ago   Up 3 minutes   2380/tcp, 0.0.0.0:2383->2379/tcp, [::]:2383->2379/tcp   etcd3
667b2643cb28   bitnami/etcd:latest   "/opt/bitnami/script…"   3 minutes ago   Up 3 minutes   2380/tcp, 0.0.0.0:2381->2379/tcp, [::]:2381->2379/tcp   etcd1
```

Проверка нод
```
daemom@OVMCOUCH:/usr/src/etcd$ sudo docker exec -it etcd1 bash
I have no name!@etcd1:/opt/bitnami/etcd$ ENDPOINTS=$(etcdctl member list | grep -o '[^ ]\+:2379' | paste -s -d,)
-endpoints=$ENDPOINTS -w tableI have no name!@etcd1:/opt/bitnami/etcd$ etcdctl endpoint status --endpoints=$ENDPOINTS -w table
+-------------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|     ENDPOINT      |        ID        | VERSION | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-------------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
| http://etcd1:2379 | ade526d28b1f92f7 |   3.6.1 |           3.6.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         2 |          8 |                  8 |        |                          |             false |
| http://etcd3:2379 | bd388e7810915853 |   3.6.1 |           3.6.0 |   20 kB |  16 kB |                   20% |   0 B |      true |      false |         2 |          8 |                  8 |        |                          |             false |
| http://etcd2:2379 | d282ac2ce600c1ce |   3.6.1 |           3.6.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         2 |          8 |                  8 |        |                          |             false |
+-------------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
I have no name!@etcd1:/opt/bitnami/etcd$
```
Видим, что мастер нодой назначена нода номер 3.

Остановим ноду номер 3 и посмотрим, что будет:   
```
daemom@OVMCOUCH:/usr/src/etcd$ sudo docker exec -it etcd1 bash
I have no name!@etcd1:/opt/bitnami/etcd$ ENDPOINTS=$(etcdctl member list | grep -o '[^ ]\+:2379' | paste -s -d,)
ints=$ENDPOINTS -w tableI have no name!@etcd1:/opt/bitnami/etcd$ etcdctl endpoint status --endpoints=$ENDPOINTS -w table
{"level":"warn","ts":"2025-06-17T18:17:06.532717Z","logger":"etcd-client","caller":"v3@v3.6.1/retry_interceptor.go:65","msg":"retrying of unary invoker failed","target":"etcd-endpoints://0xc00020f860/etcd3:2379","method":"/etcdserverpb.Maintenance/Status","attempt":0,"error":"rpc error: code = DeadlineExceeded desc = context deadline exceeded while waiting for connections to become ready"}
Failed to get the status of endpoint http://etcd3:2379 (context deadline exceeded)
+-------------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|     ENDPOINT      |        ID        | VERSION | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-------------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
| http://etcd1:2379 | ade526d28b1f92f7 |   3.6.1 |           3.6.0 |   20 kB |  16 kB |                   20% |   0 B |      true |      false |         3 |          9 |                  9 |        |                          |             false |
| http://etcd2:2379 | d282ac2ce600c1ce |   3.6.1 |           3.6.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         3 |          9 |                  9 |        |                          |             false |
+-------------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
```

Видим, что при проверке плучили ошибку при обращении к ноде номер и, и что теперь мастер нодой является нода номер 1.   

Запустим обратно ноду номер 3 и остановим ноду номер 1 и посмотрим результат:   
```
daemom@OVMCOUCH:/usr/src/etcd$ sudo docker start a9cd5abe9feb
a9cd5abe9feb
daemom@OVMCOUCH:/usr/src/etcd$ sudo docker stop 667b2643cb28
667b2643cb28
daemom@OVMCOUCH:/usr/src/etcd$ sudo docker exec -it etcd2 bash
I have no name!@etcd2:/opt/bitnami/etcd$ ENDPOINTS=$(etcdctl member list | grep -o '[^ ]\+:2379' | paste -s -d,)
ints=$ENDPOINTS -w tableI have no name!@etcd2:/opt/bitnami/etcd$ etcdctl endpoint status --endpoints=$ENDPOINTS -w table
{"level":"warn","ts":"2025-06-17T18:19:25.443884Z","logger":"etcd-client","caller":"v3@v3.6.1/retry_interceptor.go:65","msg":"retrying of unary invoker failed","target":"etcd-endpoints://0xc00020f4a0/etcd1:2379","method":"/etcdserverpb.Maintenance/Status","attempt":0,"error":"rpc error: code = DeadlineExceeded desc = context deadline exceeded while waiting for connections to become ready"}
Failed to get the status of endpoint http://etcd1:2379 (context deadline exceeded)
+-------------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|     ENDPOINT      |        ID        | VERSION | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-------------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
| http://etcd3:2379 | bd388e7810915853 |   3.6.1 |           3.6.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         4 |         12 |                 12 |        |                          |             false |
| http://etcd2:2379 | d282ac2ce600c1ce |   3.6.1 |           3.6.0 |   20 kB |  16 kB |                   20% |   0 B |      true |      false |         4 |         12 |                 12 |        |                          |             false |
+-------------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
```
Видим, что теперь мастер нодой нодой стала нода номер 2. 

Запусим обртано ноду номер 1.
```
daemom@OVMCOUCH:/usr/src/etcd$ sudo docker start 667b2643cb28
667b2643cb28
daemom@OVMCOUCH:/usr/src/etcd$ sudo docker exec -it etcd2 bash
I have no name!@etcd2:/opt/bitnami/etcd$ ENDPOINTS=$(etcdctl member list | grep -o '[^ ]\+:2379' | paste -s -d,)
ints=$ENDPOINTS -w tableI have no name!@etcd2:/opt/bitnami/etcd$ etcdctl endpoint status --endpoints=$ENDPOINTS -w table
+-------------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|     ENDPOINT      |        ID        | VERSION | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-------------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
| http://etcd1:2379 | ade526d28b1f92f7 |   3.6.1 |           3.6.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         4 |         14 |                 14 |        |                          |             false |
| http://etcd3:2379 | bd388e7810915853 |   3.6.1 |           3.6.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         4 |         14 |                 14 |        |                          |             false |
| http://etcd2:2379 | d282ac2ce600c1ce |   3.6.1 |           3.6.0 |   20 kB |  16 kB |                   20% |   0 B |      true |      false |         4 |         14 |                 14 |        |                          |             false |
+-------------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
```
Видим, что все ноды работают и мастер нодой осталась нода номер 2.

#### Consul

Установка:  
```
daemom@OVMCOUCH:/usr/src/consul$ sudo docker compose -f docker-compose.yml  up -d
WARN[0000] /usr/src/consul/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion
WARN[0000] Found orphan containers ([consul-consul2-1 consul-consul3-1 consul-consul1-1]) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up.
[+] Running 4/4
 ✔ Container consul-server1  Started                                                                                                                                                                                                    3.8s
 ✔ Container consul-server2  Started                                                                                                                                                                                                    3.4s
 ✔ Container consul-server3  Started                                                                                                                                                                                                    2.8s
 ✔ Container consul-server4  Started                                                                                                                                                                                                    3.1s
```
 Проверка:
```
daemom@OVMCOUCH:/usr/src/consul$ sudo docker ps
CONTAINER ID   IMAGE                     COMMAND                  CREATED         STATUS         PORTS                                                                                                                                                                 NAMES
6c527cf697ab   hashicorp/consul:1.14.3   "docker-entrypoint.s…"   9 seconds ago   Up 7 seconds   8300-8302/tcp, 8500/tcp, 8301-8302/udp, 8600/tcp, 8600/udp                                                                                                            consul-server3
2df4b909cee1   hashicorp/consul:1.14.3   "docker-entrypoint.s…"   9 seconds ago   Up 7 seconds   8300-8302/tcp, 8500/tcp, 8301-8302/udp, 8600/tcp, 8600/udp                                                                                                            consul-server2
be96b5c8952c   hashicorp/consul:1.14.3   "docker-entrypoint.s…"   9 seconds ago   Up 7 seconds   8300-8302/tcp, 8500/tcp, 8301-8302/udp, 8600/tcp, 8600/udp                                                                                                            consul-server4
950398083a13   hashicorp/consul:1.14.3   "docker-entrypoint.s…"   9 seconds ago   Up 7 seconds   0.0.0.0:8500->8500/tcp, [::]:8500->8500/tcp, 8300-8302/tcp, 8301-8302/udp, 0.0.0.0:8600->8600/tcp, [::]:8600->8600/tcp, 0.0.0.0:8600->8600/udp, [::]:8600->8600/udp   consul-server1
```

```
/consul/config # consul members
Node            Address          Status  Type    Build   Protocol  DC   Partition  Segment
consul-server1  172.25.0.2:8301  alive   server  1.14.3  2         dc1  default    <all>
consul-server2  172.25.0.5:8301  alive   server  1.14.3  2         dc1  default    <all>
consul-server3  172.25.0.3:8301  alive   server  1.14.3  2         dc1  default    <all>
```

К сожален, не смог настроить ACL:   
Добавлял на все ноды конфигурацию:
```
acl = {
    enabled = true
    default_policy = "deny"
    enable_token_persistence = true
}
```
На все взможные настройки получал ошибку:
```
/etc/consul.d # consul acl bootstrap
Failed ACL bootstrapping: Unexpected response code: 401 (ACL support disabled)
```
