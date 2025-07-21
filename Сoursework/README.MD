### Курсовая работа на тему: "Реализация дашборда в Metabase на Clickhouse."

#### Устанавливаем ПО

Clickhouse:   
```
daemom@OVMCOUCH:~$ sudo docker run -d --name some-clickhouse-server --ulimit nofile=262144:262144 clickhouse
[sudo] password for daemom:
Sorry, try again.
[sudo] password for daemom:
Unable to find image 'clickhouse:latest' locally
latest: Pulling from library/clickhouse
e735f3a6b701: Pull complete
68a1637f5502: Pull complete
efa28bfd8b50: Pull complete
051903cc395d: Pull complete
aa7c59ac55a8: Pull complete
63680a0a1150: Pull complete
53eec9f329db: Pull complete
7fd515ee7547: Pull complete
Digest: sha256:0553b2a0694402f0ad9a61f38d138e8347386abfba6b6520985a20f50b6930ed
Status: Downloaded newer image for clickhouse:latest
b4589774f4107535c8ae769aec9d5f2f7521f95272a3dbfa792cb0baabfc8820
daemom@OVMCOUCH:~$
```
Metabase:   
```
daemom@OVMCOUCH:~$ sudo docker pull metabase/metabase:latest
latest: Pulling from metabase/metabase
f18232174bc9: Pull complete
f6cd406c8d97: Pull complete
74f6a226ed93: Pull complete
e6744199aa66: Pull complete
cda86626eeb3: Pull complete
ff48864822fd: Pull complete
4a52f63d8c93: Pull complete
Digest: sha256:fe6f407493d4afcfa13b9c8288ca4a870b5afa2fb482fb945b883ba1e40f96b0
Status: Downloaded newer image for metabase/metabase:latest
docker.io/metabase/metabase:latest
daemom@OVMCOUCH:~$ sudo docker run -d -p 3000:3000 --name metabase metabase/metabase
15ea96936eda9b0cf60e83a756cc3d0b56ffa070d187effcd4c5de8caa13a84b
```
Проверяем статус:
```
daemom@OVMCOUCH:~$ sudo docker ps
CONTAINER ID   IMAGE               COMMAND                  CREATED         STATUS          PORTS                                         NAMES
b4589774f410   clickhouse          "/entrypoint.sh"         3 minutes ago   Up 3 minutes    8123/tcp, 9000/tcp, 9009/tcp                  some-clickhouse-server
15ea96936eda   metabase/metabase   "/app/run_metabase.sh"   5 minutes ago   Up 5 minutes    0.0.0.0:3000->3000/tcp, [::]:3000->3000/tcp   metabase
```
Настраиваем общую сеть:   
```
daemom@OVMCOUCH:~$ sudo docker network create my_network
daemom@OVMCOUCH:~$ sudo docker network connect my_network some-clickhouse-server
daemom@OVMCOUCH:~$ sudo docker network connect my_network metabase
```

#### Данные для аналитики

Данные были взяты с открытого источника https://health.google.com/covid-19/open-data/    

##### Таблица epidemiology. 

Получаем информацию о столбцах:      
```
b4589774f410 :) DESCRIBE url(
    'https://storage.googleapis.com/covid19-open-data/v3/epidemiology.csv',
    'CSVWithNames'
);

DESCRIBE TABLE url('https://storage.googleapis.com/covid19-open-data/v3/epidemiology.csv', 'CSVWithNames')

Query id: eef6987b-d08f-4564-85ba-73b364e9b19c

    ┌─name─────────────────┬─type─────────────┬─default_type─┬─default_expression─┬─comment─┬─codec_expression─┬─ttl_expression─┐
 1. │ date                 │ Nullable(Date)   │              │                    │         │                  │                │
 2. │ location_key         │ Nullable(String) │              │                    │         │                  │                │
 3. │ new_confirmed        │ Nullable(Int64)  │              │                    │         │                  │                │
 4. │ new_deceased         │ Nullable(Int64)  │              │                    │         │                  │                │
 5. │ new_recovered        │ Nullable(Int64)  │              │                    │         │                  │                │
 6. │ new_tested           │ Nullable(Int64)  │              │                    │         │                  │                │
 7. │ cumulative_confirmed │ Nullable(Int64)  │              │                    │         │                  │                │
 8. │ cumulative_deceased  │ Nullable(Int64)  │              │                    │         │                  │                │
 9. │ cumulative_recovered │ Nullable(Int64)  │              │                    │         │                  │                │
10. │ cumulative_tested    │ Nullable(Int64)  │              │                    │         │                  │                │
    └──────────────────────┴──────────────────┴──────────────┴────────────────────┴─────────┴──────────────────┴────────────────┘

10 rows in set. Elapsed: 0.206 sec.

b4589774f410 :) SELECT *
FROM url('https://storage.googleapis.com/covid19-open-data/v3/epidemiology.csv')
LIMIT 10;

SELECT *
FROM url('https://storage.googleapis.com/covid19-open-data/v3/epidemiology.csv')
LIMIT 10

Query id: d1e22557-9ae1-48f4-9699-adb08807055a

    ┌───────date─┬─location_key─┬─new_confirmed─┬─new_deceased─┬─new_recovered─┬─new_tested─┬─cumulative_confirmed─┬─cumulative_deceased─┬─cumulative_recovered─┬─cumulative_tested─┐
 1. │ 2020-01-01 │ AD           │             0 │            0 │          ᴺᵁᴸᴸ │       ᴺᵁᴸᴸ │                    0 │                   0 │                 ᴺᵁᴸᴸ │              ᴺᵁᴸᴸ │
 2. │ 2020-01-02 │ AD           │             0 │            0 │          ᴺᵁᴸᴸ │       ᴺᵁᴸᴸ │                    0 │                   0 │                 ᴺᵁᴸᴸ │              ᴺᵁᴸᴸ │
 3. │ 2020-01-03 │ AD           │             0 │            0 │          ᴺᵁᴸᴸ │       ᴺᵁᴸᴸ │                    0 │                   0 │                 ᴺᵁᴸᴸ │              ᴺᵁᴸᴸ │
 4. │ 2020-01-04 │ AD           │             0 │            0 │          ᴺᵁᴸᴸ │       ᴺᵁᴸᴸ │                    0 │                   0 │                 ᴺᵁᴸᴸ │              ᴺᵁᴸᴸ │
 5. │ 2020-01-05 │ AD           │             0 │            0 │          ᴺᵁᴸᴸ │       ᴺᵁᴸᴸ │                    0 │                   0 │                 ᴺᵁᴸᴸ │              ᴺᵁᴸᴸ │
 6. │ 2020-01-06 │ AD           │             0 │            0 │          ᴺᵁᴸᴸ │       ᴺᵁᴸᴸ │                    0 │                   0 │                 ᴺᵁᴸᴸ │              ᴺᵁᴸᴸ │
 7. │ 2020-01-07 │ AD           │             0 │            0 │          ᴺᵁᴸᴸ │       ᴺᵁᴸᴸ │                    0 │                   0 │                 ᴺᵁᴸᴸ │              ᴺᵁᴸᴸ │
 8. │ 2020-01-08 │ AD           │             0 │            0 │          ᴺᵁᴸᴸ │       ᴺᵁᴸᴸ │                    0 │                   0 │                 ᴺᵁᴸᴸ │              ᴺᵁᴸᴸ │
 9. │ 2020-01-09 │ AD           │             0 │            0 │          ᴺᵁᴸᴸ │       ᴺᵁᴸᴸ │                    0 │                   0 │                 ᴺᵁᴸᴸ │              ᴺᵁᴸᴸ │
10. │ 2020-01-10 │ AD           │             0 │            0 │          ᴺᵁᴸᴸ │       ᴺᵁᴸᴸ │                    0 │                   0 │                 ᴺᵁᴸᴸ │              ᴺᵁᴸᴸ │
    └────────────┴──────────────┴───────────────┴──────────────┴───────────────┴────────────┴──────────────────────┴─────────────────────┴──────────────────────┴───────────────────┘

10 rows in set. Elapsed: 2.690 sec.
```

