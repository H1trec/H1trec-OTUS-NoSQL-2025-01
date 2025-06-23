from confluent_kafka import Producer, Consumer

# Настройки Kafka брокера
bootstrap_servers = '192.168.56.1:9092'  # Адрес Kafka сервера
topic_name = 'PythonTopic' # Задаем имя топика


def delivery_report(err, msg):
    # Обработчик ошибок
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to topic {msg.topic()} at partition [{msg.partition()}] offset {msg.offset()}')


# Отправка сообщений в Kafka
producer = Producer({'bootstrap.servers': bootstrap_servers})
for i in range(3):
    producer.produce(topic=topic_name, value=f'python_message_{i}', callback=delivery_report)

# Ждем завершения отправки всех сообщений
producer.flush()

# Чтение сообщений из Kafka
consumer = Consumer({
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'my_group',
    'auto.offset.reset': 'earliest'  # Читаем начиная с самого начала топика
})

try:
    consumer.subscribe([topic_name])
    while True:
        message = consumer.poll(timeout=1.0)
        if message is None:
            continue
        if message.error():
            print(f'Consumer error: {message.error()}')
            break
        else:
            print(f'Received message: {message.value().decode("utf-8")}')
finally:
    consumer.close()