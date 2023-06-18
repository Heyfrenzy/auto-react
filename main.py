import discord
import json
import os, time
os.system("tls_client")
from threading import Thread
from discord.ext import commands
from base64 import b64encode
import tls_client

tkn = ""

os.system("cls" if os.name == "nt" else "clear")

__useragent__ = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"  #requests.get('https://discord-user-api.cf/api/v1/properties/web').json()['chrome_user_agent']
build_number = 165486  #int(requests.get('https://discord-user-api.cf/api/v1/properties/web').json()['client_build_number'])
cv = "108.0.0.0"
__properties__ = b64encode(
  json.dumps(
    {
      "os": "Windows",
      "browser": "Chrome",
      "device": "PC",
      "system_locale": "en-GB",
      "browser_user_agent": __useragent__,
      "browser_version": cv,
      "os_version": "10",
      "referrer": "https://discord.com/channels/@me",
      "referring_domain": "discord.com",
      "referrer_current": "",
      "referring_domain_current": "",
      "release_channel": "stable",
      "client_build_number": build_number,
      "client_event_source": None
    },
    separators=(',', ':')).encode()).decode()


def get_headers(token, channel):
  headers = {
    "Authorization": token,
    "Origin": "https://discord.com",
    "Accept": "*/*",
    "X-Discord-Locale": "en-GB",
    "X-Super-Properties": __properties__,
    "User-Agent": __useragent__,
    "Referer": f"https://discord.com/channels/{channel}",
    "X-Debug-Options": "bugReporterEnabled",
    "Content-Type": "application/json"
  }
  return headers

def add_reaction(tk, channel, message, emoji, emoji_name):
    headers = get_headers(tk, channel)
    # headers={'Authorization': tk,'accept': '*/*','accept-language': 'en-US','connection': 'keep-alive','cookie': f'__cfduid = {rc(43)}; __dcfduid={rc(32)}; __sdcfduid={rc(96)}; locale=en-US','DNT': '1','origin': 'https://discord.com','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-origin','referer': 'https://discord.com/channels/@me','TE': 'Trailers','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36','X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzk2LjAuNDY2NC40NSBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiOTYuMC40NjY0LjQ1Iiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6Imh0dHBzOi8vZGlzY29yZC5jb20vIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiZGlzY29yZC5jb20iLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoxMDg5MjQsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9',}

    # r = requests.patch('https://discord.com/api/v9/users/@me', headers=headers, json={"avatar":f'data:image/png;base64,{b64encode(img).decode("ascii")}'})
    client = tls_client.Session(client_identifier="firefox_102")
    client.headers.update(headers)
    r = client.get("https://discord.com/api/v9/users/@me")
    if r.status_code in (200, 201, 204):
        # r2 = client.put(f"https://discord.com/api/v10/channels/{channel}/messages/{message}/reactions/{emoji}/@me")
        r2 = client.put(f"https://discord.com/api/v9/channels/{channel}/messages/{message}/reactions/{emoji}/%40me?location=Message&burst=false")
        # print(r2.status_code)
        if r2.status_code in (200, 201, 204):
            print(f"[+] Successfully reacted to message {message} in channel {channel} with emoji {emoji_name} with token {tk[:30]}")
        elif r2.status_code == 429:
          os.system("kill 1")
        else:
            print(f"[-] Failed to react ", r2.text)
        # print(r2.text)

client = commands.Bot(command_prefix='nop_$', intents=discord.Intents.all(), help_command=None)
gw_bots = (824119071556763668, 720351927581278219,)

@client.event
async def on_command_error(ctx, error):
    await ctx.send(f"Error: {error}", delete_after=5)


@client.tree.command()
@commands.has_permissions(administrator=True)
async def autoreact(ctx:discord.Interaction, enabled:bool, amount: int=0):
    if not ctx.user.guild_permissions.administrator:
        return await ctx.response.send_message("Admin only command")
    with open("settings.json", "r") as file:
        settings = json.load(file)
    max_ = settings[str(ctx.guild.id)]["max_limit"]
    if amount > max_:
        await ctx.response.send_message(f"Max Amount: {max_}.\nTo increase the limit, dm scientist")
        return

    settings[str(ctx.guild.id)] = {
        "tokens": amount,
        "everyone": enabled, 
        "max_limit": max_
    }
    with open("settings.json", "w") as file:
        json.dump(settings, file, indent=4)
    await ctx.response.send_message("Auto react settings updated successfully.\n`/settings` to view the settings.")
    # await ctx.message.add_reaction("✅")

def url_encode(string1):
    return string1.replace(":", "%3A").replace("/", "%2F").replace("<", "").replace(">", "")

