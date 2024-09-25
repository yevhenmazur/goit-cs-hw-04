'''
Модуль паралельно обробляє текстові файли
для пошуку визначеного слова з використанням threading
для багатопотокового програмування
'''

import threading
import multiprocessing
from common import get_file_list, chunkify, time_execution

WORD = "error"
PATH = "/var/log"

def find_word_in_file(word: str, file_path: str, result, result_lock):
    '''
    The function searches for a word in a file
    and generates a list of files where the word is found
    '''

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if word in line:
                    with result_lock:
                        result[word].append(file_path)
                        break  # Вийти з файлу, якщо знайшлося
    except Exception as e:
        print(f"Не вдалося відкрити файл {file_path}: {e}")


def find_word_in_chunk(word, files_chunk, result_lock, result):
    '''Find word in chunk of file list'''
    for file_path in files_chunk:
        find_word_in_file(word, file_path, result, result_lock)


@time_execution
def find_word_multithread(word, directory):
    '''The function implements multi-threaded word search in all files in the directory'''
    result = {word: []}
    file_list = get_file_list(directory)
    num_cores = multiprocessing.cpu_count()
    file_chunks = chunkify(file_list, num_cores)
    result_lock = threading.Lock()

    # Створюємо потоки для обробки кожного чанку файлів
    threads = []
    for chunk in file_chunks:
        thread = threading.Thread(target=find_word_in_chunk, args=(
            word, chunk, result_lock, result))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(result)


if __name__ == "__main__":
    find_word_multithread(WORD, PATH)
