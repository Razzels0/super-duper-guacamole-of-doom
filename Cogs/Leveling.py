import discord
from discord.ext import commands
import random
import sqlite3
#from PIL import Image, ImageFont, ImageDraw
#import io

#database
levels = sqlite3.connect('./Data/levels.db')
levels.row_factory = sqlite3.Row
cur = levels.cursor()

cur.executescript('''
	DROP TABLE IF EXISTS users;
	CREATE TABLE IF NOT EXISTS users (
	id INTEGER NOT NULL,
	xp DEFAULT 0,
	level DEFAULT 1)
	''')

#cur.execute('''
#	SELECT id,xp,level FROM users
#	''')
#users = cur.fetchall()
#guild = bot.get_guild(server)
#for user in guild.members:
#	s=0
#	for us in users:
#		if user.id == us['id']:
#			s=1
#	if s==1:
#		pass
#	else:
#		u = (user.id, 0, 1)
#		cur.execute('INSERT INTO users VALUES(?,?,?)', u)
#		print('Added {}'.format(u))
#	levels.commit()


###  Vars
chars = list('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

# Server
server = 696772062164811818

# Text channels
lvls = 735225960538046475

# Roles
lvl1 = 730834782107205752


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
		

	async def lvl_up(self, user):
		pass

	@commands.Cog.listener()
	async def on_message(self, message):
		pass

	@commands.Cog.listener()
	async def on_ready(self):
		cur.execute('''
			SELECT id,xp,level FROM users
			''')
		users = cur.fetchall()
		guild = self.bot.get_guild(server)
		for user in guild.members:
			if user.bot:
				pass
			else:
				s=0
				for us in users:
					if user.id == us['id']:
						s=1
				if s==1:
					pass
				else:
					u = (user.id, 0, 1)
					cur.execute('INSERT INTO users VALUES(?,?,?)', u)
					print('Added {}'.format(u))
				levels.commit()

def setup(bot):
	bot.add_cog(settings(bot))