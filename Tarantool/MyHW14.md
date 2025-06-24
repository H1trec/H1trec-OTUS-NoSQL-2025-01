### Tarantool

#### Установка в Docker
```
daemom@OVMCOUCH:/usr/src/rabbitmq$ sudo docker run \
>   --name app-instance-001 \
>   -p 3301:3301 -d \
>   -v /path/to/my/app/instances.enabled:/opt/tarantool \
>   -e TT_APP_NAME=app \
>   -e TT_INSTANCE_NAME=instance-001 \
>   tarantool/tarantool
Unable to find image 'tarantool/tarantool:latest' locally
latest: Pulling from tarantool/tarantool
30a9c22ae099: Already exists
4f4fb700ef54: Pull complete
dd7604b60cef: Pull complete
3ffcc8cb79c8: Pull complete
2ad9de05e464: Pull complete
37df4f6ff5eb: Pull complete
87131f2c8d0c: Pull complete
235151f83eda: Pull complete
4fc8fd674ab0: Pull complete
9f5a3dce6278: Pull complete
Digest: sha256:0766d446ef48d96a21b1b451620b68d34300631c055776405c7af631eda16efc
Status: Downloaded newer image for tarantool/tarantool:latest
a0e11ed1829f3c6ba4974c2287758f13a4cd970d6a2d80f5ba88098d82457ef5
daemom@OVMCOUCH:/usr/src/rabbitmq$ sudo docker ps
CONTAINER ID   IMAGE                 COMMAND                  CREATED          STATUS                             PORTS                                         NAMES
a0e11ed1829f   tarantool/tarantool   "/docker-entrypoint.…"   25 seconds ago   Up 21 seconds (health: starting)   0.0.0.0:3301->3301/tcp, [::]:3301->3301/tcp   app-instance-001
```

#### Создание структуры

Спейс:
```
/var/run/tarantool/sys_env/app/instance-001/tarantool.control> box.schema.space.create('flights', {
    format = {
        {'id', 'unsigned'},
        {'airline', 'string'},
        {'departure_date', 'string'},
        {'departure_city', 'string'},
        {'arrival_city', 'string'},
        {'min_price', 'number'}
    }
})
---
- is_local: false
  engine: memtx
  before_replace: 'function: 0x715ca9b2f548'
  field_count: 0
  is_sync: false
  on_replace: 'function: 0x715ca9b2f510'
  state:
    is_sync: false
  temporary: false
  index: []
  type: normal
  enabled: false
  name: flights
  id: 512
- created
...
```
Первичный индекс:
```
/var/run/tarantool/sys_env/app/instance-001/tarantool.control> box.space.flights:create_index('primary', {parts={'id'}})
---
- unique: true
  parts:
  - fieldno: 1
    sort_order: asc
    type: unsigned
    exclude_null: false
    is_nullable: false
  hint: true
  id: 0
  type: TREE
  space_id: 512
  name: primary
...
```

Вторичный индекс:
```
/var/run/tarantool/sys_env/app/instance-001/tarantool.control> box.space.flights:create_index('secondary', {
    parts = {'departure_date', 'airline', 'departure_city'}
})
---
- unique: true
  parts:
  - fieldno: 3
    sort_order: asc
    type: string
    exclude_null: false
    is_nullable: false
  - fieldno: 2
    sort_order: asc
    type: string
    exclude_null: false
    is_nullable: false
  - fieldno: 4
    sort_order: asc
    type: string
    exclude_null: false
    is_nullable: false
  hint: true
  id: 1
  type: TREE
  space_id: 512
  name: secondary
...
```

Наполнение данными:
```
/var/run/tarantool/sys_env/app/instance-001/tarantool.control> box.space.flights:insert({1, 'Аэрофлот', '2025-01-01', 'Москва', 'Санкт-Петербург', 2800})
box.space.flights:insert({2, 'S7 Airlines', '2025-01-01', 'Москва', 'Сочи', 6500})
box.space.flights:insert({3, 'SmartAvia', '2025-01-01', 'Казань', 'Екатеринбург', 3500})
box.space.flights:insert({4, 'Победа', '2025-01-01', 'Санкт-Петербург', 'Калининград', 2900})
box.space.flights:insert({5, 'Уральские Авиалинии', '2025-01-01', 'Казань', 'Екатеринбург', 2500})
box.space.flights:insert({6, 'Аэрофлот', '2025-01-01', 'Санкт-Петербург', 'Екатеринбург', 4500})
box.space.flights:insert({7, 'Победа', '2025-01-01', 'Москва', 'Новосибирск', 7500})
box.space.flights:insert({8, 'Аэрофлот', '2025-01-01', 'Новосибирск', 'Омск', 2800})
box.space.flights:insert({9, 'Победа', '2025-01-01', 'Омск', 'Москва', 7500})
---
...
```

#### Работа с данными

Запрос на поиск минимальной цены:
```
/var/run/tarantool/sys_env/app/instance-001/tarantool.control> local flights_on_2025_01_01 = box.space.flights.index.secondary:select({'2025-01-01'})

local min_price_tuple = nil
for _, tuple in ipairs(flights_on_2025_01_01) do
    if not min_price_tuple or tuple[6] < min_price_tuple[6] then
        min_price_tuple = tuple
    end
end

return min_price_tuple
---
- [5, 'Уральские Авиалинии', '2025-01-01', 'Казань', 'Екатеринбург', 2500]
...
```
![query](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/Tarantool/query.JPG?raw=true)
Функция поиска билетов с ценой менее 3000:
```
/var/run/tarantool/sys_env/app/instance-001/tarantool.control> function cheap_flights()
    local result = {}
    for _, tuple in box.space.flights:pairs() do
        if tuple.min_price < 3000 then
            table.insert(result, tuple)
        end
    end
    return result
end
---
...
/var/run/tarantool/sys_env/app/instance-001/tarantool.control> cheap_flights()
---
- - [1, 'Аэрофлот', '2025-01-01', 'Москва', 'Санкт-Петербург', 2800]
  - [4, 'Победа', '2025-01-01', 'Санкт-Петербург', 'Калининград', 2900]
  - [5, 'Уральские Авиалинии', '2025-01-01', 'Казань', 'Екатеринбург', 2500]
  - [8, 'Аэрофлот', '2025-01-01', 'Новосибирск', 'Омск', 2800]
...
```
![func](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/Tarantool/func.JPG?raw=true)
