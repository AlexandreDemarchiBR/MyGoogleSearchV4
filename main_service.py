import rpyc
from itertools import cycle
import os
import pickle # usar pickle.HIGHEST_PROTOCOL
import threading

class MainService(rpyc.Service):
    metadata_file_per_worker = {} # maps workers to list of chunks in that server
    metadata_worker_per_file = {} # maps a file to a list of servers that store chunks of it

    def __init__(self):
        # lock para atender 1 request por vez
        self.lock = threading.Lock()
        # carregando lista de workers
        self.workers_list = []
        with open('workers', 'r') as workers:
            self.workers_list = [line.strip() for line in workers.readlines()]
        self.circular_queue = cycle(self.workers_list)
        # ip = next(self.circular_queue)

        # carregando metadados
        if os.path.isfile("metadata_file_per_worker"):
            with open("metadata_file_per_worker", 'rb') as metadata:
                self.metadata_file_per_worker = pickle.load(metadata)
        if os.path.isfile("metadata_worker_per_file"):
            with open('metadata_worker_per_file', 'rb') as metadata:
                self.metadata_worker_per_file = pickle.load(metadata)
        
        # criar conexões
        
        self.conns = {}
        for worker in self.workers_list:
            conn = rpyc.connect(worker, 18862)
            self.conns[worker] = conn

        
    def exposed_threaded_search_file(self, search_query, file_name):
        # process querys preventing multiple simultaneous query
        # each query will use all servers with all cores
        # one by one to avoid overloading
        print('Adquirindo lock')
        with self.lock:
            threads = []
            self.thread_results = [1] * len(self.metadata_worker_per_file[file_name])
            print('maquinas que possuem o arquivo', self.metadata_worker_per_file[file_name])
            i = 0
            for worker in self.metadata_worker_per_file[file_name]:
                thread = threading.Thread(target=self.call_worker, args=(file_name, search_query, worker, i))
                threads.append(thread)
                print(f'iniciando thread em {worker} indice {i}')
                thread.start()
                i += 1
            for thread in threads:
                thread.join()
        total = 0
        results = []
        print(type(self.thread_results))
        for result in self.thread_results:
            total += result[1]
            results += result[0]
        return results
    
    # manda uma pesquisa pra ser feita pelo worker
    def call_worker(self, file_name, search_query, worker, i):
        print('file_name', file_name)
        print('search_query', search_query)
        print('worker', worker)
        print('i', i)
        print('call_worker em:', worker)
        print(self.thread_results)
        conn = self.conns[worker]
        results, total = conn.root.multiprocessed_search(file_name, search_query, 2)
        self.thread_results[i] = (results, total)

    def exposed_distribute_file_chunks(self, original_name, chunk_name, chunk):
        # send the chunks to servers in a round-robin cycling
        # update metadata_file_per_worker
        # update metadata_worker_per_file
        worker = next(self.circular_queue)
        conn = self.conns[worker]
        conn.root.persist_chunk(original_name, chunk_name, chunk)
        
        if worker not in self.metadata_file_per_worker:
            self.metadata_file_per_worker[worker] = set()
        self.metadata_file_per_worker[worker].add(chunk_name)

        if original_name not in self.metadata_worker_per_file:
            self.metadata_worker_per_file[original_name] = set()
        self.metadata_worker_per_file[original_name].add(worker)

        self.persist_metadata()

    def persist_metadata(self):
            with open("metadata_file_per_worker", 'wb') as metadata:
                pickle.dump(self.metadata_file_per_worker, metadata)
            with open('metadata_worker_per_file', 'wb') as metadata:
                pickle.dump(self.metadata_worker_per_file, metadata)
    
    def exposed_show_metadata(self):
        # se imprimir as duas, por algum motivo o cliente bloqueia
        msg = self.metadata_file_per_worker.__str__()
        #msg = self.metadata_worker_per_file.__str__()
        return msg

    def exposed_hello_world_main(self):
        return "Hello world from main server"
    
    def exposed_hello_world_workers(self):
        msg = ''
        count = 1
        for worker in self.workers_list:
            conn = self.conns[worker]
            hello = conn.root.hello_world_worker()
            msg += f'{hello} {worker}'
            msg += '\n'
        return msg

    def exposed_list_files(self):
        # list available files to search
        pass

    def exposed_remove_files(self):
        # deletes a file from the server
        pass

    def on_connect(self, conn):
        pass

    def on_disconnect(self, conn):
        pass


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(MainService(), port=18861)
    print("MainService listening on", 18861)
    t.start()
