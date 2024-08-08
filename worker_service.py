import rpyc
import multiprocessing as mp
import json
import time
import sys
import gc
import os

class WorkerService(rpyc.Service):
    def __init__(self):
        self.json_objects = {}
        #print("carregando dados pra memória")
        self.reload_memory()

    def exposed_reload_all_files(self):
        self.reload_memory()

    def segment_search(self, file_name, search_query, start_idx, end_idx, result_queue):
        #print(f'Start search between {start_idx} and {end_idx} on file {file_name}')
        start_time = time.time()
        limit = 100
        found = 0
        results = []
        search_query = search_query.upper()
        search_query = search_query.split()
        file_obj = self.json_objects[file_name]
        for idx in range(start_idx, end_idx):
            title = file_obj[idx].get('title', '')
            if not isinstance(title, str): title = ''
            maintext = file_obj[idx].get('maintext', '')
            if not isinstance(maintext, str): maintext = ''
            text = title + maintext
            if all(query in text.upper() for query in search_query):
                found += 1
                if(found <= limit):
                    results.append(file_obj[idx])
        result_queue.put((results, found))
        #print(f'finished search between {start_idx} and {end_idx}')
        #print(f'Total time: {time.time() - start_time:.2f}')
    
    def exposed_multiprocessed_search(self, file_name, search_query, n_processes=2):
        #print(f"dividindo pesquisa em {n_processes} cores")
        result_queue = mp.Queue()

        chunk_size = len(self.json_objects[file_name])//n_processes

        processes = []
        for i in range(n_processes):
            start_idx = i * chunk_size
            if i != n_processes - 1: # se for o ultimo processo
                end_idx = (i+1) * chunk_size
            else:
                end_idx = len(self.json_objects[file_name])
            #p = mp.Process(target=lambda q=result_queue: self.segment_search(file_name, search_query, start_idx, end_idx, q))
            p = mp.Process(target=self.segment_search, args=(file_name, search_query, start_idx, end_idx, result_queue))
            processes.append(p)
            #print('appending process', i)
            p.start()
            #print('starting process', i)
        
        #print('Collecting answers...')
        total = 0
        all_results = []
        for p in processes:
            answer = result_queue.get()
            total += answer[1]
            all_results.extend(answer[0])
        for p in processes:
            p.join()
        result_queue.close()
        result_queue.join_thread()
        return all_results, total
    
    def reload_memory(self):
        #print("reload_memory")
        self.json_objects.clear()
        gc.collect()
        # OBRIGATORIAMENTE OS DIRETORIO PARA ABRIGAR OS CHUNKS E APENAS
        # ELES, DEVEM TERMINAR COM '.jsonl'
        directiories = [dir for dir in os.listdir() if dir.endswith('.jsonl')]
        for dir in directiories:
            chunk_names = os.listdir(dir)
            json_list = []
            for chunk in chunk_names:
                path = os.path.join(dir, chunk)
                with open(path, 'r') as file:
                    for line in file:
                        json_list.append(json.loads(line))
            self.json_objects[dir] = json_list

    def exposed_persist_chunk(self, output_dir, chunk_name, chunk):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(os.path.join(output_dir, chunk_name), 'w', encoding='utf-8') as file:
            for line in chunk:
                file.write(line)

    def exposed_hello_world_worker(self):
        return "Hello world from worker server"
    
    def on_connect(self, conn):
        pass

    def on_disconnect(self, conn):
        pass



if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(WorkerService(), port=18862)
    print("WorkerService listening on", 18862)
    t.start()