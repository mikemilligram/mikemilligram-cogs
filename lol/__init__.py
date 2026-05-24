from .lol import LoL


async def setup(bot):
    await bot.add_cog(LoL(bot))
