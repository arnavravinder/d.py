import discord
from discord.ext import commands
from discord.ui import Button, View

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} 🎉')

class RoleButton(Button):
    def __init__(self, role_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role_id = role_id

    async def callback(self, interaction: discord.Interaction):
        role = interaction.guild.get_role(self.role_id)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f'Removed role {role.name} ❌', ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f'Assigned role {role.name} ✅', ephemeral=True)

@bot.command(name='createrolemessage')
@commands.has_permissions(administrator=True)
async def createrolemessage(ctx, message: str, *roles: discord.Role):
    view = View()
    for role in roles:
        button = RoleButton(role.id, label=role.name, style=discord.ButtonStyle.primary)
        view.add_item(button)
    await ctx.send(message, view=view)

@bot.command(name='addrolebutton')
@commands.has_permissions(administrator=True)
async def addrolebutton(ctx, message_id: int, role: discord.Role):
    message = await ctx.channel.fetch_message(message_id)
    view = View.from_message(message)
    button = RoleButton(role.id, label=role.name, style=discord.ButtonStyle.primary)
    view.add_item(button)
    await message.edit(view=view)
    await ctx.send(f'Added role button for {role.name} to message ID {message_id} ✅')

@bot.command(name='removerolebutton')
@commands.has_permissions(administrator=True)
async def removerolebutton(ctx, message_id: int, role_name: str):
    message = await ctx.channel.fetch_message(message_id)
    view = View.from_message(message)
    for item in view.children:
        if isinstance(item, RoleButton) and item.label == role_name:
            view.remove_item(item)
    await message.edit(view=view)
    await ctx.send(f'Removed role button for {role_name} from message ID {message_id} ❌')

@bot.command(name='rolehelp')
async def rolehelp(ctx):
    help_message = """
    **Reaction Role Bot Commands** 📜
    `!createrolemessage <message> <role1> <role2> ...` - Creates a role message with buttons (Admin only)
    `!addrolebutton <message_id> <role>` - Adds a role button to an existing message (Admin only)
    `!removerolebutton <message_id> <role_name>` - Removes a role button from an existing message (Admin only)
    """
    await ctx.send(help_message)

bot.run('witheld')  # your api key