Создаем таблицу:   
```
CREATE TABLE epidemiology
(
    `date` Date,
    `location_key` LowCardinality(String),
    `new_confirmed` Int32,
    `new_deceased` Int32,
    `new_recovered` Int32,
    `new_tested` Int32,
    `cumulative_confirmed` Int32,
    `cumulative_deceased` Int32,
    `cumulative_recovered` Int32,
    `cumulative_tested` Int32
)
ENGINE = MergeTree
ORDER BY (location_key, date)

Query id: 20c41f5c-2f33-471a-9021-4a50abd727ce

Ok.

0 rows in set. Elapsed: 0.050 sec.
```

Загружаем данные:   
```
b4589774f410 :) INSERT INTO epidemiology
:-]    SELECT *
:-]    FROM
:-]       url(
:-]         'https://storage.googleapis.com/covid19-open-data/v3/epidemiology.csv',
:-]         CSVWithNames,
:-]         'date Date,
:-]         location_key LowCardinality(String),
:-]         new_confirmed Int32,
:-]         new_deceased Int32,
:-]         new_recovered Int32,
:-]         new_tested Int32,
:-]         cumulative_confirmed Int32,
:-]         cumulative_deceased Int32,
:-]         cumulative_recovered Int32,
:-]         cumulative_tested Int32'
:-]     );

INSERT INTO epidemiology SELECT *
FROM url('https://storage.googleapis.com/covid19-open-data/v3/epidemiology.csv', CSVWithNames, 'date Date,\n        location_key LowCardinality(String),\n        new_confirmed Int32,\n        new_deceased Int32,\n        new_recovered Int32,\n        new_tested Int32,\n        cumulative_confirmed Int32,\n        cumulative_deceased Int32,\n        cumulative_recovered Int32,\n        cumulative_tested Int32')

Query id: 12319a4a-748a-4d20-a6c0-f0029c601d6a

Ok.

0 rows in set. Elapsed: 141.594 sec. Processed 12.53 million rows, 837.68 MB (88.46 thousand rows/s., 5.92 MB/s.)
Peak memory usage: 139.78 MiB.
```
##### Таблица geography

Получаем информацию о столбцах:     
```
b4589774f410 :) DESCRIBE url(
    'https://storage.googleapis.com/covid19-open-data/v3/geography.csv',
    'CSVWithNames'
);

DESCRIBE TABLE url('https://storage.googleapis.com/covid19-open-data/v3/geography.csv', 'CSVWithNames')

Query id: 202467d1-db06-4af3-8399-53c58701e899

   ┌─name─────────────┬─type──────────────┬─default_type─┬─default_expression─┬─comment─┬─codec_expression─┬─ttl_expression─┐
1. │ location_key     │ Nullable(String)  │              │                    │         │                  │                │
2. │ openstreetmap_id │ Nullable(Int64)   │              │                    │         │                  │                │
3. │ latitude         │ Nullable(Float64) │              │                    │         │                  │                │
4. │ longitude        │ Nullable(Float64) │              │                    │         │                  │                │
5. │ elevation_m      │ Nullable(Int64)   │              │                    │         │                  │                │
6. │ area_sq_km       │ Nullable(Int64)   │              │                    │         │                  │                │
7. │ area_rural_sq_km │ Nullable(Int64)   │              │                    │         │                  │                │
8. │ area_urban_sq_km │ Nullable(Int64)   │              │                    │         │                  │                │
   └──────────────────┴───────────────────┴──────────────┴────────────────────┴─────────┴──────────────────┴────────────────┘

8 rows in set. Elapsed: 1.479 sec.

b4589774f410 :) CREATE TABLE geography (
:-]     location_key LowCardinality(String),
:-]     openstreetmap_id Int64,
:-]     latitude Float64,
:-]     longitude Float64,
:-]     elevation_m Int64,
:-]     area_sq_km Int64,
:-]     area_rural_sq_km Int64,
:-]     area_urban_sq_km Int64
:-] )
:-] ENGINE = MergeTree
:-] ORDER BY (location_key);
```

Создаем таблицу:   

```
CREATE TABLE geography
(
    `location_key` LowCardinality(String),
    `openstreetmap_id` Int64,
    `latitude` Float64,
    `longitude` Float64,
    `elevation_m` Int64,
    `area_sq_km` Int64,
    `area_rural_sq_km` Int64,
    `area_urban_sq_km` Int64
)
ENGINE = MergeTree
ORDER BY location_key

Query id: 24b6b10a-4507-46ac-aff6-94f1f8d5cfd7

Ok.

0 rows in set. Elapsed: 0.086 sec.
```

