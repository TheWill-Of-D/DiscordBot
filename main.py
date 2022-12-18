import os, discord
from discord.ext import commands
from gsheet import get_group_gsheet
from keep_alive import keep_alive
import asyncio


DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
SERVER_ID = 976836912792891462 # insert server id

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)


async def dm_about_roles(member):
  print(f"DMing {member.name}...")

  await member.send(
    f"""
Hi {member.name}, 
welcome to the ESCENDO 2023 discord server! 
Please enter your NTU email address for us to identify you and grant you access to your team’s discord channel.
""")



@bot.event
async def on_ready():
  print(f"{bot.user} has connected to Discord!")


@bot.event
async def on_member_join(member):
  await dm_about_roles(member)

#  await dm_about_roles(member)


async def assign_roles(message):
  print("Assigning roles...")
  await asyncio.sleep(1)
  await message.channel.send("""processing...""")
  await asyncio.sleep(1)
  list_gsheet = get_group_gsheet(message.content)
  team_name = list_gsheet[0]
  nickname = list_gsheet[1]

  
  if team_name:
    server = bot.get_guild(SERVER_ID)   
    member = await server.fetch_member(message.author.id)
    await asyncio.sleep(2)
    
    role_name = "Team "+team_name
    print(role_name)
    role = [discord.utils.get(server.roles, name=role_name),discord.utils.get(server.roles, name="Participant")]
    await asyncio.sleep(1)
     


   
    try:
       await member.add_roles(*role, reason="Roles assigned by WelcomeBot.")
       await member.edit(nick=nickname)
       await asyncio.sleep(1)
       await message.channel.send("You have been assigned to "+role_name)
  

    except Exception as e:
      print(e)
      print("Ettor...")
      await message.channel.send("""

\U0001F615
Oh No!

Something's not right... 

Please contact the ESCENDO 2023 organising committee by dropping us a DM on Instagram @escendo_ntu or emailing us at escendo2023@gmail.com
""")

  else:
    await message.channel.send("""

\U0001F914	
We couldn’t find your email address from our database...

Recheck your email and please try again!

If you think there might be a mistake, please contact the ESCENDO 2023 organising committee by dropping us a DM on Instagram @escendo_ntu or emailing us at escendo2023@gmail.com
""")


@bot.event
async def on_message(message):

  if message.author == bot.user:
    return  # prevent responding to self

  # NEW CODE BELOW
  elif message.content.startswith("!roles"):
    await dm_about_roles(message.author)
    return

  elif isinstance(message.channel, discord.channel.DMChannel):
    await assign_roles(message)
    return

  else:
    print("Not DM...")
    return

while __name__ == '__main__':
  try:
#      keep_alive()
      bot.run(DISCORD_TOKEN)
  except discord.errors.HTTPException as f:
      print(f)
      print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
#      os.system('kill 1')
