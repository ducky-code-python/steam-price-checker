from steampy.client import SteamClient
from discord.ext import commands
import discord
from dotenv import load_dotenv
import discord.ext.commands
from discord.ext import tasks
import json
from steampy.utils import GameOptions
from steampy.market import Currency
import asyncio
import os

with open('config.json') as file:
    data = json.load(file)
    steam_api_key = data['apiIDs']['steam']
    discord_token = data['apiIDs']['discord']

steam_client = SteamClient(steam_api_key)
TOKEN = discord_token

intent = discord.Intents.all()
intent.members = True
intent.message_content = True
client =  commands.Bot(command_prefix= ".", intents=intent)




@client.command()
async def start(ctx):
    if not myLoop.is_running():
        await ctx.send("Loop: Started")
        myLoop.start(ctx)
    else:
        await ctx.send("Loop already running!")
    if not check.is_running():
        check.start(ctx)
@client.command()
async def stan(ctx):
    if myLoop.is_running():
         await ctx.send("Loop: Running")
    else:
         await ctx.send("Loop: Not Running")

@client.command()
async def cena(ctx):   
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
        ans = f"{item} : **{lowest}€** ||{cost}€ ({quantity})||"
        await ctx.send(ans)
        await asyncio.sleep(5)
    f.close()

@client.command()
async def ids(ctx):   
    global steam_client
    f = open('items.json', "r")
    data = json.load(f)
    item_dict = data['items_info']
    for x in item_dict:
        item = x['item']
        id = x['id']
        await ctx.send(f"{id} : {item}")
    f.close()

@client.command()
async def sellat(ctx, id, zmiana):   
    f = open('items.json', "r")
    data = json.load(f)
    item_dict = data['items_info']
    for x in item_dict:
        if int(x['id']) == int(id):
            try:
                x['sellat'] = float(zmiana)
            except ValueError:
                await ctx.send("Sellat must be **float type**.")
                return False
            f.close()
            os.remove('items.json')
            with open('items.json', "w") as f:
                json.dump(data, f, indent=4)
            await ctx.send(f"Changed 'sellat' : {x['item']} to **{zmiana}**")
            return True
    await ctx.send("Can't find id.")

@client.command()
async def dev(ctx):   
    f = open('items.json', "r")
    data = json.load(f)
    item_dict = data['items_info']
    for x in item_dict:
        await ctx.send(f"ID {x['id']} | ITEM {x['item']} | QUANTITY {x['quantity']} | COST {x['cost']} | SELLAT {x['sellat']}")
    f.close()
    
@tasks.loop(minutes=5)
async def myLoop(ctx):
    global steam_client
    f = open('items.json', "r")
    data = json.load(f)
    item_dict = data['items_info']
 
    for x in item_dict:
        item = x['item']
        sellat = x['sellat']

        market = steam_client.market.fetch_price(item, game=GameOptions.CS, currency=Currency.EURO)
        lowest = market['lowest_price'].replace("€", "").replace(",", ".")
        if float(lowest) >= float(sellat):
            await ctx.send(f"Sell {item} : {lowest}")
            await asyncio.sleep(4)

        if not myLoop.is_running():
            await asyncio.sleep(60)
            myLoop.start(ctx)
        if not check.is_running():
            await asyncio.sleep(60)
            check.start(ctx)
    f.close()

@tasks.loop(minutes=6)
async def check(ctx):
    if not myLoop.is_running():
        await asyncio.sleep(60)
        myLoop.start(ctx)
client.run(TOKEN)

