from discord import Intents, Client, Message
from discord.ext import commands
from config import TOKEN
import csv
from driver import book_it



intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = '!', intents = intents)

@bot.command()
async def book(ctx, time_hours):
    # Send a hello message to the user
    time = float(time_hours)
    time = int(time/.5)
    a = book_it(ctx.author.name, time)
    if a == 0:
        await ctx.send("Success!")
    elif a == 2:
        await ctx.send("You don't have a login yet, use '!adprof'")
    elif a == 3:
        await ctx.send("there was an error.")

@bot.command()
async def add_prof(ctx, *args):
    #getting the arguments
    #check if we can add them
    args = list(args)
    args.insert(0, ctx.author.name)
    delete_row = None
    if len(args) == 4:
        with open('accounts.csv', 'r+', newline = '') as file:
            csv_reader = csv.DictReader(file)
            try:
                current_people = [row[0] for row in csv_reader]
                if args[0] in current_people:
                    delete_row = args[0]
            except:
                pass
            #remove row and clean data
            
            with open("accounts.csv", mode="r", newline="") as infile:
                reader = csv.reader(infile)
                rows = [row for row in reader if any(row) or row['Discord'] == delete_row]  # Keep only non-empty rows

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