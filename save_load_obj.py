import pickle
dict = {'alpha': '192.168.100.2', 'bravo': '192.168.100.3', 'charlie': '192.168.100.4', 'delta': '192.168.100.5', 'echo': '192.168.100.6'}

with open('dict', 'wb') as file:
    pickle.dump(dict, file, pickle.HIGHEST_PROTOCOL)

with open('dict', 'rb') as file:
    dict2 = pickle.load(file)

print(dict2)