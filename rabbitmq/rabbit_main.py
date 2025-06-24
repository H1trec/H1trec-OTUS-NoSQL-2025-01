import pika

# Настройки подключения к RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters(host='localhost',
                                       port=5672,
                                       virtual_host='/',
                                       credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Имя очереди
queue_name = 'rabbit_que'

# Отправка пяти сообщений
for i in range(5):
    message = f'Python_message {i+1}'
    channel.basic_publish(exchange='', routing_key=queue_name, body=message.encode())
    print(f'Message sent: {message}')

print("All messages sent.")

# Чтение всех сообщений из очереди
def callback(ch, method, properties, body):
    print(f"Message received: {body.decode()}")

# Получаем сообщения асинхронно
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

# Запускаем цикл ожидания сообщений
try:
    # Ожидаем некоторое количество секунд, пока обрабатываются сообщения
    import time
    timeout_seconds = 5
    start_time = time.time()
    while True and time.time() < start_time + timeout_seconds:
        connection.process_data_events()
except KeyboardInterrupt:
    pass

# Закрываем соединение
connection.close()