from discord.ext import commands
from discord import Embed, PermissionOverwrite
from config.db import session
from models.VoiceChannel import VoiceChannel

from config import colors
from config import default_messages


class VoiceManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command("vc-text")
    @commands.has_permissions(manage_channels=True)
    async def vc_handler(self, ctx, cmd="", channel_id=""):
        if cmd == "add":
            await self.vc_add(ctx, channel_id)
        elif cmd == "list":
            await self.vc_list(ctx)
        elif cmd == "remove":
            await self.vc_delete(ctx, channel_id)

    async def vc_add(self, ctx, voice_id):
        """ Adds a voice channel to managing the temporary text channel

        :param ctx: context of event.
        :param voice_id: the id of the voice channel in discord.
        :return:
        """
        vc = VoiceChannel(discord_id=voice_id)
        session.add(vc)
        session.commit()
        embed = Embed(
            type="rich",
            title="Success",
            description="Temporary text channel has been created",
            color=colors.COLOR_SUCCESS
        )
        await ctx.send(embed=embed, reference=ctx.message)

    async def vc_list(self, ctx):
        """ Prints a list with all voice channels being managed

        :param ctx: context of event.
        :return:
        """
        msg = ""
        #entries from database
        vcs_entries = session.query(VoiceChannel).all()
        for vc_entry in vcs_entries:
            #voice channel object by discord
            vc = ctx.guild.get_channel(int(vc_entry.discord_id))
            msg += "**"+ vc.name + ": ** \n"
            msg += "Id: *" + str(vc.id) + "*"
            msg += "\n\n"

        embed = Embed(
            type="rich",
            title="Voice channels",
            description=msg,
            color=colors.COLOR_SUCCESS
        )
        await ctx.send(embed=embed, reference=ctx.message)

    async def vc_delete(self, ctx, voice_id):
        """ Command to delete the temporary text channel

        :param ctx:
        :param voice_id: discords id of voice channel
        :return:
        """
        # entry from database
        vc_entry = session.query(VoiceChannel).filter(VoiceChannel.discord_id == voice_id).first()

        # if text channel exists delete it from discord
        if vc_entry.text_id:
            await ctx.guild.get_channel(int(vc_entry.text_id)).delete()
        session.delete(vc_entry)
        session.commit()
        embed = Embed(
            type="rich",
            title="Success",
            description="Temporary text channel has been deleted",
            color=colors.COLOR_SUCCESS
        )
        await ctx.send(embed=embed, reference=ctx.message)

    @vc_handler.error
    async def error_handler(self, ctx, error):
        """ Simple error handler nothing fancy. ugly tbh

        :param ctx:
        :param error:
        :return:
        """
        if error.missing_perms:
            await ctx.send(embed=default_messages.ERROR_PERMISSION_EMBED, reference=ctx.message)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """ Listener for a member to change their voice status

        :param member: member changing voice status
        :param before: voice channel before
        :param after: voice channel after
        :return:
        """
        if after.channel:
            await self.voice_join(after.channel, member)
        if before.channel:
            await self.voice_leave(before.channel, member)

    async def create_text_channel(self, voice_channel, member):
        """ Creates a temporary text channel

        :param voice_channel: voice channel text channel should be created for
        :param member: member giving permission to for voice channel
        :return: The created text channel
        """
        vc = session.query(VoiceChannel).filter(VoiceChannel.discord_id == voice_channel.id).first()
        guild = voice_channel.guild
        permissions = {
            guild.default_role: PermissionOverwrite(read_messages=False)
        }
        text_channel = await voice_channel.guild.create_text_channel(
            voice_channel.name,
            postion=voice_channel.position,
            category=voice_channel.category,
            overwrites=permissions
        )
        vc.text_id = text_channel.id
        session.commit()
        return text_channel

    async def delete_text_channel(self, voice_channel):
        """ Deletes the temporary text channel to the voice channel

        :param voice_channel:
        :return:
        """
        vc = session.query(VoiceChannel).filter(VoiceChannel.discord_id == voice_channel.id).first()
        text_channel = voice_channel.guild.get_channel(int(vc.text_id))
        await text_channel.delete()
        vc.text_id = ""
        session.commit()
        return

    async def give_text_channel_permission(self, member, text_channel):
        """ Gives member the permission to read the temporary text channel

        :param member: Member permission giving to
        :param text_channel: text channel altering permissions
        :return:
        """
        await text_channel.set_permissions(target=member, view_channel=True)

    async def revoke_text_channel_permission(self, member, text_channel):
        """ Revokes member the permission to read the temporary text channel

        :param member: Member permission revoking of
        :param text_channel: text channel altering permissions
        :return:
        """
        await text_channel.set_permissions(target=member, view_channel=False)

    async def voice_join(self, voice_channel, member):
        """ Managing when member joins a voice channel

        :param voice_channel: channel member joined
        :param member: member joining channel
        :return:
        """
        vc = session.query(VoiceChannel).filter(VoiceChannel.discord_id == voice_channel.id).first()
        if not vc:
            return
        if not vc.text_id:
            text_channel = await self.create_text_channel(voice_channel, member)
        else:
            text_channel = voice_channel.guild.get_channel(int(vc.text_id))

        await self.give_text_channel_permission(member, text_channel)

    async def voice_leave(self, voice_channel, member):
        """ Managing when member leaves a channel

        :param voice_channel: channel member joined left
        :param member: member leaving channel
        :return:
        """
        vc = session.query(VoiceChannel).filter(VoiceChannel.discord_id == voice_channel.id).first()
        if not vc:
            return
        if not vc.text_id:
            return
        if len(voice_channel.members) == 0:
            await self.delete_text_channel(voice_channel)
        if len(voice_channel.members) != 0:
            text_channel = voice_channel.guild.get_channel(int(vc.text_id))
            await self.revoke_text_channel_permission(member, text_channel)
