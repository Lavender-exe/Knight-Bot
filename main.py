'''
Author: Lavender-exe
Purpose: Discord Bot for WKL
'''
import os
import interactions
from interactions import (
    slash_command,
    SlashContext,
    Client,
    Intents,
    OptionType,
    slash_option,
    SlashCommandChoice,
    Permissions,
    Color,
    Status,
    Modal,
    ShortText,
    ParagraphText,
    ModalContext,
    ScheduledEvent,
    ScheduledEventPrivacyLevel,
    ScheduledEventStatus,
    listen,
)

from datetime import datetime
from dotenv import load_dotenv
from config.logging import info, exception_error
from config.git_update import origin


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
DEBUG_ID = os.getenv("DEV")
GUILD_ID = os.getenv("GUILD")

bot = Client(
    intents=Intents.DEFAULT,
    debug_scope=DEBUG_ID,
    scope=GUILD_ID,
    status=Status.ONLINE,
    activity="whiteknightlabs.com",
    disable_dm_commands=True,
)

bot.load_extension("interactions.ext.jurigged")


@slash_command(
    name="help",
    description="Display help information",
    default_member_permissions=(Permissions.MANAGE_CHANNELS | Permissions.MANAGE_ROLES),
)
async def help_command(ctx):
    """Help Function"""
    embed = interactions.Embed(
        title="Bot Commands",
        description="Here are some commands you can use with this bot:",
    )
    embed.add_field(name="Create Course",
                    value="`/create_course [category_name] [date]`", inline=False)
    embed.add_field(name="Help", value="`/help`", inline=False)
    await ctx.send(embed=embed)


@slash_command(
    name="create_course",
    description="Sets up the category, channels, and roles needed for the selected course",
    default_member_permissions=(Permissions.MANAGE_CHANNELS | Permissions.MANAGE_ROLES),
)
@slash_option(
    name="course_name",
    description="Set the Course Name",
    required=True,
    opt_type=OptionType.STRING,
    choices=[
        # Add more courses here
        SlashCommandChoice(name="Offensive Development", value="offensive-dev"),
        SlashCommandChoice(name="Advance Red Team Operator", value="adv-redteam-ops"),
    ],
)
@slash_option(
    name="course_date",
    description="Set the Date (dd-mm-yy)",
    required=True,
    opt_type=OptionType.STRING,
)

async def create_course_function(ctx: SlashContext,
                                 course_name: SlashCommandChoice, course_date: SlashCommandChoice):
    """Create Course Category with Role and Channels"""
    try:
        current_date = course_date
        role_name = f'{course_name} {current_date}'
        category_name = f'{course_name} {current_date}'
        await ctx.send(f'**Creating Course: "{course_name} for {course_date}"**')

        guild = ctx.guild
        role_check_exists = interactions.utils.get(guild.roles, name=role_name)
        if role_check_exists is None:
            if course_name == "offensive-dev":
                role = await guild.create_role(
                    name=role_name, colour=Color.from_hex("ae99ff")) # OD

            elif course_name == "adv-redteam-ops":
                role = await guild.create_role(
                    name=role_name, colour=Color.from_hex("bb3232")) # ARTO

            else:
                role = await guild.create_role(name=role_name) # Any
        else:
            role = role_check_exists
        category_check_exists = interactions.utils.get(guild.channels, name=category_name)
        if category_check_exists is None:
            category = await guild.create_category(category_name, position=6)
            await category.set_permission(role, read_message_history=True, send_messages=True)
            await category.set_permission(
                guild.default_role, read_message_history=False, send_messages=False)
        else:
            category = category_check_exists

        for channel_type in ['general', 'resources', 'troubleshooting']:
            channel_check_exists = interactions.utils.get(guild.channels, 
                                                          name=channel_type, category=category_name)
            if channel_check_exists is None:
                await category.create_text_channel(channel_type)
            else:
                channel_type = channel_check_exists
    except Exception as e:
        exception_error(e)


# @slash_command(
#     name="schedule_event",
#     description="Shedule an event",
#     default_member_permissions=(Permissions.MANAGE_EVENTS | Permissions.ADMINISTRATOR),
# )

# async def create_event_function(ctx: SlashContext):
#     '''Schedule a new event'''
#     modal = Modal(
#         ShortText(
#             label="Title",
#             custom_id="event_title",
#             placeholder="Offensive Developer",
#             required=True
#         ),
#         ParagraphText(
#             label="Description",
#             custom_id="event_description",
#             placeholder="Insert an event description here",
#             required=True
#         ),
#         ShortText(
#             label="Start Time",
#             custom_id="start_time",
#             placeholder="2023-08-13",
#             required=True
#         ),
#         ShortText(
#             label="End Time",
#             custom_id="end_time",
#             placeholder="2023-08-14",
#             required=True
#         ),
#         custom_id="create_event",
#         title="Create Event",
#     )

#     await ctx.send_modal(modal=modal)
#     modal_ctx: ModalContext = await ctx.bot.wait_for_modal(modal)

#     title = modal_ctx.responses["event_title"]
#     description = modal_ctx.responses["event_description"]
#     start_time: str = modal_ctx.responses["start_time"]
#     end_time: str = modal_ctx.responses["end_time"]
#     start_time = datetime.strptime(start_time, "%Y-%m-%d")
#     end_time = datetime.strptime(end_time, "%Y-%m-%d")

#     ScheduledEvent(
#         guild_id=DEBUG_ID,
#         name=title,
#         description=description,
#         start_time=start_time,
#         end_time=end_time,
#         privacy_level=ScheduledEventPrivacyLevel.GUILD_ONLY,
#         status=ScheduledEventStatus.SCHEDULED,
#         entity_type=3,
#         client=,
#         id=1
#     )


# DEBUG COMMANDS
@slash_command(
    name="update_repo",
    description="Update Bot Repo",
    scopes=[DEBUG_ID],
    default_member_permissions=Permissions.ADMINISTRATOR
)
async def update_repo(ctx):
    '''Updates the bot if the scope is within the dev server'''
    origin.fetch()
    await ctx.send("**Updating Repo**")


if __name__ == "__main__":
    info("Bot is Running")
    bot.start(BOT_TOKEN)
