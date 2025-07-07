### Nosql в Яндекс облаке

#### Развертывание кластера Clickhouse 

![PLAN_BEFORE](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/cloud/create.JPG?raw=true)

В качетсве примера данных взята статистика по Covid19. Файл был скачен с открытого ресурса и предварительно загружен в Object Storage.
Создаем таблицу:

![PLAN_BEFORE](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/cloud/table1.JPG?raw=true)

Вставляем данные:

![PLAN_BEFORE](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/cloud/ins1.JPG?raw=true)

#### Выполняем запросы:  
Смотрим общее количество записей:
![PLAN_BEFORE](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/cloud/q1.JPG?raw=true)
![PLAN_BEFORE](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/cloud/q1t.JPG?raw=true)
Смотрим, сколько всего случаев Covid-19 было зафиксировано:
![PLAN_BEFORE](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/cloud/q2.JPG?raw=true)
![PLAN_BEFORE](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/cloud/q2t.JPG?raw=true)
Вычисляем процент изменения новых случаев каждый день и включает простой столбец increase или decrease в результирующий набор:
![PLAN_BEFORE](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/cloud/q3.JPG?raw=true)
![PLAN_BEFORE](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/cloud/q3t.JPG?raw=true)

Запросы по довольно большому объему данных отрабатывают очень быстро.
