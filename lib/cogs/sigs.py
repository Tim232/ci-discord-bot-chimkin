from random import randint
from io import BytesIO
from array import array

from discord import Embed, File
from discord.ext.commands import Cog
from discord.ext.commands import command

from PIL import Image, ImageDraw, ImageFont, ImageOps
from aiohttp import request

class Sigs(Cog):
	def __init__(self, bot):
		self.bot = bot


	@command(name='novasig',
			 aliases=['poop'],
			 description='Gives a dirty signature of your stinky noba character.',
			 brief='Gives a dirty signature of your stinky noba character.')
	async def get_poop(self, ctx, *, charName: str):
		bgNum = randint(0,11)
		posNum = randint(0,15)
		linkName = charName.replace(' ', '%20')
		URL = f'https://novaragnarok.com/ROChargenPHP/newsig/{linkName}/{bgNum}/{posNum}'

		await ctx.send(URL)

	@command(name='hsig',
			 aliases=['helsig'],
			 description='Get a picture of your Shining Moon(Helheim) char',
			 brief='Get a picture of your Shining Moon(Helheim) char')
	async def get_helsig(self, ctx, *, charName: str):
		linkName = charName.replace(' ', '%20')
		sigURL = f'http://51.161.117.101/char/index.php/helsig/{linkName}'

		async with request("GET", sigURL, headers={'User-Agent': 'Mozilla/5.0'}) as response:
			if response.status == 200:
				sigBytes = await response.read()
			else:
				await ctx.send(f'Beep Boop\n{response.status} status')
		try:
			sig = Image.open(BytesIO(sigBytes))

			arr = BytesIO()
			sig.save(arr, format='PNG')
			arr.seek(0)

			file = File(arr, f'{charName} - Helheim.png')

			await ctx.send(file=file)
		except Exception as err:
			exception_type = type(err).__name__
			await ctx.send(exception_type)

	@command(name='nsig',
			 aliases=['nifsig'],
			 description='Get a picture of your Shining Moon(Helheim) char',
			 brief='Get a picture of your Shining Moon(Helheim) char')
	async def get_nifsig(self, ctx, *, charName: str):
		linkName = charName.replace(' ', '%20')
		sigURL = f'http://51.161.117.101/char/index.php/nifsig/{linkName}'

		async with request("GET", sigURL, headers={'User-Agent': 'Mozilla/5.0'}) as response:
			if response.status == 200:
				sigBytes = await response.read()
			else:
				await ctx.send(f'Beep Boop\n{response.status} status')
		try:
			sig = Image.open(BytesIO(sigBytes))

			arr = BytesIO()
			sig.save(arr, format='PNG')
			arr.seek(0)

			file = File(arr, f'{charName} - Niflheim.png')

			await ctx.send(file=file)
		except Exception as err:
			exception_type = type(err).__name__
			await ctx.send(exception_type)

	@command(name="navatar",
			 aliases=["niftar"],
			 description="Creates avatar for Niflheim character",
			 brief="Creates avatar for Niflheim character")
	async def get_nif_avatar(self, ctx, *, charName: str):
		linkName = charName.replace(' ', '%20')
		URL = f"http://51.161.117.101/char/index.php/avatar/{linkName}"
		await ctx.send(URL)



	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("sigs")

def setup(bot):
	bot.add_cog(Sigs(bot))