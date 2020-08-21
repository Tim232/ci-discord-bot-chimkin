from datetime import datetime, timedelta
from typing import Optional

from discord import Embed, Member
from discord.ext.commands import Cog, Greedy
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, bot_has_permissions

class Mod(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name='kick',
			 description='To kick naughty awies (Admin command)',
			 brief='To kick naughty awies (Admin command)')
	@bot_has_permissions(kick_members=True)
	@has_permissions(kick_members=True)
	async def kick_members(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = 'No reason provided'):
		if not len(targets):
			await ctx.send('One or more required arguments missing, idiot.')
		else:
			for target in targets:
				if (ctx.guild.me.top_role.position > target.top_role.position 
					and not target.guild_permissions.administrator):
					await target.kick(reason=reason)

					embed = Embed(title='Member kicked',
								  colour=0xDD2222,
								  timestamp=datetime.utcnow())

					embed.set_thumbnail(url=target.avatar_url)

					fields = [('Member', f'{target.display_name} a.k.a. {target.display_name}', False),
							  ('Done by', ctx.author.display_name, False),
							  ('Reason', reason, False)]

					for name, value, inline in fields:
						embed.add_field(name=name, value=value, inline=inline)

					await self.log_channel.send(embed=embed)

				else:
					await ctx.send(f'{target.display_name} could not be kicked')

			await ctx.send('It is done!')

	@kick_members.error
	async def kick_members_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			await ctx.send('Insufficient permissions to perform tasks.')


	@command(name='ban',
			 description='To ban REALLY naughty awies (Admin command)',
			 brief='To ban REALLY naughty awies (Admin command)')
	@bot_has_permissions(ban_members=True)
	@has_permissions(ban_members=True)
	async def ban_members(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = 'No reason provided'):
		if not len(targets):
			await ctx.send('One or more required arguments missing, idiot.')
		else:
			for target in targets:
				if (ctx.guild.me.top_role.position > target.top_role.position 
					and not target.guild_permissions.administrator):
					await target.ban(reason=reason)

					embed = Embed(title='Member banned',
								  colour=0xDD2222,
								  timestamp=datetime.utcnow())

					embed.set_thumbnail(url=target.avatar_url)

					fields = [('Member', f'{target.display_name} a.k.a. {target.display_name}', False),
							  ('Done by', ctx.author.display_name, False),
							  ('Reason', reason, False)]

					for name, value, inline in fields:
						embed.add_field(name=name, value=value, inline=inline)

					await self.log_channel.send(embed=embed)

				else:
					await ctx.send(f'{target.display_name} could not be kicked')

			await ctx.send('It is done!')

	@ban_members.error
	async def ban_members_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			await ctx.send('Insufficient permissions to perform tasks.')


	@command(name='clear',
			 aliases=['purge'])
	@bot_has_permissions(manage_messages=True)
	@has_permissions(manage_messages=True)
	async def clear_messages(self, ctx, targets: Greedy[Member], limit: Optional[int] = 1):
		def _check(message):
			return not len(targets) or message.author in targets 

		if 0 < limit <= 250:
			with ctx.channel.typing():
				await ctx.message.delete()
				deleted = await ctx.channel.purge(limit=limit, after=datetime.utcnow()-timedelta(days=14),
												  check=_check)

				await ctx.send(f'Deleted {len(deleted):,} messages', delete_after=5)
		else:
			await ctx.send('Make sure your message limit is between 0~250')


	@Cog.listener()
	async def on_ready(self):
		self.log_channel = self.bot.get_channel(739388066048770118)
		self.bot.cogs_ready.ready_up("mod")


def setup(bot):
	bot.add_cog(Mod(bot))