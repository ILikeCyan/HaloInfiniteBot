import asyncio
import copy
import json
import logging
import os
import random
import threading
from datetime import datetime
import discord
from aiohttp import ClientSession
from discord.ext import commands
from dotenv import main, load_dotenv
from spnkr import HaloInfiniteClient
from spnkr import client


# Load environment variables
load_dotenv()
token = os.environ.get("DISCORD_BOT_TOKEN")

# Initialize the bot with intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

OBJS = {
    "Capture the Flag": ["Aquarius", "Argyle", "Empyrean", "Forbidden"],
    "Oddball": ["Live Fire", "Recharge", "Streets"],
    "Strongholds": ["Live Fire", "Recharge", "Solitude", "Interference"],
    "King of the Hill": ["Live Fire", "Recharge", "Solitude", "Interference"],
}
SLAYER = ["Aquarius", "Live Fire", "Recharge", "Streets", "Solitude", "Interference"]

SLAYER2 = ["Aquarius", "Live Fire", "Recharge", "Octagon", "Solitude"]

SLAYER3 = ["Aquarius", "Live Fire", "Recharge", "Empyrean", "Solitude", "Streets", "Banished Narrows", "Sylvanus"]


#spag code but fuck it


def pick_map(available_maps, picked_maps, last_n=2):
    """
    Pick a map ensuring it wasn't picked in the last_n matchesStreets
    """
    valid_maps = list(set(available_maps) - set(picked_maps[-last_n:]))
    if valid_maps:
        return random.choice(valid_maps)
    return None


def series(length, OBJS, SLAYER):
    gts = list(OBJS)
    slayer_maps = copy.deepcopy(SLAYER)
    temp_objs = copy.deepcopy(OBJS)
    picked_gt = []
    picked_maps = []
    games = []

    for i in range(length):
        if i in [1, 4, 6]:
            cur_map = pick_map(slayer_maps, picked_maps, 2)
            if cur_map:
                picked_maps.append(cur_map)
                slayer_maps.remove(cur_map)
                games.append(f"Slayer - {cur_map}")
        elif i == 5:
            gt = random.choice(list(set(gts) - {'Capture the Flag'}))
            picked_gt.append(gt)
            cur_map = pick_map(temp_objs[gt], picked_maps, 1)
            if cur_map:
                picked_maps.append(cur_map)
                games.append(f"{gt} - {cur_map}")
        else:
            gt = random.choice(list(set(gts) - set(picked_gt)))
            picked_gt.append(gt)
            cur_map = pick_map(temp_objs[gt], picked_maps, 2)
            if cur_map:
                picked_maps.append(cur_map)
                temp_objs[gt].remove(cur_map)
                games.append(f"{gt} - {cur_map}")

    return games


def t1(SLAYER3):
    picked_gt = []
    picked_maps = []
    games = []
    cur_map = []

    slayer_maps = copy.deepcopy(SLAYER3)
    picked_maps = []
    i = 0

    while i < 3:
        map1 = str(random.choice(slayer_maps))
        games.append("Slayer - " + str(map1))
        picked_maps.append(games)
        slayer_maps.remove(map1)
        print(picked_maps)
        i += 1

    return games


def headtohead(SLAYER2):
    picked_gt = []
    picked_maps = []
    games = []
    cur_map = []

    slayer_maps = copy.deepcopy(SLAYER2)
    picked_maps = []
    cur_map = pick_map(slayer_maps, picked_maps, 4)
    if cur_map:
        picked_maps.append(cur_map)
        slayer_maps.remove(cur_map)
        games.append(f"Slayer - {cur_map}")
    return games


def create_embed(matches, length):
    embed = discord.Embed(title="Best Of " + str(length) + " Series",
                          description="Maps to be played in best of " + str(length) + " series")
    embed.set_thumbnail(
        url="https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.indiamilletinitiative.org%2Fhalo-memes-clean-q-25504420&psig=AOvVaw0ao5maoZra7Btv16-Fb-le&ust=1718669808263000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCIia65au4YYDFQAAAAAdAAAAABAE")

    for i in range(len(matches)):
        embed.add_field(name="Game " + str(i + 1), value=matches[i], inline=False)

    return embed


