import discord
from discord.ext import commands
from discord.utils import find
import asyncio

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(intents=intents, command_prefix=None)

@client.event
async def on_ready():
    print("Bin Ready!")
    while True:
        await client.change_presence(activity=discord.Game("@me for help!"))
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Game("Bro, its cold in here 🥶"))
        await asyncio.sleep(4)

@client.event
async def on_guild_join(guild):
    general = find(lambda x: x.name.lower() == 'general' or x.name.lower() == "chat" or x.name.lower() == "allgemein",  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send('Thanks for the invite!\n@me for help')

@client.event
async def on_message(ctx):
    if ctx.content == "<@926801089989333012>":
        prefix = "!"
        supported_prefixes = "`!, ?, ., -, _, $, %, &`"
        embed = discord.Embed(title="Freeze Bot", colour=discord.Colour(65535))
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/699904940231098459/879355861376573500/reFRZtransparent.png")
        embed.add_field(name="**Description**", value=f"The FRZ Bot is a Discord Bot made by Erik #8026 to analyse the stats of any map played in 6v6", inline=False)
        embed.add_field(name=f"**Requirements**", value=f"> You have to use Toadbot\n> You must have one channel for Toadbot stuff\n*else the bot is basically useless for your server*", inline=False)
        embed.add_field(name=f"**Setup**", value=f"Use `{prefix}setchannel` and `{prefix}setprefix`. Everything explained below!", inline=False)
        embed.set_footer(text="Bot made by Erik#8036", icon_url="https://cdn.discordapp.com/avatars/807602307369271306/746e74ccc5f3717d3fb1ec8489d5284d.png?size=1024")

        embed2 = discord.Embed(title="Setup Commands", colour=discord.Colour(65535))
        embed2.set_thumbnail(url="https://media.discordapp.net/attachments/699904940231098459/879355861376573500/reFRZtransparent.png")
        embed2.set_footer(text="Bot made by Erik#8036", icon_url="https://cdn.discordapp.com/avatars/807602307369271306/746e74ccc5f3717d3fb1ec8489d5284d.png?size=1024")
        embed2.add_field(name=f"`{prefix}setchannel`", value=f"Sets the Toadbot channel of your server\nCommand: `{prefix}setchannel <DiscordChannel>`", inline=False)
        embed2.add_field(name=f"`{prefix}setprefix`", value=f"Sets a custom prefix for your server\nCommand: `{prefix}setprefix <new_prefix>`\npre-entered prefix is `!`\nSupported Prefixes: {supported_prefixes}", inline=False)
        embed2.add_field(name=f"`{prefix}setpermsstats56`", value=f"Sets the permission to use the stats56 command to true or false\nCommand: `{prefix}setpermsstats56 <true/false>`\n> True: Only admins can use it\n> False: everyone can us it\n Default is true", inline=False)

        embed3 = discord.Embed(title="Stats Commands", colour=discord.Colour(65535))
        embed3.set_thumbnail(url="https://media.discordapp.net/attachments/699904940231098459/879355861376573500/reFRZtransparent.png")
        embed3.set_footer(text="Bot made by Erik#8036", icon_url="https://cdn.discordapp.com/avatars/807602307369271306/746e74ccc5f3717d3fb1ec8489d5284d.png?size=1024")
        embed3.add_field(name=f"`{prefix}stats`", value=f"Shows the stats of a specific map of a certain amount of wars\nCommand: `{prefix}stats <map> <count>`\n> `<map>`: short form of any MK8DX map. e. g. rMMM, rmmm, RMMM\n> `<count>`: The amount of wars where stats should be analysed. For performance its highly recommended to use this feature!", inline=False)
        embed3.add_field(name=f"`{prefix}overallstats`", value=f"Shows the stats of a every map of a certain amount of wars\nCommand: `{prefix}stats <count>`\n> `<count>`: The amount of wars where stats should be analysed. For performance its highly recommended to use this feature!", inline=False)
        embed3.add_field(name=f"`{prefix}stats56`", value=f"Shows the stats of every map of a certain amount entered\nCommand:`{prefix}stats56 <count>`\n> `<count>`: The amount of wars where stats should be analysed. For performance its highly recommended to use this feature!\nThe channel will be spammed quickly, make sure to have it disabled that not administrator can use this command if you want to!", inline=False)

        await ctx.channel.send(embeds=[embed, embed2, embed3])
    elif ctx.content == "botstats":
        if (ctx.author != "Erik#8036") or (not isinstance(ctx.channel, discord.DMChannel) is True):
            return
        server_count = len(client.guilds)
        servers = ""
        count = 1
        for server in client.guilds:
            servers = servers + f"`{count}.` **{server}**, Server Owner is: {client.get_user(int(server.owner.id))}\n"
            count += 1
        await ctx.channel.send(f"FRZ Bot is at the moment in **{server_count} servers**\nHere is a list of all servers:\n{servers}")
    else:
        return

client.run("token")
