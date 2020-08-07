import discord
from discord.ext import commands
import random
from PIL import Image, ImageFont, ImageDraw
import io
from Cogs.Variables import *



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
		self.ver = {}
		self.log = log
		self.server = server
		#auto_role = self.bot.get_channel(arc)
		#message = auto_role.fetch_message(arm)
		#if len(message.reactions) == 0:
		#	await message.add_reaction('👍')


	async def logg(self, message):
		chan = self.bot.get_channel(log)
		await chan.send(message)

	@commands.Cog.listener()
	async def on_member_join(self, member):
#		print(member)
#		roles = []
#		for role in join:
#			await member.add_roles(member.guild.get_role(role))
		await self.logg('{} dołączył.'.format(member.display_name))

	@commands.Cog.listener()
	async def on_member_join(self, member):
		self.ver[str(member.id)] = rcg(10)
		w = 540
		h = 540
		#image = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT))
		image = Image.open('./kote.jpg')
		draw = ImageDraw.Draw(image)
		draw.rectangle([170, 250, w-170, h-250], fill=(255,255,255), outline=(0,0,0))
		text = self.ver[str(member.id)]
		font = ImageFont.truetype('arial.ttf', 30)
		tw, th = draw.textsize(text, font=font)
		print(tw, th)
		x = (w - tw)//2
		y = (h - th)//2
		draw.text( (x, y), text, fill=(0,0,0), font=font)
		buffer = io.BytesIO()
		image.save(buffer, format='PNG')
		buffer.seek(0)
		if member.dm_channel == None:
			await member.create_dm()
		await member.dm_channel.send(file=discord.File(buffer, 'captcha.png'))

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		#chan = self.bot.get_channel(log)
		await self.logg('{} odszedł.'.format(member.display_name))

	@commands.Cog.listener()
	async def on_message(self, message):
		if type(message.channel)==discord.DMChannel:
			if str(message.author.id) in self.ver.keys():
				if message.content == self.ver[str(message.author.id)]:
					guild = self.bot.get_guild(server)
					member = guild.get_member(message.author.id)
					for role in join:
						await member.add_roles(member.guild.get_role(role))
					await self.logg('{} został zweryfikowany.'.format(message.author.display_name))
					if member.dm_channel == None:
						await member.create_dm()
					await member.dm_channel.send('Weryfikacja zakończona sukcesem.')
				else:
					if member.dm_channel == None:
						await member.create_dm()
					await member.dm_channel.send('Niepoprawny kod. Spróbuj ponownie.')

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		member = payload.member
		message = payload.message_id
		roles = [role.id for role in member.roles]
		if any(x in roles for x in REQ5):
			if message == arm:
				if payload.emoji.name == emo:
					await member.add_roles(member.guild.get_role(ar))
		else:
			print('no')

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload):
		member =  self.bot.get_guild(payload.guild_id).get_member(payload.user_id)
		message = payload.message_id
		roles = [role.id for role in member.roles]
		if any(x in roles for x in REQ5):
			if message == arm:
				if payload.emoji.name == emo:
					await member.remove_roles(member.guild.get_role(ar))
		else:
			print('no')

	#@commands.Cog.listener()
	#async def on_ready(self):
	#	auto_role = self.bot.get_channel(arc)
	#	message = await auto_role.fetch_message(arm)
	#	if len(message.reactions) == 0:
	#		await message.add_reaction('👍')


def setup(bot):
	bot.add_cog(settings(bot))