import random
import string
import time
import redis

# Настройка подключения к Redis
r = redis.Redis(host='192.168.56.1', port=6379, db=0)

# Функция для генерации случайных строк
def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

# Генерация JSON 
def generate_large_json():
    num_objects = 20 * 1024 * 1024 // 100  # ~20 МБ
    data = []
    for _ in range(num_objects):
        obj = {
            "id": generate_random_string(10),
            "name": generate_random_string(20),
            "description": generate_random_string(50),
            "score": random.random(), 
            "timestamp": int(time.time()) 
        }
        data.append(obj)
    return data

# Главная процедура
def main():
  
    large_json = generate_large_json()

 
    print("=== НАЧАЛО ТЕСТОВ ===\n")


    r.flushdb()

    # ------------------ ЗАПИСЬ ДАННЫХ В REDIS ------------------
    print("ЗАПИСЬ ДАННЫХ В REDIS...\n")

   
    chunk_size = len(large_json) // 100  

    # ------- Строки -------
    start_time = time.time()
    chunks = [large_json[i:i+chunk_size] for i in range(0, len(large_json), chunk_size)]
    iteration_times = []  # список временных интервалов каждой итерации
    for idx, chunk in enumerate(chunks):
        start_iter_time = time.time()
        r.set(f'string_chunk_{idx}', str(chunk))
        iteration_times.append(time.time() - start_iter_time)
    print(f'[STRINGS]: Время записи: {sum(iteration_times):.4f} секунд')
    print(f'Средняя продолжительность итерации: {sum(iteration_times)/len(iteration_times):.4f} секунд')

    # ------- HASH------
    start_time = time.time()
    iteration_times = []
    for obj in large_json:
        start_iter_time = time.time()
        r.hset("hset_data", obj["id"], str(obj))
        iteration_times.append(time.time() - start_iter_time)
    print(f'[HASH]: Время записи: {sum(iteration_times):.4f} секунд')
    print(f'Средняя продолжительность итерации: {sum(iteration_times)/len(iteration_times):.4f} секунд')

    # ------- SORTED SET -------
    start_time = time.time()
    iteration_times = []
    for obj in large_json:
        start_iter_time = time.time()
        r.zadd("zset_data", {obj["id"]: obj["score"]})
        iteration_times.append(time.time() - start_iter_time)
    print(f'[SORTED SET]: Время записи: {sum(iteration_times):.4f} секунд')
    print(f'Средняя продолжительность итерации: {sum(iteration_times)/len(iteration_times):.4f} секунд')

    # ------- LIST -------
    start_time = time.time()
    iteration_times = []
    for obj in large_json:
        start_iter_time = time.time()
        r.rpush("list_data", str(obj))
        iteration_times.append(time.time() - start_iter_time)
    print(f'[LIST]: Время записи: {sum(iteration_times):.4f} секунд')
    print(f'Средняя продолжительность итерации: {sum(iteration_times)/len(iteration_times):.4f} секунд')


    print("\nЧТЕНИЕ ДАННЫХ ИЗ REDIS...\n")

    # ------- Строки -------
    start_time = time.time()
    iteration_times = []
    for i in range(len(chunks)):
        start_iter_time = time.time()
        r.get(f'string_chunk_{i}')
        iteration_times.append(time.time() - start_iter_time)
    print(f'[STRINGS]: Время чтения: {sum(iteration_times):.4f} секунд')
    print(f'Средняя продолжительность итерации: {sum(iteration_times)/len(iteration_times):.4f} секунд')

    # ------- HASH -------
    start_time = time.time()
    iteration_times = []
    for obj_id in r.hkeys("hset_data"):
        start_iter_time = time.time()
        r.hget("hset_data", obj_id)
        iteration_times.append(time.time() - start_iter_time)
    print(f'[HASH]: Время чтения: {sum(iteration_times):.4f} секунд')
    print(f'Средняя продолжительность итерации: {sum(iteration_times)/len(iteration_times):.4f} секунд')

    # ------- SORTED SET -------
    start_time = time.time()
    iteration_times = []
    members = r.zrange("zset_data", 0, -1)
    for member in members:
        start_iter_time = time.time()
        r.zscore("zset_data", member)
        iteration_times.append(time.time() - start_iter_time)
    print(f'[SORTED SET]: Время чтения: {sum(iteration_times):.4f} секунд')
    print(f'Средняя продолжительность итерации: {sum(iteration_times)/len(iteration_times):.4f} секунд')

    # ------- LIST -------
    start_time = time.time()
    iteration_times = []
    elements = r.lrange("list_data", 0, -1)
    for element in elements:
        start_iter_time = time.time()
        pass  # Просто проходим по каждому элементу списка
        iteration_times.append(time.time() - start_iter_time)
    print(f'[LIST]: Время чтения: {sum(iteration_times):.4f} секунд')
    print(f'Средняя продолжительность итерации: {sum(iteration_times)/len(iteration_times):.4f} секунд')

    print("\n=== КОНЕЦ ТЕСТОВ ===")

if __name__ == "__main__":
    main()
