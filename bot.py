from discord.ext import commands

from cogs.VoiceManager import VoiceManager
from cogs.EmojiManager import EmojiManager

bot = commands.Bot(command_prefix="$")

bot.add_cog(VoiceManager(bot))
bot.add_cog(EmojiManager(bot))

@bot.command("ping")
async def ping(ctx):
    await ctx.send("pong")
