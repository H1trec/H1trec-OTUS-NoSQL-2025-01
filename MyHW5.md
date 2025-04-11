#### Clickhouse

### Установка Clickhouse

Установка Clickhouse производится в Docker при помощи следюущих команд:   

```
daemom@OVMCOUCH:~$ sudo docker run -d --name some-clickhouse-server --ulimit nofile=262144:262144 clickhouse
daemom@OVMCOUCH:~$ sudo docker exec -it some-clickhouse-server clickhouse-client
ClickHouse client version 25.3.2.39 (official build).
Connecting to localhost:9000 as user default.
Connected to ClickHouse server version 25.3.2.

Warnings:
 * Delay accounting is not enabled, OSIOWaitMicroseconds will not be gathered. You can enable it using `echo 1 > /proc/sys/kernel/task_delayacct` or by using sysctl.

25ff152d4820 :)
```

### Загрузка тестовых данных:   

Заходим в клиент:

```
daemom@OVMCOUCH:~$ sudo docker exec -it some-clickhouse-server clickhouse-client
ClickHouse client version 25.3.2.39 (official build).
Connecting to localhost:9000 as user default.
Connected to ClickHouse server version 25.3.2.
25ff152d4820 :)
```

Создаем таблицу:


```
25ff152d4820 :) CREATE TABLE trips
:-] (
:-]     `trip_id` UInt32,
:-]     `vendor_id` Enum8('1' = 1, '2' = 2, '3' = 3, '4' = 4, 'CMT' = 5, 'VTS' = 6, 'DDS' = 7, 'B02512' = 10, 'B02598' = 11, 'B02617' = 12, 'B02682' = 13, 'B02764' = 14, '' = 15),
:-]     `pickup_date` Date,
:-]     `pickup_datetime` DateTime,
:-]     `dropoff_date` Date,
:-]     `dropoff_datetime` DateTime,
:-]     `store_and_fwd_flag` UInt8,
:-]     `rate_code_id` UInt8,
:-]     `pickup_longitude` Float64,
:-]     `pickup_latitude` Float64,
:-]     `dropoff_longitude` Float64,
:-]     `dropoff_latitude` Float64,
:-]     `passenger_count` UInt8,
:-]     `trip_distance` Float64,
:-]     `fare_amount` Float32,
:-]     `extra` Float32,
:-]     `mta_tax` Float32,
:-]     `tip_amount` Float32,
:-]     `tolls_amount` Float32,
:-]     `ehail_fee` Float32,
:-]     `improvement_surcharge` Float32,
:-]     `total_amount` Float32,
:-]     `payment_type` Enum8('UNK' = 0, 'CSH' = 1, 'CRE' = 2, 'NOC' = 3, 'DIS' = 4),
:-]     `trip_type` UInt8,
:-]     `pickup` FixedString(25),
:-]     `dropoff` FixedString(25),
:-]     `cab_type` Enum8('yellow' = 1, 'green' = 2, 'uber' = 3),
:-]     `pickup_nyct2010_gid` Int8,
:-]     `pickup_ctlabel` Float32,
:-]     `pickup_borocode` Int8,
:-]     `pickup_ct2010` String,
:-]     `pickup_boroct2010` String,
:-]     `pickup_cdeligibil` String,
:-]     `pickup_ntacode` FixedString(4),
:-]     `pickup_ntaname` String,
:-]     `pickup_puma` UInt16,
:-]     `dropoff_nyct2010_gid` UInt8,
:-]     `dropoff_ctlabel` Float32,
:-]     `dropoff_borocode` UInt8,
:-]     `dropoff_ct2010` String,
:-]     `dropoff_boroct2010` String,
:-]     `dropoff_cdeligibil` String,
:-]     `dropoff_ntacode` FixedString(4),
:-]     `dropoff_ntaname` String,
:-]     `dropoff_puma` UInt16
:-] )
:-] ENGINE = MergeTree
:-] PARTITION BY toYYYYMM(pickup_date)
:-] ORDER BY pickup_datetime;
```

