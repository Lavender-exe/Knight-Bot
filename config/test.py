import discord
from discord.ext import commands
from interactions import slash_command, SlashContext

BOT_TOKEN = "MTE4NDM3OTU2Mzk1NDk1MDE1NA.GXbVuK.30DJWskc1jTzcVPgiB1tSedZU0BIppLu3lDDl0"
GUILD_ID = 459123789049888791

intents = discord.Intents(messages=True, guilds=True)

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.command(name="create_category")
async def create_category(ctx, category_name):
    guild = ctx.guild(GUILD_ID)

    # Create category
    category = await guild.create_category(category_name)
    await ctx.send(f"Category '{category_name}' created!")

@bot.command(name="create_channel")
async def create_category(ctx, category_name: str, default_role: discord.Role = None):
    if any(permission in ctx.author.guild_permissions for permission in [discord.Permissions(administrator=True)]):
        current_date = datetime.now().strftime("%d/%m/%y")

        full_category_name = f'{category_name}-{current_date}'  # You can customize the naming convention
        category = await ctx.guild.create_category(full_category_name)

        # Create channels within the category
        for channel_type in ['general', 'troubleshooting', 'resources']:
            channel = await category.create_text_channel(f'{channel_type}')

            await channel.set_permissions(ctx.guild.default_role, read_messages=False)
            if default_role:
                await channel.set_permissions(default_role, read_messages=True)
            else:
                await channel.set_permissions(ctx.author, read_messages=True)

        await ctx.send(f'Category "{full_category_name}" created with channels.')

        view = discord.ui.View()
        button = Button(style=discord.ButtonStyle.link, label="Red Team Training", url="https://whiteknightlabs.com/training/")
        view.add_item(button)
        await ctx.send("Click the button to visit the website:", view=view)
    else:
        await ctx.send("You don't have the necessary permissions to create a category.")

bot.run(BOT_TOKEN)