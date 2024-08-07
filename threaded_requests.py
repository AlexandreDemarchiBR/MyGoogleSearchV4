import rpyc
from concurrent.futures import ThreadPoolExecutor
import threading

class MainServerService(rpyc.Service):
    def __init__(self):
        self.lock = threading.Lock()

    def exposed_call_workers(self, workers):
        with self.lock:
            with ThreadPoolExecutor(max_workers=len(workers)) as executor:
                future_to_worker = {
                    executor.submit(self.call_worker, host, port): (host, port) 
                    for host, port in workers
                }
                results = {}
                for future in future_to_worker:
                    host, port = future_to_worker[future]
                    try:
                        result = future.result()
                    except Exception as exc:
                        results[(host, port)] = f'Error: {exc}'
                    else:
                        results[(host, port)] = result
                return results

    def call_worker(self, host, port):
        conn = rpyc.connect(host, port)
        result = conn.root.remote_method()  # remote_method is the method exposed by the worker
        conn.close()
        return result

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    server = ThreadedServer(MainServerService, port=18861)
    server.start()