import os

def split_json_file(input_file_path, chunk_size_mb=100):
    chunk_size_bytes = 1024*1024
    file_index = 0
    current_chunk_size = 0

    # chunks armazenados no diretório com nome do arquivo original (sem extensão)
    output_dir = os.path.splitext(os.path.basename(input_file_path))[0]

    # cria diretório se não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(input_file_path, 'r', encoding='utf-8') as in_file:
        out_file = open((output_dir + f'/{output_dir}_chunk{file_index}.jsonl'), 'w', encoding='utf-8')

        for line in in_file:
            line_size = len(line.encode('utf-8'))
            if line_size + current_chunk_size > chunk_size_bytes:
                out_file.close()
                file_index += 1
                current_chunk_size = 0
                out_file = open((output_dir + f'/{output_dir}_chunk{file_index}.jsonl'), 'w', encoding='utf-8')
            out_file.write(line)
            current_chunk_size = line_size + current_chunk_size
        out_file.close()

path = '/home/milton/multiprocessing/2017_pt.jsonl'

split_json_file(path)