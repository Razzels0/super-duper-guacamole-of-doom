import asyncio
from discord.ext import commands, tasks
import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN1 = os.environ["TOKEN1"]
TOKEN2 = os.environ["TOKEN2"]
TOKEN = TOKEN1 + TOKEN2
BOT_PREFIX=(',')
bot = commands.Bot(command_prefix = BOT_PREFIX)
# mywaifulist.moe/random
#reddit = praw.Reddit(client_id='https://www.reddit.com', client_secret='Va3_xSGvN8qkbzKlu9s9FdmfJck', user_agent='testscript')

bot.remove_command('help')
OWNERS = ['215553356452724747', '390394829789593601']
initial_extensions = ['Cogs.AutoRole', 'Cogs.Commands', 'Cogs.Leveling']
blacklists = {
	'servers':[], 
	'users':[], 
	'channels':[]
}
#initial_extensions = ['Cogs.AutoRole']

if __name__ == '__main__':
	for extension in initial_extensions:
		bot.load_extension(extension)

@bot.command(pass_context=True, help='OWNER ONLY', brief='OWNER ONLY', usage='OWNER ONLY')
async def reload(ctx):
	if str(ctx.message.author.id) in OWNERS:
		text = ''
		for extension in initial_extensions:
			try:
				bot.reload_extension(extension)
				text += 'Succesfully reloaded ' + str(extension) + ' :white_check_mark:\n'
				print('Reloaded ' + str(extension))
			except:
				print('Failed to reload ' + str(extension))
				text += 'Failed to reload ' + str(extension) + ' :negative_squared_cross_mark:\n'
		await ctx.send(text)

@bot.event
async def on_error(error, *args):
	if str(error) != 'on_message':
		for item in OWNERS:
			user = bot.get_user(int(item))
			if user.dm_channel == None:
				await user.create_dm()
			await user.dm_channel.send(error)

@bot.event
async def on_message(message):
	await bot.process_commands(message)

@bot.event
async def on_ready():
	print('------------')
	print('Logged in as:')
	print(bot.user.name)
	print(bot.user.id)
	print('Connected to ' + str(len(bot.guilds)) + ' servers.')
	print('------------')

bot.run(TOKEN[::-1])