Загружаем данные:   
```
b4589774f410 :) INSERT INTO geography
:-]    SELECT *
:-]    FROM
:-]       url(
:-]         'https://storage.googleapis.com/covid19-open-data/v3/geography.csv',
:-]          CSVWithNames,
:-]         'location_key LowCardinality(String),
:-]          openstreetmap_id Int64,
:-]          latitude Float64,
:-]          longitude Float64,
:-]          elevation_m Int64,
:-]          area_sq_km Int64,
:-]          area_rural_sq_km Int64,
:-]          area_urban_sq_km Int64'
:-]          );

INSERT INTO geography SELECT *
FROM url('https://storage.googleapis.com/covid19-open-data/v3/geography.csv', CSVWithNames, 'location_key LowCardinality(String),\n         openstreetmap_id Int64,\n         latitude Float64,\n         longitude Float64,\n         elevation_m Int64,\n         area_sq_km Int64,\n         area_rural_sq_km Int64,\n         area_urban_sq_km Int64')

Query id: 432c36cb-4ab4-4d68-95ae-95ae78dca287

Ok.

0 rows in set. Elapsed: 1.695 sec. Processed 22.13 thousand rows, 1.01 MB (13.05 thousand rows/s., 592.86 KB/s.)
Peak memory usage: 6.31 MiB.

```

##### Таблица index

Получаем информацию о столбцах:   
```
b4589774f410 :) DESCRIBE url(
:-]     'https://storage.googleapis.com/covid19-open-data/v3/index.csv',
:-]     'CSVWithNames'
:-] );

DESCRIBE TABLE url('https://storage.googleapis.com/covid19-open-data/v3/index.csv', 'CSVWithNames')

Query id: 0aafacf1-d3d8-4e53-b2f5-c068627900e8

    ┌─name───────────────┬─type─────────────┬─default_type─┬─default_expression─┬─comment─┬─codec_expression─┬─ttl_expression─┐
 1. │ location_key       │ Nullable(String) │              │                    │         │                  │                │
 2. │ place_id           │ Nullable(String) │              │                    │         │                  │                │
 3. │ wikidata_id        │ Nullable(String) │              │                    │         │                  │                │
 4. │ datacommons_id     │ Nullable(String) │              │                    │         │                  │                │
 5. │ country_code       │ Nullable(String) │              │                    │         │                  │                │
 6. │ country_name       │ Nullable(String) │              │                    │         │                  │                │
 7. │ subregion1_code    │ Nullable(String) │              │                    │         │                  │                │
 8. │ subregion1_name    │ Nullable(String) │              │                    │         │                  │                │
 9. │ subregion2_code    │ Nullable(String) │              │                    │         │                  │                │
10. │ subregion2_name    │ Nullable(String) │              │                    │         │                  │                │
11. │ locality_code      │ Nullable(String) │              │                    │         │                  │                │
12. │ locality_name      │ Nullable(String) │              │                    │         │                  │                │
13. │ iso_3166_1_alpha_2 │ Nullable(String) │              │                    │         │                  │                │
14. │ iso_3166_1_alpha_3 │ Nullable(String) │              │                    │         │                  │                │
15. │ aggregation_level  │ Nullable(Int64)  │              │                    │         │                  │                │
    └────────────────────┴──────────────────┴──────────────┴────────────────────┴─────────┴──────────────────┴────────────────┘

15 rows in set. Elapsed: 1.938 sec.
```
Создаем таблицу:   

```
b4589774f410 :) CREATE TABLE index_covid
:-] (
:-] location_key   String,
:-] place_id    String,
:-] wikidata_id  String,
:-] datacommons_id  String,
:-] country_code  String,
:-] country_name  String,
:-] subregion1_code  String,
:-] subregion1_name  String,
:-] subregion2_code  String,
:-] subregion2_name  String,
:-] locality_code  String,
:-] locality_name  String,
:-] iso_3166_1_alpha_2  String,
:-] iso_3166_1_alpha_3  String,
:-] aggregation_level  Int64
:-] )
:-] ENGINE = MergeTree
:-] ORDER BY (location_key,);

CREATE TABLE index_covid
(
    `location_key` String,
    `place_id` String,
    `wikidata_id` String,
    `datacommons_id` String,
    `country_code` String,
    `country_name` String,
    `subregion1_code` String,
    `subregion1_name` String,
    `subregion2_code` String,
    `subregion2_name` String,
    `locality_code` String,
    `locality_name` String,
    `iso_3166_1_alpha_2` String,
    `iso_3166_1_alpha_3` String,
    `aggregation_level` Int64
)
ENGINE = MergeTree
ORDER BY tuple(location_key)

Query id: 45d96190-27d8-44b1-9abf-394f0f34fab1

Ok.

0 rows in set. Elapsed: 0.084 sec.
```

Загружаем данные:   

```
b4589774f410 :) INSERT INTO index_covid
:-]    SELECT *
:-]    FROM
:-]       url(
:-]         'https://storage.googleapis.com/covid19-open-data/v3/index.csv',
:-]          CSVWithNames,
:-]         'location_key   String,
:-] place_id    String,
:-] wikidata_id  String,
:-] datacommons_id  String,
:-] country_code  String,
:-] country_name  String,
:-] subregion1_code  String,
:-] subregion1_name  String,
:-] subregion2_code  String,
:-] subregion2_name  String,
:-] locality_code  String,
:-] locality_name  String,
:-] iso_3166_1_alpha_2  String,
:-] iso_3166_1_alpha_3  String,
:-] aggregation_level  Int64'
:-]          );

INSERT INTO index_covid SELECT *
FROM url('https://storage.googleapis.com/covid19-open-data/v3/index.csv', CSVWithNames, 'location_key   String,\nplace_id    String,\nwikidata_id  String,\ndatacommons_id  String,\ncountry_code  String,\ncountry_name  String,\nsubregion1_code  String,\nsubregion1_name  String,\nsubregion2_code  String,\nsubregion2_name  String,\nlocality_code  String,\nlocality_name  String,\niso_3166_1_alpha_2  String,\niso_3166_1_alpha_3  String,\naggregation_level  Int64')

Query id: d793f14b-1da1-453d-baae-798f07acaf0f

Ok.

0 rows in set. Elapsed: 1.967 sec. Processed 22.96 thousand rows, 2.43 MB (11.67 thousand rows/s., 1.23 MB/s.)
Peak memory usage: 10.67 MiB.

b4589774f410 :)
```
##### Таблица demographics

