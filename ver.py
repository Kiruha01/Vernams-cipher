from sys import argv
import random

DELTA = 126 - 32

def sep(num, key):
    return 

def encr(data, ke):
    if data:
        random.seed(ke)
        s = data
    else:
        s = ke
    c = ''
    k = ''
    for i in s:
        key = random.randint(0, 200)
        c += chr((ord(i)-32 + key) % DELTA + 32)
        k += str(key) + ' '
    return c, k

def decr(data, key):
    s = data
    c = ''
    k = key.split(' ')
    for ke, i in enumerate(s):
        c += chr((ord(i) - 32 - int(k[ke])) % DELTA + 32)
    return c
    

if argv[1] == '-h' or argv[1] == '--help':
    print('''
            888     888                                             
            888     888                                             
            888     888                                             
            Y88b   d88P .d88b. 888d88888888b.d88b.  8888b. 88888b.  
             Y88b d88P d8P  Y8b888P"  888 "888 "88b    "88b888 "88b 
              Y88o88P  88888888888    888  888  888.d888888888  888 
               Y888P   Y8b.    888    888  888  888888  888888  888 
                Y8P     "Y8888 888    888  888  888"Y888888888  888 
                                                                    
                                                  
''')

    print('Шифр Вермана v1.0\nВведи ver.py -e [ключ] ваше сообщение - для шифровки\n\
Введи viz.py -d ключ ваше сообщение - для дешифровки\n\
             -f [имя файла] для сохранения в файл')

elif argv[1] == '-e':
    try:
        data = encr(argv[3], argv[2])
    except:
        data = encr(None, argv[2])
    print(data[0], data[1], sep='\n')

elif argv[1] == '-d':
    data = decr(argv[3], argv[2])
    print(data)

elif argv[1] == '-f':
    if argv[3] =='-e':
        try:
            data = encr(argv[5], argv[4])
        except:
            data = encr(None, argv[4])
        name = argv[2]
        if '.' not in name:
            name += '.txt'
        with open(name, 'w') as file:
            file.write(data[0])
        with open('key.' + name, 'w') as file:
            file.write(data[1])
        print('[+] Succsses!')
    elif argv[3] =='-d':
        with open(argv[2], 'r') as file:
            text = file.read()
        with open ('key.' + argv[2], 'r') as file:
            key = file.read()
        data = decr(text, key)
        print(data)
        