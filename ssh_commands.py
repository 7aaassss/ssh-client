import paramiko as p
import time
import ping3


user = '' # введите имя пользователя
secret = '' # пароль пользователя



port = 99999 # порт подключения

start = 1
finish = 8 # старт  - начальная октета; финиш - конечная

not_ping = [] #список октет, которые не нужно пинговать


commands = [        # Список команд которые вводятся на устройстве
        'put [sy identity get name]',
    ]


pings = [f'192.168.3.{i}' for i in range(start, finish) if i not in not_ping] # список айпишников которые будут пропингуются
# ['192.168.3.1', '192.168.3.2'] - примерно такой вид

print(f'Список айпи которые будут пропингованы: {pings}')

 

def foo(adresses): # функция пинга каждого устройства
    good = [] # список устройств, которые пингуются
    for ip in adresses:
        flag = ping3.ping(ip)
        print(flag, ip)
        if isinstance(flag, float):
            good.append(ip)
        if adresses.index(ip) == len(adresses) // 2:
            print('complited 50%')
        time.sleep(1)   
        
    print(f'Адреса, которые успешно пропингованы: {good}')
    return good




def boo(ip): # функция получает список устройств, которые пингуются и будет создавать коннект и пытаться применить команды

    try:
        client = p.SSHClient() #создание ssh клиента 
        client.set_missing_host_key_policy(p.AutoAddPolicy()) # установление политики 
        
        client.connect( # параметры конекта 
            hostname=ip, # ip адрес, например 192.168.01.01
            username=user, # юзер 
            password=secret, # пароль либо pkey
            port = port
        )

        print(f'Соединение c тачкой {ip} установлено!')
        for command in commands:
            stdin, stdout, stderr = client.exec_command(command) # применение каждой команды к устройству
            print(''.join(stdout.readline()))
            time.sleep(2) # чтобы успевал придти ответ от ус-ва

    except Exception as e:
        print(f'Ошибка {e}') # ловля ошибок при коннекте

    finally: # закрытие сессии
        client.close()



for ip in foo(pings): # для каждого айпи функцию с командой
    boo(ip)