Получаем информацию о столбцах:  

```
b4589774f410 :) DESCRIBE url(
:-]     'https://storage.googleapis.com/covid19-open-data/v3/demographics.csv',
:-]     'CSVWithNames'
:-] );

DESCRIBE TABLE url('https://storage.googleapis.com/covid19-open-data/v3/demographics.csv', 'CSVWithNames')

Query id: 7a103481-e2f7-461a-b290-99a696ca1bf3

    ┌─name────────────────────────┬─type──────────────┬─default_type─┬─default_expression─┬─comment─┬─codec_expression─┬─ttl_expression─┐
 1. │ location_key                │ Nullable(String)  │              │                    │         │                  │                │
 2. │ population                  │ Nullable(Int64)   │              │                    │         │                  │                │
 3. │ population_male             │ Nullable(Int64)   │              │                    │         │                  │                │
 4. │ population_female           │ Nullable(Int64)   │              │                    │         │                  │                │
 5. │ population_rural            │ Nullable(Int64)   │              │                    │         │                  │                │
 6. │ population_urban            │ Nullable(Int64)   │              │                    │         │                  │                │
 7. │ population_largest_city     │ Nullable(Int64)   │              │                    │         │                  │                │
 8. │ population_clustered        │ Nullable(Int64)   │              │                    │         │                  │                │
 9. │ population_density          │ Nullable(Float64) │              │                    │         │                  │                │
10. │ human_development_index     │ Nullable(Float64) │              │                    │         │                  │                │
11. │ population_age_00_09        │ Nullable(Int64)   │              │                    │         │                  │                │
12. │ population_age_10_19        │ Nullable(Int64)   │              │                    │         │                  │                │
13. │ population_age_20_29        │ Nullable(Int64)   │              │                    │         │                  │                │
14. │ population_age_30_39        │ Nullable(Int64)   │              │                    │         │                  │                │
15. │ population_age_40_49        │ Nullable(Int64)   │              │                    │         │                  │                │
16. │ population_age_50_59        │ Nullable(Int64)   │              │                    │         │                  │                │
17. │ population_age_60_69        │ Nullable(Int64)   │              │                    │         │                  │                │
18. │ population_age_70_79        │ Nullable(Int64)   │              │                    │         │                  │                │
19. │ population_age_80_and_older │ Nullable(Int64)   │              │                    │         │                  │                │
    └─────────────────────────────┴───────────────────┴──────────────┴────────────────────┴─────────┴──────────────────┴────────────────┘

19 rows in set. Elapsed: 1.624 sec.
```

Создаем таблицу:   

```
b4589774f410 :) CREATE TABLE demographics
:-] (
:-] location_key   String,
:-] population    Int64,
:-] population_male  Int64,
:-] population_female  Int64,
:-] population_rural  Int64,
:-] population_urban  Int64,
:-] population_largest_city  Int64,
:-] population_clustered  Int64,
:-] population_density  Float64,
:-] human_development_index  Float64,
:-] population_age_00_09 Int64,
:-] population_age_10_09 Int64,
:-] population_age_20_29 Int64,
:-] population_age_30_39 Int64,
:-] population_age_40_49 Int64,
:-] population_age_50_59 Int64,
:-] population_age_60_69 Int64,
:-] population_age_70_79 Int64,
:-] population_age_80_and_older Int64
:-] )
:-] ENGINE = MergeTree
:-] ORDER BY (location_key,);

CREATE TABLE demographics
(
    `location_key` String,
    `population` Int64,
    `population_male` Int64,
    `population_female` Int64,
    `population_rural` Int64,
    `population_urban` Int64,
    `population_largest_city` Int64,
    `population_clustered` Int64,
    `population_density` Float64,
    `human_development_index` Float64,
    `population_age_00_09` Int64,
    `population_age_10_09` Int64,
    `population_age_20_29` Int64,
    `population_age_30_39` Int64,
    `population_age_40_49` Int64,
    `population_age_50_59` Int64,
    `population_age_60_69` Int64,
    `population_age_70_79` Int64,
    `population_age_80_and_older` Int64
)
ENGINE = MergeTree
ORDER BY tuple(location_key)

Query id: aa6d2562-50c3-4888-9837-4cf65fb82b41

Ok.

0 rows in set. Elapsed: 0.301 sec.

```


Загружаем данные:   

```
b4589774f410 :) INSERT INTO demographics
:-]    SELECT *
:-]    FROM
:-]       url(
:-]         'https://storage.googleapis.com/covid19-open-data/v3/demographics.csv',
:-]          CSVWithNames,
:-]  'location_key   String,
:-] population    Int64,
:-] population_male  Int64,
:-] population_female  Int64,
:-] population_rural  Int64,
:-] population_urban  Int64,
:-] population_largest_city  Int64,
:-] population_clustered  Int64,
:-] population_density  Float64,
:-] human_development_index  Float64,
:-] population_age_00_09 Int64,
:-] population_age_10_09 Int64,
:-] population_age_20_29 Int64,
:-] population_age_30_39 Int64,
:-] population_age_40_49 Int64,
:-] population_age_50_59 Int64,
:-] population_age_60_69 Int64,
:-] population_age_70_79 Int64,
:-] population_age_80_and_older Int64');

INSERT INTO demographics SELECT *
FROM url('https://storage.googleapis.com/covid19-open-data/v3/demographics.csv', CSVWithNames, 'location_key   String,\npopulation    Int64,\npopulation_male  Int64,\npopulation_female  Int64,\npopulation_rural  Int64,\npopulation_urban  Int64,\npopulation_largest_city  Int64,\npopulation_clustered  Int64,\npopulation_density  Float64,\nhuman_development_index  Float64,\npopulation_age_00_09 Int64,\npopulation_age_10_09 Int64,\npopulation_age_20_29 Int64,\npopulation_age_30_39 Int64,\npopulation_age_40_49 Int64,\npopulation_age_50_59 Int64,\npopulation_age_60_69 Int64,\npopulation_age_70_79 Int64,\npopulation_age_80_and_older Int64')

Query id: b5cf11b6-6661-4ae6-a95f-a81187733ccf

Ok.

0 rows in set. Elapsed: 1.920 sec. Processed 21.69 thousand rows, 1.54 MB (11.30 thousand rows/s., 804.49 KB/s.)
Peak memory usage: 8.24 MiB.

```
##### Таблица health

