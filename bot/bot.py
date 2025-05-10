import discord
import os
import asyncio
import requests
import json
import random
import logging
from discord.ext import commands, tasks
from discord import app_commands
from itertools import cycle
from datetime import timedelta, datetime

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Bot is online and ready to use")
    change_bot_status.start()
    print("Bot status is changing")

######################
#  Global Vairables  #
######################

hr_role_id = 1346570257833263265
log_channel_id = 1346929071363330098
high_moderation = ['| FOUNDER |', '| OWNER |', '| HEAD OF STAFF |']
staff = ['| RS STAFF |', '| FOUNDER |', '| OWNER |', '| HEAD OF STAFF |']
member = ['| SYNDICATORS |', '| FOUNDER |', '| OWNER |', '| HEAD OF STAFF |', '| RS STAFF |']
LOGGING_URL = "https://yourwebsite.com/api/logs"

##################
#  Sync Command  #
##################

@bot.command(name='sync')
@commands.has_any_role(*high_moderation)
async def sync(ctx):
  await ctx.send("Restarting the bot...")
  await asyncio.sleep(1)
  await ctx.send(f"Bot restart initiated by {ctx.author.mention}")

###################
#  Status System  #
###################
bot_statuses = cycle(["Watching over Redline Syndicate.", "Getting SSL in rocket league.", "Helping out the staff team."])

@tasks.loop(seconds=120)
async def change_bot_status():
    await bot.change_presence(activity=discord.Game(next(bot_statuses)))

##################
#  Help Command  #
##################

@bot.tree.command(name="staff_help", description="Brings up a embed message on commands you can do")
@commands.has_any_role(*high_moderation)
async def staff_help(interaction: discord.Interaction):
    # Provide a list of available commands
    embed = discord.Embed(title='Staff Bot Help', description='List of available commands:', color=discord.Color.blue())
    embed.add_field(name='/permaban', value='Permanently ban a member', inline=False)
    embed.add_field(name='/timeout', value='Timeout a member', inline=False)
    embed.add_field(name='/ping', value='Get the latency of the bot', inline=False)
    embed.add_field(name='/announce', value='Create an announcement', inline=False)
    embed.add_field(name='/help', value='Display this help message', inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=False)

@bot.tree.command(name="help", description="Brings up a embed message on commands you can do")
@commands.has_any_role(*member)
async def help(interaction: discord.Interaction):
    # Provide a list of available commands
    embed = discord.Embed(title='Help for members', description='List of available commands:', color=discord.Color.blue())
    embed.add_field(name='/rules', value='Display the rules', inline=False)
    embed.add_field(name='/server_status', value='Get an update on the server', inline=False)
    embed.add_field(name='/ping', value='Get the latency of the bot', inline=False)
    embed.add_field(name='/help', value='Display this help message', inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=False)

@bot.tree.command(name="guide", description="Brings up a embed message on what to do in the server")
@commands.has_any_role(*member)
async def guide(interaction: discord.Interaction):
    # Provide a list of available commands
    embed = discord.Embed(title='Guide for members', description='A Guide for server member`s', color=discord.Color.blue())
    embed.add_field(name='#📚│rules', value='Read the rules to get an understanding of them.', inline=False)
    embed.add_field(name='#🔔│announcements', value='Take a look at announcements to keep yourlself updated', inline=False)
    embed.add_field(name='#🔰│staff', value='Get familar with the staff team.', inline=False)
    embed.add_field(name='#👤│lineup', value='Have a look at our team lineup.', inline=False)
    embed.add_field(name='#❔│create-ticket', value='You can submit a ticket here if you need support.', inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=False)

####################
#  Rules Commmand  #
####################

@bot.tree.command(name="rules", description="Display the server rules.")
async def rules(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Server Rules",
        description="1. Be respectful\n2. No spamming\n3. Follow Discord's Terms of Service\n4. Use appropriate channels for discussions\n5. No hate speech or bullying \n6. Listen to the staff team.",
        color=discord.Color.green()
    )
    embed.set_footer(text='Please follow these rules to ensure a friendly environment for everyone.')
    await interaction.response.send_message(embed=embed, ephemeral=False)

##################
#  Ping Command  #
##################

@bot.tree.command(name="ping",description="Show the bot's latency in ms.")
async def ping(interaction: discord.Interaction):
    bot_latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"Ping! {bot_latency} ms.")

