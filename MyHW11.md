### Elasticsearch
#### Установка ES в Docker:

```
daemom@OVMCOUCH:~$ curl -O -L "https://github.com/sigstore/cosign/releases/latest/download/cosign-linux-amd64"
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:--  0:00:02 --:--:--     0
  0     0    0     0    0     0      0      0 --:--:--  0:00:02 --:--:--     0
100  126M  100  126M    0     0  63771      0  0:34:38  0:34:38 --:--:-- 88450
daemom@OVMCOUCH:~$ sudo mv cosign-linux-amd64 /usr/local/bin/cosign
[sudo] password for daemom:
daemom@OVMCOUCH:~$ sudo chmod +x /usr/local/bin/cosign
daemom@OVMCOUCH:~$ wget https://artifacts.elastic.co/cosign.pub
--2025-06-20 20:10:17--  https://artifacts.elastic.co/cosign.pub
ch:9.0.0Resolving artifacts.elastic.co (artifacts.elastic.co)... 34.120.127.130, 2600:1901:0:1d7::
Connecting to artifacts.elastic.co (artifacts.elastic.co)|34.120.127.130|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 178 [application/x-mspublisher]
Saving to: ‘cosign.pub.1’

cosign.pub.1                                      100%[==========================================================================================================>]     178  --.-KB/s    in 0s

2025-06-20 20:10:18 (33.7 MB/s) - ‘cosign.pub.1’ saved [178/178]

daemom@OVMCOUCH:~$ cosign verify --key cosign.pub docker.elastic.co/elasticsearch/elasticsearch:9.0.0

Verification for docker.elastic.co/elasticsearch/elasticsearch:9.0.0 --
The following checks were performed on each of these signatures:
  - The cosign claims were validated
  - Existence of the claims in the transparency log was verified offline
  - The signatures were verified against the specified public key 

daemom@OVMCOUCH:~$ sudo docker run --name es01 --net elastic -p 9200:9200 -it -m 1GB docker.elastic.co/elasticsearch/elasticsearch:9.0.0
Unable to find image 'docker.elastic.co/elasticsearch/elasticsearch:9.0.0' locally
9.0.0: Pulling from elasticsearch/elasticsearch
2177df6171a1: Pull complete
f27163823ee0: Pull complete
81fc6b832e3e: Pull complete
d0ccef208de1: Pull complete
4ca545ee6d5d: Pull complete
65c8acd9a8cb: Pull complete
999b049e9e35: Pull complete
32b8ad7318a1: Pull complete
ed59f12c1fbb: Pull complete
a40a4e423e41: Pull complete
e09b96420d70: Pull complete
Digest: sha256:5856b2c77263336792b80fc0e03df42922b2f86a816a4daf23397fb02ef7b138
Status: Downloaded newer image for docker.elastic.co/elasticsearch/elasticsearch:9.0.0

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Elasticsearch security features have been automatically configured!
✅ Authentication is enabled and cluster connections are encrypted.

daemom@OVMCOUCH:/usr/src/neo4j$ sudo docker ps
[sudo] password for daemom:
CONTAINER ID   IMAGE                                                 COMMAND                  CREATED         STATUS         PORTS                                                                                                NAMES
1ffe4f5f669a   docker.elastic.co/elasticsearch/elasticsearch:9.0.0   "/bin/tini -- /usr/l…"   3 minutes ago   Up 3 minutes   0.0.0.0:9200->9200/tcp, [::]:9200->9200/tcp, 9300/tcp                                                es01
```

### Создаем структуру:  

```

[root@1ffe4f5f669a certs]# curl -X PUT "https://elastic:*yajrsbiDbr4qKsbq1Di@localhost:9200/myindex" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "text": { "type": "text" } // Индексы типа string не поддержваются в новых версиях, поэтому заменил на text.
    }
  }
}'

[root@1ffe4f5f669a certs]# curl -X GET 'https://elastic:*yajrsbiDbr4qKsbq1Di@localhost:9200/_cat/indices?v'
health status index   uuid                   pri rep docs.count docs.deleted store.size pri.store.size dataset.size
yellow open   myindex G_jB5JLQQem5WTjOIfqzmg   1   1          0            0       227b           227b         227b



# Документ №1
curl -X POST "https://elastic:*yajrsbiDbr4qKsbq1Di@localhost:9200/myindex/_doc/1" -H 'Content-Type: application/json' -d'
{"text":"моя мама мыла посуду а кот жевал сосиски"}'

# Документ №2
curl -X POST "https://elastic:*yajrsbiDbr4qKsbq1Di@localhost:9200/myindex/_doc/2" -H 'Content-Type: application/json' -d'
{"text":"рама была отмыта и вылизана котом"}'

# Документ №3
curl -X POST "https://elastic:*yajrsbiDbr4qKsbq1Di@localhost:9200/myindex/_doc/3" -H 'Content-Type: application/json' -d'
{"text":"мама мыла раму"}'



fuzzy search для сопоставления близкой строки:


curl -X GET "https://elastic:*yajrsbiDbr4qKsbq1Di@localhost:9200/myindex/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "fuzzy": {
      "text": {"value": "мама ела сосиски"}
    }
  }
}'
```
### Экспорт в Postman
[JSON-файл](ESC.postman_collection.json)
