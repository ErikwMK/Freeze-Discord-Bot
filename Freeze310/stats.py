# The FRZ Bot, a Discord.py Bot for Mario Kart 8 Deluxe.
# It analyses the stats of the maps a team played in a 6v6 war from the embeds of the toadbot
# The backend making it works on any servers is made with a Google spreadsheet
# The bot is made by Erik#0045

import discord
from discord.ext import commands
import asyncio
import gspread
# imports discord.py for the whole bot, asyncio for the bots status and gspread for the Google spreadsheet backend

# global maps_in_the_game
# maps_in_the_game = 56
gs = gspread.service_account("service_account.json")
sh = gs.open("FreezeBot")
wks = sh.worksheet("Servers")
# sets everything for the backend up

# functions for setting and getting data out of the spreadsheet
def AddServer(server):  # function: if bot joins a server, automatically fill everything in the spreadsheet
    if str(server.id) not in wks.col_values(1):
        wks.update_cell(len(wks.col_values(1)) + 1, 1, str(server.id))
        wks.update_cell(len(wks.col_values(1)), 2, str(server.name))
        wks.update_cell(len(wks.col_values(1)), 4, str("!"))
        wks.update_cell(len(wks.col_values(1)), 5, str("true"))

async def SetPrefix(ctx, prefix):  # function: updates the entered prefix in the spreadsheet
    supported_prefixes = ["!", "?", ".", "-", "_", "$", "%", "&"]
    if prefix not in supported_prefixes:
        await ctx.channel.send("Not supported prefix! Supported ones are: `!, ?, ., -, _, $, %, &`")
    if str(ctx.guild.id) not in wks.col_values(1):
        await ctx.channel.send("There is an error in the sheet! Please DM Erik#8036")
        return
    cell = wks.find(str(ctx.guild.id))
    wks.update_cell(cell.row, 4, str(prefix))

async def SetToadbot(ctx, toadbot):  # function: sets the toadbot_channel in the spreadsheet
    if str(ctx.guild.id) not in wks.col_values(1):
        await ctx.channel.send("There is an error in the sheet! Please DM Erik#8036")
        return
    cell = wks.find(str(ctx.guild.id))
    wks.update_cell(cell.row, 3, str(toadbot.id))

async def SetPermsStats56(ctx, bool):  # function: sets OnlyAdmin usage of stats56 command to true or false
    if bool.lower() != "true" or bool.lower() != "false":
        await ctx.channel.send("Use `True/False`! Default is set to false")
        return
    if str(ctx.guild.id) not in wks.col_values(1):
        await ctx.channel.send("There is an error in the sheet! Please DM Erik#8036")
        return
    cell = wks.find(str(ctx.guild.id))
    wks.update_cell(cell.row, 5, str(bool))

def GetPrefix(client, message):
    cell = wks.find(str(message.guild.id))
    prefix_cell = wks.cell(cell.row, 4).value
    return prefix_cell

def GetToadbot(guild):
    cell = wks.find(str(guild))
    toadbot_cell = wks.cell(cell.row, 3).value
    return toadbot_cell

def GetPermsStats56(guild):
    cell = wks.find(str(guild))
    getperms_cell = wks.cell(cell.row, 5).value
    bool_ = True
    if getperms_cell == "true":
        bool_ = True
    elif getperms_cell == "false":
        bool_ = False
    return bool_

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=GetPrefix, intents=intents)
class MyHelp(commands.HelpCommand):  # custom help command `!help`
    async def send_bot_help(self, mapping):
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
        embed2.add_field(name=f"`{prefix}setprefix`", value=f"Sets a custom prefix for your server\nCommand: `{prefix}setprefix <new_prefix>`\ndefault prefix is `!`\nSupported Prefixes: {supported_prefixes}", inline=False)
        embed2.add_field(name=f"`{prefix}setpermsstats56`", value=f"Sets the permission to use the stats56 command to true or false\nCommand: `{prefix}setpermsstats56 <true/false>`\n> True: Only admins can use it\n> False: everyone can us it\n Default is true", inline=False)

        embed3 = discord.Embed(title="Stats Commands", colour=discord.Colour(65535))
        embed3.set_thumbnail(url="https://media.discordapp.net/attachments/699904940231098459/879355861376573500/reFRZtransparent.png")
        embed3.set_footer(text="Bot made by Erik#8036", icon_url="https://cdn.discordapp.com/avatars/807602307369271306/746e74ccc5f3717d3fb1ec8489d5284d.png?size=1024")
        embed3.add_field(name=f"`{prefix}stats`", value=f"Shows the stats of a specific map of a certain amount of wars\nCommand: `{prefix}stats <map> <count>`\n> `<map>`: short form of any MK8DX map. e. g. rMMM, rmmm, RMMM\n> `<count>`: The amount of wars where stats should be analysed. For performance its highly recommended to use this feature!", inline=False)
        embed3.add_field(name=f"`{prefix}overallstats`", value=f"Shows the stats of a every map of a certain amount of wars\nCommand: `{prefix}stats <count>`\n> `<count>`: The amount of wars where stats should be analysed. For performance its highly recommended to use this feature!", inline=False)
        embed3.add_field(name=f"`{prefix}stats56`", value=f"Shows the stats of every map of a certain amount entered\nCommand:`{prefix}stats56 <count>`\n> `<count>`: The amount of wars where stats should be analysed. For performance its highly recommended to use this feature!\nThe channel will be spammed quickly, make sure to have it disabled that not leaders (people with manage_messages permission) can use this command if you want to!", inline=False)

        channel = self.get_destination()
        await channel.send(embeds=[embed, embed2, embed3])
client.help_command = MyHelp()

@client.event
async def on_ready():  # login: set status
    print("Bin Ready!")

@client.event
async def on_command_error(ctx, error):  # Errorhandler
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send("Argument missing! Use `@me for help`")
        return
    if isinstance(error, commands.BadArgument):
        await ctx.channel.send("Argument False! @me for help")
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.channel.send("You don't have permission to use this command!")
        return
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.channel.send('This command has a cooldown of 5 minutes, please try again in {:.0f} seconds'.format(error.retry_after))
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.channel.send("Me is missing a permission to do this! Please check")
    if isinstance(error, commands.CommandInvokeError):
        await ctx.channel.send("Unexpected error! Pls DM Erik#8036 if this happens again")
        return
    if isinstance(error, AttributeError):
        return
    else:
        await ctx.channel.send("Unexpected error! Pls DM Erik#8036 if this happens again")

@client.event
async def on_guild_join(guild):  # event for AddServer function
    AddServer(guild)

@client.command(name="settoadbot")
async def SetToadbotCommand(ctx, channel: discord.TextChannel):  # Command for SetToadBotFunction
    await SetToadbot(ctx, channel)
    await ctx.channel.send("Done!")