##########################
#  Fun System Command's  #
##########################

# Rock, Paper, Scissor Command
@bot.tree.command(name='rps', description='Play Rock, Paper, Scissors with the bot.')
async def rps(interaction: discord.Interaction, choice: str):
    await interaction.response.defer(ephemeral=False, thinking=True)

    choices = ["rock", "paper", "scissors"]
    bot_choice = random.choice(choices)

    result = ""
    if choice == bot_choice:
        result = "It's a tie!"
    elif (choice == "rock" and bot_choice == "scissors") or \
         (choice == "paper" and bot_choice == "rock") or \
         (choice == "scissors" and bot_choice == "paper"):
        result = "You win!"
    else:
        result = "You lose!"

    embed = discord.Embed(
        title='Rock, Paper, Scissors',
        description=f"You chose **{choice}**. The bot chose **{bot_choice}**.\n\n**{result}**",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    embed.set_footer(text='Redline Syndicate', icon_url=interaction.guild.icon.url)
    await interaction.followup.send(embed=embed)

# Coin Flip Command
@bot.tree.command(name='coinflip', description='Flip a coin.')
async def coinflip(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False, thinking=True)

    outcome = random.choice(["Heads", "Tails"])

    embed = discord.Embed(
        title='Coin Flip',
        description=f"The coin landed on **{outcome}**.",
        color=discord.Color.gold(),
        timestamp=datetime.utcnow()
    )
    embed.set_footer(text='Redline Syndicate', icon_url=interaction.guild.icon.url)
    await interaction.followup.send(embed=embed)

# roll Command
@bot.tree.command(name='roll', description='Roll a dice.')
async def roll(interaction: discord.Interaction, sides: int = 6):
    await interaction.response.defer(ephemeral=False, thinking=True)

    if sides < 2:
        await interaction.followup.send("Number of sides must be at least 2.", ephemeral=True)
        return

    result = random.randint(1, sides)

    embed = discord.Embed(
        title='Dice Roll',
        description=f"You rolled a **{result}** (1-{sides}).",
        color=discord.Color.green(),
        timestamp=datetime.utcnow()
    )
    embed.set_footer(text='Redline Syndicate', icon_url=interaction.guild.icon.url)
    await interaction.followup.send(embed=embed)

# 8ball Command
@bot.tree.command(name='8ball', description='Ask the magic 8-ball a question.')
async def eight_ball(interaction: discord.Interaction, question: str):
    await interaction.response.defer(ephemeral=False, thinking=True)

    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]

    response = random.choice(responses)

    embed = discord.Embed(
        title='Magic 8-Ball',
        description=f"Question: {question}\nAnswer: {response}",
        color=discord.Color.purple(),
        timestamp=datetime.utcnow()
    )
    embed.set_footer(text='Redline Syndicate', icon_url=interaction.guild.icon.url)
    await interaction.followup.send(embed=embed)

# Quote Command
@bot.tree.command(name='quote', description='Get a random quote.')
async def quote(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False, thinking=True)

    response = requests.get('https://api.quotable.io/random')
    if response.status_code == 200:
        data = response.json()
        content = data['content']
        author = data['author']
        
        embed = discord.Embed(
            title='Random Quote',
            description=f"\"{content}\"\n\n- {author}",
            color=discord.Color.teal(),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text='Redline Syndicate', icon_url=interaction.guild.icon.url)
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send("Failed to fetch a quote. Please try again later.", ephemeral=True)

# Joke Command
@bot.tree.command(name='joke', description='Get a random joke.')
async def joke(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False, thinking=True)

    response = requests.get('https://official-joke-api.appspot.com/jokes/random')
    if response.status_code == 200:
        data = response.json()
        setup = data['setup']
        punchline = data['punchline']

        embed = discord.Embed(
            title='Random Joke',
            description=f"**{setup}**\n*{punchline}*",
            color=discord.Color.orange(),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text='Redline Syndicate', icon_url=interaction.guild.icon.url)
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send("Failed to fetch a joke. Please try again later.", ephemeral=True)

######################
#  USER INFO MODULE  #
######################

