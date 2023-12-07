from .genshin import Genshin


async def setup(bot):
    await bot.add_cog(Genshin(bot))
