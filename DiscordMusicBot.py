import discord
from discord import commands

TOKEN = 'NTM3MzczMTU5ODc2MTk4NDAw.XnfPcQ.quxF8FZ3E7tgWUNrFzJb1Iy_jJQ'
client = commands.Bot(command_prefix = '.')
BOT_NAME = 'Music Player'

@client.event
async def on_ready():
	print('Bot Online')
	
@client.command
async def join(ctx):
	channel = ctx.message.author.voice.voice_channel
	await client.join_voice_channel(channel)
	
@client.command
async def leave(ctx):
	guild = ctx.message.guild
	voice_client = guild.voice_client
	await voice_client.disconnect()
	

client.run(TOKEN)