@bot.tree.command(name='userinfo', description='Fetch information about a user.')
@commands.has_any_role(*staff)
async def userinfo(interaction: discord.Interaction, member: discord.Member):
    embed = discord.Embed(
        title=f"User Info - {member}",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="ID", value=member.id, inline=False)
    embed.add_field(name="Username", value=member.name, inline=False)
    embed.add_field(name="Discriminator", value=member.discriminator, inline=False)
    embed.add_field(name="Joined at", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    embed.add_field(name="Roles", value=", ".join([role.name for role in member.roles if role.name != "@everyone"]), inline=False)
    embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url)

    await interaction.response.send_message(embed=embed)

########################
#  SERVER INFO MODULE  #
########################

@bot.tree.command(name='serverinfo', description='Fetch information about the server.')
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(
        title=f"Server Info - {guild.name}",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="Server ID", value=guild.id, inline=False)
    embed.add_field(name="Owner", value=guild.owner, inline=False)
    embed.add_field(name="Member Count", value=guild.member_count, inline=False)
    embed.add_field(name="Creation Date", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    embed.add_field(name="Boost Level", value=guild.premium_tier, inline=False)
    embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url)

    await interaction.response.send_message(embed=embed)

#################################
#  Moderation System Command's  #
#################################

# Create a dictionary to store things
warnings = {}
timeouts = {}

# TIMEOUT MODULE

@bot.tree.command(name="timeout", description="Timeout a member from the server.")
@commands.has_any_role(*staff)
async def timeout(interaction: discord.Interaction, member: discord.Member, duration: int, reason: str = "No reason provided"):
    await interaction.response.defer(ephemeral=False, thinking=True)

    if interaction.user.top_role.position > member.top_role.position:
        try:
            # Timeout the member
            timeout_duration = discord.utils.utcnow() + timedelta(minutes=duration)
            await member.timeout(timeout_until=timeout_duration, reason=reason)
            timeouts[member.id] = (interaction.guild.id, duration)

            embed = discord.Embed(
                title='Member Timed Out',
                description=f"{member.mention} has been timed out for {duration} minutes. Reason: {reason}",
                color=discord.Color.red()
                )
            embed.set_footer(text='Redline Syndicate', icon_url=interaction.guild.icon.url)
            await interaction.followup.send(embed=embed, ephemeral=False)

            # Wait for the duration of the timeout
            await asyncio.sleep(duration * 60)

            # Check if the member is still timed out
            if timeouts.get(member.id) == (interaction.guild.id, duration):
                await member.edit(timeout=None, reason="Timeout expired")
                await member.send(f"Your timeout in {member.guild.name} has expired.")
                del timeouts[member.id]

        except discord.Forbidden:
            await interaction.followup.send("I don't have permission to timeout that member.")
        except discord.HTTPException:
            await interaction.followup.send("Failed to timeout the member. Something went wrong.")
    else:
        await interaction.followup.send("You don't have permission to timeout this member.", ephemeral=True)

###############
# KICK MODULE #
###############

@bot.tree.command(name="kick", description="Kick a member from the server")
@commands.has_any_role(*staff)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    await interaction.response.defer(ephemeral=False, thinking=True)
    if interaction.user.top_role.position > member.top_role.position:
        try:
            await member.kick(reason=reason)
            await interaction.followup.send(f"{member.mention} has been kicked for: {reason}", ephemeral=False)
        except discord.Forbidden:
            await interaction.followup.send("I don't have permission to kick that member.")
        except discord.HTTPException:
            await interaction.followup.send("Failed to kick the member. Something went wrong.")
    else:
        await interaction.followup.send("You don't have permission to kick this member.", ephemeral=True)

##############
# BAN MODULE #
##############

# Ban
@bot.tree.command(name="ban", description="Ban a member from the server.")
@commands.has_any_role(*staff)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    await interaction.response.defer(ephemeral=False, thinking=True)
    if interaction.user.top_role.position > member.top_role.position:
        try:
            await member.ban(reason=reason)
            await interaction.followup.send(f"{member.mention} has been banned for: {reason}", ephemeral=False)
        except discord.Forbidden:
            await interaction.followup.send("I don't have permission to ban that member.")
        except discord.HTTPException:
            await interaction.followup.send("Failed to ban the member. Something went wrong.")
    else:
        await interaction.followup.send("You don't have permission to ban this member.", ephemeral=True)

