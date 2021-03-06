import discord
from discord.ext import commands
from discord.ext.commands import Context
from models.AvatarEmoji import AvatarEmoji

from config import default_messages
from config.db import session
from config import colors


def help_message(command: str = "") -> discord.Embed:
    if command == "add":
        output = discord.Embed(
            title="Help for \"avatar add\" command",
            description="avatar add <Ping users here>",
            color=colors.COLOR_GENERIC
        )
    elif command == "remove":
        output = discord.Embed(
            title="Help for \"avatar remove\" command",
            description="avatar remove <Ping users here>",
            color=colors.COLOR_GENERIC
        )
    else:
        output = discord.Embed(
            title="Help for \"avatar\" command",
            description="avatar add/remove",
            color=colors.COLOR_GENERIC
        )
    return output

class EmojiManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command("avatar")
    @commands.has_permissions(manage_emojis=True)
    async def avatar_handler(self, ctx: Context, cmd: str = None, parameter: str = None):
        """ Manage Emojis which are made form avatars of users

        :param ctx:
        :param cmd: command like "add" or "delete"
        :param parameter: Additional parameter (not used yet)
        :return:
        """
        if cmd == "add":
            await self.emoji_add(ctx)
        if cmd == "remove":
            await self.delete_emoji(ctx)
        if cmd == "list":
            pass

    async def emoji_add(self, ctx: Context):
        """ Command to create or update an emoji

        :param ctx:
        :return:
        """

        # list of emojis for reaction
        emojis = []

        # action for every mentioned member
        async with ctx.typing():
            for member in ctx.message.mentions:
                profile_picture_entry = session.query(AvatarEmoji)\
                    .filter(AvatarEmoji.user_id == member.id and AvatarEmoji.guild_id == member.guild.id)\
                    .first()
                if profile_picture_entry:
                    await self.delete_emoji_by_member(member)
                emoji = await self.create_emoji_for_member(member)
                emojis.append(emoji)

            # create success message
            msg = discord.Embed(
                type="rich",
                title="Sucess",
                color=colors.COLOR_SUCCESS,
                description="Emoji has been successfully created"
            )
            success_msg = await ctx.send(embed=msg)
            for e in emojis:
                if e:
                    await success_msg.add_reaction(e)

    async def delete_emoji(self, ctx: Context):
        """ Deletes emojis for members

        :param ctx:
        :return:
        """
        for member in ctx.message.mentions:
            await self.delete_emoji_by_member(member)

        # create success message
        msg = discord.Embed(
            type="rich",
            title="Sucess",
            color=colors.COLOR_SUCCESS,
            description="Emoji has been successfully removed"
        )
        await ctx.send(embed=msg)

    async def create_emoji_for_member(self, member: discord.Member) -> discord.Emoji:
        """ Creates the emoji for given member

        :param member: member emoji should be created for
        :return: [discord.Emoji] created Emoji
        """
        # generate name
        name = member.name + member.discriminator

        # download avatar
        profile_picture = await member.avatar_url_as(format="png", size=64).read()

        # create avatar and yield
        emoji = await member.guild.create_custom_emoji(name=name, image=profile_picture)

        # if failed return
        if not emoji:
            return None

        # create entry for database
        emoji_entry = AvatarEmoji(
            name=emoji.name,
            discord_id=emoji.id,
            user_id=str(member.id),
            guild_id=str(member.guild.id)
        )
        session.add(emoji_entry)
        session.commit()
        return emoji

    async def delete_emoji_by_member(self, member: discord.Member):
        """ deletes an Emoji for given member

        :param member:
        :return:
        """
        # get emoji from database
        emoji_entry = session.query(AvatarEmoji)\
            .filter(AvatarEmoji.user_id == member.id and AvatarEmoji.guild_id == member.guild.id)\
            .first()
        # get emoji from discord
        emoji = discord.utils.get(member.guild.emojis, id=int(emoji_entry.discord_id))
        if not emoji:
            return False
        # delete emoji on discord
        await emoji.delete()

        # delete in database
        session.delete(emoji_entry)
        session.commit()

    @avatar_handler.error
    async def error_handler(self, ctx: Context, error):
        """ Error handler

        :param ctx:
        :param error:
        :return:
        """
        if hasattr(error, 'missing_perms'):
            await ctx.send(embed=default_messages.ERROR_PERMISSION_EMBED, reference=ctx.message)
        else:
            await ctx.send(embed=default_messages.ERROR_GENERIC_EMBED, reference=ctx.message)