@client.tree.command()
@commands.has_permissions(administrator=True)
@commands.cooldown(3, 60, commands.BucketType.guild)
async def react(ctx: discord.Interaction, channel_id: str, message_id: str, amount: int, emoji:str) -> None:
    if not ctx.user.guild_permissions.administrator:
        await ctx.response.send_message("Admin only command")
        return
    with open("settings.json", "r") as file:
        settings = json.load(file)
    max_ = settings[str(ctx.guild.id)]["max_limit"]
    enabled = settings[str(ctx.guild.id)]["everyone"]
    if not enabled:
        await ctx.response.send_message("Reactions are disabled for this server.")
        return
    if amount > max_:
        await ctx.response.send_message(f"Max Amount: {max_}.\nTo increase the limit, dm scientist")
        return
    if str(ctx.guild.id) in settings:
        print("ok")
        f = open(f"{ctx.guild.id}.txt", "r")
        tlist = f.read().splitlines()
        f.close()
        success = 0 
        await ctx.response.send_message("Request sent!")
        for tk in tlist:
            # tk = tk.split(":")[2]
            success += 1
            if success >= amount:
                break
            time.sleep(0.2)
            # emoji1 = f"{emoji.name}:{emoji.id}"
            emoji2 = url_encode(emoji)
            # emoji_name = emoji1.split(":")[0]
            Thread(target=add_reaction, args=(tk, channel_id, message_id, emoji2,"disabled atm",)).start()
        return 

# Command to view the auto-react settings for the server
@client.tree.command()
@commands.has_permissions(administrator=True)
async def settings(ctx: discord.Interaction):
    if not ctx.user.guild_permissions.administrator:
        return await ctx.response.send_message("Admin only command")
    with open("settings.json", "r") as file:
        settings = json.load(file)
    if str(ctx.guild.id) not in settings:
        await ctx.response.send_message("Auto-react settings not set for this server.")
        return
    tokens = settings[str(ctx.guild.id)]["tokens"]
    everyone = settings[str(ctx.guild.id)]["everyone"]
    await ctx.response.send_message(f"Auto-react settings:\n\nAmount: {tokens}\nEnabled: {everyone}")

# Command to view the client's commands
@client.tree.command()
async def help(ctx:discord.Interaction):
    embed = discord.Embed(title="Commands", color=00000, description="`/autoreact`: Set auto-react settings for giveaways in server.\n`/react`: Add reactions to a message.\n`/settings`: View auto-react settings for the server.\n\n**Note:**\n1. As the tokens dont have nitro, message should have atleast 1 reaction before they can react to it.\n2. Too much spamming can result in tokens being locked.\n3. Tokens should be verified in server, if u have a rules screen setup or moderation set to phone verfied.\n4. Tokens should be able to see channel where u want to react.\n5. Make sure bot is online before staring a giveaway or reactions will fail.")
    embed.set_footer(text="Made by scientist")
    await ctx.response.send_message(embed=embed)



@client.event
async def on_message(message):
    await client.process_commands(message)
    with open("settings.json", "r") as file:
        settings = json.load(file)
    max_ = settings[str(message.guild.id)]["max_limit"]
    if str(message.guild.id) in settings:
        if message.author.id in gw_bots:
            amount = settings[str(message.guild.id)]["tokens"]
            everyone = settings[str(message.guild.id)]["everyone"]
            if not everyone:
                return 
            if "giveaway" in message.content.lower():
                print("ok") 
                f = open(f"{message.guild.id}.txt", "r")
                tlist = f.read().splitlines()
                f.close()
                success = 0 
                for tk in tlist:
                    # tk = tk.split(":")[2]
                    success += 1
                    if success >= amount:
                        break
                    time.sleep(0.2)
                    Thread(target=add_reaction, args=(tk, message.channel.id, message.id, "%F0%9F%8E%89","tada",)).start()
                return 

# @client.command()
@commands.is_owner()
async def synclock1337(ctx):
    with open('settings.json', 'r') as f:
        data = json.load(f)
    for guild in client.guilds:
        if str(guild.id) not in data:
            data[str(guild.id)] = {
                'tokens': 0,
                'everyone': False,
                'max_limit': 0
            }
    with open('settings.json', 'w') as f:
        json.dump(data, f, indent=4)
    await ctx.send("Synced!")

@client.event
async def on_disconnect():
  os.system("kill 1 && python3 main.py")
  
@client.event
async def on_ready():
    os.system("cls if os.name == 'nt' else clear")
    whitelist = open("whitelist.txt", "r").read().splitlines()
    with open('settings.json', 'r') as f:
        data = json.load(f)
    for guild in client.guilds:
        if str(guild.id) not in whitelist:
            await guild.leave()
            return
        if str(guild.id) not in data:
            data[str(guild.id)] = {
                'tokens': 0,
                'everyone': False,
                'max_limit': 0
            }
    with open('settings.json', 'w') as f:
        json.dump(data, f, indent=4)
    print(client.user, client.user.id)
    ok = await client.tree.sync()

@client.event
async def on_guild_join(guild):
    with open('settings.json', 'r') as f:
        data = json.load(f)
    whitelist = open("whitelist.txt", "r").read().splitlines()
    ok = await client.tree.sync()
    for guild in client.guilds:
        if str(guild.id) not in whitelist:
            await guild.leave()
            return
        data[str(guild.id)] = {
            'tokens': 0,
            'everyone': False,
            'max_limit': 0
        }
        with open('settings.json', 'w') as f:
            json.dump(data, f, indent=4)
 

try:
  client.run(tkn, reconnect=True)
except:
  os.system("kill 1")
