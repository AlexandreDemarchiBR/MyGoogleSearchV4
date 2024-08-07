import rpyc
from itertools import cycle
import os
import pickle  # usar pickle.HIGHEST_PROTOCOL
from concurrent.futures import ThreadPoolExecutor
import threading

class MainService(rpyc.Service):
    metadata_file_per_worker = {}  # maps workers to list of chunks in that server
    metadata_worker_per_file = {}  # maps a file to a list of servers that store chunks of it

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
            c = rpyc.connect(worker, 18862)
            self.conns[worker] = c.root

    def exposed_threaded_search_file(self, file_name, search_query):
        # process querys preventing multiple simultaneous query
        # each query will use all servers with all cores
        # one by one to avoid overloading
        with self.lock:
            with ThreadPoolExecutor(max_workers=len(self.workers_list)) as executor:
                future_to_worker = {
                    executor.submit(self.call_worker, file_name, search_query, worker): worker for worker in self.workers_list
                }
                results = {}
                for future in future_to_worker:
                    worker = future_to_worker[future]
                    try:
                        result = future.result()
                    except Exception as exc:
                        results[worker] = f'Error: {exc}'
                    else:
                        results[worker] = result
                return results
    
    def call_worker(self, file_name, search_query, worker):
        conn = self.conns[worker]
        results, total = conn.multiprocessed_search(file_name, search_query, 2)
        return results, total

    def exposed_distribute_file_chunks(self, input_file_path, chunk_size_mb=100):
        # divide file in chunks and send the chunks to servers in a round-robin cycling
        chunk_size_bytes = 1024 * 1024 * chunk_size_mb
        file_index = 0
        current_chunk_size = 0
        current_chunk = []
        output_dir = os.path.basename(input_file_path)
        output_without_extension = os.path.splitext(output_dir)[0]
        with open(input_file_path, 'r', encoding='utf-8') as in_file:
            for line in in_file:
                line_size = len(line.encode('utf-8'))
                if line_size + current_chunk_size > chunk_size_bytes:
                    # faz a chamada
                    chunk_name = f'{output_without_extension}_chunk{file_index}.jsonl'
                    worker = next(self.circular_queue)
                    self.conns[worker].persist_chunk(output_dir, chunk_name, current_chunk)
                    file_index += 1
                    current_chunk_size = 0
                    current_chunk = []
                current_chunk.append(line)
                current_chunk_size += line_size
            # Persist the last chunk if it exists
            if current_chunk:
                chunk_name = f'{output_without_extension}_chunk{file_index}.jsonl'
                worker = next(self.circular_queue)
                self.conns[worker].persist_chunk(output_dir, chunk_name, current_chunk)

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
    t.start()
