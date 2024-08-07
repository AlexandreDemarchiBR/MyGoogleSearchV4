import multiprocessing as mp
import json
import time
import sys


class LoadAndSearchMonothread():

    def __init__(self) -> None:
        self.json_objects = []

    def load_jsonl_to_memory(self, jsonl_file_path):
        with open(jsonl_file_path, 'r') as file:
            lines = file.readlines()

        self.json_objects = [json.loads(line) for line in lines]
    
    def search_jsonl_in_memory(self, search_query, start_idx, end_idx, result_queue):
        print(f'start search between {start_idx} and {end_idx}')
        limit = 100 # limita a quantidade de resultados
        found = 0   # quantidade total de resultados
        results = list()
        search_query = search_query.upper()
        search_query = search_query.split()
        for idx in range(start_idx, end_idx):
            title = self.json_objects[idx].get('title', '')
            if not isinstance(title, str): title = ''
            maintext = self.json_objects[idx].get('maintext', '')
            if not isinstance(maintext, str): maintext = ''
            text = title + maintext
            if all(query in text.upper() for query in search_query):
                found += 1
                if(found <= limit):
                    results.append(self.json_objects[idx])
        print(f'finished search between {start_idx} and {end_idx}')
        result_queue.put((results, found))
    
    def paralel_search(self, search_query, n_processes):
        result_queue = mp.Queue()

        chunk_size = len(self.json_objects)//n_processes

        processes = []
        for i in range(n_processes):
            start_idx = i * chunk_size
            if i != n_processes - 1: # se for o ultimo processo
                end_idx = (i+1) * chunk_size
            else:
                end_idx = len(self.json_objects)
            p = mp.Process(target=lambda q=result_queue: self.search_jsonl_in_memory(search_query, start_idx, end_idx, q))
            processes.append(p)
            print('appending process', i)
            p.start()
            print('starting process', i)
        
        print('Collecting answers...')
        total = 0
        all_results = []
        for p in processes:
            answer = result_queue.get()
            total += answer[1]
            all_results.extend(answer[0])
        for p in processes:
            p.join()

        return all_results, total
    
    def get_size_of_loaded_jsonl(self):
        return sys.getsizeof(self.json_objects), len(self.json_objects)




if __name__ == '__main__':
    pesquisa = LoadAndSearchMonothread()
    size, items = pesquisa.get_size_of_loaded_jsonl()
    print('Tamanho antes do carregamento:', size)
    start = time.time()
    pesquisa.load_jsonl_to_memory('2017_pt.jsonl')
    end = time.time()
    print(f'Tempo de carregamento do db: {end - start:.3f}s')
    size, items = pesquisa.get_size_of_loaded_jsonl()
    print('Tamanho do objeto carregado:', size)
    print('Quantidade de itens no objeto', items)
    print('\n')

    while True:
        print('#' * 30)
        query = input('Palavras chave (q - sair) > ')
        if query.strip() == 'q': break
        n_processes = int(input('Quantidade de processos >'))
        
        print('Quantidade de termos de pesquisa:', len(query.split()))
        start = time.time()
        results, total = pesquisa.paralel_search(query, n_processes)
        end = time.time()
        print(f'Tempo de pesquisa com {len(query.split())} termos: {end - start:.3f}s')
        print('Quantidade de resultados:', total)
        print('\n')