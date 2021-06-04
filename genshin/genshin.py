from redbot.core import commands
from redbot.core import Config
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu
from redbot.core.data_manager import bundled_data_path
import math


class Genshin(commands.Cog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = Config.get_conf(self, identifier=3547)
        self.data = bundled_data_path(self)
        default_global = {

        }
        default_member = {

        }
        self.config.register_global(**default_global)
        self.config.register_member(**default_member)

    @donate.command(name='talents')
    async def talents(self, ctx, gold: int, silver: int, bronze: int, goal: int):

        if not 5 < goal < 11:
            await ctx.send("goal needs to be between 6 and 10")
            return
        levels = [198, 306, 468, 792, 1224]
        average_gain = 9.7
        current_bronze = gold * 9 + silver * 3 + bronze

        needed = levels[goal-6]

        domains = math.ceil((needed - current_bronze) / average_gain)
        condensed = math.ceil(((needed - current_bronze) / average_gain) / 2)

        await ctx.send(f"to reach talent level {goal}/{goal}/{goal} you need to claim {domains} domains ({condensed} "
                       f"if using condensed resin)")
