### S3-Minio

#### Установка в Docker
Пробросили порты и установили пароль для admin
```
daemom@OVMCOUCH:~$ sudo docker run -p 9000:9000 -p 9001:9001 --name minio -v ~/usr/src/minio:/data -e "MINIO_ROOT_USER=admin" -e "MINIO_ROOT_PASSWORD=password123"  minio/minio server --console-address ":9001" /data

INFO: WARNING: MINIO_ACCESS_KEY and MINIO_SECRET_KEY are deprecated.
         Please use MINIO_ROOT_USER and MINIO_ROOT_PASSWORD
MinIO Object Storage Server
Copyright: 2015-2025 MinIO, Inc.
License: GNU AGPLv3 - https://www.gnu.org/licenses/agpl-3.0.html
Version: RELEASE.2025-06-13T11-33-47Z (go1.24.4 linux/amd64)

API: http://172.17.0.3:9000  http://127.0.0.1:9000
WebUI: http://172.17.0.3:9001 http://127.0.0.1:9001

Docs: https://docs.min.io
```
#### Работа в WebAPI

Создаем бакет:   
![API_BACKET](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/minio/apibacket.JPG?raw=true)
Загружаем файл:   
![API_FILE1](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/minio/apifile.JPG?raw=true)
![API_FILE2](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/minio/apifile2.JPG?raw=true)
#### Работа через Python
Исходный код:
[PYTHON-файл](minio/main.py)   
Реузльтат отработки скрипта:   
![PYTHON](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/minio/pythonbacket.JPG?raw=true)
