'''
Модуль паралельно обробляє текстові файли
для пошуку визначеного слова з використанням multiprocessing
для багатопотокового програмування
'''

import multiprocessing
from common import get_file_list, chunkify, time_execution

WORD = "error"
PATH = "/var/log"

def find_word_in_file(word: str, file_path: str):
    '''The function searches for a word in a file and returns the file path if found'''
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if word in line:
                    return file_path  # Повертаємо шлях до файлу, якщо слово знайдено
    except Exception as e:
        print(f"Не вдалося відкрити файл {file_path}: {e}")
    return None


def find_word_in_chunk(word, files_chunk, queue):
    '''Searches for word in a chunk of files and sends results to Queue'''
    results = []
    for file_path in files_chunk:
        found_file = find_word_in_file(word, file_path)
        if found_file:
            results.append(found_file)

    queue.put(results)  # Відправляємо результати в Queue


@time_execution
def find_word_multiprocessing(word, directory):
    '''The function implements multi-process word search in all files in the directory'''
    result = {word: []}
    file_list = get_file_list(directory)
    num_cores = multiprocessing.cpu_count()
    file_chunks = chunkify(file_list, num_cores)

    # Створюємо чергу для передачі результатів
    queue = multiprocessing.Queue()
    processes = []

    for chunk in file_chunks:
        process = multiprocessing.Process(
            target=find_word_in_chunk, args=(word, chunk, queue))
        processes.append(process)
        process.start()

    # Збираємо результати з кожного процесу
    for process in processes:
        process.join()
        result[word].extend(queue.get())

    print(result)


if __name__ == "__main__":
    find_word_multiprocessing(WORD, PATH)