Загружаем данные: 
```
25ff152d4820 :) INSERT INTO trips
:-] SELECT * FROM s3(
:-]     'https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/trips_{1..2}.gz',
:-]     'TabSeparatedWithNames', "
:-]     `trip_id` UInt32,
:-]     `vendor_id` Enum8('1' = 1, '2' = 2, '3' = 3, '4' = 4, 'CMT' = 5, 'VTS' = 6, 'DDS' = 7, 'B02512' = 10, 'B02598' = 11, 'B02617' = 12, 'B02682' = 13, 'B02764' = 14, '' = 15),
:-]     `pickup_date` Date,
:-]     `pickup_datetime` DateTime,
:-]     `dropoff_date` Date,
:-]     `dropoff_datetime` DateTime,
:-]     `store_and_fwd_flag` UInt8,
:-]     `rate_code_id` UInt8,
:-]     `pickup_longitude` Float64,
:-]     `pickup_latitude` Float64,
:-]     `dropoff_longitude` Float64,
:-]     `dropoff_latitude` Float64,
:-]     `passenger_count` UInt8,
:-]     `trip_distance` Float64,
:-]     `fare_amount` Float32,
:-]     `extra` Float32,
:-]     `mta_tax` Float32,
:-]     `tip_amount` Float32,
:-]     `tolls_amount` Float32,
:-]     `ehail_fee` Float32,
:-]     `improvement_surcharge` Float32,
:-]     `total_amount` Float32,
:-]     `payment_type` Enum8('UNK' = 0, 'CSH' = 1, 'CRE' = 2, 'NOC' = 3, 'DIS' = 4),
:-]     `trip_type` UInt8,
:-]     `pickup` FixedString(25),
:-]     `dropoff` FixedString(25),
:-]     `cab_type` Enum8('yellow' = 1, 'green' = 2, 'uber' = 3),
:-]     `pickup_nyct2010_gid` Int8,
:-]     `pickup_ctlabel` Float32,
:-]     `pickup_borocode` Int8,
:-]     `pickup_ct2010` String,
:-]     `pickup_boroct2010` String,
:-]     `pickup_cdeligibil` String,
:-]     `pickup_ntacode` FixedString(4),
:-]     `pickup_ntaname` String,
:-]     `pickup_puma` UInt16,
:-]     `dropoff_nyct2010_gid` UInt8,
:-]     `dropoff_ctlabel` Float32,
:-]     `dropoff_borocode` UInt8,
:-]     `dropoff_ct2010` String,
:-]     `dropoff_boroct2010` String,
:-]     `dropoff_cdeligibil` String,
:-]     `dropoff_ntacode` FixedString(4),
:-]     `dropoff_ntaname` String,
:-]     `dropoff_puma` UInt16
:-] ") SETTINGS input_format_try_infer_datetimes = 0

INSERT INTO trips
SETTINGS input_format_try_infer_datetimes = 0
SELECT *
FROM s3('https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/trips_{1..2}.gz', 'TabSeparatedWithNames', `\n    \`trip_id\` UInt32,\n    \`vendor_id\` Enum8('1' = 1, '2' = 2, '3' = 3, '4' = 4, 'CMT' = 5, 'VTS' = 6, 'DDS' = 7, 'B02512' = 10, 'B02598' = 11, 'B02617' = 12, 'B02682' = 13, 'B02764' = 14, '' = 15),\n    \`pickup_date\` Date,\n    \`pickup_datetime\` DateTime,\n    \`dropoff_date\` Date,\n    \`dropoff_datetime\` DateTime,\n    \`store_and_fwd_flag\` UInt8,\n    \`rate_code_id\` UInt8,\n    \`pickup_longitude\` Float64,\n    \`pickup_latitude\` Float64,\n    \`dropoff_longitude\` Float64,\n    \`dropoff_latitude\` Float64,\n    \`passenger_count\` UInt8,\n    \`trip_distance\` Float64,\n    \`fare_amount\` Float32,\n    \`extra\` Float32,\n    \`mta_tax\` Float32,\n    \`tip_amount\` Float32,\n    \`tolls_amount\` Float32,\n    \`ehail_fee\` Float32,\n    \`improvement_surcharge\` Float32,\n    \`total_amount\` Float32,\n    \`payment_type\` Enum8('UNK' = 0, 'CSH' = 1, 'CRE' = 2, 'NOC' = 3, 'DIS' = 4),\n    \`trip_type\` UInt8,\n    \`pickup\` FixedString(25),\n    \`dropoff\` FixedString(25),\n    \`cab_type\` Enum8('yellow' = 1, 'green' = 2, 'uber' = 3),\n    \`pickup_nyct2010_gid\` Int8,\n    \`pickup_ctlabel\` Float32,\n    \`pickup_borocode\` Int8,\n    \`pickup_ct2010\` String,\n    \`pickup_boroct2010\` String,\n    \`pickup_cdeligibil\` String,\n    \`pickup_ntacode\` FixedString(4),\n    \`pickup_ntaname\` String,\n    \`pickup_puma\` UInt16,\n    \`dropoff_nyct2010_gid\` UInt8,\n    \`dropoff_ctlabel\` Float32,\n    \`dropoff_borocode\` UInt8,\n    \`dropoff_ct2010\` String,\n    \`dropoff_boroct2010\` String,\n    \`dropoff_cdeligibil\` String,\n    \`dropoff_ntacode\` FixedString(4),\n    \`dropoff_ntaname\` String,\n    \`dropoff_puma\` UInt16\n`)
SETTINGS input_format_try_infer_datetimes = 0

Query id: e5248f44-2fa9-4477-81ca-cf13d4f234de

Ok.

0 rows in set. Elapsed: 60.179 sec. Processed 2.00 million rows, 163.07 MB (33.23 thousand rows/s., 2.71 MB/s.)
Peak memory usage: 901.77 MiB.

25ff152d4820 :)
```

Создадим еще одну таблицу:

```
CREATE DICTIONARY taxi_zone_dictionary
(
    `LocationID` UInt16 DEFAULT 0,
    `Borough` String,
    `Zone` String,
    `service_zone` String
)
PRIMARY KEY LocationID
SOURCE(HTTP(URL 'https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/taxi_zone_lookup.csv' FORMAT 'CSVWithNames'))
LIFETIME(MIN 0 MAX 0)
LAYOUT(HASHED_ARRAY())