# Unban
@bot.tree.command(name="unban", description="Unban a previously banned member.")
@commands.has_any_role(*staff)
async def unban(interaction: discord.Interaction, user: str):
    await interaction.response.defer(ephemeral=False, thinking=True)
    try:
        user_id = int(user) if user.isdigit() else None
        banned_users = await interaction.guild.bans()
        user_to_unban = discord.utils.find(lambda u: u.user.id == user_id or str(u.user) == user, banned_users)
        if user_to_unban:
            await interaction.guild.unban(user_to_unban.user)
            await interaction.followup.send(f"{user_to_unban.user.mention} has been unbanned.", ephemeral=False)
        else:
            await interaction.followup.send(f"User {user} not found in banned users.", ephemeral=True)
    except discord.Forbidden:
        await interaction.followup.send("I don't have permission to unban that user.")
    except discord.HTTPException:
        await interaction.followup.send("Failed to unban the user. Something went wrong.")

##################
# WARNING MODULE #
##################

# Warn
@bot.tree.command(name="warn", description="Warn a member.")
@commands.has_any_role(*staff)
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str):
    await interaction.response.defer(ephemeral=False, thinking=True)
    if member.id not in warnings:
        warnings[member.id] = []
    warnings[member.id].append(reason)
    embed = discord.Embed(
        title='Member Warned',
        description=f"{member.mention} has been warned for: {reason}",
        color=discord.Color.orange()
    )
    embed.set_footer(text='Redline Syndicate', icon_url=interaction.guild.icon.url)
    await interaction.followup.send(embed=embed, ephemeral=False)

