import requests
sender = input("What is your name?\n")

bot_message = ""
while bot_message != "Adiós":
    message = input("What's your message?\n")

    print("Sending message now...")

    r = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"sender": sender, "message": message})

    print(r.json())

    print("Bot says, ")
    for i in r.json():
        try:
            bot_message = i['text']
        except KeyError:
            try:
                bot_message = i['image']
            except KeyError:
                bot_message = ''
        print(f"{bot_message}")