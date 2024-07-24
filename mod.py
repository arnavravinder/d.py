import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} 🔧')

@bot.command(name='ban')
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention} 🚫 Reason: {reason}')

@bot.command(name='unban')
@has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention} ✅')
            return

@bot.command(name='kick')
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention} 👢 Reason: {reason}')

@bot.command(name='mute')
@has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
    if not muted_role:
        muted_role = await ctx.guild.create_role(name='Muted')

        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    await member.add_roles(muted_role, reason=reason)
    await ctx.send(f'Muted {member.mention} 🤐 Reason: {reason}')

@bot.command(name='unmute')
@has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name='Muted')

    if muted_role in member.roles:
        await member.remove_roles(muted_role)
        await ctx.send(f'Unmuted {member.mention} 🔊')
    else:
        await ctx.send(f'{member.mention} is not muted.')

@bot.command(name='warn')
@has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    await ctx.send(f'Warned {member.mention} ⚠️ Reason: {reason}')

@bot.command(name='clear')
@has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'Cleared {amount} messages 🧹', delete_after=5)

@bot.command(name='lockdown')
@has_permissions(manage_channels=True)
async def lockdown(ctx):
    role = ctx.guild.default_role
    overwrite = discord.PermissionOverwrite(send_messages=False)
    await ctx.channel.set_permissions(role, overwrite=overwrite)
    await ctx.send('Channel locked down 🔒')

@bot.command(name='unlock')
@has_permissions(manage_channels=True)
async def unlock(ctx):
    role = ctx.guild.default_role
    overwrite = discord.PermissionOverwrite(send_messages=True)
    await ctx.channel.set_permissions(role, overwrite=overwrite)
    await ctx.send('Channel unlocked 🔓')

@bot.command(name='slowmode')
@has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f'Slowmode set to {seconds} seconds 🐢')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have the required permissions to use this command ❌")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument ❗")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid argument ❗")
    else:
        await ctx.send("An error occurred while processing the command ❗")

@bot.command(name='addrole')
@has_permissions(manage_roles=True)
async def addrole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f'Added role {role.name} to {member.mention} 🏷️')

@bot.command(name='removerole')
@has_permissions(manage_roles=True)
async def removerole(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f'Removed role {role.name} from {member.mention} 🏷️')

@bot.command(name='roleinfo')
@has_permissions(manage_roles=True)
async def roleinfo(ctx, role: discord.Role):
    await ctx.send(f'Role: {role.name}\nID: {role.id}\nColor: {role.color}\nMembers: {len(role.members)}')

@bot.command(name='userinfo')
async def userinfo(ctx, member: discord.Member):
    roles = [role for role in member.roles]
    embed = discord.Embed(color=discord.Color.blue(), timestamp=ctx.message.created_at)
    embed.set_author(name=f'User Info - {member}')
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
    embed.add_field(name='ID:', value=member.id)
    embed.add_field(name='Guild name:', value=member.display_name)
    embed.add_field(name='Created at:', value=member.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
    embed.add_field(name='Joined at:', value=member.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
    embed.add_field(name=f'Roles ({len(roles)})', value=' '.join([role.mention for role in roles]))
    embed.add_field(name='Top role:', value=member.top_role.mention)
    embed.add_field(name='Bot?', value=member.bot)

    await ctx.send(embed=embed)

bot.run('witheld')