Получаем информацию о столбцах:  


```
:-] );DESCRIBE url('https://storage.googleapis.com/covid19-open-data/v3/health.csv','CSVWithNames');

DESCRIBE TABLE url('https://storage.googleapis.com/covid19-open-data/v3/health.csv', 'CSVWithNames')

Query id: 8397e5d2-dc9a-464c-b058-45d0bb3831fc

    ┌─name─────────────────────────────────┬─type──────────────┬─default_type─┬─default_expression─┬─comment─┬─codec_expression─┬─ttl_expression─┐
 1. │ location_key                         │ Nullable(String)  │              │                    │         │                  │                │
 2. │ life_expectancy                      │ Nullable(Float64) │              │                    │         │                  │                │
 3. │ smoking_prevalence                   │ Nullable(Float64) │              │                    │         │                  │                │
 4. │ diabetes_prevalence                  │ Nullable(Float64) │              │                    │         │                  │                │
 5. │ infant_mortality_rate                │ Nullable(Float64) │              │                    │         │                  │                │
 6. │ adult_male_mortality_rate            │ Nullable(Float64) │              │                    │         │                  │                │
 7. │ adult_female_mortality_rate          │ Nullable(Float64) │              │                    │         │                  │                │
 8. │ pollution_mortality_rate             │ Nullable(Float64) │              │                    │         │                  │                │
 9. │ comorbidity_mortality_rate           │ Nullable(Float64) │              │                    │         │                  │                │
10. │ hospital_beds_per_1000               │ Nullable(Float64) │              │                    │         │                  │                │
11. │ nurses_per_1000                      │ Nullable(Float64) │              │                    │         │                  │                │
12. │ physicians_per_1000                  │ Nullable(Float64) │              │                    │         │                  │                │
13. │ health_expenditure_usd               │ Nullable(Float64) │              │                    │         │                  │                │
14. │ out_of_pocket_health_expenditure_usd │ Nullable(Float64) │              │                    │         │                  │                │
    └──────────────────────────────────────┴───────────────────┴──────────────┴────────────────────┴─────────┴──────────────────┴────────────────┘

14 rows in set. Elapsed: 0.590 sec.

```

Создаем таблицу:   

```
b4589774f410 :) CREATE TABLE health
:-] (
:-] location_key   String,
:-] life_expectancy    Float64,
:-] smoking_prevalence  Float64,
:-] population_female  Float64,
:-] diabetes_prevalence  Float64,
:-] infant_mortality_rate  Float64,
:-] adult_male_mortality_rate  Float64,
:-] adult_female_mortality_rate  Float64,
:-] pollution_mortality_rate  Float64,
:-] comorbidity_mortality_rate  Float64,
:-] hospital_beds_per_1000 Float64,
:-] nurses_per_1000 Float64,
:-] health_expenditure_usd Float64,
:-] out_of_pocket_health_expenditure_usd Float64
:-] )
:-] ENGINE = MergeTree
:-] ORDER BY (location_key);

CREATE TABLE health
(
    `location_key` String,
    `life_expectancy` Float64,
    `smoking_prevalence` Float64,
    `population_female` Float64,
    `diabetes_prevalence` Float64,
    `infant_mortality_rate` Float64,
    `adult_male_mortality_rate` Float64,
    `adult_female_mortality_rate` Float64,
    `pollution_mortality_rate` Float64,
    `comorbidity_mortality_rate` Float64,
    `hospital_beds_per_1000` Float64,
    `nurses_per_1000` Float64,
    `health_expenditure_usd` Float64,
    `out_of_pocket_health_expenditure_usd` Float64
)
ENGINE = MergeTree
ORDER BY location_key

Query id: f64a6edf-3b4e-4164-be37-486b70a83e34

Ok.

0 rows in set. Elapsed: 0.065 sec.
```
Загружаем данные:   

```
b4589774f410 :) INSERT INTO health
:-]    SELECT *
:-]    FROM
:-]       url(
:-]         'https://storage.googleapis.com/covid19-open-data/v3/health.csv',
:-]          CSVWithNames,
:-]  'location_key   String,
:-] life_expectancy    Float64,
:-] smoking_prevalence  Float64,
:-] population_female  Float64,
:-] diabetes_prevalence  Float64,
:-] infant_mortality_rate  Float64,
:-] adult_male_mortality_rate  Float64,
:-] adult_female_mortality_rate  Float64,
:-] pollution_mortality_rate  Float64,
:-] comorbidity_mortality_rate  Float64,
:-] hospital_beds_per_1000 Float64,
:-] nurses_per_1000 Float64,
:-] health_expenditure_usd Float64,
:-] out_of_pocket_health_expenditure_usd Float64');

INSERT INTO health SELECT *
FROM url('https://storage.googleapis.com/covid19-open-data/v3/health.csv', CSVWithNames, 'location_key   String,\nlife_expectancy    Float64,\nsmoking_prevalence  Float64,\npopulation_female  Float64,\ndiabetes_prevalence  Float64,\ninfant_mortality_rate  Float64,\nadult_male_mortality_rate  Float64,\nadult_female_mortality_rate  Float64,\npollution_mortality_rate  Float64,\ncomorbidity_mortality_rate  Float64,\nhospital_beds_per_1000 Float64,\nnurses_per_1000 Float64,\nhealth_expenditure_usd Float64,\nout_of_pocket_health_expenditure_usd Float64')

Query id: 05ee2491-a882-4320-a3ab-8e3fedd24524

Ok.

0 rows in set. Elapsed: 1.332 sec. Processed 3.50 thousand rows, 122.07 KB (2.63 thousand rows/s., 91.65 KB/s.)
Peak memory usage: 4.12 MiB.
```


##### Таблица hospitalizations

Получаем информацию о столбцах:  

