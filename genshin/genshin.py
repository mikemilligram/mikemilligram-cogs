from redbot.core import commands
from redbot.core import Config
import math

class Genshin(commands.Cog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = Config.get_conf(self, identifier=3547)
        default_global = {

        }
        default_member = {

        }
        self.config.register_global(**default_global)
        self.config.register_member(**default_member)

    @commands.command(name='talents')
    async def talents(self, ctx, gold: int, silver: int, bronze: int):

        levels = [198, 306, 468, 792, 1224]
        average_gain = 9.7
        current_bronze = gold * 9 + silver * 3 + bronze

        tier = 6
        output = ""
        for level in levels:
            domains = math.ceil((level - current_bronze) / average_gain)
            condensed = math.ceil(((level - current_bronze) / average_gain) / 2)
            output += f"{tier}/{tier}/{tier}:\t{domains} ({condensed})\n"
            tier += 1
        await ctx.send(output)
