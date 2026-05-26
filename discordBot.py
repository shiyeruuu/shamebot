import discord
from dotenv import load_dotenv
import os
import asyncio 
import datetime

load_dotenv()

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
	print(f'Logged in as {client.user}')

@client.event
async def on_voice_state_update(member, before, after):
	if member.bot:
		return

	if before.channel is None or after.channel is not None:
		return

	guild = member.guild

	general = discord.utils.get(guild.text_channels, name='┊・⊱・wall-of-shame')
	if not general:
		return

	await asyncio.sleep(1)
	
	async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.member_disconnect):
		age = (datetime.datetime.now(datetime.timezone.utc) - entry.created_at).total_seconds()
		if age > 5:
			return
		disconnector = entry.user
		if disconnector.bot:
			return
	
	if disconnector.id == 902424435489923102:
		return
	
	embed = discord.Embed(title="Member Disconnected", description=f"{member.mention} was disconnected from {before.channel.mention} by {disconnector.mention} SHAME ON YOU!")
	embed.set_image(url='https://imgur.com/a/jBctAAF')
	await general.send(embed=embed)

client.run(os.getenv('DISCORD_TOKEN'))

	