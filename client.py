import rpyc

class Client:
    def __init__(self):
        self.conn = rpyc.connect('localhost', 18861)
        self.conn = self.conn.root

    def upload_file(self, file_name):
        self.conn.distribute_file_chunks(file_name, 5)

    def search_file(self, search_query, file_name='all'):
        self.last_results = self.conn.threaded_search_file(self, file_name, search_query)
        print("Resultados encontrados:", len(self.last_results))

    def list_files(self):
        list = self.conn.list_files()
        for item in list:
            print(item)

    def show_results(self):
        message = 'Total de resultados: ' + len(self.last_results) + '\n\n'
        for item in self.last_results:
            title = item['title'] if isinstance(item['title'], str) else 'SEM TITULO'
            description = item['description'] if isinstance(item['description'], str) else 'SEM DESCRIÇÃO'
            url = item['url'] if isinstance(item['url'], str) else 'SEM LINK'
            message += 'Título: ' + title + '\n' + 'Descrição: ' + description + '\n' + 'URL: ' + url + '\n\n'
        print(message)

    def remove_file(self, filename):
        pass

if __name__ == "__main__":
    client = Client()
    #client.upload_file()
    #client.search_file()