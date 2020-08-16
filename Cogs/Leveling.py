import discord
from discord.ext import commands, tasks
import random
import json
import datetime
from Cogs.Variables import *
from PIL import Image, ImageFont, ImageDraw, ImageOps
import io
import os
from dotenv import load_dotenv
import re
import unicodedata
from firebase import firebase
from math import *

#from PIL import Image, ImageFont, ImageDraw
#import io

#database

fb = os.environ["FIREBASE"]
fbs = os.environ["FIREBASE_SECRET"]

authentication = firebase.FirebaseAuthentication(secret=fbs, email='skanerooo5@gmail.com')
firebase = firebase.FirebaseApplication(fb, authentication=authentication)
levels = profiles = firebase.get('/LVL/', '')

def most_frequent_colour(image):

    w, h = image.size
    pixels = image.getcolors(w * h)

    most_frequent_pixel = pixels[0]

    for count, colour in pixels:
        if count > most_frequent_pixel[0]:
            most_frequent_pixel = (count, colour)

    return most_frequent_pixel[1]

def average_colour(image):

    colour_tuple = [None, None, None]
    for channel in range(3):

        # Get data for one channel at a time
        pixels = image.getdata(band=channel)

        values = []
        for pixel in pixels:
            values.append(pixel)

        colour_tuple[channel] = floor(sum(values) / len(values))

    return tuple(colour_tuple)

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

	async def xp_bar(self, ctx):
		await ctx.message.author.avatar_url_as(format='png', static_format='png', size=1024).save('./buffer.png')
		avatar = Image.open('./buffer.png')
		xpc = average_colour(avatar)
		noxpc = (255-xpc[0], 255-xpc[1], 255-xpc[2])
		bar = Image.new('RGBA', (1152, 70), (0, 0, 0))
		b = Image.new('RGBA', (1148, 66), noxpc)
		bar.paste(b, (2, 2), b)
		xp = levels[str(ctx.message.author.id)]["xp"]
		nexp = 500+((15*levels[str(ctx.message.author.id)]["lvl"])*levels[str(ctx.message.author.id)]["lvl"])
		p = xp/nexp
		draw = ImageDraw.Draw(bar, 'RGBA')
		draw.rectangle([1, 1, round(1148*p), 68], fill=xpc, outline=(0,0,0))
		bar = self._add_corners(bar, rad=35)
		#buffer = io.BytesIO()
		#bar.save(buffer, format='PNG')
		#buffer.seek(0)
		#await ctx.send(file=discord.File(buffer, 'profile.png'))
		draw.arc([0, 0, 70, 70], 90, 270, fill=(0,0,0), width=2)
		draw.arc([1082, 0, 1152, 70], 270, 90, fill=(0,0,0), width=2)
		return bar

	def _add_corners(self, im, rad=100):
		circle = Image.new('L', (rad * 2, rad * 2), 0)
		draw = ImageDraw.Draw(circle)
		draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
		alpha = Image.new('L', im.size, "white")
		w, h = im.size
		alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
		alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
		alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
		alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
		im.putalpha(alpha)
		return im

#	@commands.command(brief='', help='', usage='', aliases=['p'])
#	@commands.guild_only()
#	async def profil(self, ctx):
#		await ctx.message.author.avatar_url_as(format='png', static_format='png', size=1024).save('./buffer.png')
#		avatar = Image.open('./buffer.png')
#		await ctx.send(average_colour(avatar))

	@commands.command(brief='', help='', usage='', aliases=['p'])
	@commands.guild_only()
	async def profil(self, ctx):
		w = 1280
		h = 640
		bw = 384
		image = Image.new('RGB', (w, h))
		draw = ImageDraw.Draw(image, 'RGBA')
		await ctx.message.author.avatar_url_as(format='png', static_format='png', size=512).save('./buffer.png')
		avatar = Image.open('./buffer.png')
		bg = Image.open('./zero0.jpg')
		image.paste(bg, (0, 0))
		#draw.rectangle([0, 0, w, h], fill=(49,49,49), outline=(49,49,49))
		#draw.rectangle([0, 0, w, h], fill=(0,0,0, 125), outline=(0,0,0,0))
		draw.rectangle([640, 32, 1216, 480], fill=(70,70,70, 150), outline=(70,70,70), width=3)
		#image = Image.open('./kote.jpg')
		#draw.polygon([(48, 224), (32, 224), (w-16, 288), (w-32, 288)], fill=(155,155,155), outline=(155,155,155))
		#text = self.ver[str(member.id)]
		font = ImageFont.truetype('arial.ttf', 70)
		#tw, th = draw.textsize(text, font=font)
		#print(tw, th)
		#x = (w - tw)//2
		#y = (h - th)//2
		xp = int(levels[str(ctx.message.author.id)]["xp"])
		nexp = 500+((15*levels[str(ctx.message.author.id)]["lvl"])*levels[str(ctx.message.author.id)]["lvl"])
		p = xp/nexp
		#draw.polygon([(32, 224), (32+round((w-64)*p), 224), (32, 288), (32, 288)], fill=(155,0,0), outline=(155,0,0))
		#image.paste(self.xp_bar(str(ctx.message.author.id)), (0, 0))
		name = str(unicodedata.normalize('NFKD', ctx.message.author.display_name).encode('ascii','ignore'), 'utf-8')
		text = f'''{name}
Poziom {levels[str(ctx.message.author.id)]["lvl"]}
{xp}/{nexp} XP'''
		draw.text((645, 37), text, fill=(255,255,255), font=font)
		draw.line([640, 256, 1216, 256], (70, 70,70), 3)
		size = (512, 512)
		mask = Image.new('L', size, 0)
		mdraw = ImageDraw.Draw(mask) 
		mdraw.ellipse((0, 0) + size, fill=255)
		cavatar = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
		cavatar.putalpha(mask)
		xpbar = await self.xp_bar(ctx)
		image.paste(xpbar, (64, 558), xpbar)
		draw.ellipse([61, 29, 579, 547], (0,0,0), (0,0,0), 3)
		image.paste(cavatar, (64, 32), cavatar)
		#draw.arc([64, 32, 576, 544], 270, 90, fill=(0,0,0), width=5)
		#draw.arc([64, 32, 576, 544], 90, 270, fill=(0,0,0), width=5)
		buffer = io.BytesIO()
		image.save(buffer, format='PNG')
		buffer.seek(0)
		await ctx.send(file=discord.File(buffer, 'profile.png'))

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
				points = ((1 + round(len(message.content)/25)) + (5 * len(message.attachments)))*premium
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

	@tasks.loop(minutes=5.0)
	async def check_voice(self):
		guild = self.bot.get_guild(server)
		for channel in guild.voice_channels:
			if len(channel.members) > 0:
				for user in channel.members:
					levels[str(user.id)]['xp'] += 5
					if user.premium_since != None:
						levels[str(user.id)]['xp'] += 10
					await self.lvl_up(str(user.id))

	@tasks.loop(minutes=1.0)
	async def update_database(self):
		firebase.put('/', 'LVL', levels)

	def cog_unload(self):
		self.update_database.cancel()
		firebase.put('/', 'LVL', levels)

def setup(bot):
	bot.add_cog(settings(bot))
