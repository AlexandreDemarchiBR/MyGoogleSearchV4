import rpyc
import multiprocessing as mp

class WorkerService(rpyc.Service):
    def __init__(self):
        pass

    def 


    def on_connect(self, conn):
        pass

    def on_disconnect(self, conn):
        pass



if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(WorkerService(), port=18862)
    t.start()