```
b4589774f410 :) DESCRIBE url('https://storage.googleapis.com/covid19-open-data/v3/hospitalizations.csv','CSVWithNames');

DESCRIBE TABLE url('https://storage.googleapis.com/covid19-open-data/v3/hospitalizations.csv', 'CSVWithNames')

Query id: a49ce496-9d40-44d1-8f67-d304f5fe6b2d

    ┌─name───────────────────────────────┬─type─────────────┬─default_type─┬─default_expression─┬─comment─┬─codec_expression─┬─ttl_expression─┐
 1. │ date                               │ Nullable(Date)   │              │                    │         │                  │                │
 2. │ location_key                       │ Nullable(String) │              │                    │         │                  │                │
 3. │ new_hospitalized_patients          │ Nullable(Int64)  │              │                    │         │                  │                │
 4. │ cumulative_hospitalized_patients   │ Nullable(Int64)  │              │                    │         │                  │                │
 5. │ current_hospitalized_patients      │ Nullable(String) │              │                    │         │                  │                │
 6. │ new_intensive_care_patients        │ Nullable(Int64)  │              │                    │         │                  │                │
 7. │ cumulative_intensive_care_patients │ Nullable(Int64)  │              │                    │         │                  │                │
 8. │ current_intensive_care_patients    │ Nullable(String) │              │                    │         │                  │                │
 9. │ new_ventilator_patients            │ Nullable(String) │              │                    │         │                  │                │
10. │ cumulative_ventilator_patients     │ Nullable(String) │              │                    │         │                  │                │
11. │ current_ventilator_patients        │ Nullable(String) │              │                    │         │                  │                │
    └────────────────────────────────────┴──────────────────┴──────────────┴────────────────────┴─────────┴──────────────────┴────────────────┘

11 rows in set. Elapsed: 2.305 sec.
```

Создаем таблицу:   

```
b4589774f410 :) CREATE TABLE hospitalizations
:-] (
:-] date Date,
:-] location_key   String,
:-] new_hospitalized_patients    Int64,
:-] cumulative_hospitalized_patients  Int64,
:-] current_hospitalized_patients  String,
:-] new_intensive_care_patients  Int64,
:-] cumulative_intensive_care_patients  Int64,
:-] current_intensive_care_patients  String,
:-] new_ventilator_patients  String,
:-] cumulative_ventilator_patients  String,
:-] current_ventilator_patients  String
:-] )
:-] ENGINE = MergeTree
:-] ORDER BY (location_key, date);

CREATE TABLE hospitalizations
(
    `date` Date,
    `location_key` String,
    `new_hospitalized_patients` Int64,
    `cumulative_hospitalized_patients` Int64,
    `current_hospitalized_patients` String,
    `new_intensive_care_patients` Int64,
    `cumulative_intensive_care_patients` Int64,
    `current_intensive_care_patients` String,
    `new_ventilator_patients` String,
    `cumulative_ventilator_patients` String,
    `current_ventilator_patients` String
)
ENGINE = MergeTree
ORDER BY (location_key, date)

Query id: 8bdf4366-ca8f-45b1-9796-70f2ae81f815

Ok.

0 rows in set. Elapsed: 0.063 sec.
```
Загружаем данные:   


```
b4589774f410 :) INSERT INTO hospitalizations
   SELECT *
   FROM
      url(
        'https://storage.googleapis.com/covid19-open-data/v3/hospitalizations.csv',
         CSVWithNames,
 'date Date,
location_key   String,
new_hospitalized_patients    Int64,
cumulative_hospitalized_patients  Int64,
current_hospitalized_patients  String,
new_intensive_care_patients  Int64,
cumulative_intensive_care_patients  Int64,
current_intensive_care_patients  String,
new_ventilator_patients  String,
cumulative_ventilator_patients  String,
current_ventilator_patients  String');

INSERT INTO hospitalizations SELECT *
FROM url('https://storage.googleapis.com/covid19-open-data/v3/hospitalizations.csv', CSVWithNames, 'date Date,\nlocation_key   String,\nnew_hospitalized_patients    Int64,\ncumulative_hospitalized_patients  Int64,\ncurrent_hospitalized_patients  String,\nnew_intensive_care_patients  Int64,\ncumulative_intensive_care_patients  Int64,\ncurrent_intensive_care_patients  String,\nnew_ventilator_patients  String,\ncumulative_ventilator_patients  String,\ncurrent_ventilator_patients  String')

Query id: 6924206c-84fa-4fe2-95d0-23d5ea6a38e6

Ok.

0 rows in set. Elapsed: 21.644 sec. Processed 1.77 million rows, 169.74 MB (81.71 thousand rows/s., 7.84 MB/s.)
Peak memory usage: 162.74 MiB.
```

##### Таблица vaccinations

Получаем информацию о столбцах:  

