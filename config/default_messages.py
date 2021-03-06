from discord import Embed
from config import colors

ERROR_PERMISSION_EMBED = Embed(
                type="rich",
                title="Error",
                description="You are not permitted to run this command",
                color=colors.COLOR_ERROR
            )
