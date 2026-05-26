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

	general = discord.utils.get(guild.text_channels, name='┊・⊱・shining-shame-ring')
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
	
	await general.send(
			f'**{member.display_name}** was disconnected from '
			f'**{before.channel.name}** by **{disconnector.display_name} **.'
			f'**SHAME ON YOU!!!"**'
		)
	return


client.run(os.getenv('DISCORD_TOKEN'))

	