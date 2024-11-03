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
    args = list(args)
    args.insert(0, ctx.author.name)
    delete_row = None
    if len(args) == 4:
        with open('accounts.csv', 'a', newline = '') as file:
            csv_reader = csv.DictReader(file)
            current_people = [row["ColumnName"] for row in csv_reader]
            #remove row and clean data
            if args[0] in current_people:
                delete_row = args[0]
            with open("accounts.csv", mode="r", newline="") as infile:
                reader = csv.reader(infile)
                rows = [row for row in reader if any(row) or row['Name'] == delete_row]  # Keep only non-empty rows

            # Write the cleaned data back to the same file
            with open("accounts.csv", mode="w", newline="") as outfile:
                writer = csv.writer(outfile)
                writer.writerows(rows)
            
            writer = csv.writer(file)
            writer.writerow(args)
            await ctx.send(f"UPDATED!")
        print("DONE")
    else:
        #send the correct format
        await ctx.send(f"Enter your first name, last name, email") 
        await ctx.send(f'Format: "\!add_prof first last email"')

# Run the bot with your token
bot.run(TOKEN)