import os
from minio import Minio
import urllib3

# Настройка HTTP-клиента (без SSL-проверки)
http_client = urllib3.PoolManager(cert_reqs='CERT_NONE')

# Параметры MinIO
MINIO_ENDPOINT = '192.168.56.1:9000'
ACCESS_KEY = 'admin'
SECRET_KEY = 'password123'
BUCKET_NAME = 'mypythonbucket'

# Инициализация клиента
client = Minio(
    endpoint=MINIO_ENDPOINT,
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    secure=False,
    http_client=http_client
)

# Проверка/создание бакета
if not client.bucket_exists(BUCKET_NAME):
    client.make_bucket(BUCKET_NAME)
    print(f"Бакет '{BUCKET_NAME}' создан.")
else:
    print(f"Бакет '{BUCKET_NAME}' уже существует.")

# Загрузка файлов
files_to_upload = ["./uploaded/example_file_1.txt", "./uploaded/example_file_2.txt"]
for file_path in files_to_upload:
    object_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)  # Получаем размер файла заранее

    with open(file_path, 'rb') as file_data:
        client.put_object(
            BUCKET_NAME,
            object_name,
            file_data,
            file_size  # Используем заранее вычисленный размер
        )
    print(f"Файл {object_name} загружен.")

# Скачивание файлов
DOWNLOAD_DIR = './downloaded/'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

objects = client.list_objects(BUCKET_NAME, recursive=True)
for obj in objects:
    local_path = os.path.join(DOWNLOAD_DIR, obj.object_name)
    client.fget_object(BUCKET_NAME, obj.object_name, local_path)
    print(f"Файл {obj.object_name} скачан в {local_path}.")

# Вывод списка скачанных файлов
print("\nСкачанные файлы:")
for file in os.listdir(DOWNLOAD_DIR):
    print(file)
