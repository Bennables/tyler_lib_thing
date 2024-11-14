from discord import Intents, Client, Message
from discord.ext import commands
from config import TOKEN
import csv
from driver import book_it
from datetime import datetime


intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = '!', intents = intents)

def find_matching_format(time_string):
    if len(time_string) ==1:
        time_string = f'0{time_string}'

    # Check the format based on the presence of a colon and string length
    if ":" in time_string and len(time_string) == 5:  # "HH:MM" format
        format_str = "%H:%M"
        
    elif len(time_string) == 2:  # "HH" format
        format_str = "%H"
    else:
        raise ValueError("Invalid time format. Use 'HH' or 'HH:MM'.")

    # Parse the time based on the detected format
    specified_time = datetime.strptime(time_string, format_str)

    hour = specified_time.hour
    if not 8<= hour <=22:
        hour += 12


    # Replace the date part with the current date
    current_date_time = datetime.now().replace(
        hour=hour,
        minute=specified_time.minute,
        second=0,
        microsecond=0
    )
    
    # Return both the datetime object and the format used
    return current_date_time, format_str



@bot.command()
async def book(ctx, start = None, time_hours = None, days_ahead = 0):
    if start == None or time_hours == None:
        await ctx.send("!book (time to start) (hrs) (optional, days ahead)")
    else:
        find_time, format = find_matching_format(start)

        # Send a hello message to the user
        time = float(time_hours)
        time = int(time/.5)
        print(start, find_time, time_hours)
        a = book_it(ctx.author.name, time, find_time, days_ahead)
        if a == 0:
            await ctx.send("Success!")
        elif a == 2:
            await ctx.send("You don't have a login yet, use '!adprof'")
        elif a == 3:
            await ctx.send("there was an error.")
        elif a == 4:
            await ctx.send("that time isn't available")

    # except:
    #     await ctx.send('Please use in format: "!book time_in_hours"')

@bot.command()
async def addprof(ctx, *args):
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

@bot.command()
async def checkprof(ctx):
    done = False
    with open("accounts.csv", mode="r", newline="") as file:
        reader = csv.reader(file)
        for i in reader:
            if i['Discord'] == ctx.author.name:
                # Keep only non-empty rows
                done = True
                await ctx.send(f'{i[1], i[2], i[3]}')
    if not done:
        await ctx.send("No existing account")

@bot.command()
async def helps(ctx):
    await ctx.send("!addprof")
    await ctx.send("!checkprof")
    await ctx.send("!book")


# Run the bot with your token
bot.run(TOKEN)