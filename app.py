import aiohttp
import discord
import requests
from bs4 import BeautifulSoup
import datetime
import asyncio
from dotenv import load_dotenv
import os

bot = discord.Bot()

@bot.event
async def on_ready():
    print("Bot is ready!")


# The website for is down for now will put back and update once it's back up 
# async def fetch(payload):
#     req = requests.get("https://macreconline.ca/FacilityOccupancy/GetFacilityData", data=payload)
#     res = req.text()
#     soup = BeautifulSoup(res, "html.parser")
#     max_cap = soup.find("p", {"class": "max-occupancy"}).get_text()
#     occupancy = soup.find("p", {"class": "occupancy-count"}).get_text()
#     return (occupancy, max_cap[15:])



# @bot.slash_command()
# async def pulse(ctx):
#     """
#     Reverse engineer macreconline.ca to get API endpoints :p
#     """
#     payloads = [
#         {
#             "facilityId": "0986c0ef-0cc6-4659-9f7c-925af22a98c6",
#             "occupancyDisplayType": "00000000-0000-0000-0000-000000004488",
#         },
#         {
#             "facilityId": "7a0d7831-5fa8-4bfb-804b-0128d1dd6a18",
#             "occupancyDisplayType": "00000000-0000-0000-0000-000000004488",
#         },
#         {
#             "facilityId": "da4739b0-2ecb-4a55-9247-b411669f4ad8",
#             "occupancyDisplayType": "00000000-0000-0000-0000-000000004488",
#         },
#     ]
#     tasks = []
#     for payload in payloads:
#         tasks.append(await fetch(payload))
#     results = tasks
#     embed = discord.Embed(
#         title="The Pulse Stats",
#         description="Live Stats! More live than the actual website",
#         color=0x00FF00,
#     )
#     embed.add_field(
#         name="the Pulse | Sport Hall", value=f"`{results[0][0]} | {results[0][1]}`"
#     )
#     embed.add_field(
#         name="Pop Up Pulse", value=f"`{results[1][0]} | {results[1][1]}`"
#     )
#     embed.add_field(
#         name="Track Pulse", value=f"`{results[2][0]} | {results[2][1]}`"
#     )
#     await ctx.send(embed=embed)

@bot.slash_command(name="pulse", description="Get realtime information of dbac capacity")
async def pulse(ctx):
    embed = discord.Embed(
        title="The Pulse Stats",
        description="Live Stats! More live than the actual website (Litereally since the website is down)\n\n ```I'll update this once(if) the website is back up```",
        color=0x00FF00,
    )
    await ctx.respond(embed=embed)

@bot.slash_command(name="library", description="Get realtime information of libraries around campus")
async def library(ctx, location : discord.Option(str, "Which library do you want to check?", choices=["Mills","Thode","Health Sciences","Lyons"]) = None):
    await ctx.defer()
    req = requests.get("https://library.mcmaster.ca/php/occupancy-spaces.php")
    res = req.text
    soup = BeautifulSoup(res, "html.parser")
    data = list(
        map(lambda x: x.get_text(), soup.find_all("p", {"class": "mt-2"}))
    )
    if(location != None):
        formatted_data = []
        for i in data:
            if location in i:
                formatted_data.append(i)
    else:
        formatted_data = data        
    formatted_data = "\n".join(formatted_data)
    embed = discord.Embed(
        title="Library Stats",
        description=f"`Live Stats! More live than the actual website`\n\n```{formatted_data}```",
        color=0x00FF00,
        timestamp=datetime.datetime.utcnow(),
    )
    await ctx.send_followup(embed=embed)

load_dotenv()
bot.run(os.getenv("DISCORD_TOKEN"))
