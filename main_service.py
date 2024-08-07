import rpyc
from itertools import cycle
import os
import pickle # usar pickle.HIGHEST_PROTOCOL

class MainService(rpyc.Service):
    metadata_file_per_worker = {} # maps workers to list of chunks in that server
    metadata_worker_per_file = {} # maps a file to a list of servers that store chunks of it

    def __init__(self):
        # carregando lista de workers
        workers_list = []
        with open('workers', 'r') as workers:
            workers_list.append(workers.readline())
        self.circular_queue = cycle(workers_list)
        # ip = next(self.circular_queue)

        # carregando metadados
        if os.path.isfile("metadata_file_per_worker"):
            with open("metadata_file_per_worker", 'rb') as metadata:
                self.metadata_file_per_worker = pickle.load(metadata)
        if os.path.isfile("metadata_worker_per_file"):
            with open('metadata_worker_per_file', 'wb') as metadata:
                self.metadata_worker_per_file = pickle.load(metadata)
        
    def exposed_threaded_search_file(self, file_name, search_query):
        # process querys preventing multiple simultaneous query
        # each query will use all servers with all cores
        # one by one to avoid overloading
        pass

    def exposed_distribute_file_chunks(self):
        # divide file in chunks and send the chunks to servers in a round-robin cycling
        pass

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
