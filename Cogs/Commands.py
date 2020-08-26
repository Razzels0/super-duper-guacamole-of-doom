import discord
from discord.ext import commands
import asyncio
from Cogs.Variables import *



class Cmds(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.log = self.bot.get_cog('settings').logg
		self.channels=[]

	@commands.command(brief='', help='', usage='')
	@commands.guild_only()
	async def purge(self, ctx, num):
		if str(ctx.message.author.id) in OWNERS:
			deleted = await ctx.channel.purge(limit=int(num)+1)
			await ctx.send('Deleted {} message(s)'.format(len(deleted)-1), delete_after=5)

	@commands.command(brief='', help='', usage='')
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

	@commands.command(brief='', help='', usage='')
	@commands.guild_only()
	async def vc(self, ctx):
		member = ctx.message.author
		role = ctx.message.guild.get_role(priv)
		if role in member.roles:
			#overwrites = {member: discord.PermissionOverwrite(manage_channels=True), member: discord.PermissionOverwrite(connect=True),
			overwrites = {member: discord.PermissionOverwrite(manage_channels=True, connect=True, manage_permissions=True),
			ctx.message.guild.default_role: discord.PermissionOverwrite(connect=False)}
			channel = await ctx.message.guild.create_voice_channel(name=ctx.message.author.display_name, category=ctx.message.guild.get_channel(734480118797434951), user_limit=1, overwrites=overwrites)
			await ctx.send('Utworzono kanał głosowy. Miłej zabawy.')
			await self.log('Utworzono kanał głosowy dla **{}**.'.format(ctx.message.author.display_name))
			self.channels.append(channel.id)
			await self.chan_check(ctx, channel)
		else:
			await ctx.send('Nie masz wymaganej do tego roli.')

	async def chan_check(self, ctx, channel):
		await asyncio.sleep(30)
		try:
			chan = ctx.message.guild.get_channel(channel.id)
			if len(chan.members) == 0:
				await chan.delete()
				self.channels.remove(channel.id)
				await self.log('Usunięto kanał **{}** ponieważ nikt do niego nie dołączył przez 30 sekund.'.format(chan.name))
		except:
			pass
			
	@commands.command(brief='', help='', usage='', hidden=True)
	async def ram(self, ctx, *args):
		if str(ctx.message.author.id) in OWNERS:
			pid = os.getpid()
			py = psutil.Process(pid)
			memoryUse = py.memory_info()[0]/2.**20
			memoryUse = round(memoryUse, 1)
			await ctx.send('memory use: '+ str(memoryUse) + 'MB')

	@commands.command(brief='', help='', usage='', hidden=True)
	async def otc(self, ctx):
		auto_role = self.bot.get_channel(748244523972296807)
		message = await auto_role.fetch_message(748244725399683187)
		for item in CR.keys():
			await message.add_reaction(item)

	@commands.Cog.listener()
	async def on_voice_state_update(self, member, before, after):
		if before.channel != None and after.channel == None:
			if before.channel.id in self.channels:
				if len(before.channel.members) == 0:
					await before.channel.delete()
					self.channels.remove(before.channel.id)
					await self.log('Usunięto kanał **{}** ponieważ wszyscy uczestnicy rozmowy opuścili kanał.'.format(before.channel.name))

	@commands.Cog.listener()
	async def on_message(self, message):
		pass

def setup(bot):
	bot.add_cog(Cmds(bot))