@client.command(name="setprefix")
async def SetPrefixCommand(ctx, prefix):  # Command for SetPrefixFunction
    await SetPrefix(ctx, prefix)
    await ctx.channel.send("Done!")

@client.command(name="setpermsstats56")
async def SetPermsStats56Command(ctx, bool):  # Command for SetPermsFunction
    await SetPermsStats56(ctx, bool.lower())
    await ctx.channel.send("Done!")

@client.command(name="mapstats", aliases=["ms"])
async def mapstats(ctx, map, count: int = None):  # mapstats command: analyse the data of the toadbot channel
    toadchannel_id = int(GetToadbot(str(ctx.guild.id)))
    if count is None:  # sets the limit of message history
        limit = None
    elif int(count) < 0:  # if number < 0, give error
        ctx.channel.send("The number of wars is invalid!")
        return
    else:  # converts to wars into messages for limit
        try:
            limit = int(count) * 12 * 3 + 1
        except Exception:
            ctx.channel.send("The number of wars is invalid!")
            return
    process_msg = await ctx.channel.send("❗ **The process of the analysation will take a bit! Please be patient and don't add another command when it's not working in a few seconds!** ❗")
    map = map.lower()  # checks if the map is valid
    if map.lower() in ["mks", "wp", "ssc", "tr", "mc", "th", "tm", "sgf", "sa", "ds", "ed", "mw", "cc", "bdd", "bc",
                       "rr", "rmmm", "rmc", "rccb", "rtt", "rddd", "rdp3", "rrry", "rdkj", "rws", "rsl", "rmp", "ryv",
                       "rttc", "rpps", "rgv", "rrrd", "dyc", "dea", "ddd", "dmc", "dwgm", "drr", "diio", "dhc", "dBP",
                       "dcl", "dww", "dac", "dnbc", "drir", "dsbs", "dbb", "bpp", "btc", "bcm64", "bcmo", "bch", "bcmw",
                       "bcma", "bcom", "btb", "bsr", "bsg", "bnh"]:
        # gives the long form of the map and link for embed
        if map.lower() == "mks":
            track_shown = "**Mario Kart Stadium (MKS)**"
            l = "https://images-ext-2.discordapp.net/external/_Uf097v5rOGaoLyt0D_ZbcHesmnH70Mz67ZcIxw5l0g/https/i.imgur.com/x2KufpY.png"
        elif map.lower() == "wp":
            track_shown = "**Water Park (WP)**"
            l = "https://images-ext-2.discordapp.net/external/_0RyxvSKHHkFbHGozhD0sDQulInS1Z7gw6lQQTvG8-k/https/i.imgur.com/oRKjkU4.png"
        elif map.lower() == "ssc":
            track_shown = "**Sweet Sweet Canyon (SSC)**"
            l = "https://images-ext-2.discordapp.net/external/g4TCl2kB9i1rEaD4qvrYXliFE-GSVYPbmsdSkgz7oOA/https/i.imgur.com/FNd8cqL.png"
        elif map.lower() == "tr":
            track_shown = "**Thwomp Ruins (TR)**"
            l = "https://images-ext-1.discordapp.net/external/2KKxkZBNG8xoKO_B8mWcOHYBelqOo9WMFaRdDgK7GPU/https/i.imgur.com/CqWeTRF.png"
        elif map.lower() == "mc":
            track_shown = "**Mario Circuit (MC)**"
            l = "https://images-ext-2.discordapp.net/external/78-ECGwrSxMPxV1BkWV78WI1j2mbZg79sJ44r5wtyHc/https/i.imgur.com/kLWQ3PG.png"
        elif map.lower() == "th":
            track_shown = "**Toad Harbor (TH)**"
            l = "https://images-ext-2.discordapp.net/external/suCjE8V-YTtHy-ExuM9QdnCb7GjtYGuiqavldN562XE/https/i.imgur.com/FYu4brr.png"
        elif map.lower() == "tm":
            track_shown = "**Twisted Mansion (TM)**"
            l = "https://images-ext-2.discordapp.net/external/EtxNCLxssibCTu3BJYpGG2xf7CIcoj8yWjPK5o_WgDk/https/i.imgur.com/gDqTSTK.png"
        elif map.lower() == "sgf":
            track_shown = "**Shy Guy Falls (SGF)**"
            l = "https://images-ext-1.discordapp.net/external/dp8q5kNo0Qha9niqqF2VVmfT-zUGFmce9LLaxWPd3NY/https/i.imgur.com/u1DldtB.png"
        elif map.lower() == "sa":
            track_shown = "**Sunshine Airport (SA)**"
            l = "https://images-ext-2.discordapp.net/external/A63KGCm3QCeMWPkOcjn8uRmZAKkXdTsKs01nGAhmIUU/https/i.imgur.com/AHMg0iD.png"
        elif map.lower() == "ds":
            track_shown = "**Dolphin Shoals (DS)**"
            l = "https://images-ext-1.discordapp.net/external/vMhKuI5Z9rheJfsouyE3eFBlr_djUfwLestWNACtZIg/https/i.imgur.com/S8bSb2i.png"
        elif map.lower() == "ed":
            track_shown = "**Electrodrome (ED)**"
            l = "https://images-ext-1.discordapp.net/external/ypTysMD6l4RLJQFS9CWdTyMG9JCWvKGGhAhkGlfdQIo/https/i.imgur.com/IzFL0Wy.png"
        elif map.lower() == "mw":
            track_shown = "**Mount Wario (MW)**"
            l = "https://images-ext-2.discordapp.net/external/RRMPB_7_4pZaGJuZKgBFjoRDOY22LxUh1u8sprJXGOE/https/i.imgur.com/D5AGGZk.png"
        elif map.lower() == "cc":
            track_shown = "**Cloudtop Cruise (CC)**"
            l = "https://images-ext-1.discordapp.net/external/tO7Vgf2YcJ5B7167z6kAaux5fATh-FrG3UrkoNwNtpE/https/i.imgur.com/kocoKcq.png"
        elif map.lower() == "bdd":
            track_shown = "**Bone-Dry Dunes (BDD)**"
            l = "https://images-ext-1.discordapp.net/external/9RGtZleR5Cv8nyHXHb42XjmER1DJ6JABFFA4aVgplKU/https/i.imgur.com/ChMkdXy.png"
        elif map.lower == "bc":
            track_shown = "**Bowser\'s Castle (BC)**"
            l = "https://images-ext-1.discordapp.net/external/uCV-JqA-L-A844wlDRE0c0ArwroeljE93H4ZKN3PMt8/https/i.imgur.com/F4i4OTB.png"
        elif map.lower() == "rr":
            track_shown = "**Rainbow Road (RR)**"
            l = "https://images-ext-2.discordapp.net/external/sK75OxBy4beSnFuiQ9b82XwSWQqDKSVJwW4JsozKnao/https/i.imgur.com/Gq8ynLF.png"
        elif map.lower() == "rmmm":
            track_shown = "**Wii Moo Moo Meadows (rMMM)**"
            l = "https://images-ext-2.discordapp.net/external/CY4j84Z_l_hwubdZUBaOfLfK3-LsxieU12kfi3Wjz8Q/https/i.imgur.com/bAhUGdN.png"
        elif map.lower() == "rmc":
            track_shown = "**GBA Mario Circuit (rMC)**"
            l = "https://images-ext-2.discordapp.net/external/zxpBNNQV9bnWHfewm9-PvHmhDlxa6yVtlfoHiA0tHjo/https/i.imgur.com/gB4c69G.png"
        elif map.lower() == "rccb":
            track_shown = "**DS Cheep Cheep Beach (rCCB)**"
            l = "https://images-ext-2.discordapp.net/external/YHueaD-VXA8HnAM1ZZZGm1aoQJWMiYUilC2h8V_UxJA/https/i.imgur.com/pTmv1ng.png"
        elif map.lower() == "rtt":
            track_shown = "** N64 Toad\'s Turnpike (rTT)**"
            l = "https://images-ext-1.discordapp.net/external/MHNzqb2vzIVWa-pyfqfCKb1HEfBEZWcCseawmfk1XHQ/https/i.imgur.com/NshE4yu.png"
        elif map.lower() == "rddd":
            track_shown = "**GCN Dry Dry Desert (rDDD)**"
            l = "https://images-ext-1.discordapp.net/external/NC00hiaM6uAoZHWKsYt9mbJwUpUl82e1DbyhtJxGdCA/https/i.imgur.com/QAuzvJB.png"
        elif map.lower() == "rdp3":
            track_shown = "**SNES Donut Plains 3 (rDP3)**"
            l = "https://images-ext-2.discordapp.net/external/j6zV5qDXkSw1EFbfuzj8brNU0AyWkGr5e9er0cuqzj0/https/i.imgur.com/rELdEcJ.png"
        elif map.lower() == "rrry":
            track_shown = "**N64 Royal Raceway (rRRy)**"
            l = "https://images-ext-1.discordapp.net/external/6YFo1w8HmpDkZ9wM-Wm2AmuAK78ltDdiwVp5cexXvpU/https/i.imgur.com/wF0P4L0.png"
        elif map.lower() == "rdkj":
            track_shown = "**3DS DK Jungle (rDKJ)**"
            l = "https://images-ext-1.discordapp.net/external/Og1SD2Dua1mZoJ6IQW6ItVejVZg2E99xUy9R6aYwF8c/https/i.imgur.com/vcGy5bY.png"
        elif map.lower() == "rws":
            track_shown = "**DS Wario Stadium (rWS)**"
            l = "https://images-ext-2.discordapp.net/external/mGhG3ws0QSDtgpYmc2cDzquDYyRDcfTQ7RKGG5WhwTs/https/i.imgur.com/l0fXw5q.png"
        elif map.lower() == "rsl":
            track_shown = "**GCN Sherbet Land (rSL)**"
            l = "https://images-ext-2.discordapp.net/external/uagElNkQI2PWMn7DBASIo840_kyLWb0JyLNGKxmCptk/https/i.imgur.com/KR5hpqy.png"
        elif map.lower() == "rmp":
            track_shown = "**3DS Music Park(rMP)**"
            l = "https://images-ext-2.discordapp.net/external/hbR_5RK75W5lojtUKFArnOxjeuMv4V0gefNm8UQIbxw/https/i.imgur.com/mo37kKo.png"
        elif map.lower() == "ryv":
            track_shown = "**N64 Yoshi Valley (rYV)**"
            l = "https://images-ext-2.discordapp.net/external/UrrtZSdKG4VOr-2z6S1YS-mpqd22SLXJrf4SlHlPZZs/https/i.imgur.com/uymaWqK.png"
        elif map.lower() == "rttc":
            track_shown = "**DS Tick-Tock Clock (rTTC)**"
            l = "https://images-ext-2.discordapp.net/external/hg-WVUyn5PcCb88tbjuFkcr6epfSPPZkhUgkz1jxBKc/https/i.imgur.com/2JituCs.png"
        elif map.lower() == "rpps":
            track_shown = "**3DS Piranha plant Slide (rPPS)**"
            l = "https://images-ext-1.discordapp.net/external/z99OC5pWBJ7Xc4nkhNqWj4VxqwgBEfsjgAfnMd21-ZI/https/i.imgur.com/5i6A3II.png"
        elif map.lower() == "rgv":
            track_shown = "**Wii Grumble Volcano (rGV)**"
            l = "https://images-ext-2.discordapp.net/external/pTxGnePtu5UhGCmSipCLmXw8ebH1dzsf9_3jv-55hos/https/i.imgur.com/WGS2ojx.png"
        elif map.lower() == "rrrd":
            track_shown = "**N64 Rainbow Road (rRRd)**"
            l = "https://images-ext-1.discordapp.net/external/aKzWCsYyPFkc6gjNPBXYn6E0z5AgIbJq8UFDC3o1RQk/https/i.imgur.com/qflI1QP.png"
        elif map.lower() == "dyc":
            track_shown = "**GCN Yoshi Circuit (dYC)**"
            l = "https://images-ext-2.discordapp.net/external/SN3a5jdlADWK5hKeg7r-eTJaNAQhTct6d6rlSNNjlFg/https/i.imgur.com/bvkqGEL.png"
        elif map.lower() == "dea":
            track_shown = "**Excite Bike Arena (dEA)**"
            l = "https://images-ext-1.discordapp.net/external/5_cJ92ZV6-wqKig2fSV2NJaQYoPtV5hcPij8AtEW1H4/https/i.imgur.com/H3h3JT0.png"
        elif map.lower() == "ddd":
            track_shown = "**Dragon Driftway (dDD)**"
            l = "https://images-ext-2.discordapp.net/external/KLR6fC8Cbdu5grOaKsG8EQSsSgu3eHXyJuxnt2XptEo/https/i.imgur.com/LeYOzs1.png"
        elif map.lower() == "dmc":
            track_shown = "**Mute City (dMC)**"
            l = "https://images-ext-1.discordapp.net/external/2gmyNfyyePllHR1ewdKKUOY9l5RoVoxsTkQO--zrvDA/https/i.imgur.com/224DyTF.png"
        elif map.lower() == "dwgm":
            track_shown = "**Wii Wario\'s Gold Mine (dWGM)**"
            l = "https://images-ext-1.discordapp.net/external/GddNL-hmWbENA4AUCAnHhJQHB_bMl1s-s1gUvnQ6th0/https/i.imgur.com/Pjyewat.png"
        elif map.lower() == "drr":
            track_shown = "**SNES Rainbow Road (dRR)**"
            l = "https://images-ext-1.discordapp.net/external/WW8spbvRLUfFlDVg-lQwn-Q_z82clCSpDkRZ-5n3pzI/https/i.imgur.com/ogwuCwZ.png"
        elif map.lower() == "diio":
            track_shown = "**Ice Ice Outpost (dIIO)**"
            l = "https://images-ext-1.discordapp.net/external/0ITvNvoUoWUTv-HifmeCYmReqCrzi8lZ4Eoh0haj5zU/https/i.imgur.com/X4QD87f.png"
        elif map.lower() == "dhc":
            track_shown = "**Hyrule Circuit (dHC)**"
            l = "https://images-ext-2.discordapp.net/external/KzNks7dOoO6oicnGvZOB5OPzCkC8Hsvlqg89RYBu-xE/https/i.imgur.com/eM2YHQw.png"
        elif map.lower() == "dbp":
            track_shown = "**GCN Baby Park (dBP)**"
            l = "https://images-ext-1.discordapp.net/external/NVdasyrMIZinw_6s10wcNFY28r6i4PEg6WUtf7xXBvc/https/i.imgur.com/DKAXxiW.png"
        elif map.lower() == "dcl":
            track_shown = "**GBA Cheese Land (dCL)**"
            l = "https://images-ext-2.discordapp.net/external/Be5wTkv0wHiv97u7esFLCWzE45SCbi4pgg8AV_XA5zs/https/i.imgur.com/JVPSAtV.png"
        elif map.lower() == "dww":
            track_shown = "**Wild Woods (dWW)**"
            l = "https://images-ext-2.discordapp.net/external/ZHmmOS6kC5Cr4vxdHImdrrPVJ77VkN7Pi81oEM3RF30/https/i.imgur.com/5TZg4kh.png"
        elif map.lower() == "dac":
            track_shown = "**Animal Crossing (dAC)**"
            l = "https://images-ext-1.discordapp.net/external/DyYiBqof494_j66puFOelfoiVQCtAWok0cgLLpvl8KA/https/i.imgur.com/cjNpw2m.png"
        elif map.lower() == "dnbc":
            track_shown = "**3DS Neo Bowser City (dNBC)**"
            l = "https://images-ext-1.discordapp.net/external/44MHipqSAqyFYjKjjyF8vcJaFVjlL9nncM9MDXmk9WU/https/i.imgur.com/dfvv1Uw.png"
        elif map.lower() == "drir":
            track_shown = "**GBA Ribbon Road (dRiR)**"
            l = "https://images-ext-2.discordapp.net/external/DKwFQv8GNOLv9kq2TD5jgmucCIcF4aeT1RElsL0zRcY/https/i.imgur.com/Uc597hp.png"
        elif map.lower() == "dsbs":
            track_shown = "**Super Bell Subway (dSBS)**"
            l = "https://images-ext-1.discordapp.net/external/3gG88U2Xvu428zmDd1YxxIyzU1iMURCVBBqJSAHZjA0/https/i.imgur.com/spI2tsr.png"
        elif map.lower() == "dbb":
            track_shown = "**Big Blue (dBB)**"
            l = "https://images-ext-1.discordapp.net/external/frpsxwFnrLz-kYwCZbwZ5-XO7B8Xe_oMfR2bUohAA2Y/https/i.imgur.com/C1YYKFH.png"
        elif map.lower() == "bpp":
            track_shown = "**Tour Paris Promenade (bPP)**"
            l = "https://images-ext-2.discordapp.net/external/bLVril6oc46zUNEkZ8Nz18ZtW5M854ZNmW0CMsIbwvY/https/i.imgur.com/rrwvSjq.png"
        elif map.lower() == "btc":
            track_shown = "**3DS Toad Circuit (bTC)**"
            l = "https://images-ext-1.discordapp.net/external/ekilPteazkHz4Vy5l0rquDSwpwOQHlMoMzJHpCH-YGk/https/i.imgur.com/bK9csi6.png"
        elif map.lower() == "bcm64" or map.lower() == "bcmo" or map.lower() == "bchm":
            track_shown = "**N64 Choco Mountain (bCMo)**"
            l = "https://images-ext-1.discordapp.net/external/BJAbSbZ6eSuoYu7dfD01ePL6l-ec2Igj29y-w6AGpTw/https/i.imgur.com/ktqlNP7.png"
        elif map.lower() == "bcmw" or map.lower() == "bcma" or map.lower() == "bcom":
            track_shown = "**Wii Coconut Mall (bCMa)**"
            l = "https://images-ext-1.discordapp.net/external/EHTZ0Is0L_gfqF_yoB44-PuOqnWKtMZJOECSRdBlsDI/https/i.imgur.com/EUXlLQ6.png"
        elif map.lower() == "btb":
            track_shown = "**Tour Tokyo Blur (bTB)**"
            l = "https://images-ext-2.discordapp.net/external/mshUVNu-AtQJbeim02rP6dnUtudPKsv0fUuULeMKbRQ/https/i.imgur.com/bIHXjVC.png"
        elif map.lower() == "bsr":
            track_shown = "**DS Shroom Ridge (bSR)**"
            l = "https://images-ext-2.discordapp.net/external/IdtY222Uizlw0X2erPq5D46FB2d-Aek_PRHTCotMa3c/https/i.imgur.com/4XTF56w.png"
        elif map.lower() == "bsg":
            track_shown = "**GBA Sky Garden (bSG)**"
            l = "https://images-ext-2.discordapp.net/external/47avJT2DLdC15DMGYI26JEFsZ6eJjy6jTf0wvP_hkd4/https/i.imgur.com/efMObR1.png"
        elif map.lower() == "bnh":
            track_shown = "**Ninja Hideway (bNH)**"
            l = "https://images-ext-1.discordapp.net/external/RKcMfdqHd3dC0d7x2IZktDtO40zjTTEn2z2VufOHefo/https/i.imgur.com/o9RWZ0t.png"
        else:
            return
    else:
        await ctx.channel.send("This map doesn't exist!")
        await process_msg.delete()
        return
    toadchannel = client.get_channel(toadchannel_id)
    msglist = await toadchannel.history(limit=limit).flatten()
    all_differences = []  # all spots played in the amount of wars
    for i in msglist:  # gets the spot of every 6v6 race and writes it into the list ^
        embeds = i.embeds
        for embed in embeds:  # analyses all data and puts it into lists
            track_asked_for = track_shown.split(" (")[0].split("**")[1].split("**")[0]
            try:
                if embed.title.startswith("Score") and embed.fields[4].value.startswith(track_asked_for):
                    all_differences.append(int(embed.fields[3].value))
                else:
                    pass
            except:
                pass
    # times the map was player
    count_list_map_played = int(len(all_differences))
    if count_list_map_played == 0:  # for maps which haven't been played
        embed = discord.Embed(colour=discord.Colour(65535))
        embed.set_thumbnail(url=l)
        embed.add_field(name=f"This map wasn't played in the amount of wars, you entered!", value="Enter a higher amount!", inline=False)
        await ctx.channel.send(embed=embed)
        await process_msg.delete()
        return
    # average of difference
    avg_difference = round(sum(all_differences) / len(all_differences), 2)
    if avg_difference > 0:  # all analysed data
        avg_difference = f"+{avg_difference}"
    else:
        pass
    max_difference = max(all_differences)
    if max_difference > 0:
        max_difference = f"+{max_difference}"
    min_difference = min(all_differences)
    if min_difference > 0:
        min_difference = f"+{min_difference}"
    last_difference = all_differences[-1]
    if last_difference > 0:
        last_difference = f"+{last_difference}"

    if count is None:  # prints embed
        embed_name = f"In all wars, "
    else:
        embed_name = f"In the last {count} wars, "
    embed = discord.Embed(colour=discord.Colour(65535))
    embed.set_thumbnail(url=l)
    embed.add_field(name=f"{embed_name}{track_shown} was played {count_list_map_played} times.", value="Here the stats:", inline=False)
    embed.add_field(name=f"Average score: ", value=f"{avg_difference}", inline=False)
    embed.add_field(name=f"Last score: ", value=f"{last_difference}", inline=False)
    embed.add_field(name=f"Maximum score: ", value=f"{max_difference}", inline=False)
    embed.add_field(name=f"Minimum score: ", value=f"{min_difference}", inline=False)
    await ctx.channel.send(embed=embed)
    await process_msg.delete()
    return

