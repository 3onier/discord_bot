from discord.ext import commands

from cogs.VoiceManager import VoiceManager

bot = commands.Bot(command_prefix="$")

bot.add_cog(VoiceManager(bot))

@bot.command("ping")
async def ping(ctx):
    await ctx.send("pong")
