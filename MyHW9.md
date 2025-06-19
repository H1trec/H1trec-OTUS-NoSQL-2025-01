### Графовые БД

#### Примеры применения графовых БД:   
1. Социальная сеть или сервис знакомств
Пользователи социальной сети связаны множеством отношений («друзья», «подписчики», «группы»). Такие связи легко представить в виде графа, где вершины — пользователи, а рёбра — отношения между ними.  
Например:
 * Найти друзей друзей конкретного человека.   
 * Определить круг общения пользователя.   
 * Выявлять сообщества пользователей на основе общих интересов или контактов.   

2. Логистика и управление цепочками поставок
Крупные ритейлеры и транспортные компании ежедневно сталкиваются с необходимостью эффективного планирования маршрутов транспортировки товаров.
Представляя географические точки и объекты инфраструктуры в виде вершин графа, графовая база данных упрощает вычисление оптимального маршрута, минимизируя затраты на транспортировку и ускоряя доставку продукции конечному потребителю.

#### Тестовый пример.
Рассмотрим случай библиотеки, в которой мы хотим хранить информацию о книгах, авторе, издателях и читателях.   

Модель данных:   
##### PostgreSQL:
Таблица	
Описание 
------------------------
|authors	|  Авторы книг|
|books	  |  Книги      |
|readers	|  Читатели   |
|editions |	Издательства|
------------------------

Структура таблиц:   
```
CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE books (
    isbn VARCHAR(13) PRIMARY KEY,
    title TEXT NOT NULL,
    author_id INT REFERENCES authors(id),
    edition_id INT REFERENCES editions(id)
);

CREATE TABLE readers (
    reader_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL
);

CREATE TABLE editions (
    id SERIAL PRIMARY KEY,
    publisher VARCHAR(255) NOT NULL
);

-- Связующая таблица (many-to-many) между книгами и читателями
CREATE TABLE book_readers (
    isbn VARCHAR(13) REFERENCES books(isbn),
    reader_id INT REFERENCES readers(reader_id),
    PRIMARY KEY (isbn, reader_id)
);
```

##### Neo4j:
Модель представлена набором узлов и ребер, отражающих сущности и связи между ними.   

Условимся обозначать типы узлов и рёбер следующим образом:   
:Author — авторы книг   
:Book — книги   
:Reader — читатели   
:Edition — издательства   
:WROTE — связь автора с книгой   
:READ_BY — связь книги с читателем   
:PUBLISHED_BY — связь книги с издательством   
Пример заполнения графовой структуры:   