def rand_number():
    return random.randint(1, 10)


COMMAND_LOG_COUNT = {'BO3': 0, 'BO5': 0, 'BO7': 0, 'Acc': 0, '2v2': 0, 'headtohead': 0}


def handle_bo_command(length, message):
    matches = series(length, OBJS, SLAYER, SLAYER2, SLAYER3)
    embed = create_embed(matches, length)
    COMMAND_LOG_COUNT[f'BO{length}'] += 1
    return embed


COMMANDS = {
    '!bo3': lambda m: handle_bo_command(3, m),
    '!bo5': lambda m: handle_bo_command(5, m),
    '!headtohead': lambda m: handle_bo_command(1, 1),
    '!bo7': lambda m: handle_bo_command(7, m),
    '!2v2': lambda m: handle_bo_command(3, 5),
    '!acc': lambda m: main(),
    '!botservers': lambda m: f"I'm in {len(client.guilds)} servers!"
}


class MatchCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="bo3", description="Starts a BO3 series")
    async def bo3(self, interaction: discord.Interaction):
        matches = series(3, OBJS, SLAYER)
        embed = create_embed(matches, 3)
        await interaction.response.send_message(embed=embed)
        COMMAND_LOG_COUNT['BO3'] += 1

    @discord.app_commands.command(name="headtohead", description="Starts a 1v1")
    async def headtohead(self, interaction: discord.Interaction):
        matches = headtohead(SLAYER2)
        embed = create_embed(matches, 1)
        await interaction.response.send_message(embed=embed)
        COMMAND_LOG_COUNT['headtohead'] += 1

    @discord.app_commands.command(name="bo5", description="Starts a BO5 series")
    async def bo5(self, interaction: discord.Interaction):
        matches = series(5, OBJS, SLAYER)
        embed = create_embed(matches, 5)
        await interaction.response.send_message(embed=embed)
        COMMAND_LOG_COUNT['BO5'] += 1

    @discord.app_commands.command(name="bo7", description="Starts a BO7 series")
    async def bo7(self, interaction: discord.Interaction):
        matches = series(7, OBJS, SLAYER)
        embed = create_embed(matches, 7)
        await interaction.response.send_message(embed=embed)
        COMMAND_LOG_COUNT['BO7'] += 1

    @discord.app_commands.command(name="acc", description="Nothing")
    async def acc(self, interaction: discord.Interaction):
        await interaction.response.send_message("D")
        COMMAND_LOG_COUNT['Acc'] += 1

    @discord.app_commands.command(name="2v2", description="2v2 Series")
    async def t1(self, interaction: discord.Interaction):
        matches = t1(SLAYER3)
        embed = create_embed(matches, 3)
        await interaction.response.send_message(embed=embed)
        COMMAND_LOG_COUNT['2v2'] += 1

    @discord.app_commands.command(name="botservers", description="Shows the number of servers the bot is in")
    async def botservers(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"I'm in {len(self.bot)} servers!")


async def setup(bot):
    await bot.add_cog(MatchCommands(bot))
    await bot.tree.sync()


@bot.event
async def on_ready():
    await setup(bot)
    logging.info(f"We have logged in as {bot.user}")


def checkTime():
    # This function runs periodically every hour
    threading.Timer(3600, checkTime).start()

    # Log current time with format "Mon Month Day HH:MM:SS", e.g., "Thu Oct 14 15:30:45"
    logging.info(f"Current Time = {datetime.now().strftime('%a %b %d %H:%M:%S')}")
    logging.info(f"Command Log Count: {json.dumps(COMMAND_LOG_COUNT)}")


checkTime()

if __name__ == "__main__":
    asyncio.run(main())
    bot.run(token)
