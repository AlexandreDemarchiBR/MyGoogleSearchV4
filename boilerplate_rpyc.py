import rpyc

class MyService(rpyc.Service):
    def on_connect(self, conn):
        # code that runs when a connection is created
        # (to init the service, if needed)
        pass

    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # (to finalize the service, if needed)
        pass

    def exposed_get_answer(self): # this is an exposed method
        return 42

    exposed_the_real_answer_though = 43     # an exposed attribute

    def get_question(self):  # while this method is not exposed
        return "what is the airspeed velocity of an unladen swallow?"

# ... continuing the code snippet from above ...


'''
if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    
    t = ThreadedServer(MyService, port=18861) # cada conexão tem seu proprio objeto

    t = ThreadedServer(MyService(), port=18861) # toda conexão compartilha mesmo objeto

    from rpyc.utils.helpers import classpartial
    service = classpartial(MyService, 1, 2, pi=3)   # cada conexão tem seu próprio objeto
    t = ThreadedServer(service, port=18861)         # mas com parametros passados pelo classpartial
    t.start()

'''