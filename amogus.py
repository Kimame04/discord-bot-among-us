import discord
from discord.ext import commands
import pickle

bot = commands.Bot(command_prefix='!ab ')
banned = []
whats = []
names = []
fines = {}
TOKEN = ''
code = 'No code'

def get_key(val):
    for key, value in fines.items():
         if val == value:
             return key
 
    return "key doesn't exist"

def fetchData():
    global banned
    global whats
    global TOKEN
    with open('banned.txt','r') as file:
        banned = file.read().split(',')[:-1]
    with open('whats_this.txt','r') as file1:
        whats = file1.read().split(',')[:-1]

def appendData(string):
    with open('banned.txt','a') as file:
        file.write(string + ',')

@bot.command(name='setcode')
async def setcode(ctx,arg1):
    global code
    code = arg1
    await ctx.send('Code set!')

@bot.command(name='getcode')
async def getcode(ctx):
    await ctx.send(str(code)) 
    
@bot.command(name='kill')
async def smh(ctx):
    await ctx.send('I died')
    await ctx.bot.logout()

@bot.command(name='addword')
async def addword(ctx,arg1):
    if ctx.author.name == 'Kimame_04':
        banned.append(arg1)
        appendData(arg1)
        await ctx.send('Gamer word added')
    else:
        await ctx.send('Only Kieran is allowed to add words, sucks to be you!')

@bot.command(name='checkfine')
async def checkfine(ctx):
    await ctx.send('Your fine is $' + str(fines[ctx.author.name]*0.5)) 
    
@bot.command(name='leaderboard')
async def leaderboard(ctx):
    vals = list(fines.values())
    vals.sort(reverse=True)
    string = '**YOUR TOP OFFENDERS:**\n'
    for i in range(len(names)):
        string += '`' + str(i+1)+ '. ' + get_key(vals[i]) + ': ' + str(vals[i]) + '`\n'
    await ctx.send(string)

@bot.event
async def on_ready():
    fetchData()
    print('Data loaded')
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bool([ele for ele in banned if (ele in message.content.lower())]):
        if message.author.name not in names:
            names.append(message.author.name)
            fines[message.author.name] = 1
        else:
            fines[message.author.name] += 1
        await message.channel.send('You have breached the 1-week Amogus ban. Please pay $0.50 to the class fund.\n') #+  'Total fine for ' + message.author.name + ': $' + str(fines[message.author.name]*0.5)

    if bool([ele for ele in whats if (ele in message.content.lower())]):
        await message.channel.send('What\'s this?')
        
    await bot.process_commands(message)

if __name__ == '__main__':
    with open('token.txt','r') as file2:
        TOKEN = file2.read()
    bot.run(TOKEN)