Query id: ef092f56-c8c9-4ceb-a240-cee13fa4afda

Ok.
```

### Тестирование запросов

Проверяем количество загруженных данных:

```
25ff152d4820 :) SELECT count() FROM trips

SELECT count()
FROM trips

Query id: e0410a51-3e4f-4454-91be-0f3a41b294d5

   ┌─count()─┐
1. │ 1999657 │ -- 2.00 million
   └─────────┘

1 row in set. Elapsed: 0.007 sec.
```


Выполним команду distinct:
```
25ff152d4820 :) SELECT DISTINCT(pickup_ntaname) FROM trips

SELECT DISTINCT pickup_ntaname
FROM trips

Query id: fc634b26-2f06-4c51-b6ee-1389fdbaf588

     ┌─pickup_ntaname───────────────────────────────────────────┐
  1. │ Upper West Side                                          │
  2. │ Midtown-Midtown South                                    │
  3. │ Clinton                                                  │
  4. │ SoHo-TriBeCa-Civic Center-Little Italy                   │
  5. │ Murray Hill-Kips Bay                                     │
  6. │ Upper East Side-Carnegie Hill                            │
  7. │ Lincoln Square                                           │
  8. │ Hudson Yards-Chelsea-Flatiron-Union Square               │
  9. │ Airport                                                  │
 10. │ Battery Park City-Lower Manhattan                        │
 11. │ Bushwick South                                           │
 12. │ Lower East Side                                          │
 13. │ Gramercy                                                 │
 14. │ East Village                                             │
 15. │ Turtle Bay-East Midtown                                  │
 16. │ Chinatown                                                │
 17. │ West Village                                             │
 18. │ Lenox Hill-Roosevelt Island                              │
 19. │                                                          │
 20. │ park-cemetery-etc-Manhattan                              │
 21. │ Bedford                                                  │
 22. │ West Concourse                                           │
 23. │ Astoria                                                  │
 24. │ Fort Greene                                              │
 25. │ Yorkville                                                │
 26. │ Park Slope-Gowanus                                       │
 27. │ East Williamsburg                                        │
 28. │ University Heights-Morris Heights                        │
 29. │ North Side-South Side                                    │
 30. │ Hunters Point-Sunnyside-West Maspeth                     │
 31. │ Bushwick North                                           │
 32. │ Morningside Heights                                      │
 33. │ East Harlem South                                        │
 34. │ Flatbush                                                 │
 35. │ DUMBO-Vinegar Hill-Downtown Brooklyn-Boerum Hill         │
 36. │ Hamilton Heights                                         │
 37. │ Stuyvesant Town-Cooper Village                           │
 38. │ Prospect Heights                                         │
 39. │ Greenpoint                                               │
 40. │ Fordham South                                            │
 41. │ Brooklyn Heights-Cobble Hill                             │
 42. │ Borough Park                                             │
 43. │ Central Harlem South                                     │
 44. │ Soundview-Castle Hill-Clason Point-Harding Park          │
 45. │ Highbridge                                               │
 46. │ Forest Hills                                             │
 47. │ East Harlem North                                        │
 48. │ Manhattanville                                           │
 49. │ Crown Heights South                                      │
 50. │ Briarwood-Jamaica Hills                                  │
 51. │ Steinway                                                 │
 52. │ Jackson Heights                                          │
 53. │ Elmhurst                                                 │
 54. │ Elmhurst-Maspeth                                         │
 55. │ East Concourse-Concourse Village                         │
 56. │ Carroll Gardens-Columbia Street-Red Hook                 │
 57. │ Woodside                                                 │
 58. │ Washington Heights South                                 │
 59. │ East Elmhurst                                            │
 60. │ Old Astoria                                              │
 61. │ Newark Airport                                           │
 62. │ Prospect Lefferts Gardens-Wingate                        │
 63. │ Erasmus                                                  │
 64. │ park-cemetery-etc-Queens                                 │
 65. │ Washington Heights North                                 │
 66. │ Springfield Gardens South-Brookville                     │
 67. │ Brighton Beach                                           │
 68. │ Flushing                                                 │
 69. │ Central Harlem North-Polo Grounds                        │
 70. │ Melrose South-Mott Haven North                           │
 71. │ Jamaica                                                  │
 72. │ Rego Park                                                │
 73. │ Crown Heights North                                      │
 74. │ Clinton Hill                                             │
 75. │ Sunset Park West                                         │
 76. │ Midwood                                                  │
 77. │ Kensington-Ocean Parkway                                 │
 78. │ Stuyvesant Heights                                       │
 79. │ Williamsburg                                             │
 80. │ Queensbridge-Ravenswood-Long Island City                 │
 81. │ Mott Haven-Port Morris                                   │
 82. │ Cypress Hills-City Line                                  │
 83. │ Bensonhurst West                                         │
 84. │ Dyker Heights                                            │
 85. │ Richmond Hill                                            │
 86. │ South Ozone Park                                         │
 87. │ Canarsie                                                 │
 88. │ Kew Gardens Hills                                        │
 89. │ Rugby-Remsen Village                                     │
 90. │ Windsor Terrace                                          │
 91. │ Spuyten Duyvil-Kingsbridge                               │
 92. │ park-cemetery-etc-Brooklyn                               │
 93. │ North Corona                                             │
 94. │ Murray Hill                                              │
 95. │ Ocean Hill                                               │
 96. │ Marble Hill-Inwood                                       │
 97. │ College Point                                            │
 98. │ Whitestone                                               │
 99. │ Rosedale                                                 │
