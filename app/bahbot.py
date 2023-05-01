import discord
import random
from discord.ext import commands
import argparse

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
  print("Bot is up and running!") # verify that the bot is running

@client.command(name='roll')
async def roll(context):
	await context.message.delete()
	reactdict = {
    100:    "👑",
    1:      "💀",
    69:     "😉"
    }
	x = random.randint(1,100)
	embedroll = discord.Embed(
		color=0x325c6b,
		description=(f'{context.author.display_name} rolls **{x}** (1-100)')
	)
	rollmsg = await context.message.channel.send(embed=embedroll)
	if x in reactdict:
		await rollmsg.add_reaction(reactdict[x])

@client.command(name="randomteam")
async def randomteam(context):
	if not context.author.voice:
		await context.send("`You are not in a voice channel`")
	elif context.author.voice.channel and len(context.author.voice.channel.members) <= 1:
		await context.send("`Try a single player game...`")
	else:
		teamNames = ["Blue", "Red"]
		vc = context.author.voice.channel
		teamsdict = shuffle_and_assign_players(vc.members, teamNames)
		embed1 = create_embed_for_randomteam(vc, teamNames)

		## Fill the embed with info (teams, players, amount etc)
		embed1.set_footer(text=f"{len(vc.members)} players total")
		print(teamsdict)
		for k, v in teamsdict.items():
			embed1.add_field(name=k, value=f">>> {v}",inline=True)
		await context.send(embed=embed1)

def shuffle_and_assign_players(members, teamNames):
	random.shuffle(members)
	middle_index = len(members)//2
	teamsdict = {}
	for t in teamNames:
		teamsdict[t] = ""
	for p in members[:middle_index]:
		teamsdict[list(teamsdict.keys())[0]] += p.display_name+'\n'
	for p in members[middle_index:]:
		teamsdict[list(teamsdict.keys())[1]] += p.display_name+'\n'
	return teamsdict

def create_embed_for_randomteam(vc, teams):
	embedvar = discord.Embed(
		title=f"Random Teams for channel: {vc}",
		color=0xFA9C1D,
		description=f"Team {random.choice(list(teams))} moves to different channel"
		)
	return embedvar

parser = argparse.ArgumentParser(description='bahbot v. 0.2')
parser.add_argument("-t", type=str, help="your discord bot token")
args = parser.parse_args()

if args.t == 'token':
	sys.stdout.write('Please provide a token')
else:
    client.run(args.t)
