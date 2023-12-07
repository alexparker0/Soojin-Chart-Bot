from melonapi import scrapeMelon
import discord
from discord.ext import commands
#from discord import app_commands
import os
import json

#MY_GUILD = discord.Object(id=1176471349896683550)
#class MyClient(discord.Client):
 # def __init__(self, *, intents: discord.Intents):
  #  super().__init__(intents=intents)
    # A CommandTree is a special type that holds all the application command
    # state required to make it work. This is a separate class because it
    # allows all the extra state to be opt-in.
    # Whenever you want to work with application commands, your tree is used
    # to store and work with them.
    # Note: When using commands.Bot instead of discord.Client, the bot will
    # maintain its own tree instead.
    #self.tree = app_commands.CommandTree(self)

intents = discord.Intents.default()
bot = commands.Bot("!", intents=intents)

@bot.event
async def on_ready():
  print("Get ready to kpop!")

  
#async def setup_hook(self):
    # This copies the global commands over to your guild.
   # self.tree.copy_global_to(guild=MY_GUILD)
    #await self.tree.sync(guild=MY_GUILD)




def truncate_string(original_string, max_length):
  if len(original_string) > max_length:
      return original_string[:max_length] + '...'
  else:
      return original_string


  
@bot.slash_command(name="live_chart", description="Gives the live Melon chart!")
async def live_chart(ctx):
  await ctx.respond("Loading your data...")
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

  await ctx.followup.send(embed=embed)  
  
@bot.slash_command(name="daily_chart", description="Gives the Melon chart of the day!")
async def daily_chart(ctx):
  await ctx.respond("Loading your data...")
  day_chart = scrapeMelon.getList("DAY").decode()
  data = json.loads(day_chart)
  print(data)
  embed = discord.Embed(title="Top 10 Songs - Daily Melon Chart")

  for i in range(1, 26):
      item_key = str(i)
      item_data = data.get(item_key)

      if item_data:
          name = item_data.get("name")
          artists = item_data.get("artists")
          ranking = item_data.get("ranking")

          embed.add_field(name=f"{ranking}. {name}", value=f"Artists: {artists}", inline=False)

  await ctx.followup.send(embed=embed)

@bot.slash_command(name="weekly_chart", description="Gives the Melon chart of the week!")
async def weekly_chart(ctx):
  await ctx.respond("Loading your data...")
  week_chart = scrapeMelon.getList("WEEK").decode()
  data = json.loads(week_chart)
  print(data)
  embed = discord.Embed(title="Top 10 Songs - Weekly Melon Chart")

  for i in range(1, 26):
      item_key = str(i)
      item_data = data.get(item_key)
  
      if item_data:
          name = item_data.get("name")
          artists = item_data.get("artists")
          ranking = item_data.get("ranking")
  
          embed.add_field(name=f"{ranking}. {name}", value=f"Artists: {artists}", inline=False)
  
  await ctx.followup.send(embed=embed)

@bot.slash_command(name="monthly_chart", description="Gives the Melon chart of the month!")
async def monthly_chart(ctx):
  await ctx.respond("Loading your data...")
  month_chart = scrapeMelon.getList("MONTH").decode()
  data = json.loads(month_chart)
  print(data)
  embed = discord.Embed(title="Top 10 Songs - Monthly Melon Chart")
  for i in range(1, 26):
      item_key = str(i)
      item_data = data.get(item_key)

      if item_data:
          name = item_data.get("name")
          artists = item_data.get("artists")
          ranking = item_data.get("ranking")

          embed.add_field(name=f"{ranking}. {name}", value=f"Artists: {artists}", inline=False)

  await ctx.followup.send(embed=embed)

@bot.slash_command(name="search_lyrics", description="Gives the lyrics of a song!")
async def search_lyrics(ctx, song_name: str):
  """Searches for the lyrics of a song!"""
  await ctx.respond("Loading your data...")
  song_list = scrapeMelon.getList("LIVE").decode()
  data = json.loads(song_list)
  matching_item = next((item for item in data.values() if song_name.lower() in item.get("name", "").lower()), None)
  print(matching_item)
  if matching_item:
    lyrics = scrapeMelon.getLyric(matching_item.get("songId"))
    print(lyrics)
    send_lyrics = truncate_string(lyrics, 1990)
    print(send_lyrics)
    await ctx.followup.send(send_lyrics)

bot.run("MTE3NjQ3MTU0ODM3OTU0OTc5Ng.GRUbG9.oC4n2uf-2CFD2k7jxeJ62Q3Jv7ysXB_Boop4Mw")
