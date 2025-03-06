from struct import *
from time import time
from os.path import getsize
from bitarray import bitarray

class Unit():
    def __init__(self, name, value, code):
        self.name = name
        self.value = value
        self.code = code
    
def shannon_fano(list_objects):
    summ = 0
    for object in list_objects:
        summ += object.value
        
    group = summ/2
    index = 0 
    group1 = []
    group2 = []
    
    for object in list_objects:
        if index < group:
            object.code += '0'
            group1.append(object)
            index += object.value
        else:
            object.code += '1'
            group2.append(object)
            
    if len(group1) != 1:
        shannon_fano(group1)
    if len(group2) != 1:
        shannon_fano(group2)
        
    return list_objects

def encode(file_name, list_objects, string):
    NAME = file_name.split('.')
    with open(NAME[0] + '.out.' + NAME[-1], "wb") as fout:
        l = ''
        for letter in string:
            for object in list_objects:
                if object.name == letter:
                    for letter_code in object.code:
                        l += letter_code
                        if len(l) == 16:
                            fout.write(bitarray(l).tobytes())
                            l = ''
                    break
    fout.close()
    
    end_time = time()
    return end_time

def decode(file_name, list_objects):
    NAME = file_name.split('.')
    fin = open(file_name, "rb")
    compressed_data = ''
    
    while True:
        rec = fin.read(2)
        if len(rec) != 2:
            break
        (data, ) = unpack('>H', rec)
        bin_code = bin(data)[2:]
        while len(bin_code) != 16:
            bin_code = '0' + bin_code
        compressed_data += bin_code
    
    with open('deocode.' + NAME[0] + '.' + NAME[-1], "w") as fdecode:
        l = ''
        for letter in compressed_data:
            l += letter
            for object in list_objects:
                if object.code == l:
                    fdecode.write(object.name)
                    l = ''
                    break    
    fin.close()
    fdecode.close()
    
    end_time = time()
    return end_time



n = int(input("Введите:\n1 - Закодировать текст.\n2 - Раскодировать текст.\n"))
file_name = input("Введите название файла:\n")
NAME = file_name.split('.')

start_time = time()
    
fin = open(NAME[0] + '.' + NAME[-1], "rb")

string = list(map(chr, fin.read()))

alf = list(set(string))
frequency = sorted([[round(str(string).count(alf[i]), 5), i] for i in range(5)], reverse = True)

data = []
for i in range(5):
    name = alf[frequency[i][1]]
    object = Unit(name, frequency[i][0], '')
    data.append(object)
data = shannon_fano(data)

fin.close()

if n == 1:
    print(f"Время кодирования: {(encode(file_name, data, string) - start_time):.6f} c.")
else:
    print(f"Время раскодирования: {(decode(file_name, data) - start_time):.6f} c.")

print(f"Коэффициент сжатия: {(getsize(NAME[0] + '.out.' + NAME[-1]) / getsize(NAME[0] + '.' + NAME[-1])):.6f}.")
