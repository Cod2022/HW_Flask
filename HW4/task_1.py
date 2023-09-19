# # Написать программу, которая скачивает изображения с заданных URL-адресов и
# сохраняет их на диск. Каждое изображение должно сохраняться в отдельном
# файле, название которого соответствует названию изображения в URL-адресе.
# � Например URL-адрес: https://example/images/image1.jpg -> файл на диске:
# image1.jpg
# � Программа должна использовать многопоточный, многопроцессорный и
# асинхронный подходы.
# � Программа должна иметь возможность задавать список URL-адресов через
# аргументы командной строки.
# � Программа должна выводить в консоль информацию о времени скачивания
# каждого изображения и общем времени выполнения программы

import threading
import time
import os
import urllib.request 
from urllib.parse import urlparse
from multiprocessing import Process, Pool

urls = ['https://mykaleidoscope.ru/x/uploads/posts/2022-10/1666361425_1-mykaleidoscope-ru-p-peizazhi-prirodi-krasivo-1.jpg',
        'https://mykaleidoscope.ru/x/uploads/posts/2022-10/1666365069_59-mykaleidoscope-ru-p-krasivie-peizazhi-prirodi-oboi-67.jpg',
        'https://img2.goodfon.ru/original/2560x1698/2/15/nebo-oblaka-gory-sneg-derevya-4255.jpg']

start_time = time.time()

def sync_approach(urls):
    for url in urls:
        path = urlparse(url).path
        ext = os.path.splitext(path)
        file, extension = ext
        fl = file.split('/')
        filename = ("").join(fl[-1:]) + extension
        urllib.request.urlretrieve(url, f'sync_{filename}')
        print(f"Downloaded {url} in {time.time()-start_time:.2f} seconds")

def download_thread(url):
    path = urlparse(url).path
    ext = os.path.splitext(path)
    file, extension = ext
    fl = file.split('/')
    filename = ("").join(fl[-1:]) + extension
    urllib.request.urlretrieve(url, f'thread_{filename}')
    print(f"Downloaded {url} in {time.time()-start_time:.2f} seconds")

def download_multiprocessiong(url):
    path = urlparse(url).path
    ext = os.path.splitext(path)
    file, extension = ext
    fl = file.split('/')
    filename = ("").join(fl[-1:]) + extension
    urllib.request.urlretrieve(url, f'multiprocessing_{filename}')
    print(f"Downloaded {url} in {time.time()-start_time:.2f} seconds")

def threading_approach(urls):
    threads = []
    for url in urls:
        thread = threading.Thread(target=download_thread, args=[url])
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

def multiple_processing_approach(urls):
    processes = []
    start_time = time.time()
    for url in urls:
        process = Process(target=download_multiprocessiong, args=(url,))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    


if __name__ == '__main__':
    sync_approach(urls)
    threading_approach(urls)
    multiple_processing_approach(urls)









