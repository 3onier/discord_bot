from discord import Embed

from discord.ext import commands
from discord.ext.commands import Context

from cogs import VoiceManager
from cogs import EmojiManager

from config import colors

bot = commands.Bot(command_prefix="$")

bot.add_cog(VoiceManager.VoiceManager(bot))
bot.add_cog(EmojiManager.EmojiManager(bot))
bot.remove_command('help')


@bot.command("ping")
async def ping(ctx):
    await ctx.send("pong")


@bot.command("help")
async def help_command(ctx: Context, command: str = "", specifier: str = ""):
    if command == "vc-text":
        await ctx.send(embed=VoiceManager.help_message(specifier), reference=ctx.message)
    elif command == "avatar":
        await ctx.send(embed=EmojiManager.help_message(specifier), reference=ctx.message)
    else:
        embed = Embed(
            title="Help message",
            description="**Available Commands**: vc-text, avatar",
            color=colors.COLOR_GENERIC
        )
        await ctx.send(embed=embed, reference=ctx.message)
