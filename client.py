import rpyc
import os

class Client:
    def __init__(self):
        self.conn = rpyc.connect('localhost', 18861)

    def upload_file(self, file_path, chunk_size_mb=5):
        chunk_size_bytes = 1024*1024*chunk_size_mb
        file_index = 0
        current_chunk_size = 0
        current_chunk = []
        file_orig_name = os.path.basename(file_path)
        with open(file_path, 'r', encoding='utf-8') as in_file:
            for line in in_file:
                line_size = len(line.encode('utf-8'))
                if line_size + current_chunk_size > chunk_size_bytes:
                    chunk_name = f'{file_orig_name}_chunk{file_index}.jsonl'
                    self.conn.root.distribute_file_chunks(file_orig_name, chunk_name, current_chunk)
                    file_index += 1
                    current_chunk_size = 0
                    current_chunk = []
                current_chunk.append(line)
                current_chunk_size = line_size + current_chunk_size

    def search_file(self, search_query, file_name):
        self.last_results = self.conn.root.threaded_search_file(search_query, file_name)
        print("Resultados encontrados:", len(self.last_results))

    def list_files(self):
        list = self.conn.root.list_files()
        for item in list:
            print(item)

    def show_results(self):
        message = 'Total de resultados: ' + str(len(self.last_results)) + '\n\n'
        count = 0
        for item in self.last_results:
            title = item['title'] if isinstance(item['title'], str) else 'SEM TITULO'
            description = item['description'] if isinstance(item['description'], str) else 'SEM DESCRIÇÃO'
            url = item['url'] if isinstance(item['url'], str) else 'SEM LINK'
            message += 'Título: ' + title + '\n' + 'Descrição: ' + description + '\n' + 'URL: ' + url + '\n\n'
            count += 1
            if count > 10: break
        print(message)
    def ask_hello_from_main(self):
        print(self.conn.root.hello_world_main())

    def ask_hello_from_workers(self):
        print(self.conn.root.hello_world_workers())

    def print_metadata(self):
        print(self.conn.root.show_metadata())
        
    def remove_file(self, filename):
        pass

if __name__ == "__main__":
    client = Client()
    #client.ask_hello_from_main()
    #client.ask_hello_from_workers()
    #client.print_metadata()
    #client.upload_file('2016_pt.jsonl')
    client.search_file("ola mundo" , '2016_pt.jsonl')
    print(client.show_results())
    #client.search_file()