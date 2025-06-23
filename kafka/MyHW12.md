### Kafka

#### Установка в Docker
[docker-compose](docker-compose.yml)
```
daemom@OVMCOUCH:/usr/src/kafka$ sudo docker compose -f docker-compose.yml  up -d
WARN[0000] /usr/src/kafka/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion
[+] Running 36/36
 ✔ kafka-ui Pulled                                                                                                                                                                            453.3s
 ✔ zookeeper Pulled                                                                                                                                                                           426.0s
 ✔ kafka Pulled                                                                                                                                                                               571.9s
[+] Running 4/4
 ✔ Network kafka_local-kafka  Created                                                                                                                                                           0.3s
 ✔ Container zookeeper        Started                                                                                                                                                          17.9s
 ✔ Container kafka            Started                                                                                                                                                           2.1s
 ✔ Container kafka-ui         Started                                                                                                                                                           3.4s
daemom@OVMCOUCH:/usr/src/kafka$ sudo docker ps
CONTAINER ID   IMAGE                              COMMAND                  CREATED          STATUS          PORTS                                                                                      NAMES
c6808afb2d41   provectuslabs/kafka-ui:latest      "/bin/sh -c 'java --…"   36 seconds ago   Up 33 seconds   0.0.0.0:8082->8080/tcp, [::]:8082->8080/tcp                                                kafka-ui
5c98cd8e9fcc   confluentinc/cp-server:7.5.0       "/etc/confluent/dock…"   36 seconds ago   Up 34 seconds   0.0.0.0:9092->9092/tcp, [::]:9092->9092/tcp, 0.0.0.0:9997->9997/tcp, [::]:9997->9997/tcp   kafka
0faa4783a86b   confluentinc/cp-zookeeper:latest   "/etc/confluent/dock…"   53 seconds ago   Up 35 seconds   2888/tcp, 0.0.0.0:2181->2181/tcp, [::]:2181->2181/tcp, 3888/tcp                            zookeeper
```

#### Создание топика и отправка сообщений через kafka-producer
```
[root@kafka appuser]# kafka-topics --create --topic test --bootstrap-server localhost:9092
Created topic test.


[root@kafka appuser]# kafka-console-producer --topic test --bootstrap-server localhost:9092
>message1
>message2
```
![Python](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/kafka/kafka_send.JPG?raw=true)
#### Чтением сообщений через kafka-consumer
```
>[root@kafka appuser]# kafka-console-consumer --topic test --from-beginning -\-bootstrap-server localhost:9092
message1
message2
```
![Python](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/kafka/kafka_rcv.JPG?raw=true)
#### Отправка и получение сообщений с использованием Python
[Python-код](kafka_main.py)   
Результать работы скрипта:   
![Python](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/kafka/kafka_pytnon.JPG?raw=true)

