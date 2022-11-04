import requests


def send_message(msg):
    #chat id do grupo do telegram que irar rebecer as mensagens
    chat_id = 'seu_chat_id'
    # token do seu bot que esta no grupo relacinado ao chat_id acima
    token = 'seu_token'
    try:
        data = {"chat_id": chat_id, "text": msg}
        url = "https://api.telegram.org/bot{}/sendMessage".format(token)
        requests.post(url, data)
    except Exception as e:
        print("Erro no sendMessage:", e)