100. │ Eastchester-Edenwald-Baychester                          │
101. │ Ridgewood                                                │
102. │ Allerton-Pelham Gardens                                  │
103. │ Baisley Park                                             │
104. │ Kew Gardens                                              │
105. │ Claremont-Bathgate                                       │
106. │ Woodlawn-Wakefield                                       │
107. │ Queens Village                                           │
108. │ Lindenwood-Howard Beach                                  │
109. │ West Brighton                                            │
110. │ Seagate-Coney Island                                     │
111. │ Westchester-Unionport                                    │
112. │ Kingsbridge Heights                                      │
113. │ Sunset Park East                                         │
114. │ Brownsville                                              │
115. │ Stapleton-Rosebank                                       │
116. │ South Jamaica                                            │
117. │ Bellerose                                                │
118. │ Co-op City                                               │
119. │ Van Cortlandt Village                                    │
120. │ Flatlands                                                │
121. │ Corona                                                   │
122. │ Auburndale                                               │
123. │ Homecrest                                                │
124. │ Mount Hope                                               │
125. │ Maspeth                                                  │
126. │ Old Town-Dongan Hills-South Beach                        │
127. │ Bay Ridge                                                │
128. │ Douglas Manor-Douglaston-Little Neck                     │
129. │ Queensboro Hill                                          │
130. │ Ozone Park                                               │
131. │ Crotona Park East                                        │
132. │ Sheepshead Bay-Gerritsen Beach-Manhattan Beach           │
133. │ Gravesend                                                │
134. │ Bensonhurst East                                         │
135. │ Springfield Gardens North                                │
136. │ Georgetown-Marine Park-Bergen Beach-Mill Basin           │
137. │ Woodhaven                                                │
138. │ East New York                                            │
139. │ Hunts Point                                              │
140. │ Longwood                                                 │
141. │ Ocean Parkway South                                      │
142. │ Glendale                                                 │
143. │ St. Albans                                               │
144. │ East Flushing                                            │
145. │ Van Nest-Morris Park-Westchester Square                  │
146. │ Ft. Totten-Bay Terrace-Clearview                         │
147. │ Pomonok-Flushing Heights-Hillcrest                       │
148. │ Parkchester                                              │
149. │ Great Kills                                              │
150. │ Norwood                                                  │
151. │ Middle Village                                           │
152. │ Morrisania-Melrose                                       │
153. │ Jamaica Estates-Holliswood                               │
154. │ New Springville-Bloomfield-Travis                        │
155. │ Madison                                                  │
156. │ East New York (Pennsylvania Ave)                         │
157. │ Bedford Park-Fordham North                               │
158. │ East Flatbush-Farragut                                   │
159. │ Oakland Gardens                                          │
160. │ Hammels-Arverne-Edgemere                                 │
161. │ Bath Beach                                               │
162. │ East Tremont                                             │
163. │ Bronxdale                                                │
164. │ West Farms-Bronx River                                   │
165. │ Pelham Bay-Country Club-City Island                      │
166. │ Far Rockaway-Bayswater                                   │
167. │ Bayside-Bayside Hills                                    │
168. │ New Brighton-Silver Lake                                 │
169. │ park-cemetery-etc-Bronx                                  │
170. │ Schuylerville-Throgs Neck-Edgewater Park                 │
171. │ Todt Hill-Emerson Hill-Heartland Village-Lighthouse Hill │
172. │ Fresh Meadows-Utopia                                     │
173. │ Soundview-Bruckner                                       │
174. │ North Riverdale-Fieldston-Riverdale                      │
175. │ Williamsbridge-Olinville                                 │
176. │ Belmont                                                  │
177. │ Pelham Parkway                                           │
178. │ Laurelton                                                │
179. │ Grymes Hill-Clifton-Fox Hills                            │
180. │ Breezy Point-Belle Harbor-Rockaway Park-Broad Channel    │
181. │ Hollis                                                   │
182. │ West New Brighton-New Brighton-St. George                │
183. │ Starrett City                                            │
184. │ Grasmere-Arrochar-Ft. Wadsworth                          │
185. │ Glen Oaks-Floral Park-New Hyde Park                      │
186. │ New Dorp-Midland Beach                                   │
187. │ Mariner's Harbor-Arlington-Port Ivory-Graniteville       │
188. │ Cambria Heights                                          │
189. │ Arden Heights                                            │
190. │ Annadale-Huguenot-Prince's Bay-Eltingville               │
     └─pickup_ntaname───────────────────────────────────────────┘

190 rows in set. Elapsed: 0.242 sec. Processed 2.00 million rows, 60.32 MB (8.26 million rows/s., 249.20 MB/s.)
Peak memory usage: 50.72 KiB.

