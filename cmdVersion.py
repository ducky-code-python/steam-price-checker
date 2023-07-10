from steampy.client import SteamClient
from dotenv import load_dotenv
import json
from steampy.utils import GameOptions
from steampy.market import Currency
import time
import os

with open('config.json') as file:
    data = json.load(file)
    steam_api_key = str(data['apiIDs']['steam'])
steam_client = SteamClient(steam_api_key)



def prices():   
    global steam_client
    f = open('items.json', "r")
    data = json.load(f)
    item_dict = data['items_info']
    for x in item_dict:
        item = x['item']
        quantity = x['quantity']
        cost = x['cost']
        market = steam_client.market.fetch_price(item, game=GameOptions.CS, currency=Currency.EURO)
        lowest = market['lowest_price'].replace("€", "").replace(",", ".")
        ans = f"{item} || : {lowest}€| Bought for {cost}€ | Quantity: {quantity}"
        print(ans)
        time.sleep(5)
    f.close()
    input()
    os.system("cls")

def ids():   
    global steam_client
    f = open('items.json', "r")
    data = json.load(f)
    item_dict = data['items_info']
    for x in item_dict:
        item = x['item']
        id = x['id']
        print(f"{id} : {item}")
    f.close()
    input()
    os.system("cls")

def sellat(id, zmiana):   
    f = open('items.json', "r")
    data = json.load(f)
    item_dict = data['items_info']
    for x in item_dict:
        if int(x['id']) == int(id):
            try:
                x['sellat'] = float(zmiana)
            except ValueError:
                print("Sellat must be float type.")
                return False
            f.close()
            os.remove('items.json')
            with open('items.json', "w") as f:
                json.dump(data, f, indent=4)
            print(f"Changed 'sellat' : {x['item']} to **{zmiana}**")
            return True
    print("Can't find id.")

def dev():   
    f = open('items.json', "r")
    data = json.load(f)
    item_dict = data['items_info']
    for x in item_dict:
        print(f"ID {x['id']} | ITEM {x['item']} | QUANTITY {x['quantity']} | COST {x['cost']} | SELLAT {x['sellat']}")
    f.close()
    print("Done")
    input()
    os.system("cls")
    start()

def start():
    ans = input("Command: ")
    if ans == "prices":
        prices()
        start()
    elif ans == "ids":
        ids()
        start()
    elif ans == "sellat":
        ID = input("Item ID")
        TO = input("New sell at: ")
        sellat(ID, TO)
        input()
        os.system("cls")
        start()
    elif ans == "dev":
        dev()
start()