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
    
    def search_jsonl_in_memory(self, search_query: str):
        limit = 100 # limita a quantidade de resultados
        found = 0   # quantidade total de resultados
        results = list()
        search_query = search_query.upper()
        search_query = search_query.split()
        for obj in self.json_objects:
            title = obj.get('title', '')
            if not isinstance(title, str): title = ''
            maintext = obj.get('maintext', '')
            if not isinstance(maintext, str): maintext = ''
            text = title + maintext
            if all(query in text.upper() for query in search_query):
                found += 1
                if(found <= 100):
                    results.append(obj)
        return results, found
    
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
        print('Quantidade de termos de pesquisa:', len(query.split()))
        start = time.time()
        results, total = pesquisa.search_jsonl_in_memory(query)
        end = time.time()
        print(f'Tempo de pesquisa com {len(query.split())} termos: {end - start:.3f}s')
        print('Quantidade de resultados:', total)
        print('\n')