```
b4589774f410 :) DESCRIBE url('https://storage.googleapis.com/covid19-open-data/v3/vaccinations.csv','CSVWithNames');

DESCRIBE TABLE url('https://storage.googleapis.com/covid19-open-data/v3/vaccinations.csv', 'CSVWithNames')

Query id: c6c3e189-8f94-4b6c-85a6-e161cfb20b09

    ┌─name──────────────────────────────────────────┬─type─────────────┬─default_type─┬─default_expression─┬─comment─┬─codec_expression─┬─ttl_expression─┐
 1. │ date                                          │ Nullable(Date)   │              │                    │         │                  │                │
 2. │ location_key                                  │ Nullable(String) │              │                    │         │                  │                │
 3. │ new_persons_vaccinated                        │ Nullable(Int64)  │              │                    │         │                  │                │
 4. │ cumulative_persons_vaccinated                 │ Nullable(Int64)  │              │                    │         │                  │                │
 5. │ new_persons_fully_vaccinated                  │ Nullable(Int64)  │              │                    │         │                  │                │
 6. │ cumulative_persons_fully_vaccinated           │ Nullable(Int64)  │              │                    │         │                  │                │
 7. │ new_vaccine_doses_administered                │ Nullable(Int64)  │              │                    │         │                  │                │
 8. │ cumulative_vaccine_doses_administered         │ Nullable(Int64)  │              │                    │         │                  │                │
 9. │ new_persons_vaccinated_pfizer                 │ Nullable(String) │              │                    │         │                  │                │
10. │ cumulative_persons_vaccinated_pfizer          │ Nullable(String) │              │                    │         │                  │                │
11. │ new_persons_fully_vaccinated_pfizer           │ Nullable(String) │              │                    │         │                  │                │
12. │ cumulative_persons_fully_vaccinated_pfizer    │ Nullable(String) │              │                    │         │                  │                │
13. │ new_vaccine_doses_administered_pfizer         │ Nullable(String) │              │                    │         │                  │                │
14. │ cumulative_vaccine_doses_administered_pfizer  │ Nullable(String) │              │                    │         │                  │                │
15. │ new_persons_vaccinated_moderna                │ Nullable(String) │              │                    │         │                  │                │
16. │ cumulative_persons_vaccinated_moderna         │ Nullable(String) │              │                    │         │                  │                │
17. │ new_persons_fully_vaccinated_moderna          │ Nullable(String) │              │                    │         │                  │                │
18. │ cumulative_persons_fully_vaccinated_moderna   │ Nullable(String) │              │                    │         │                  │                │
19. │ new_vaccine_doses_administered_moderna        │ Nullable(String) │              │                    │         │                  │                │
20. │ cumulative_vaccine_doses_administered_moderna │ Nullable(String) │              │                    │         │                  │                │
21. │ new_persons_vaccinated_janssen                │ Nullable(String) │              │                    │         │                  │                │
22. │ cumulative_persons_vaccinated_janssen         │ Nullable(String) │              │                    │         │                  │                │
23. │ new_persons_fully_vaccinated_janssen          │ Nullable(String) │              │                    │         │                  │                │
24. │ cumulative_persons_fully_vaccinated_janssen   │ Nullable(String) │              │                    │         │                  │                │
25. │ new_vaccine_doses_administered_janssen        │ Nullable(String) │              │                    │         │                  │                │
26. │ cumulative_vaccine_doses_administered_janssen │ Nullable(String) │              │                    │         │                  │                │
27. │ new_persons_vaccinated_sinovac                │ Nullable(String) │              │                    │         │                  │                │
28. │ total_persons_vaccinated_sinovac              │ Nullable(String) │              │                    │         │                  │                │
29. │ new_persons_fully_vaccinated_sinovac          │ Nullable(String) │              │                    │         │                  │                │
30. │ total_persons_fully_vaccinated_sinovac        │ Nullable(String) │              │                    │         │                  │                │
31. │ new_vaccine_doses_administered_sinovac        │ Nullable(String) │              │                    │         │                  │                │
32. │ total_vaccine_doses_administered_sinovac      │ Nullable(String) │              │                    │         │                  │                │
    └───────────────────────────────────────────────┴──────────────────┴──────────────┴────────────────────┴─────────┴──────────────────┴────────────────┘

32 rows in set. Elapsed: 2.562 sec.

```

Создаем таблицу:   

```

b4589774f410 :) CREATE TABLE vaccinations
:-] (
:-] date Date,
:-] location_key   String,
:-] new_persons_vaccinated    Int64,
:-] cumulative_persons_vaccinated  Int64,
:-] new_persons_fully_vaccinated  Int64,
:-] cumulative_persons_fully_vaccinated  Int64,
:-] new_vaccine_doses_administered  Int64,
:-] cumulative_vaccine_doses_administered  Int64,
:-] new_persons_vaccinated_pfizer  String,
:-] cumulative_persons_vaccinated_pfizer  String,
:-] new_persons_fully_vaccinated_pfizer  String,
:-] cumulative_persons_fully_vaccinated_pfizer  String,
:-] new_vaccine_doses_administered_pfizer  String,
:-] cumulative_vaccine_doses_administered_pfizer  String,
:-] new_persons_vaccinated_moderna  String,
:-] cumulative_persons_vaccinated_moderna  String,
:-] new_persons_fully_vaccinated_moderna  String,
:-] cumulative_persons_fully_vaccinated_moderna  String,
:-] new_vaccine_doses_administered_moderna  String,
:-] cumulative_vaccine_doses_administered_moderna  String,
:-] new_persons_vaccinated_janssen  String,
:-] cumulative_persons_vaccinated_janssen  String,
:-] new_persons_fully_vaccinated_janssen  String,
:-] cumulative_persons_fully_vaccinated_janssen  String,
:-] new_vaccine_doses_administered_janssen  String,
:-] cumulative_vaccine_doses_administered_janssen  String,
:-] new_persons_vaccinated_sinovac  String,
:-] total_persons_vaccinated_sinovac  String,
:-] new_persons_fully_vaccinated_sinovac  String,
:-] total_persons_fully_vaccinated_sinovac  String,
:-] new_vaccine_doses_administered_sinovac  String,
:-] total_vaccine_doses_administered_sinovac  String
:-] )
:-] ENGINE = MergeTree
:-] ORDER BY (location_key, date);

CREATE TABLE vaccinations
(
    `date` Date,
    `location_key` String,
    `new_persons_vaccinated` Int64,
    `cumulative_persons_vaccinated` Int64,
    `new_persons_fully_vaccinated` Int64,
    `cumulative_persons_fully_vaccinated` Int64,
    `new_vaccine_doses_administered` Int64,
    `cumulative_vaccine_doses_administered` Int64,
    `new_persons_vaccinated_pfizer` String,
    `cumulative_persons_vaccinated_pfizer` String,
    `new_persons_fully_vaccinated_pfizer` String,
    `cumulative_persons_fully_vaccinated_pfizer` String,
    `new_vaccine_doses_administered_pfizer` String,
    `cumulative_vaccine_doses_administered_pfizer` String,
    `new_persons_vaccinated_moderna` String,
    `cumulative_persons_vaccinated_moderna` String,
    `new_persons_fully_vaccinated_moderna` String,
    `cumulative_persons_fully_vaccinated_moderna` String,
    `new_vaccine_doses_administered_moderna` String,
    `cumulative_vaccine_doses_administered_moderna` String,
    `new_persons_vaccinated_janssen` String,
    `cumulative_persons_vaccinated_janssen` String,
    `new_persons_fully_vaccinated_janssen` String,
    `cumulative_persons_fully_vaccinated_janssen` String,
    `new_vaccine_doses_administered_janssen` String,
    `cumulative_vaccine_doses_administered_janssen` String,
    `new_persons_vaccinated_sinovac` String,
    `total_persons_vaccinated_sinovac` String,
    `new_persons_fully_vaccinated_sinovac` String,
    `total_persons_fully_vaccinated_sinovac` String,
    `new_vaccine_doses_administered_sinovac` String,
    `total_vaccine_doses_administered_sinovac` String
)
ENGINE = MergeTree
ORDER BY (location_key, date)

Query id: fc4d3975-1637-4c5e-8084-0b8797b801ef

Ok.

0 rows in set. Elapsed: 0.084 sec.
```

