'''
Модуль паралельно обробляє та аналізує текстові файли
для пошуку визначених ключових слів з використанням threading
для багатопотокового програмування
'''

import os
import threading
import multiprocessing


def get_file_list(directory: str) -> list:
    '''The function traverses the directory and returns a list of files'''
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)
    return file_list


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


def chunkify(lst: list, n: int) -> list:
    '''Divides the list `lst` into `n` approximately equal parts'''
    return [lst[i::n] for i in range(n)]


def find_word_in_chunk(word, files_chunk, result_lock, result):
# def find_word_in_chunk(word, files_chunk, result):
    '''Find word in chunk of file list'''
    for file_path in files_chunk:
        find_word_in_file(word, file_path, result, result_lock)


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

    return result


WORD = "error"
PATH = "/var/log"

def main():
    result = find_word_multithread(WORD, PATH)
    print(result)


if __name__ == "__main__":
    main()
