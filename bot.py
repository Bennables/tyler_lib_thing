from discord import Intents, Client, Message
from discord.ext import commands
from config import TOKEN
import csv



intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = '!', intents = intents)

@bot.command()
async def book(ctx, time):
    # Send a hello message to the user
    pass

@bot.command()
async def add_prof(ctx, *args):
    #getting the arguments
    #check if we can add them
    if len(args) == 3:
        with open('accounts.csv', 'a', newline = '') as file:
            writer = csv.writer(file)
            writer.writerow(list(args))
            await ctx.send(f"UPDATED!")
        print("DONE")
    else:
        #send the correct format
        await ctx.send(f"Enter your first name, last name, email") 
        await ctx.send(f'Format: "\!add_prof first last email"')

    #Cleaning empty lines
    # Read the original file and filter out empty lines
    with open("accounts.csv", mode="r", newline="") as infile:
        reader = csv.reader(infile)
        rows = [row for row in reader if any(row)]  # Keep only non-empty rows

    # Write the cleaned data back to the same file
    with open("accounts.csv", mode="w", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)


# Run the bot with your token
bot.run(TOKEN)