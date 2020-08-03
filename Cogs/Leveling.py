import discord
from discord.ext import commands, tasks
import random
import json
import datetime
from Cogs.Variables import *

#from PIL import Image, ImageFont, ImageDraw
#import io

#database
with open('./Data/lvl_data.json') as data:
    levels = json.load(data)




def rcg(leng):
	a=''
	while len(a) != leng:
		a += random.choice(chars)
	return a

def round(num, deg=0):
	num = num*(10**deg)
	mod = num%1
	if mod<0.5:
		return (num-mod)/(10**deg)
	else:
		return (num-mod+1)/(10**deg)

class settings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.log = self.bot.get_cog('settings').logg
		self.update_database.start()
		print(levels)
		
	async def lvl_ann(self, message):
		chan = self.bot.get_channel(lvls)
		await chan.send(message)

	async def lvl_up(self, user):
		xp = levels[user]['xp']
		lvl = levels[user]['lvl']
		req = 500 + ((15 * lvl) * lvl)
		if xp >= req:
			levels[user]['xp'] -= req
			levels[user]['lvl'] += 1
			await self.lvl_ann(f'<@{user}> Posiada teraz poziom {levels[user]["lvl"]}.')
			if levels[user]['lvl'] in lln:
				print('yas')
				guild = self.bot.get_guild(server)
				member = guild.get_member(int(user))
				nex = lln.index(levels[user]['lvl'])
				await member.add_roles(member.guild.get_role(ll[nex]))
				await member.remove_roles(member.guild.get_role(ll[nex-1]))

	@commands.Cog.listener()
	async def on_message(self, message):
		if not message.author.bot:
			user = str(message.author.id)
			cooldown = datetime.datetime.strptime(levels[user]['cooldown'], "%m/%d/%Y, %H:%M:%S")
			now = datetime.datetime.now()
			if cooldown<now:
				guild = self.bot.get_guild(server)
				member = guild.get_member(int(user))
				if member.premium_since != None:
					premium = 5
				else:
					premium = 1
				points = (1 + round(len(message.content)/25))*premium
				levels[user]['xp'] += points
				levels[user]['cooldown'] = (now+datetime.timedelta(seconds=30)).strftime("%m/%d/%Y, %H:%M:%S")
				await self.lvl_up(user)
				#await self.log(f'Added {points} xp.')

	@commands.Cog.listener()
	async def on_member_join(self, member):
		levels[str(member.id)] = {'xp': 0, 'lvl': 1, 'cooldown': datetime.datetime.min.strftime("%m/%d/%Y, %H:%M:%S")}

	@commands.Cog.listener()
	async def on_ready(self):
		guild = self.bot.get_guild(server)
		for user in guild.members:
			if not user.bot:
				if not str(user.id) in levels.keys():
					levels[str(user.id)] = {'xp': 0, 'lvl': 1, 'cooldown': datetime.datetime.min.strftime("%m/%d/%Y, %H:%M:%S")}
					print(f'Added {user.id}')

	@tasks.loop(minutes=1.0)
	async def update_database(self):
		with open('./Data/lvl_data.json', 'w') as data:
			json.dump(levels, data)

def setup(bot):
	bot.add_cog(settings(bot))