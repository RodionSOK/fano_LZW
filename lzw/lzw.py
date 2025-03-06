from time import time
from os.path import getsize
from struct import *

def encode(file_name):
    NAME = file_name.split('.')
    
    start_time = time()
    
    max_table_size = pow(2, 16)
    
    fin = open(file_name, "rb")
    string = list(map(chr, fin.read()))

    dictionary_size = 256
    dictionary = {chr(i) : i for i in range(dictionary_size)}
    l = ""
    compressed_string = []

    for letter in string:
        l_plus = l + letter
        if l_plus in dictionary:
            l = l_plus
        else:
            compressed_string.append(dictionary[l])
            if len(dictionary) <= max_table_size:
                dictionary[l_plus] = dictionary_size
                dictionary_size += 1
            l = letter
            
    if l in dictionary:
        compressed_string.append(dictionary[l])
        
    fout = open(NAME[0] + '.lzw.' + NAME[-1], "wb")
    for code in compressed_string:
        fout.write(pack('>H', int(code)))
        
    fin.close()
    fout.close()
    
    end_time = time()
    return (end_time - start_time)
    
def decode(file_name):
    NAME = file_name.split('.')
    
    start_time = time()
    
    fin = open(file_name, "rb")
    compressed_string = []
    
    while True:
        rec = fin.read(2)
        if len(rec) != 2:
            break
        (data, ) = unpack('>H', rec)
        compressed_string.append(data)

    next_code = 256
    dictionary_size = 256
    decompressed_string = ""
    l = ""

    dictionary = dict([(x, chr(x)) for x in range(dictionary_size)])

    for code in compressed_string:
        if not (code in dictionary):
            dictionary[code] = l + l[0]
        decompressed_string += dictionary[code]
        if not(len(l) == 0):
            dictionary[next_code] = l + (dictionary[code][0])
            next_code += 1
        l = dictionary[code]
        
    fdecode = open("decode." + NAME[0] + '.' + NAME[-1], "w")
    for letter in decompressed_string:
        fdecode.write(letter)
        
    fin.close()
    fdecode.close()
    
    end_time = time()
    return (end_time - start_time)
    

n = int(input("Введите:\n1 - Закодировать текст.\n2 - Раскодировать текст.\n"))
file_name = input("Введите название файла:\n")
NAME = file_name.split('.')

if n == 1:
    print(f"Время кодирования: {(encode(file_name)):.6f} c.")
else:
    print(f"Время раскодирования: {(decode(file_name)):.6f} c.")
  
print(f"Коэффициент сжатия: {getsize(NAME[0] + '.lzw.' + NAME[-1]) / getsize("input.txt"):.6f}.")