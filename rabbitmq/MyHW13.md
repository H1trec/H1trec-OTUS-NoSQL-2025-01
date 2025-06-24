### RabbitMQ

#### Установка в Docker
```
daemom@OVMCOUCH:/usr/src/rabbitmq$ sudo docker compose -f docker-compose.yml  up -d
WARN[0000] /usr/src/rabbitmq/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion
[+] Running 11/11
 ✔ rabbitmq Pulled                                                                                                                                                                                                           39.9s
   ✔ d9d352c11bbd Pull complete                                                                                                                                                                                              28.4s
   ✔ d19a4db29034 Pull complete                                                                                                                                                                                              33.9s
   ✔ a5ef8534c749 Pull complete                                                                                                                                                                                              34.5s
   ✔ cded84d26f3b Pull complete                                                                                                                                                                                              34.6s
   ✔ 043ce8dc74f7 Pull complete                                                                                                                                                                                              36.0s
   ✔ a84ca2415d3c Pull complete                                                                                                                                                                                              36.1s
   ✔ f4c2d31994d1 Pull complete                                                                                                                                                                                              36.2s
   ✔ 5a8da38dcd6a Pull complete                                                                                                                                                                                              36.3s
   ✔ d79093ee6e39 Pull complete                                                                                                                                                                                              36.4s
   ✔ 0d5ff8ef488e Pull complete                                                                                                                                                                                              37.4s
[+] Running 2/2
 ✔ Network rabbitmq_default       Created                                                                                                                                                                                     0.3s
 ✔ Container rabbitmq-rabbitmq-1  Started                                                                                                                                                                                    10.1s
CONTAINER ID   IMAGE                   COMMAND                  CREATED          STATUS         PORTS                                                                                                                                                     NAMES
873eb7667c6b   rabbitmq:4-management   "docker-entrypoint.s…"   10 seconds ago   Up 7 seconds   4369/tcp, 5671/tcp, 0.0.0.0:5672->5672/tcp, [::]:5672->5672/tcp, 15671/tcp, 15691-15692/tcp, 25672/tcp, 0.0.0.0:15672->15672/tcp, [::]:15672->15672/tcp   rabbitmq-rabbitmq-1
```

#### Отправка сообщений в GUI

#### Отправка сообщений через Python
