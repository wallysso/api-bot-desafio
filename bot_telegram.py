import json
import requests
from time import sleep
from threading import Thread, Lock
from datetime import datetime

global config
config = {
    'url': 'https://api.telegram.org/bot1816785911:AAFxQbZNKHNlZaRQZ3iCgi5OnAUP09KOkmw/',
    'lock': Lock(),
    'apiDjango': 'http://127.0.0.1:8000/api/'
}


def del_update(data):
    global config

    config['lock'].acquire()
    requests.post(config['url'] + 'getUpdates', {'offset': data['update_id'] + 1})
    config['lock'].release()


def send_message(data, msg):
    global config

    config['lock'].acquire()
    requests.post(config['url'] + 'sendMessage', {'chat_id': data['message']['chat']['id'], 'text': str(msg)})
    config['lock'].release()


while True:

    # enviar mensagens
    req = requests.get(config['apiDjango'] + 'mensagem/nao-enviadas')
    mensagens = json.loads(req.content)

    for mensagem in mensagens:
        reqExiste = requests.get(config['apiDjango'] + 'usuariover/' + str(mensagem['fromId']))
        if reqExiste.content.decode('UTF-8') != '':
            print("pode mandar")
            send_message({'message': {'chat': {'id': mensagem['fromId']}}}, mensagem['nome'] + ' - ' + mensagem['text'])
            requests.get(config['apiDjango'] + 'mensagem/lida/' + str(mensagem['id']))
        else:
            print("nao pode mandar")

        # send_message({'message': {'chat': {'id': mensagem['fromId']}}}, mensagem['nome'] + ' - ' + mensagem['text'])
        # requests.get(config['apiDjango'] + 'mensagem/lida/' + str(mensagem['id']))
    # enviar mensagens

    x = ''
    while 'result' not in x:
        try:
            x = json.loads(requests.get(config['url'] + 'getUpdates').text)
        except Exception as e:
            x = ''
            if 'Failed to establish a new connection' in str(e):
                print('Perca de conexão')
            else:
                print('Erro desconhecido: ' + str(e))

    if len(x['result']) > 0:
        for data in x['result']:
            Thread(target=del_update, args=(data,)).start()

            print(json.dumps(data, indent=1))

            if data['message']['text'] != 'SIM' and data['message']['text'] != 'NÃO':
                reqExiste = requests.get(config['apiDjango'] + 'usuariover/' + str(data['message']['from']['id']))

                if reqExiste.content.decode('UTF-8') != '':
                    Thread(target=send_message, args=(data, 'Olá, tudo bem? você já autorizou os comunicados, quando nao quiser mais receber digite *NÃO*!')).start()
                else:
                    Thread(target=send_message, args=(data, 'Olá, tudo bem? Digite *SIM* ou *NÃO* para autorizar o recebimento de comunicados!')).start()

            if data['message']['text'] == 'SIM':
                requests.post(config['apiDjango'] + 'usuario/', {'fromId': data['message']['from']['id'], 'dataCadastro': datetime.now()})
                Thread(target=send_message,
                       args=(data, 'Certo! Você receberá nossas mensagens!')).start()

            if data['message']['text'] == 'NÃO':
                requests.delete(config['apiDjango'] + 'usuario/' + str(data['message']['from']['id']))
                Thread(target=send_message,
                       args=(data, 'Certo! Você não receberá mais nossas mensagens!')).start()




        sleep(1.5)