25ff152d4820 :)
```
 Команда отработала за 0.242 sec при этом вернув 190 уникальных значений из 1999657 строк.
 
 Посмотрим на работу с join:
 
 ```
 25ff152d4820 :) SELECT
:-]     count(1) AS total,
:-]     Borough
:-] FROM trips
:-] JOIN taxi_zone_dictionary ON toUInt64(trips.pickup_nyct2010_gid) = taxi_zone_dictionary.LocationID
:-] WHERE dropoff_nyct2010_gid = 132 OR dropoff_nyct2010_gid = 138
:-] GROUP BY Borough
:-] ORDER BY total DESC

SELECT
    count(1) AS total,
    Borough
FROM trips
INNER JOIN taxi_zone_dictionary ON toUInt64(trips.pickup_nyct2010_gid) = taxi_zone_dictionary.LocationID
WHERE (dropoff_nyct2010_gid = 132) OR (dropoff_nyct2010_gid = 138)
GROUP BY Borough
ORDER BY total DESC

Query id: 61e4842a-50b7-486f-83c0-a46f829740a6

   ┌─total─┬─Borough───────┐
1. │  7053 │ Manhattan     │
2. │  6828 │ Brooklyn      │
3. │  4458 │ Queens        │
4. │  2670 │ Bronx         │
5. │   554 │ Staten Island │
6. │    53 │ EWR           │
   └───────┴───────────────┘

6 rows in set. Elapsed: 0.247 sec. Processed 2.00 million rows, 4.00 MB (8.11 million rows/s., 16.22 MB/s.)
Peak memory usage: 7.85 KiB.

25ff152d4820 :)
```

команда отработала за 0.247 sec выполнив join двух таблиц: в одной из них  1999657 строк, в другой 265 строк.   
Фактический мы соединили огромную таблицу фактов и справочник и получили аналитиц по всей таблице фактов за такое маленькое время.

### 

Загрузка в Clickhouse
Загрузка архива данных:   
```
wget -O- https://zenodo.org/records/5092942 | grep -oE 'https://zenodo.org/records/5092942/files/flightlist_[0-9]+_[0-9]+\.csv\.gz' | xargs wget
```

Создаем таблицу:
```
CREATE TABLE opensky
(
    callsign String,
    number String,
    icao24 String,
    registration String,
    typecode String,
    origin String,
    destination String,
    firstseen DateTime,
    lastseen DateTime,
    day DateTime,
    latitude_1 Float64,
    longitude_1 Float64,
    altitude_1 Float64,
    latitude_2 Float64,
    longitude_2 Float64,
    altitude_2 Float64
) ENGINE = MergeTree ORDER BY (origin, destination, callsign);

```
Импорт данных:   
```
ls -1 flightlist_*.csv.gz | xargs -P100 -I{} bash -c 'gzip -c -d "{}" | clickhouse-client --date_time_input_format best_effort --query "INSERT INTO opensky FORMAT CSVWithNames"'
```

#### Тестирование запросов в PostgreSQL
```
select max(day) from public.opensky;
```
Отработал за 00:01:58.905

```
select count(*)  from public.opensky;
```
Отработал за 00:01:56.457

```
SELECT
    date_part('month', day) AS m, 
    date_part('year', day) AS y,
	count(*) AS c
FROM public.opensky
WHERE origin IN ('UUEE', 'UUDD', 'UUWW')
GROUP BY date_part('year', day),date_part('month', day)
ORDER BY date_part('year', day),date_part('month', day) ASC;
```
Отработал за 00:02:03.194

```
SELECT
    origin,
    count(*)
FROM opensky
WHERE origin != ''
GROUP BY origin
ORDER BY count(*) DESC
LIMIT 100;
```
Отработал за 00:02:08.243

#### Тестирование запросов в Clickhouse

```
SELECT max(day)
FROM opensky

Query id: 487b6331-757d-4b9d-b4c3-115fcbcebde1

   ┌────────────max(day)─┐
1. │ 2021-06-30 00:00:00 │
   └─────────────────────┘

1 row in set. Elapsed: 6.608 sec.
```

```
SELECT count()
FROM opensky

Query id: d5926499-3a6b-4224-8244-6893bba42218

   ┌──count()─┐
1. │ 66010819 │ -- 66.01 million
   └──────────┘

1 row in set. Elapsed: 0.003 sec.
```

```
SELECT
    formatDateTime(day, '%m') AS m,
    formatDateTime(day, '%Y') AS y,
    count() AS c
FROM opensky
WHERE origin IN ('UUEE', 'UUDD', 'UUWW')
GROUP BY
    y,
    m
ORDER BY
    y ASC,
    m ASC

Query id: 68cc2955-0ea4-4853-9692-58fb0ecffc47

    ┌─m──┬─y────┬─────c─┐
 1. │ 01 │ 2019 │ 26138 │
 2. │ 02 │ 2019 │ 22929 │
 3. │ 03 │ 2019 │ 26191 │
 4. │ 04 │ 2019 │ 26741 │
 5. │ 05 │ 2019 │ 29486 │
 6. │ 06 │ 2019 │ 29792 │
 7. │ 07 │ 2019 │ 31896 │
 8. │ 08 │ 2019 │ 32970 │
 9. │ 09 │ 2019 │ 29250 │
