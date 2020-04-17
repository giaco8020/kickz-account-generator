import requests
from discord_webhook import DiscordWebhook, DiscordEmbed
import random
import time
import json
import os , datetime
from faker import Faker
from proxy import get_random_proxy


#Data
fake = Faker()

headers1 = {
"authority": "www.kickz.com",
"method": "GET",
"path": "/it/",
"scheme": "https" ,
"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"accept-encoding": "gzip, deflate, br",
"accept-language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5",
"cache-control": "max-age=0",
"sec-fetch-dest": "document",
"sec-fetch-mode": "navigate",
"sec-fetch-site": "none",
"sec-fetch-user": "?1",
"upgrade-insecure-requests": "1",
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"
}


def gettime():
    timetest = time.asctime().split()[3]
    localtime = "[" + timetest + "]"
    return str(localtime)

def checkproxy(catchall, password, webhook_url):

    s = requests.session()
    proxy = get_random_proxy()

    # Gen email

    email = str(fake.name()).replace(" ", "") + str(random.randint(0, 100000)) + str(catchall)

    test_proxy = s.get("https://www.kickz.com/it/", headers = headers1, proxies = proxy)

    if (test_proxy.status_code == 200 or 201):
        print(gettime() + "Good Proxy!")
    else:
        print(gettime() + "Proxy Error!")
        checkproxy(catchall, password, webhook_url)



    def createAcc():

        data_acc = {
            "login": str(email),
            "password": str(password),
            "passwordVeryfication": str(password),
            "submit": "Accedi adesso",
        }

        acc = s.post("https://www.kickz.com/it/user/new/method/partlyRegister", headers = headers1 , data = data_acc, allow_redirects = True, proxies = proxy)
        if(acc.status_code == 200 or 201):
            print(gettime() + "Account successfully created! ")
            log = open("account.txt", 'a+')
            log.write(str(email) + " ")
            log.write(str(password) + "\n")

        else:
            print(gettime() + "Error while creating account!")


        #Send webhoock
        if (webhook_url != "None"):

            try:
                webhook = DiscordWebhook(url=webhook_url)
                embed = DiscordEmbed(title='Account successfully created!', color=57856)
                embed.add_embed_field(name='Email', value=str(email))
                embed.add_embed_field(name='Password', value=("||" +str(password) + "||"))
                embed.set_footer(text='giacomo#8020')
                embed.set_timestamp()
                webhook.add_embed(embed)
                webhook.execute()
            except:
                print("Error sending webhook")


    createAcc()

#Loading Settings

try:
    data = json.loads(open("config.json").read())
    catchall = str(data["catchall"])
    password = str(data["password"])
    webhook_url = data["webhook_url"]
    print(gettime() + "Loaded Settings!")
except:
    print(gettime() + "Error loading settings...")
    time.sleep(5)
    exit()

if(os.stat("proxies.txt").st_size == 0):
    print(gettime() + "Running Localhost!")
else:
    print(gettime() + "Proxies Loaded!")


print("------------Kickz Account Generator------------")
print("Twitter --> @Giaco8020")
print("Discord --> giacomo#8020")
print("-----------------------------------------------")
time.sleep(1)
print(" ")
number = input(gettime() + " How many account would you generate?")
print(" ")

try:
    for n in range(0, int(number)):
        checkproxy(catchall, password, webhook_url)
except:
    print(gettime() + "generic error!")