Загружаем данные:   

```

b4589774f410 :) INSERT INTO vaccinations
:-]    SELECT *
:-]    FROM
:-]       url(
:-]         'https://storage.googleapis.com/covid19-open-data/v3/vaccinations.csv',
:-]          CSVWithNames,
:-]  'date Date,
:-] location_key   String,
:-] new_persons_vaccinated    Int64,
:-] cumulative_persons_vaccinated  Int64,
:-] new_persons_fully_vaccinated  Int64,
:-] cumulative_persons_fully_vaccinated  Int64,
:-] new_vaccine_doses_administered  Int64,
:-] cumulative_vaccine_doses_administered  Int64,
:-] new_persons_vaccinated_pfizer  String,
:-] cumulative_persons_vaccinated_pfizer  String,
:-] new_persons_fully_vaccinated_pfizer  String,
:-] cumulative_persons_fully_vaccinated_pfizer  String,
:-] new_vaccine_doses_administered_pfizer  String,
:-] cumulative_vaccine_doses_administered_pfizer  String,
:-] new_persons_vaccinated_moderna  String,
:-] cumulative_persons_vaccinated_moderna  String,
:-] new_persons_fully_vaccinated_moderna  String,
:-] cumulative_persons_fully_vaccinated_moderna  String,
:-] new_vaccine_doses_administered_moderna  String,
:-] cumulative_vaccine_doses_administered_moderna  String,
:-] new_persons_vaccinated_janssen  String,
:-] cumulative_persons_vaccinated_janssen  String,
:-] new_persons_fully_vaccinated_janssen  String,
:-] cumulative_persons_fully_vaccinated_janssen  String,
:-] new_vaccine_doses_administered_janssen  String,
:-] cumulative_vaccine_doses_administered_janssen  String,
:-] new_persons_vaccinated_sinovac  String,
:-] total_persons_vaccinated_sinovac  String,
:-] new_persons_fully_vaccinated_sinovac  String,
:-] total_persons_fully_vaccinated_sinovac  String,
:-] new_vaccine_doses_administered_sinovac  String,
:-] total_vaccine_doses_administered_sinovac  String');

INSERT INTO vaccinations SELECT *
FROM url('https://storage.googleapis.com/covid19-open-data/v3/vaccinations.csv', CSVWithNames, 'date Date,\nlocation_key   String,\nnew_persons_vaccinated    Int64,\ncumulative_persons_vaccinated  Int64,\nnew_persons_fully_vaccinated  Int64,\ncumulative_persons_fully_vaccinated  Int64,\nnew_vaccine_doses_administered  Int64,\ncumulative_vaccine_doses_administered  Int64,\nnew_persons_vaccinated_pfizer  String,\ncumulative_persons_vaccinated_pfizer  String,\nnew_persons_fully_vaccinated_pfizer  String,\ncumulative_persons_fully_vaccinated_pfizer  String,\nnew_vaccine_doses_administered_pfizer  String,\ncumulative_vaccine_doses_administered_pfizer  String,\nnew_persons_vaccinated_moderna  String,\ncumulative_persons_vaccinated_moderna  String,\nnew_persons_fully_vaccinated_moderna  String,\ncumulative_persons_fully_vaccinated_moderna  String,\nnew_vaccine_doses_administered_moderna  String,\ncumulative_vaccine_doses_administered_moderna  String,\nnew_persons_vaccinated_janssen  String,\ncumulative_persons_vaccinated_janssen  String,\nnew_persons_fully_vaccinated_janssen  String,\ncumulative_persons_fully_vaccinated_janssen  String,\nnew_vaccine_doses_administered_janssen  String,\ncumulative_vaccine_doses_administered_janssen  String,\nnew_persons_vaccinated_sinovac  String,\ntotal_persons_vaccinated_sinovac  String,\nnew_persons_fully_vaccinated_sinovac  String,\ntotal_persons_fully_vaccinated_sinovac  String,\nnew_vaccine_doses_administered_sinovac  String,\ntotal_vaccine_doses_administered_sinovac  String')

Query id: 7bda6452-19ef-4ff1-af01-5b6881919098

Ok.

0 rows in set. Elapsed: 55.571 sec. Processed 2.55 million rows, 538.36 MB (45.80 thousand rows/s., 9.69 MB/s.)
Peak memory usage: 550.25 MiB.
```
##### Создаем пользователя и даем ему права

```
b4589774f410 :) CREATE USER user_cli IDENTIFIED WITH plaintext_password BY 'Password_123';

CREATE USER user_cli IDENTIFIED WITH plaintext_password BY 'Password_123'

Query id: 2c47841e-bb90-41d7-b93f-eede2c8ede31

Ok.

0 rows in set. Elapsed: 0.016 sec.

b4589774f410 :) GRANT ALL ON default.* TO user_cli WITH GRANT OPTION;

GRANT ALL ON default.* TO user_cli WITH GRANT OPTION

Query id: 440317b3-b4aa-49d2-b2de-706f57a320e6

Ok.

0 rows in set. Elapsed: 0.020 sec.
```

#### Настраиваем Metabase

##### Создаем подключение к Clickhouse:   

![DBConnect](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/Сoursework/DB.JPG?raw=true)

##### Создаем наборы данных для диаграмм:   

Vaccinations:   
![Vaccinations](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/Сoursework/Vacc.JPG?raw=true)

Hospitalizations:   
![Hospitalizations](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/Сoursework/Hosp.JPG?raw=true)

Demographics:   
![Demographics](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/Сoursework/DemogrJPG.JPG?raw=true)

Epidemiology:   
![Epidemiology](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/Сoursework/pid.JPG?raw=true)

Health:   
![Health](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/Сoursework/Healf.JPG?raw=true)

##### Настраиваем Дашборд

![Tab1](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/Сoursework/dashb1.JPG?raw=true)
![Tab2](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/Сoursework/dashb2.JPG?raw=true)
![Tab3](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/Сoursework/dashb3.JPG?raw=true)