10. │ 10 │ 2019 │ 29332 │
11. │ 11 │ 2019 │ 26330 │
12. │ 12 │ 2019 │ 25004 │
13. │ 01 │ 2020 │ 25044 │
14. │ 02 │ 2020 │ 24245 │
15. │ 03 │ 2020 │ 21976 │
16. │ 04 │ 2020 │  3753 │
17. │ 05 │ 2020 │  4703 │
18. │ 06 │ 2020 │  9731 │
19. │ 07 │ 2020 │ 16078 │
20. │ 08 │ 2020 │ 20603 │
21. │ 09 │ 2020 │ 19558 │
22. │ 10 │ 2020 │ 18058 │
23. │ 11 │ 2020 │ 14479 │
24. │ 12 │ 2020 │ 15560 │
25. │ 01 │ 2021 │ 15219 │
26. │ 02 │ 2021 │ 13630 │
27. │ 03 │ 2021 │ 16181 │
28. │ 04 │ 2021 │ 18758 │
29. │ 05 │ 2021 │ 21669 │
30. │ 06 │ 2021 │ 24704 │
    └────┴──────┴───────┘

30 rows in set. Elapsed: 0.544 sec.
```

```
SELECT
    origin,
    count(*)
FROM opensky
WHERE origin != ''
GROUP BY origin
ORDER BY count(*) DESC
LIMIT 100

Query id: c89716af-2996-4883-9b8c-fb436fa1787c

     ┌─origin─┬─count()─┐
  1. │ KORD   │  745007 │
  2. │ KDFW   │  696702 │
  3. │ KATL   │  667286 │
  4. │ KDEN   │  582709 │
  5. │ KLAX   │  581952 │
  6. │ KLAS   │  447789 │
  7. │ KPHX   │  428558 │
  8. │ KSEA   │  412592 │
  9. │ KCLT   │  404612 │
 10. │ VIDP   │  363074 │
 11. │ EDDF   │  362643 │
 12. │ KSFO   │  361869 │
 13. │ KJFK   │  349232 │
 14. │ KMSP   │  346010 │
 15. │ LFPG   │  344748 │
 16. │ EGLL   │  341370 │
 17. │ EHAM   │  340272 │
 18. │ KEWR   │  337696 │
 19. │ KPHL   │  320762 │
 20. │ OMDB   │  308855 │
 21. │ UUEE   │  307098 │
 22. │ KBOS   │  304416 │
 23. │ LEMD   │  291787 │
 24. │ YSSY   │  272979 │
 25. │ KMIA   │  265121 │
 26. │ ZGSZ   │  263497 │
 27. │ EDDM   │  256691 │
 28. │ WMKK   │  254264 │
 29. │ CYYZ   │  251192 │
 30. │ KLGA   │  248699 │
 31. │ VHHH   │  248473 │
 32. │ RJTT   │  243477 │
 33. │ KBWI   │  241440 │
 34. │ KIAD   │  239558 │
 35. │ KIAH   │  234202 │
 36. │ KFLL   │  223447 │
 37. │ KDAL   │  212055 │
 38. │ KDCA   │  207883 │
 39. │ LIRF   │  207047 │
 40. │ PANC   │  206007 │
 41. │ LTFJ   │  205415 │
 42. │ KDTW   │  204020 │
 43. │ VABB   │  201679 │
 44. │ OTHH   │  200797 │
 45. │ KMDW   │  200796 │
 46. │ KSAN   │  198003 │
 47. │ KPDX   │  197760 │
 48. │ SBGR   │  197624 │
 49. │ VOBL   │  189011 │
 50. │ LEBL   │  188956 │
 51. │ YBBN   │  188011 │
 52. │ LSZH   │  187934 │
 53. │ YMML   │  187643 │
 54. │ RCTP   │  184466 │
 55. │ KSNA   │  180045 │
 56. │ EGKK   │  176420 │
 57. │ LOWW   │  176191 │
 58. │ UUDD   │  176099 │
 59. │ RKSI   │  173466 │
 60. │ EKCH   │  172128 │
 61. │ KOAK   │  171119 │
 62. │ RPLL   │  170122 │
 63. │ KRDU   │  167001 │
 64. │ KAUS   │  164524 │
 65. │ KBNA   │  163242 │
 66. │ KSDF   │  162655 │
 67. │ ENGM   │  160732 │
 68. │ LIMC   │  160696 │
 69. │ KSJC   │  159278 │
 70. │ KSTL   │  157984 │
 71. │ UUWW   │  156811 │
 72. │ KIND   │  153929 │
 73. │ ESSA   │  153390 │
 74. │ KMCO   │  153351 │
 75. │ KDVT   │  152895 │
 76. │ VTBS   │  152645 │
 77. │ CYVR   │  149574 │
 78. │ EIDW   │  148723 │
 79. │ LFPO   │  143277 │
 80. │ EGSS   │  140830 │
 81. │ KAPA   │  140776 │
 82. │ KHOU   │  138985 │
 83. │ KTPA   │  138033 │
 84. │ KFFZ   │  137333 │
 85. │ NZAA   │  136092 │
 86. │ YPPH   │  133916 │
 87. │ RJBB   │  133522 │
 88. │ EDDL   │  133018 │
 89. │ ULLI   │  130501 │
 90. │ KIWA   │  127195 │
 91. │ KTEB   │  126969 │
 92. │ VOMM   │  125616 │
 93. │ LSGG   │  123998 │
 94. │ LPPT   │  122733 │
 95. │ WSSS   │  120493 │
 96. │ EBBR   │  118539 │
 97. │ VTBD   │  118107 │
 98. │ KVNY   │  116326 │
 99. │ EDDT   │  115122 │