# Check Warnings
@bot.tree.command(name="check_warnings", description="Check warnings for a member.")
@commands.has_any_role(*staff)
async def check_warnings(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.defer(ephemeral=False, thinking=True)
    member_warnings = warnings.get(member.id, [])
    if member_warnings:
        embed = discord.Embed(
            title='Member Warnings',
            description=f"{member.mention} has the following warnings:",
            color=discord.Color.orange()
        )
        for i, warn in enumerate(member_warnings, 1):
            embed.add_field(name=f"Warning {i}", value=warn, inline=False)
    else:
        embed = discord.Embed(
            title='No Warnings',
            description=f"{member.mention} has no warnings.",
            color=discord.Color.green()
        )
    embed.set_footer(text='Redline Syndicate', icon_url=interaction.guild.icon.url)
    await interaction.followup.send(embed=embed, ephemeral=False)

# Clear Warnings
@bot.tree.command(name="clear_warnings", description="Clear all warnings for a member.")
@commands.has_any_role(*staff)
async def clear_warnings(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.defer(ephemeral=False, thinking=True)
    if member.id in warnings:
        warnings.pop(member.id)
        embed = discord.Embed(
            title='Warnings Cleared',
            description=f"All warnings for {member.mention} have been cleared.",
            color=discord.Color.green()
        )
    else:
        embed = discord.Embed(
            title='No Warnings',
            description=f"{member.mention} has no warnings to clear.",
            color=discord.Color.green()
        )
    embed.set_footer(text='Redline Syndicate', icon_url=interaction.guild.icon.url)
    await interaction.followup.send(embed=embed, ephemeral=False)

###############
# MUTE MODULE #
###############

# Mute
@bot.tree.command(name="mute", description="Mute a member for a specified duration.")
@commands.has_any_role(*staff)
async def mute(interaction: discord.Interaction, member: discord.Member, duration: int, reason: str = "No reason provided"):
    await interaction.response.defer(ephemeral=False, thinking=True)
    muted_role = discord.utils.get(member.guild.roles, name="Muted")
    if not muted_role:
        muted_role = await member.guild.create_role(name="Muted")

    for channel in member.guild.channels:
        await channel.set_permissions(muted_role, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    await member.add_roles(muted_role)
    embed = discord.Embed(
        title='Member Muted',
        description=f"{member.mention} has been muted for {duration} minutes. Reason: {reason}",
        color=discord.Color.orange()
    )
    embed.set_footer(text='Redline Syndicate', icon_url=interaction.guild.icon.url)
    await interaction.followup.send(embed=embed, ephemeral=False)

    await asyncio.sleep(duration * 60)
    await member.remove_roles(muted_role)
    await member.send(f"You have been unmuted in {member.guild.name}.")

# Unmute
@bot.tree.command(name="unmute", description="Unmute a muted member.")
@commands.has_any_role(*staff)
async def unmute(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.defer(ephemeral=False, thinking=True)
    muted_role = discord.utils.get(member.guild.roles, name="Muted")
    if muted_role in member.roles:
        await member.remove_roles(muted_role)
        embed = discord.Embed(
            title='Member Unmuted',
            description=f"{member.mention} has been unmuted.",
            color=discord.Color.green()
        )
        embed.set_footer(text='Redline Syndicate', icon_url=interaction.guild.icon.url)
        await interaction.followup.send(embed=embed, ephemeral=False)
    else:
        await interaction.followup.send(f"{member.mention} is not muted.", ephemeral=True)

#################
#  ROLE MODULE  #
#################

# Add role
@bot.tree.command(name='addrole', description='Assign a role to a user.')
@commands.has_any_role(*staff)
async def addrole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    await interaction.response.defer(ephemeral=False, thinking=True)

    if interaction.user.top_role.position > member.top_role.position:
        if role not in member.roles:
            try:
                await member.add_roles(role)
                embed = discord.Embed(
                title='Role Assigned',
                    description=f"{role.mention} has been assigned to {member.mention}",
                    color=discord.Color.green(),
                    timestamp=datetime.utcnow()
                    )
                embed.set_footer(text='Redline Syndicate', icon_url=interaction.guild.icon.url)
                embed.add_field(name='Assigned by', value=interaction.user.mention, inline=True)
                embed.add_field(name='Role', value=role.mention, inline=True)
                await interaction.followup.send(embed=embed, ephemeral=False)
            except discord.Forbidden:
                await interaction.followup.send("I don't have permission to add that role.", ephemeral=True)
            except discord.HTTPException:
                await interaction.followup.send("Failed to add the role. Something went wrong.", ephemeral=True)
        else:
            embed = discord.Embed(
                title='Failed to Assign Role',
                description=f"{member.mention} already has {role.mention}",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(
            title='Failed to Assign Role',
            description=f"You don't have permission to assign roles to {member.mention}.",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

# Remove Role
@bot.tree.command(name='removerole', description='Remove a role from a user.')
@commands.has_any_role(*staff)
async def removerole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    await interaction.response.defer(ephemeral=False, thinking=True)

    if interaction.user.top_role.position > member.top_role.position:
        if role in member.roles:
            try:
                await member.remove_roles(role)
                embed = discord.Embed(
                    title='Role Removed',
                    description=f"{role.mention} has been removed from {member.mention}",
                    color=discord.Color.orange(),
                    timestamp=datetime.utcnow()
                )
                embed.set_footer(text='Redline Syndicate', icon_url=interaction.guild.icon.url)
                embed.add_field(name='Removed by', value=interaction.user.mention, inline=True)
                embed.add_field(name='Role', value=role.mention, inline=True)
                await interaction.followup.send(embed=embed, ephemeral=False)
            except discord.Forbidden:
                await interaction.followup.send("I don't have permission to remove that role.", ephemeral=True)
            except discord.HTTPException:
                await interaction.followup.send("Failed to remove the role. Something went wrong.", ephemeral=True)
        else:
            embed = discord.Embed(
                title='Failed to Remove Role',
                description=f"{member.mention} does not have {role.mention}",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(
            title='Failed to Remove Role',
            description=f"You don't have permission to remove roles from {member.mention}.",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

# Role All
@bot.tree.command(name="roleall", description="Assign a role to all members in the server.")
@commands.has_any_role(*high_moderation)
async def roleall(interaction: discord.Interaction, role: discord.Role):
    await interaction.response.defer(ephemeral=False, thinking=True)
    if not interaction.user.guild_permissions.manage_roles:
        await interaction.followup.send("You don't have permission to manage roles.", ephemeral=True)
        return

    guild = interaction.guild
    success_count = 0
    failed_count = 0

    for member in guild.members:
        if role not in member.roles:
            try:
                await member.add_roles(role)
                success_count += 1
            except discord.Forbidden:
                failed_count += 1
            except discord.HTTPException:
                failed_count += 1

    embed = discord.Embed(
        title="Role Assignment Complete",
        description=f"Successfully assigned {role.mention} to {success_count} members.\nFailed to assign to {failed_count} members.",
        color=discord.Color.blue()
    )
    embed.set_footer(text='Redline Syndicate')
    await interaction.followup.send(embed=embed)

# Role Remove All
@bot.tree.command(name="removeallrole", description="Remove a role from all members in the server.")
async def removeallrole(interaction: discord.Interaction, role: discord.Role):
    await interaction.response.defer(ephemeral=False, thinking=True)
    if not interaction.user.guild_permissions.manage_roles:
        await interaction.followup.send("You don't have permission to manage roles.", ephemeral=True)
        return

    guild = interaction.guild
    success_count = 0
    failed_count = 0

    for member in guild.members:
        if role in member.roles:
            try:
                await member.remove_roles(role)
                success_count += 1
            except discord.Forbidden:
                failed_count += 1
            except discord.HTTPException:
                failed_count += 1

    embed = discord.Embed(
        title="Role Removal Complete",
        description=f"Successfully removed {role.mention} from {success_count} members.\nFailed to remove from {failed_count} members.",
        color=discord.Color.red()
    )
    embed.set_footer(text='Redline Syndicate')
    await interaction.followup.send(embed=embed)

#####################
#  LOCKDOWN MODULE  #
#####################

@bot.tree.command(name='lockchannel', description='Lock a channel.')
@commands.has_any_role(*staff)
async def lockchannel(interaction: discord.Interaction, channel: discord.TextChannel):
    await interaction.response.defer(ephemeral=False, thinking=True)
    overwrite = channel.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
    await interaction.followup.send(f"{channel.mention} has been locked.", ephemeral=True)

@bot.tree.command(name='unlockchannel', description='Unlock a channel.')
@commands.has_any_role(*staff)
async def unlockchannel(interaction: discord.Interaction, channel: discord.TextChannel):
    await interaction.response.defer(ephemeral=False, thinking=True)
    overwrite = channel.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
    await interaction.followup.send(f"{channel.mention} has been unlocked.", ephemeral=True)

##################
#  PURGE MODULE  #
##################

@bot.tree.command(name='purge', description='Clear a specified number of messages from a channel.')
@commands.has_any_role(*staff)
async def purge(interaction: discord.Interaction, amount: int):
    await interaction.response.defer(ephemeral=False, thinking=True)
    await interaction.channel.purge(limit=amount)
    embed = discord.Embed(
        title='Pruge Messages',
        description=f"Messages have been pruged.\n Amount of message's purged **{amount}**.",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    embed.set_footer(text='Redline Syndicate', icon_url=interaction.guild.icon.url)
    await interaction.followup.send(embed=embed)

########################
#  SETNICKNAME MODULE  # 
########################

@bot.tree.command(name='setnickname', description='Set the nickname of a member.')
@commands.has_any_role(*staff)
async def setnickname(interaction: discord.Interaction, member: discord.Member, nickname: str):
    await interaction.response.defer(ephemeral=False, thinking=True)
    try:
        await member.edit(nick=nickname)
        embed = discord.Embed(
            title='Nickname Changed',
            description=f"{member.mention}'s nickname has been changed to **{nickname}**.",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text='Redline Syndicate', icon_url=interaction.guild.icon.url)
        await interaction.followup.send(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(
            title='Error',
            description="I don't have permission to change that member's nickname.",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text='Redline Syndicate', icon_url=interaction.guild.icon.url)
        await interaction.followup.send(embed=embed)
    except discord.HTTPException:
         embed = discord.Embed(
            title='Error',
            description="Failed to change the nickname. Something went wrong.",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
    embed.set_footer(text='Redline Syndicate', icon_url=interaction.guild.icon.url)
    await interaction.followup.send(embed=embed)

##########################
#  Announcement Command  #
##########################

@bot.tree.command(name="announce", description="Create an announcement")
@commands.has_any_role(*high_moderation)
async def announce(interaction: discord.Interaction, title: str, description: str, signed: str):
    await interaction.response.defer(ephemeral=False, thinking=True)
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.blue()
        )
    embed.set_footer(text=f"Signed: \n{signed}")

    await interaction.response.send_message(embed=embed)

async def edit_announcement(interaction: discord.Interaction, message: discord.Message, title: str, description: str, signed: str):
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.blue()
     )
    embed.set_footer(text=f"Signed: {signed}", icon_url=interaction.guild.icon.url)

    await message.edit(embed=embed)
    await interaction.response.send_message("Announcement edited successfully.", ephemeral=True)

################
#  Log System  #
################

@bot.event
async def on_member_join(message):
    log_channel = discord.utils.get(member.guild.channels, name="💻│logs")

    event_embed = discord.Embed(title="Message Log", description="Edited thier message", color=discord.Color.red())
    event_embed.add_field(name="Message Author: ", value=message.author.mention, inline=False)
    event_embed.add_field(name="Channle Orgin: ", value=message.channel.mention, inline=False)
    event_embed.add_field(name="Message Content: ", value=message.content, inline=False)
    await log_channel.send(embed=event_embed)
    
@bot.event
async def on_member_join(member):
    log_channel = discord.utils.get(member.guild.channels, name="💻│logs")

    event_embed = discord.Embed(title="Member Log", description="This user joined the server", color=discord.Color.green())
    event_embed.add_field(name="Arrival Log: ", value=member.mention, timestamp=datetime.utcnow(), inline=False)
    event_embed.set_footer(text='Redline Syndicate')

    await log_channel.send(embed=event_embed)

@bot.event
async def on_member_remove(member):
    log_channel = discord.utils.get(member.guild.channels, name="💻│logs")
    
    event_embed = discord.Embed(title="Member Log", description="This user left the server", timestamp=datetime.utcnow(), color=discord.Color.red())
    event_embed.add_field(name="Departure Log: ", value=member.mention, inline=False)
    event_embed.set_footer(text='Redline Syndicate')
    await log_channel.send(embed=event_embed)

@bot.event
async def on_voice_state_update(member, before, after):
    log_channel = discord.utils.get(member.guild.channels, name="💻│logs")

    event_embed = discord.Embed(title="Voice Log", description="This user joined a voice chat", color=discord.Color.green())
    event_embed.add_field(name="user log: ", value=member.mention, inline=False)
    #event_embed.add_field(name="Channle Orgin: ", value=channel.mention, inline=False)
    await log_channel.send(embed=event_embed)

#####################################
#  Send log to the website backend  #
#####################################

def send_log(action, user, reason=None):
    payload = {
        'action': action,
        'user': str(user),
        'reason': reason if reason else 'N/A'
    }
    try:
        response = requests.post(LOGGING_URL, json=payload)
        if response.status_code == 200:
            logging.info(f"Log sent successfully: {payload}")
        else:
            logging.error(f"Failed to send log: {response.text}")
    except Exception as e:
        logging.error(f"Error sending log: {e}")

##################
#  Error System  #
##################

@bot.event
async def removeallrole_error(interaction: discord.Interaction, error: commands.CommandError):
    if isinstance(error, commands.MissingAnyRole):
        await interaction.response.send_message("You don't have the required role to use this command.", ephemeral=False)
    else:
        await interaction.response.send_message("An error occurred while executing the command.", ephemeral=False)

@bot.event # General Error for MissingRequiredArguement
async def removeallrole_error(interaction: discord.Interaction, error: commands.CommandError):
    if isinstance(error, commands.MissingRequiredArgument):
        await interaction.response.send_message("Are you sure you provided __all__ the required arguements.", ephemeral=False)
    else:
        await interaction.response.send_message("An error occurred while executing the command.", ephemeral=False)

###################
# One Off Error's #
###################

@warn.error # If you want a one off error for a message
async def warn_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Error: Missing Required Arguement. Are you sure you provided __all__ the required arguements such as member you are warning.")

@roleall.error
async def roleall_error(interaction: discord.Interaction, error: commands.CommandError):
    if isinstance(error, commands.MissingAnyRole):
        await interaction.response.send_message("You don't have the required role to use this command.", ephemeral=False)
    else:
        await interaction.response.send_message("An error occurred while executing the command.", ephemeral=False)

@removeallrole.error
async def removeallrole_error(interaction: discord.Interaction, error: commands.CommandError):
    if isinstance(error, commands.MissingAnyRole):
        await interaction.response.send_message("You don't have the required role to use this command.", ephemeral=False)
    else:
        await interaction.response.send_message("An error occurred while executing the command.", ephemeral=False)

######################
#  Open File System  #
######################

with open ("token.txt") as f:
    token = f.read()

bot.run(token)
