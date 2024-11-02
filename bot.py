from discord import Intents, Client, Message
from discord.ext import commands
from config import TOKEN



intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = '!', intents = intents)

@bot.command()
async def book(ctx, *args):
    # Send a hello message to the user
    await ctx.send(f"Hello, {ctx.author.mention}!")


# Run the bot with your token
bot.run(TOKEN)