100. │ EFHK   │  114860 │
     └─origin─┴─count()─┘

100 rows in set. Elapsed: 2.149 sec.
```
### Тестирование в кластере.

#### Создаем кластер.

Содаем кластер в Докере. Используем для этого файлы(находятся в каталоге cli_claster):   
config_1.xml
config_2.xml
config_3.xml
config_4.xml
docker-compose.yml
haproxy.cfg

Поднимем кластер:
```
┌─cluster─┬─shard_num─┬─shard_weight─┬─replica_num─┬─host_name───┬─host_address─┬─port─┬─is_local─┬─user────┬─default_database─┬─errors_count─┬─slowdowns_count─┬─estimated_recovery_time─┐
│ example │         1 │            1 │           1 │ clickhouse1 │ 172.19.0.2   │ 9000 │        1 │ default │                  │            0 │               0 │                       0 │
│ example │         1 │            1 │           2 │ clickhouse2 │ 172.19.0.4   │ 9000 │        0 │ default │                  │            0 │               0 │                       0 │
│ example │         2 │            1 │           1 │ clickhouse2 │ 172.19.0.4   │ 9000 │        0 │ default │                  │            0 │               0 │                       0 │
│ example │         2 │            1 │           2 │ clickhouse4 │ 172.19.0.3   │ 9000 │        0 │ default │                  │            0 │               0 │                       0 │
└─────────┴───────────┴──────────────┴─────────────┴─────────────┴──────────────┴──────┴──────────┴─────────┴──────────────────┴──────────────┴─────────────────┴─────────────────────────┘
```
Создаем в каждой ноде таблицу:
```
CREATE TABLE db.opensky
(
    callsign String,
    number String,
    icao24 String,
    registration String,
    typecode String,
    origin String,
    destination String,
    firstseen DateTime,
    lastseen DateTime,
    day DateTime,
    latitude_1 Float64,
    longitude_1 Float64,
    altitude_1 Float64,
    latitude_2 Float64,
    longitude_2 Float64,
    altitude_2 Float64
) ENGINE = MergeTree ORDER BY (origin, destination, callsign);
```
Создаем в мастер ноде шардиророванную таблицу:  
```
CREATE TABLE IF NOT EXISTS db.opensky_shard as db.opensky ENGINE = Distributed('example', 'db', 'opensky', rand());
```
Загружаем данные:
```
ls -1 flightlist_*.csv.gz | xargs -P100 -I{} bash -c 'gzip -c -d "{}" | clickhouse-client --date_time_input_format best_effort --query "INSERT INTO db.opensky_shard FORMAT CSVWithNames"'
```

Тестируем запросы:


#### Первый запрос
```

SELECT count()
FROM db.opensky_shard

Query id: bd7a4420-dbd6-49c1-8f63-ecaaf93b01eb

┌──count()─┐
│ 99016343 │
└──────────┘

1 rows in set. Elapsed: 0.007 sec.

```

Подсчет количества работает чуть хуже, но это может быть из-за настроек кластера.

#### Второй запрос
```
SELECT max(day)
FROM db.opensky_shard

Query id: 4e2b28be-472f-4483-86f8-b976afc37726

┌────────────max(day)─┐
│ 2021-06-30 00:00:00 │
└─────────────────────┘

1 rows in set. Elapsed: 2.094 sec. Processed 66.01 million rows, 264.04 MB (31.53 million rows/s., 126.11 MB/s.)

```

Вычисление максимальной даты работает почти в 3 раза быстрее.

#### Третий запрос

```
SELECT
    formatDateTime(day, '%m') AS m,
    formatDateTime(day, '%Y') AS y,
    count() AS c
FROM db.opensky_shard
WHERE origin IN ('UUEE', 'UUDD', 'UUWW')
GROUP BY
    y,
    m
ORDER BY
    y ASC,
    m ASC

Query id: 0025bdb6-1fdb-4410-98e6-44fbfa53c3a9

