'''
Цей модуль містить спільні функції, які використовуються в інших модулях.
Не призначений для самостійного виконання.
'''

import os
import time


def get_file_list(directory: str) -> list:
    '''The function traverses the directory and returns a list of files'''
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)
    return file_list


def chunkify(lst: list, n: int) -> list:
    '''Divides the list `lst` into `n` approximately equal parts'''
    return [lst[i::n] for i in range(n)]


def time_execution(func):
    '''Decorator for measuring the execution time of a function'''
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Час виконання функції '{func.__name__}': {
              execution_time:.2f} секунд")
        return result
    return wrapper


if __name__ == "__main__":
    print("Цей модуль не призначений для самостійного виконання.")
