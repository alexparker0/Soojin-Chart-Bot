from melonapi import scrapeMelon
import discord
from discord.ext import commands
from discord import app_commands
import os
import json

MY_GUILD = discord.Object(id=settings.GUILDS_ID)
class MyClient(discord.Client):
  def __init__(self, *, intents: discord.Intents):
    super().__init__(intents=intents)
    # A CommandTree is a special type that holds all the application command
    # state required to make it work. This is a separate class because it
    # allows all the extra state to be opt-in.
    # Whenever you want to work with application commands, your tree is used
    # to store and work with them.
    # Note: When using commands.Bot instead of discord.Client, the bot will
    # maintain its own tree instead.
    self.tree = app_commands.CommandTree(self)

  async def setup_hook(self):
    # This copies the global commands over to your guild.
    self.tree.copy_global_to(guild=MY_GUILD)
    await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)

def truncate_string(original_string, max_length):
  if len(original_string) > max_length:
      return original_string[:max_length] + '...'
  else:
      return original_string

@client.event
async def on_ready():
  print("Get ready to kpop!")
  
@client.tree.command()
async def chart_live(interaction: discord.Interaction):
  """Gives the live Melon chart!"""
  await interaction.response.send_message("Loading your data...")
  live_chart = scrapeMelon.getList("LIVE").decode()
  data = json.loads(live_chart)
  print(data)

  embed = discord.Embed(title="Top 10 Songs - Live Melon Chart")

  for i in range(1, 26):
      item_key = str(i)
      item_data = data.get(item_key)

      if item_data:
          name = item_data.get("name")
          artists = item_data.get("artists")
          ranking = item_data.get("ranking")

          embed.add_field(name=f"{ranking}. {name}", value=f"Artists: {artists}", inline=False)

  await interaction.followup.send(embed=embed)  
  
@client.tree.command()
async def chart_day(interaction: discord.Interaction):
  """Gives the Melon chart for the day!"""
  await interaction.response.send_message("Loading your data...")
  day_chart = scrapeMelon.getList("DAY").decode()
  data = json.loads(day_chart)
  print(data)
  embed = discord.Embed(title="Top 10 Songs - Daily Melon Chart", color=discord.Color.red())

  for i in range(1, 26):
      item_key = str(i)
      item_data = data.get(item_key)

      if item_data:
          name = item_data.get("name")
          artists = item_data.get("artists")
          ranking = item_data.get("ranking")

          embed.add_field(name=f"{ranking}. {name}", value=f"Artists: {artists}", inline=False)

  await interaction.followup.send(embed=embed)

@client.tree.command()
async def chart_week(interaction: discord.Interaction):
  """Gives the Melon chart for the week!"""
  await interaction.response.send_message("Loading your data...")
  week_chart = scrapeMelon.getList("WEEK").decode()
  data = json.loads(week_chart)
  print(data)
  embed = discord.Embed(title="Top 10 Songs - Weekly Melon Chart", color=discord.Color.red())

  for i in range(1, 26):
      item_key = str(i)
      item_data = data.get(item_key)
  
      if item_data:
          name = item_data.get("name")
          artists = item_data.get("artists")
          ranking = item_data.get("ranking")
  
          embed.add_field(name=f"{ranking}. {name}", value=f"Artists: {artists}", inline=False)
  
  await interaction.followup.send(embed=embed)

@client.tree.command()
async def chart_month(interaction: discord.Interaction):
  """Gives the Melon chart for the month!"""
  await interaction.response.send_message("Loading your data...")
  month_chart = scrapeMelon.getList("MONTH").decode()
  data = json.loads(month_chart)
  print(data)
  embed = discord.Embed(title="Top 10 Songs - Monthly Melon Chart", color=discord.Color.red())
  for i in range(1, 26):
      item_key = str(i)
      item_data = data.get(item_key)

      if item_data:
          name = item_data.get("name")
          artists = item_data.get("artists")
          ranking = item_data.get("ranking")

          embed.add_field(name=f"{ranking}. {name}", value=f"Artists: {artists}", inline=False)

  await interaction.followup.send(embed=embed)

@client.tree.command()
@app_commands.describe(
  song_name="The name of the song you want the lyrics of"
)
async def search_lyrics(interaction: discord.Interaction, song_name: str):
  """Searches for the lyrics of a song!"""
  await interaction.response.send_message("Loading your data...")
  song_list = scrapeMelon.getList("LIVE").decode()
  data = json.loads(song_list)
  matching_item = next((item for item in data.values() if song_name.lower() in item.get("name", "").lower()), None)
  print(matching_item)
  if matching_item:
    lyrics = scrapeMelon.getLyric(matching_item.get("songId"))
    print(lyrics)
    send_lyrics = truncate_string(lyrics, 1990)
    print(send_lyrics)
    await interaction.followup.send(send_lyrics)

client.run("MTE3NjQ3MTU0ODM3OTU0OTc5Ng.GRUbG9.oC4n2uf-2CFD2k7jxeJ62Q3Jv7ysXB_Boop4Mw")