┌─m──┬─y────┬─────c─┐
│ 01 │ 2019 │ 39217 │
│ 02 │ 2019 │ 34338 │
│ 03 │ 2019 │ 39310 │
│ 04 │ 2019 │ 40116 │
│ 05 │ 2019 │ 44312 │
│ 06 │ 2019 │ 44763 │
│ 07 │ 2019 │ 47955 │
│ 08 │ 2019 │ 49453 │
│ 09 │ 2019 │ 43747 │
│ 10 │ 2019 │ 43927 │
│ 11 │ 2019 │ 39570 │
│ 12 │ 2019 │ 37383 │
│ 01 │ 2020 │ 37573 │
│ 02 │ 2020 │ 36478 │
│ 03 │ 2020 │ 32887 │
│ 04 │ 2020 │  5635 │
│ 05 │ 2020 │  7024 │
│ 06 │ 2020 │ 14560 │
│ 07 │ 2020 │ 24104 │
│ 08 │ 2020 │ 30824 │
│ 09 │ 2020 │ 29405 │
│ 10 │ 2020 │ 27106 │
│ 11 │ 2020 │ 21681 │
│ 12 │ 2020 │ 23372 │
│ 01 │ 2021 │ 22816 │
│ 02 │ 2021 │ 20573 │
│ 03 │ 2021 │ 24270 │
│ 04 │ 2021 │ 28069 │
│ 05 │ 2021 │ 32401 │
│ 06 │ 2021 │ 36975 │
└────┴──────┴───────┘

30 rows in set. Elapsed: 0.246 sec. Processed 1.10 million rows, 18.66 MB (4.47 million rows/s., 76.01 MB/s.)
```
Третийзапрос работает почти в 2 раза быстрее.

#### Четвертый запрос

```
SELECT
    origin,
    count(*)
FROM db.opensky_shard
WHERE origin != ''
GROUP BY origin
ORDER BY count(*) DESC
LIMIT 100

Query id: d0da7ffd-9e85-419f-bbf3-2302bedd0ac9

┌─origin─┬─count()─┐
│ KORD   │  745007 │
│ KDFW   │  696702 │
│ KATL   │  667286 │
│ KDEN   │  582709 │
│ KLAX   │  581952 │
│ KLAS   │  447789 │
│ KPHX   │  428558 │
│ KSEA   │  412592 │
│ KCLT   │  404612 │
│ VIDP   │  363074 │
│ EDDF   │  362643 │
│ KSFO   │  361869 │
│ KJFK   │  349232 │
│ KMSP   │  346010 │
│ LFPG   │  344748 │
│ EGLL   │  341370 │
│ EHAM   │  340272 │
│ KEWR   │  337696 │
│ KPHL   │  320762 │
│ OMDB   │  308855 │
│ UUEE   │  307098 │
│ KBOS   │  304416 │
│ LEMD   │  291787 │
│ YSSY   │  272979 │
│ KMIA   │  265121 │
│ ZGSZ   │  263497 │
│ EDDM   │  256691 │
│ WMKK   │  254264 │
│ CYYZ   │  251192 │
│ KLGA   │  248699 │
│ VHHH   │  248473 │
│ RJTT   │  243477 │
│ KBWI   │  241440 │
│ KIAD   │  239558 │
│ KIAH   │  234202 │
│ KFLL   │  223447 │
│ KDAL   │  212055 │
│ KDCA   │  207883 │
│ LIRF   │  207047 │
│ PANC   │  206007 │
│ LTFJ   │  205415 │
│ KDTW   │  204020 │
│ VABB   │  201679 │
│ OTHH   │  200797 │
│ KMDW   │  200796 │
│ KSAN   │  198003 │
│ KPDX   │  197760 │
│ SBGR   │  197624 │
│ VOBL   │  189011 │
│ LEBL   │  188956 │
│ YBBN   │  188011 │
│ LSZH   │  187934 │
│ YMML   │  187643 │
│ RCTP   │  184466 │
│ KSNA   │  180045 │
│ EGKK   │  176420 │
│ LOWW   │  176191 │
│ UUDD   │  176099 │
│ RKSI   │  173466 │
│ EKCH   │  172128 │
│ KOAK   │  171119 │
│ RPLL   │  170122 │
│ KRDU   │  167001 │
│ KAUS   │  164524 │
│ KBNA   │  163242 │
│ KSDF   │  162655 │
│ ENGM   │  160732 │
│ LIMC   │  160696 │
│ KSJC   │  159278 │
│ KSTL   │  157984 │
│ UUWW   │  156811 │
│ KIND   │  153929 │
│ ESSA   │  153390 │
│ KMCO   │  153351 │
│ KDVT   │  152895 │
│ VTBS   │  152645 │
│ CYVR   │  149574 │
│ EIDW   │  148723 │
│ LFPO   │  143277 │
│ EGSS   │  140830 │
│ KAPA   │  140776 │
│ KHOU   │  138985 │
│ KTPA   │  138033 │
│ KFFZ   │  137333 │
│ NZAA   │  136092 │
│ YPPH   │  133916 │
│ RJBB   │  133522 │
│ EDDL   │  133018 │
│ ULLI   │  130501 │
│ KIWA   │  127195 │
│ KTEB   │  126969 │
│ VOMM   │  125616 │
│ LSGG   │  123998 │
│ LPPT   │  122733 │
│ WSSS   │  120493 │
│ EBBR   │  118539 │
│ VTBD   │  118107 │
│ KVNY   │  116326 │
│ EDDT   │  115122 │
│ EFHK   │  114860 │
└────────┴─────────┘

100 rows in set. Elapsed: 2.175 sec. Processed 48.35 million rows, 628.35 MB (22.23 million rows/s., 288.87 MB/s.)
```
Последний запрос показывате практически тоже самое время.