@client.command(name="stats56")
async def stats56(ctx, count: int = None):
    if GetPermsStats56(str(ctx.guild.id)) is True:
        if "manage_messages" not in [perm[0] for perm in ctx.author.guild_permissions if perm[1]]:
            await ctx.channel.send("You don't have permission to use this command!")
            return
    toadchannel_id = int(GetToadbot(str(ctx.guild.id)))  # gets the toadbot channel out of the GetToadbot function
    if count is None:  # sets the limit
        limit = None
    elif int(count) < 0:
        ctx.channel.send("The number of wars is invalid!")
        return
    else:
        try:
            limit = int(count) * 12 * 3 + 1
        except Exception:
            ctx.channel.send("The number of wars is invalid!")
            return
    process_msg = await ctx.channel.send("❗ **The process of the analysation will take a bit! Please be patient and don't add another command when it's not working in a few seconds!** ❗")
    toadchannel = client.get_channel(toadchannel_id)
    msglist = await toadchannel.history(limit=limit).flatten()
    all_differences = []  # lists for every map
    MKS = []
    WP = []
    SSC = []
    TR = []
    MC = []
    TH = []
    TM = []
    SGF = []
    SA = []
    DS = []
    ED = []
    MW = []
    CC = []
    BDD = []
    BC = []
    RR = []
    rMMM = []
    rMC = []
    rCCB = []
    rTT = []
    rDDD = []
    rDP3 = []
    rRRy = []
    rDKJ = []
    rWS = []
    rSL = []
    rMP = []
    rYV = []
    rTTC = []
    rPPS = []
    rGV = []
    rRRd = []
    dYC = []
    dEA = []
    dDD = []
    dMC = []
    dWGM = []
    dRR = []
    dIIO = []
    dHC = []
    dBP = []
    dCL = []
    dWW = []
    dAC = []
    dNBC = []
    dRiR = []
    dSBS = []
    dBB = []
    bPP = []
    bTC = []
    bCMo = []
    bCMa = []
    bTB = []
    bSR = []
    bSG = []
    bNH = []
    for i in msglist:  # gets the spot of every 6v6 race and writes it into the list ^
        embeds = i.embeds
        for embed in embeds:
            try:
                if embed.title.startswith("Score"):
                    all_differences.append(int(embed.fields[3].value))
                    if embed.fields[4].value == "Mario Kart Stadium":
                        MKS.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Water Park":
                        WP.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Sweet Sweet Canyon":
                        SSC.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Thwomb Ruins":
                        TR.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Mario Circuit":
                        MC.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Toad Harbor":
                        TH.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Twisted Mansion":
                        TM.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Shy Guy Falls":
                        SGF.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Sunshine Airport":
                        SA.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Dolphin Shoals":
                        DS.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Electrodrome":
                        ED.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Mount Wario":
                        MW.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Cloudtop Cruise":
                        CC.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Bone-Dry Dunes":
                        BDD.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Bowser's Castle":
                        BC.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Rainbow Road":
                        RR.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Wii Moo Moo Meadows":
                        rMMM.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "GBA Mario Circuit":
                        rMC.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "DS Cheep Cheep Beach":
                        rCCB.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "N64 Toads Turnpike":
                        rTT.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "GCN Dry Dry Desert":
                        rDDD.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "SNES Donut Plains 3":
                        rDP3.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "N64 Royal Raceway":
                        rRRy.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "3DS DK Jungle":
                        rDKJ.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "DS Wario Stadium":
                        rWS.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "GCN Sherbert Land":
                        rSL.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "3DS Music Park":
                        rMP.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "N64 Yoshi Valley":
                        rYV.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "DS Tick-Tock Clock":
                        rTTC.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "3DS Piranha Plant Slide":
                        rPPS.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Wii Grumble Volcano":
                        rGV.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "N64 Rainbow Road":
                        rRRd.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "GCN Yoshi Circuit":
                        dYC.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Excitebike Arena":
                        dEA.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Dragon Driftway":
                        dDD.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Mute City":
                        dMC.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Wii Wario's Gold Mine":
                        dWGM.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "SNES Rainbow Road":
                        dRR.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Ice Ice Outpost":
                        dIIO.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Hyrule Circuit":
                        dHC.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "GCN Baby Park":
                        dBP.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "GBA Cheeseland":
                        dCL.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Wild Woods":
                        dWW.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Animal Crossing":
                        dAC.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "3DS Neo Bowser City":
                        dNBC.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "GBA Ribbon Road":
                        dRiR.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Super Bell Subway":
                        dSBS.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Big Blue":
                        dBB.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Tour Paris Promenade":
                        bPP.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "DS Toad Circuit":
                        bTC.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "N64 Choco Mountain":
                        bCMo.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Wii Coconut Mall":
                        bCMa.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Tour Tokyo Blur":
                        bTB.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "DS Shroom Ridge":
                        bSR.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "GBA Sky Garden":
                        bSG.append(int(embed.fields[3].value))
                    elif embed.fields[4].value == "Ninja Hideway":
                        bNH.append(int(embed.fields[3].value))
            except IndexError:
                continue
            except AttributeError:
                pass
    embed_list = []
    if len(all_differences) == 0:  # embed if no maps
        embed_not_played = discord.Embed(colour=discord.Colour(65535))
        embed_not_played.set_thumbnail(url="https://media.discordapp.net/attachments/932023933392285706/932024135041814528/reFRZtransparent.png")
        embed_not_played.add_field(name=f"There was no map played in the amount of wars you entered!", value="Enter a higher amount!", inline=False)
        await ctx.channel.send(embed=embed_not_played)
        return
    else:  # embed for all maps
        if count is None:
            embed_name = f"of all wars, "
        else:
            embed_name = f"of the last {count} wars, "
        avg_difference = round(sum(all_differences) / len(all_differences), 2)
        max_difference = max(all_differences)
        min_difference = min(all_differences)
        embed_played_all = discord.Embed(colour=discord.Colour(65535))
        embed_played_all.set_thumbnail(url="https://media.discordapp.net/attachments/932023933392285706/932024135041814528/reFRZtransparent.png")
        embed_played_all.add_field(name=f"Overall stats from {embed_name}and of every map.", value="Here the stats:", inline=False)
        embed_played_all.add_field(name=f"Average score: ", value=f"{avg_difference}", inline=False)
        embed_played_all.add_field(name=f"Maximum score: ", value=f"{max_difference}", inline=False)
        embed_played_all.add_field(name=f"Minimum score: ", value=f"{min_difference}", inline=False)
        embed_list.append(embed_played_all)

    maps_list = [MKS, WP, SSC, TR, MC, TH, TM, SGF, SA, DS, ED, MW, CC, BDD, BC, RR, rMMM, rMC, rCCB, rTT, rDDD, rDP3,
                 rRRy, rDKJ, rWS, rSL, rMP, rYV, rTTC, rPPS, rGV, rRRd, dYC, dEA, dDD, dMC, dWGM, dRR, dIIO, dHC, dBP,
                 dCL, dWW, dAC, dNBC, dRiR, dSBS, dBB, bPP, bTC, bCMo, bCMa, bTB, bSG, bSR, bNH]  # for loop
    links = [
        "https://images-ext-2.discordapp.net/external/_Uf097v5rOGaoLyt0D_ZbcHesmnH70Mz67ZcIxw5l0g/https/i.imgur.com/x2KufpY.png",
        "https://images-ext-2.discordapp.net/external/_0RyxvSKHHkFbHGozhD0sDQulInS1Z7gw6lQQTvG8-k/https/i.imgur.com/oRKjkU4.png",
        "https://images-ext-2.discordapp.net/external/g4TCl2kB9i1rEaD4qvrYXliFE-GSVYPbmsdSkgz7oOA/https/i.imgur.com/FNd8cqL.png",
        "https://images-ext-1.discordapp.net/external/2KKxkZBNG8xoKO_B8mWcOHYBelqOo9WMFaRdDgK7GPU/https/i.imgur.com/CqWeTRF.png",
        "https://images-ext-2.discordapp.net/external/78-ECGwrSxMPxV1BkWV78WI1j2mbZg79sJ44r5wtyHc/https/i.imgur.com/kLWQ3PG.png",
        "https://images-ext-2.discordapp.net/external/suCjE8V-YTtHy-ExuM9QdnCb7GjtYGuiqavldN562XE/https/i.imgur.com/FYu4brr.png",
        "https://images-ext-2.discordapp.net/external/EtxNCLxssibCTu3BJYpGG2xf7CIcoj8yWjPK5o_WgDk/https/i.imgur.com/gDqTSTK.png",
        "https://images-ext-1.discordapp.net/external/dp8q5kNo0Qha9niqqF2VVmfT-zUGFmce9LLaxWPd3NY/https/i.imgur.com/u1DldtB.png",
        "https://images-ext-2.discordapp.net/external/A63KGCm3QCeMWPkOcjn8uRmZAKkXdTsKs01nGAhmIUU/https/i.imgur.com/AHMg0iD.png",
        "https://images-ext-1.discordapp.net/external/vMhKuI5Z9rheJfsouyE3eFBlr_djUfwLestWNACtZIg/https/i.imgur.com/S8bSb2i.png",
        "https://images-ext-1.discordapp.net/external/ypTysMD6l4RLJQFS9CWdTyMG9JCWvKGGhAhkGlfdQIo/https/i.imgur.com/IzFL0Wy.png",
        "https://images-ext-2.discordapp.net/external/RRMPB_7_4pZaGJuZKgBFjoRDOY22LxUh1u8sprJXGOE/https/i.imgur.com/D5AGGZk.png",
        "https://images-ext-1.discordapp.net/external/tO7Vgf2YcJ5B7167z6kAaux5fATh-FrG3UrkoNwNtpE/https/i.imgur.com/kocoKcq.png",
        "https://images-ext-1.discordapp.net/external/9RGtZleR5Cv8nyHXHb42XjmER1DJ6JABFFA4aVgplKU/https/i.imgur.com/ChMkdXy.png",
        "https://images-ext-1.discordapp.net/external/uCV-JqA-L-A844wlDRE0c0ArwroeljE93H4ZKN3PMt8/https/i.imgur.com/F4i4OTB.png",
        "https://images-ext-2.discordapp.net/external/sK75OxBy4beSnFuiQ9b82XwSWQqDKSVJwW4JsozKnao/https/i.imgur.com/Gq8ynLF.png",
        "https://images-ext-2.discordapp.net/external/CY4j84Z_l_hwubdZUBaOfLfK3-LsxieU12kfi3Wjz8Q/https/i.imgur.com/bAhUGdN.png",
        "https://images-ext-2.discordapp.net/external/zxpBNNQV9bnWHfewm9-PvHmhDlxa6yVtlfoHiA0tHjo/https/i.imgur.com/gB4c69G.png",
        "https://images-ext-2.discordapp.net/external/YHueaD-VXA8HnAM1ZZZGm1aoQJWMiYUilC2h8V_UxJA/https/i.imgur.com/pTmv1ng.png",
        "https://images-ext-1.discordapp.net/external/MHNzqb2vzIVWa-pyfqfCKb1HEfBEZWcCseawmfk1XHQ/https/i.imgur.com/NshE4yu.png",
        "https://images-ext-1.discordapp.net/external/NC00hiaM6uAoZHWKsYt9mbJwUpUl82e1DbyhtJxGdCA/https/i.imgur.com/QAuzvJB.png",
        "https://images-ext-2.discordapp.net/external/j6zV5qDXkSw1EFbfuzj8brNU0AyWkGr5e9er0cuqzj0/https/i.imgur.com/rELdEcJ.png",
        "https://images-ext-1.discordapp.net/external/6YFo1w8HmpDkZ9wM-Wm2AmuAK78ltDdiwVp5cexXvpU/https/i.imgur.com/wF0P4L0.png",
        "https://images-ext-1.discordapp.net/external/Og1SD2Dua1mZoJ6IQW6ItVejVZg2E99xUy9R6aYwF8c/https/i.imgur.com/vcGy5bY.png",
        "https://images-ext-2.discordapp.net/external/mGhG3ws0QSDtgpYmc2cDzquDYyRDcfTQ7RKGG5WhwTs/https/i.imgur.com/l0fXw5q.png",
        "https://images-ext-2.discordapp.net/external/uagElNkQI2PWMn7DBASIo840_kyLWb0JyLNGKxmCptk/https/i.imgur.com/KR5hpqy.png",
        "https://images-ext-2.discordapp.net/external/hbR_5RK75W5lojtUKFArnOxjeuMv4V0gefNm8UQIbxw/https/i.imgur.com/mo37kKo.png",
        "https://images-ext-2.discordapp.net/external/UrrtZSdKG4VOr-2z6S1YS-mpqd22SLXJrf4SlHlPZZs/https/i.imgur.com/uymaWqK.png",
        "https://images-ext-2.discordapp.net/external/hg-WVUyn5PcCb88tbjuFkcr6epfSPPZkhUgkz1jxBKc/https/i.imgur.com/2JituCs.png",
        "https://images-ext-1.discordapp.net/external/z99OC5pWBJ7Xc4nkhNqWj4VxqwgBEfsjgAfnMd21-ZI/https/i.imgur.com/5i6A3II.png",
        "https://images-ext-2.discordapp.net/external/pTxGnePtu5UhGCmSipCLmXw8ebH1dzsf9_3jv-55hos/https/i.imgur.com/WGS2ojx.png",
        "https://images-ext-1.discordapp.net/external/aKzWCsYyPFkc6gjNPBXYn6E0z5AgIbJq8UFDC3o1RQk/https/i.imgur.com/qflI1QP.png",
        "https://images-ext-2.discordapp.net/external/SN3a5jdlADWK5hKeg7r-eTJaNAQhTct6d6rlSNNjlFg/https/i.imgur.com/bvkqGEL.png",
        "https://images-ext-1.discordapp.net/external/5_cJ92ZV6-wqKig2fSV2NJaQYoPtV5hcPij8AtEW1H4/https/i.imgur.com/H3h3JT0.png",
        "https://images-ext-2.discordapp.net/external/KLR6fC8Cbdu5grOaKsG8EQSsSgu3eHXyJuxnt2XptEo/https/i.imgur.com/LeYOzs1.png",
        "https://images-ext-1.discordapp.net/external/2gmyNfyyePllHR1ewdKKUOY9l5RoVoxsTkQO--zrvDA/https/i.imgur.com/224DyTF.png",
        "https://images-ext-1.discordapp.net/external/GddNL-hmWbENA4AUCAnHhJQHB_bMl1s-s1gUvnQ6th0/https/i.imgur.com/Pjyewat.png",
        "https://images-ext-1.discordapp.net/external/WW8spbvRLUfFlDVg-lQwn-Q_z82clCSpDkRZ-5n3pzI/https/i.imgur.com/ogwuCwZ.png",
        "https://images-ext-1.discordapp.net/external/0ITvNvoUoWUTv-HifmeCYmReqCrzi8lZ4Eoh0haj5zU/https/i.imgur.com/X4QD87f.png",
        "https://images-ext-2.discordapp.net/external/KzNks7dOoO6oicnGvZOB5OPzCkC8Hsvlqg89RYBu-xE/https/i.imgur.com/eM2YHQw.png",
        "https://images-ext-1.discordapp.net/external/NVdasyrMIZinw_6s10wcNFY28r6i4PEg6WUtf7xXBvc/https/i.imgur.com/DKAXxiW.png",
        "https://images-ext-2.discordapp.net/external/Be5wTkv0wHiv97u7esFLCWzE45SCbi4pgg8AV_XA5zs/https/i.imgur.com/JVPSAtV.png",
        "https://images-ext-2.discordapp.net/external/ZHmmOS6kC5Cr4vxdHImdrrPVJ77VkN7Pi81oEM3RF30/https/i.imgur.com/5TZg4kh.png",
        "https://images-ext-1.discordapp.net/external/DyYiBqof494_j66puFOelfoiVQCtAWok0cgLLpvl8KA/https/i.imgur.com/cjNpw2m.png",
        "https://images-ext-1.discordapp.net/external/44MHipqSAqyFYjKjjyF8vcJaFVjlL9nncM9MDXmk9WU/https/i.imgur.com/dfvv1Uw.png",
        "https://images-ext-2.discordapp.net/external/DKwFQv8GNOLv9kq2TD5jgmucCIcF4aeT1RElsL0zRcY/https/i.imgur.com/Uc597hp.png",
        "https://images-ext-1.discordapp.net/external/3gG88U2Xvu428zmDd1YxxIyzU1iMURCVBBqJSAHZjA0/https/i.imgur.com/spI2tsr.png",
        "https://images-ext-1.discordapp.net/external/frpsxwFnrLz-kYwCZbwZ5-XO7B8Xe_oMfR2bUohAA2Y/https/i.imgur.com/C1YYKFH.png",
        "https://images-ext-2.discordapp.net/external/bLVril6oc46zUNEkZ8Nz18ZtW5M854ZNmW0CMsIbwvY/https/i.imgur.com/rrwvSjq.png",
        "https://images-ext-1.discordapp.net/external/ekilPteazkHz4Vy5l0rquDSwpwOQHlMoMzJHpCH-YGk/https/i.imgur.com/bK9csi6.png",
        "https://images-ext-1.discordapp.net/external/BJAbSbZ6eSuoYu7dfD01ePL6l-ec2Igj29y-w6AGpTw/https/i.imgur.com/ktqlNP7.png",
        "https://images-ext-1.discordapp.net/external/EHTZ0Is0L_gfqF_yoB44-PuOqnWKtMZJOECSRdBlsDI/https/i.imgur.com/EUXlLQ6.png",
        "https://images-ext-2.discordapp.net/external/mshUVNu-AtQJbeim02rP6dnUtudPKsv0fUuULeMKbRQ/https/i.imgur.com/bIHXjVC.png",
        "https://images-ext-2.discordapp.net/external/IdtY222Uizlw0X2erPq5D46FB2d-Aek_PRHTCotMa3c/https/i.imgur.com/4XTF56w.png",
        "https://images-ext-2.discordapp.net/external/47avJT2DLdC15DMGYI26JEFsZ6eJjy6jTf0wvP_hkd4/https/i.imgur.com/efMObR1.png",
        "https://images-ext-1.discordapp.net/external/RKcMfdqHd3dC0d7x2IZktDtO40zjTTEn2z2VufOHefo/https/i.imgur.com/o9RWZ0t.png"]
    tracks_long = ["**Mario Kart Stadium (MKS)**", "**Water Park (WP)**", "**Sweet Sweet Canyon (SSC)**", "**Thwomp Ruins (TR)**",
                   "**Mario Circuit (MC)**", "**Toad Harbor (TH)**", "**Twisted Mansion (TM)**", "**Shy Guy Falls (SGF)**",
                   "**Sunshine Airport (SA)**", "**Dolphin Shoals (DS)**", "**Electrodrome (ED)**", "**Mount Wario (MW)**",
                   "**Cloudtop Cruise (CC)**", "**Bone-Dry Dunes (BDD)**", "**Bowser\'s Castle (BC)**", "**Rainbow Road (RR)**",
                   "**Wii Moo Moo Meadows (rMMM)**", "**GBA Mario Circuit (rMC)**", "**DS Cheep Cheep Beach (rCCB)**", "** N64 Toad\'s Turnpike (rTT)**",
                   "**GCN Dry Dry Desert (rDDD)**", "**SNES Donut Plains 3 (rDP3)**", "**N64 Royal Raceway (rRRy)**", "**3DS DK Jungle (rDKJ)**",
                   "**DS Wario Stadium (rWS)**", "**GCN Sherbet Land (rSL)**", "**3DS Music Park(rMP)**", "**N64 Yoshi Valley (rYV)**",
                   "**DS Tick-Tock Clock (rTTC)**", "**3DS Piranha plant Slide (rPPS)**", "**Wii Grumble Volcano (rGV)**", "**N64 Rainbow Road (rRRd)**",
                   "**GCN Yoshi Circuit (dYC)**", "**Excite Bike Arena (dEA)**", "**Dragon Driftway (dDD)**", "**Mute City (dMC)**",
                   "**Wii Wario\'s Gold Mine (dWGM)**", "**SNES Rainbow Road (dRR)**", "**Ice Ice Outpost (dIIO)**", "**Hyrule Circuit (dHC)**",
                   "**GCN Baby Park (dBP)**", "**GBA Cheese Land (dCL)**", "**Wild Woods (dWW)**", "**Animal Crossing (dAC)**",
                   "**3DS Neo Bowser City (dNBC)**", "**GBA Ribbon Road (dRiR)**", "**Super Bell Subway (dSBS)**", "**Big Blue (dBB)**",
                   "**Tour Paris Promenade (bPP)**", "**3DS Toad Circuit (bTC)**", "**N64 Choco Mountain (bCMo)**", "**Wii Coconut Mall (bCMa)**",
                   "**Tour Tokyo Blur (bTB)**", "**DS Shroom Ridge (bSR)**", "**GBA Sky Garden (bSG)**", "**Ninja Hideway (bNH)**"]
    for i in range(0, len(maps_list)):  # loops though every map
        map = maps_list[i]
        link = links[i]
        track_shown = tracks_long[i]
        if len(map) == 0:  # builds the embed, if map not played
            embed_not_played_map = discord.Embed(colour=discord.Colour(65535))
            embed_not_played_map.set_thumbnail(url=str(link))
            embed_not_played_map.add_field(name=f"{track_shown} wasn't played in the amount of wars, you entered!", value="Enter a higher amount!", inline=False)
            embed_list.append(embed_not_played_map)
        else:  # builds the embed if played
            if count is None:
                embed_name = f"In all wars, "
            else:
                embed_name = f"In the last {count} wars, "
            avg_difference = round(sum(map) / len(map), 2)
            max_difference = max(map)
            min_difference = min(map)
            last_difference = map[-1]
            count_list_map_played = len(map)
            embed_played_map = discord.Embed(colour=discord.Colour(65535))
            embed_played_map.set_thumbnail(url=str(link))
            embed_played_map.add_field(name=f"{embed_name}{track_shown} was played {count_list_map_played} times.", value="Here the stats:", inline=False)
            embed_played_map.add_field(name=f"Average score: ", value=f"{avg_difference}", inline=False)
            embed_played_map.add_field(name=f"Last score: ", value=f"{last_difference}", inline=False)
            embed_played_map.add_field(name=f"Maximum score: ", value=f"{max_difference}", inline=False)
            embed_played_map.add_field(name=f"Minimum score: ", value=f"{min_difference}", inline=False)
            embed_list.append(embed_played_map)
    for i in range(0, len(embed_list) + 1):
        await ctx.channel.send(embed=embed_list[i])
        await asyncio.sleep(0.8)
    await process_msg.delete()

