import rpyc

class Client:
    def __init__(self):
        self.conn = rpyc.connect('localhost', 18861)
        self.conn = self.conn.root

    def upload_file(self, file_name):
        pass

    def search_file(self, search_query, file_name='all'):
        self.conn.threaded_search_file(self, file_name, search_query)

    def list_files(self):
        pass

    def show_results(self):
        pass

if __name__ == "__main__":
    client = Client()
    #client.upload_file()
    #client.search_file()