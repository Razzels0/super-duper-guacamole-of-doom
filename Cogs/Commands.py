import discord
from discord.ext import commands
import random
from PIL import Image, ImageFont, ImageDraw
import io

server = 696772062164811818

class Cmds(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.log = self.bot.get_cog('settings').logg

	@commands.command(brief='Set waifu spawn channel', help='Sets current channel as waifu spawn channel', usage='w.set')
	@commands.guild_only()
	async def kick(self, ctx, user, *args):
		if ctx.message.author.guild_permissions.administrator or ctx.message.author.guild_permissions.kick_members:
			user = ctx.message.mentions[0]
			guild = self.bot.get_guild(server)
			member = guild.get_member(user.id)
			reason = ''
			for item in args:
				reason += item + ' '
			await member.kick(reason=reason)
			await self.log('{} został wyrzucony z powodu:\n{}'.format(member.display_name, reason))

	@commands.Cog.listener()
	async def on_message(self, message):
		pass

def setup(bot):
	bot.add_cog(Cmds(bot))