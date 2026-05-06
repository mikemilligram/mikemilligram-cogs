from .ha import HomeAssistant


async def setup(bot):
    await bot.add_cog(HomeAssistant(bot))