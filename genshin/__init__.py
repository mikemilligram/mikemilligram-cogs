from .genshin import Genshin


def setup(bot):
    bot.add_cog(Genshin())