```
// Добавляем авторов
MERGE (:Author {name: 'Лев Толстой'});
MERGE (:Author {name: 'Федор Достоевский'});
MERGE (:Author {name: 'Антон Чехов'});

// Добавляем книги
MERGE (:Book {title: 'Война и мир', isbn: '978-5-17-082465-3'});
MERGE (:Book {title: 'Преступление и наказание', isbn: '978-5-17-082466-0'});
MERGE (:Book {title: 'Чайка', isbn: '978-5-17-082467-7'});

// Связываем авторов с книгами
MATCH (a:Author {name: 'Лев Толстой'}), (b:Book {isbn: '978-5-17-082465-3'})
MERGE (a)-[:WROTE]->(b);
MATCH (a:Author {name: 'Федор Достоевский'}), (b:Book {isbn: '978-5-17-082466-0'})
MERGE (a)-[:WROTE]->(b);
MATCH (a:Author {name: 'Антон Чехов'}), (b:Book {isbn: '978-5-17-082467-7'})
MERGE (a)-[:WROTE]->(b);

// Добавляем авторов
MERGE (:Author {name: 'Лев Толстой'});
MERGE (:Author {name: 'Федор Достоевский'});
MERGE (:Author {name: 'Антон Чехов'});

// Добавляем книги
MERGE (:Book {title: 'Война и мир', isbn: '978-5-17-082465-3'});
MERGE (:Book {title: 'Преступление и наказание', isbn: '978-5-17-082466-0'});
MERGE (:Book {title: 'Чайка', isbn: '978-5-17-082467-7'});

// Связываем авторов с книгами
MATCH (a:Author {name: 'Лев Толстой'}), (b:Book {isbn: '978-5-17-082465-3'})
MERGE (a)-[:WROTE]->(b);

MATCH (a:Author {name: 'Федор Достоевский'}), (b:Book {isbn: '978-5-17-082466-0'})
MERGE (a)-[:WROTE]->(b);

MATCH (a:Author {name: 'Антон Чехов'}), (b:Book {isbn: '978-5-17-082467-7'})
MERGE (a)-[:WROTE]->(b);

// Добавляем читателей
MERGE (:Reader {firstName: 'Иван', lastName: 'Иванов'});
MERGE (:Reader {firstName: 'Алексей', lastName: 'Сергеев'});
MERGE (:Reader {firstName: 'Мария', lastName: 'Петрова'});

// Связываем книги с читателями
MATCH (r:Reader {firstName: 'Иван', lastName: 'Иванов'}), (b:Book {isbn: '978-5-17-082465-3'})
MERGE (r)-[:READ_BY]->(b);

MATCH (r:Reader {firstName: 'Иван', lastName: 'Иванов'}), (b:Book {isbn: '978-5-17-082467-7'})
MERGE (r)-[:READ_BY]->(b);

MATCH (r:Reader {firstName: 'Иван', lastName: 'Иванов'}), (b:Book {isbn: '978-5-17-082466-0'})
MERGE (r)-[:READ_BY]->(b);

MATCH (r:Reader {firstName: 'Алексей', lastName: 'Сергеев'}), (b:Book {isbn: '978-5-17-082467-7'})
MERGE (r)-[:READ_BY]->(b);

MATCH (r:Reader {firstName: 'Мария', lastName: 'Петрова'}), (b:Book {isbn: '978-5-17-082466-0'})
MERGE (r)-[:READ_BY]->(b);

// Добавляем издательства
MERGE (:Edition {publisher: 'АСТ'});
MERGE (:Edition {publisher: 'Эксмо'});
MERGE (:Edition {publisher: 'Азбука'});

// Связываем книги с издательствами
MATCH (ed:Edition {publisher: 'АСТ'}), (b:Book {isbn: '978-5-17-082465-3'})
MERGE (b)-[:PUBLISHED_BY]->(ed);

MATCH (ed:Edition {publisher: 'Эксмо'}), (b:Book {isbn: '978-5-17-082466-0'})
MERGE (b)-[:PUBLISHED_BY]->(ed);

MATCH (ed:Edition {publisher: 'Азбука'}), (b:Book {isbn: '978-5-17-082467-7'})
MERGE (b)-[:PUBLISHED_BY]->(ed);
```

Примеры запросов:   
```
Пример 1: Получить список всех читателей, которые прочитали книгу Лев Толстого "Война и мир":
PostgreSQL:

SELECT r.first_name, r.last_name
FROM readers AS r
JOIN book_readers br ON r.reader_id = br.reader_id
JOIN books b ON br.isbn = b.isbn
WHERE b.title = 'Война и мир' AND EXISTS(
    SELECT *
    FROM authors a
    WHERE a.id = b.author_id AND a.name = 'Лев Толстой'
);

Neo4j:

MATCH (author:Author {name: 'Лев Толстой'})-[:WROTE]->(book:Book {title: 'Война и мир'})<-[:READ_BY]-(reader:Reader)
RETURN reader.firstName, reader.lastName;
```
Пример 2: Найти авторов, чьи книги изданы больше всего раз одним и тем же издательством:
```
PostgreSQL:

WITH AuthorEditionsCount AS (
    SELECT a.name as author_name, COUNT(DISTINCT e.publisher) as unique_publishers_count
    FROM authors a
    JOIN books b ON a.id = b.author_id
    JOIN editions e ON b.edition_id = e.id
    GROUP BY a.name
)
SELECT author_name
FROM AuthorEditionsCount
ORDER BY unique_publishers_count DESC
LIMIT 1;

Neo4j:

MATCH (author:Author)-[:WROTE]->(:Book)-[:PUBLISHED_BY]->(edition:Edition)
WITH author, COUNT(DISTINCT edition.publisher) AS publishers_count
ORDER BY publishers_count DESC
LIMIT 1
RETURN author.name AS most_published_author;
```
Пример 3: Найти все книги, которые читал конкретный читатель ("Иван Иванов"):
```
PostgreSQL:

SELECT b.title
FROM books b
JOIN book_readers br ON b.isbn = br.isbn
JOIN readers r ON br.reader_id = r.reader_id
WHERE r.first_name = 'Иван' AND r.last_name = 'Иванов';
Neo4j:

MATCH (reader:Reader {lastName: "Иванов"})-[:READ_BY]->(book:Book) RETURN book;
```
Таким образом, сравнение двух подходов показывает различия в способах организации и обработки данных. Neo4j хорошо работает с запросами, основанными на связях, тогда как SQL-ориентированная база данных эффективнее обрабатывает структурированную табличную информацию и агрегирует данные по заданным критериям.




