import logging
import disnake
from disnake.ext import commands
from config import TOKEN
bot = commands.Bot(intents=disnake.Intents.all(),
                   activity=disnake.Game('Salvador'))
bot.load_extension('cogs.utils')
logging.basicConfig(level=logging.INFO)

bot.run(TOKEN)

