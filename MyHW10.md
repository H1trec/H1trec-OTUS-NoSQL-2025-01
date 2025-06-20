### Использование neo4j

#### Создание модели

Создадим следующие типы узлов:   

* Туристический оператор (TourOperator)
* Страна (Country)
* Место отдыха (Location)
* Город (City)   

Также будем создавать отношения:   

* PROVIDES_TOURS_TO — отношение оператора к месту отдыха
* IN_COUNTRY — связь места отдыха с конкретной страной
* NEARBY_CITY — обозначение ближайшего города рядом с местом отдыха
* TRANSPORT_ROUTE — транспортная связь между двумя городами с указанием вида транспорта.


```

//Создаем туристических операторов

CREATE (:TourOperator {name:"TUI"});
CREATE (:TourOperator {name:"Pegas Touristik"});
CREATE (:TourOperator {name:"Coral Travel"});
CREATE (:TourOperator {name:"Anex Tour"});

// Создаем Страны и места отдыха
CREATE (:Country {name:'Россия'});
CREATE (:Location {name:'Алтай', country:'Россия'});
CREATE (:Location {name:'Байкал', country:'Россия'});
CREATE (:Location {name:'Камчатка', country:'Россия'});
CREATE (:Location {name:'Краснодарский край', country:'Россия'});
CREATE (:Location {name:'Крым', country:'Россия'});
CREATE (:Country {name:'Турция'});
CREATE (:Location {name:'Анталия', country:'Турция'});
CREATE (:Location {name:'Кемер', country:'Турция'});
CREATE (:Location {name:'Белек', country:'Турция'});
CREATE (:Country {name:'Испания'});
CREATE (:Location {name:'Барселона', country:'Испания'});
CREATE (:Country {name:'Италия'});
CREATE (:Location {name:'Рим', country:'Италия'});
CREATE (:Country {name:'Мальдивы'});
CREATE (:Location {name:'Атолл Ари', country:'Мальдивы'});
CREATE (:Country {name:'Греция'});
CREATE (:Location {name:'Крит', country:'Греция'});
CREATE (:Country {name:'Франция'});
CREATE (:Location {name:'Прованс', country:'Франция'});

//Связываем места отдыха со странами

MATCH (c:Country), (l:Location)
WHERE l.country = c.name
MERGE (l)-[:IN_COUNTRY]->(c);

// Для каждого места отдыха создаем ближайший город с транспортным узлом
CREATE (:City {name:'Горно-Алтайск', hasAirport:true, hasRailwayStation:true, hasBusStation:true});
CREATE (:City {name:'Иркутск', hasRailwayStation:true, hasBusStation:true});
CREATE (:City {name:'Анталья', hasAirport:true, hasBusStation:true});
CREATE (:City {name:'Аланья', hasAirport:true, hasPort:true, hasBusStation:true}); 
CREATE (:City {name:'Петропавловск-Камчатский', hasAirport:true});
CREATE (:City {name:'Адлер', hasAirport:true, hasRailwayStation:true, hasBusStation:true});
CREATE (:City {name:'Симферополь', hasAirport:true, hasRailwayStation:true, hasBusStation:true});
CREATE (:City {name:'Мале', hasAirport:true}); 
CREATE (:City {name:'Ираклион', hasAirport:true, hasBusStation:true}); 
CREATE (:City {name:'Марсель', hasAirport:true, hasRailwayStation:true, hasBusStation:true}); 
// Связываем места отдыха и города
MATCH (l:Location),(c:City)
WHERE l.name='Алтай' AND c.name='Горно-Алтайск'
MERGE (l)-[:NEARBY_CITY]->(c);
MATCH (l:Location),(c:City)
WHERE l.name='Байкал' AND c.name='Иркутск'
MERGE (l)-[:NEARBY_CITY]->(c);
MATCH (l:Location),(c:City)
WHERE l.name='Камчатка' AND c.name='Петропавловск-Камчатский'
MERGE (l)-[:NEARBY_CITY]->(c);
MATCH (l:Location),(c:City)
WHERE l.name='Краснодарский край' AND c.name='Адлер'
MERGE (l)-[:NEARBY_CITY]->(c);
MATCH (l:Location),(c:City)
WHERE l.name='Крым' AND c.name='Симферополь'
MERGE (l)-[:NEARBY_CITY]->(c);
MATCH (l:Location),(c:City)
WHERE l.name='Атолл Ари' AND c.name='Мале'
MERGE (l)-[:NEARBY_CITY]->(c);
MATCH (l:Location),(c:City)
WHERE l.name='Крит' AND c.name='Ираклион'
MERGE (l)-[:NEARBY_CITY]->(c);
MATCH (l:Location),(c:City)
WHERE l.name='Прованс' AND c.name='Марсель'
MERGE (l)-[:NEARBY_CITY]->(c);
// Содаем маршруты:
Автобусные маршруты:
MATCH (c1:City),(c2:City)
WHERE c1.hasBusStation=true AND c2.hasBusStation=true
AND ID(c1) > ID(c2) 
AND NOT ((c1)-[:TRANSPORT_ROUTE {type:'bus'}]->(c2))
MERGE (c1)-[:TRANSPORT_ROUTE {type:'bus'}]->(c2);

MATCH (c1:City),(c2:City)
WHERE c1.hasBusStation=true AND c2.hasBusStation=true
AND ID(c1) < ID(c2) 
AND NOT ((c1)-[:TRANSPORT_ROUTE {type:'bus'}]->(c2))
MERGE (c1)-[:TRANSPORT_ROUTE {type:'bus'}]->(c2);


Железнодорожные маршруты:

MATCH (c1:City),(c2:City)
WHERE c1.hasRailwayStation=true AND c2.hasRailwayStation=true
AND ID(c1) > ID(c2) 
AND NOT ((c1)-[:TRANSPORT_ROUTE {type:'train'}]->(c2))
MERGE (c1)-[:TRANSPORT_ROUTE {type:'train'}]->(c2);


MATCH (c1:City),(c2:City)
WHERE c1.hasRailwayStation=true AND c2.hasRailwayStation=true
AND ID(c1) < ID(c2) 
AND NOT ((c1)-[:TRANSPORT_ROUTE {type:'train'}]->(c2))
MERGE (c1)-[:TRANSPORT_ROUTE {type:'train'}]->(c2);

Авиарейсы:
MATCH (c1:City), (c2:City)
WHERE c1.hasAirport=TRUE AND c2.hasAirport=TRUE
AND ID(c1) < ID(c2)  
AND NOT ((c1)-[:TRANSPORT_ROUTE {type:'airplane'}]->(c2))
MERGE (c1)-[:TRANSPORT_ROUTE {type:'airplane'}]->(c2);

MATCH (c1:City), (c2:City)
WHERE c1.hasAirport=TRUE AND c2.hasAirport=TRUE
AND ID(c1) > ID(c2)  
AND NOT ((c1)-[:TRANSPORT_ROUTE {type:'airplane'}]->(c2))
MERGE (c1)-[:TRANSPORT_ROUTE {type:'airplane'}]->(c2);
```

#### Запрос, который бы выводил направление (со всеми промежуточными точками), который можно осуществить только наземным транспортом.
Сам запрос:   
```
MATCH (startCity:City {name: 'Иркутск'}),
      (endCity:City {name: 'Симферополь'})
CALL {
  WITH startCity, endCity
  MATCH path=(startCity)-[:TRANSPORT_ROUTE*..10]->(endCity)
  WHERE ALL(r IN relationships(path) WHERE r.type IN ['bus', 'train'])
  RETURN path
}
RETURN startCity.name AS StartCity, [node IN nodes(path) | node.name] AS RoutePath, endCity.name AS EndCity
LIMIT 10
```
План запроса:
![PLAN_BEFORE](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/plan_before.png?raw=true)
Создаем индексы:   

```
CREATE INDEX FOR ()-[r:TRANSPORT_ROUTE]-() ON (r.type);
CREATE INDEX FOR (c:City) ON (c.name);
```

План запроса после создания индексов:
![PLAN_AFTER](https://github.com/H1trec/H1trec-OTUS-NoSQL-2025-01/blob/main/plan_after.png?raw=true)

Видим, что после доавления индексов произошла оптимизацияи запрос встал на индексы.