@client.command(name="overallstats", aliases=["os"])
async def overallstats(ctx, count: int = None):
    toadchannel_id = int(GetToadbot(str(ctx.guild.id)))  # gets the toadbot channel from the GetToadbot function
    if count is None:  # sets the limit
        limit = None
    elif count < 0:
        ctx.channel.send("The number of wars is invalid!")
        return
    else:
        limit = count * 12 * 3 + 1
    process_msg = await ctx.channel.send("❗ **The process of the analysation will take a bit! Please be patient and don't add another command when it's not working in a few seconds!** ❗")
    toadchannel = client.get_channel(toadchannel_id)
    msglist = await toadchannel.history(limit=limit).flatten()
    all_differences = []
    for i in msglist:  # gets the spot of every 6v6 race and writes it into the list ^
        embeds = i.embeds
        for embed in embeds:
            if embed.title.startswith("Score"):
                all_differences.append(int(embed.fields[3].value))
    embed_list = []
    if len(all_differences) == 0:  # build the embed
        embed_not_played = discord.Embed(colour=discord.Colour(65535))
        embed_not_played.set_thumbnail(url="https://media.discordapp.net/attachments/932023933392285706/932024135041814528/reFRZtransparent.png")
        embed_not_played.add_field(name=f"There was no map played in the amount of wars you entered!", value="Enter a higher amount!", inline=False)
        embed_list.append(embed_not_played)
    else:
        if count is None:
            embed_name = f"of all wars, "
        else:
            embed_name = f"of the last {count} wars, "
        avg_difference = round(sum(all_differences) / len(all_differences), 2)
        max_difference = max(all_differences)
        min_difference = min(all_differences)
        embed_played_all = discord.Embed(colour=discord.Colour(65535))
        embed_played_all.set_thumbnail(url="https://media.discordapp.net/attachments/932023933392285706/932024135041814528/reFRZtransparent.png")
        embed_played_all.add_field(name=f"Overall stats from {embed_name}and of every map.", value="Here the stats:", inline=False)
        embed_played_all.add_field(name=f"Average score: ", value=f"{avg_difference}", inline=False)
        embed_played_all.add_field(name=f"Maximum score: ", value=f"{max_difference}", inline=False)
        embed_played_all.add_field(name=f"Minimum score: ", value=f"{min_difference}", inline=False)
        embed_list.append(embed_played_all)

    for embed_item in embed_list:
        await ctx.channel.send(embed=embed_item)
    await process_msg.delete()

client.run("token")