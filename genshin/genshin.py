from redbot.core import commands
from redbot.core import Config
from datetime import datetime
import math


class Genshin(commands.Cog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = Config.get_conf(self, identifier=3547)
        default_global = {
            grind: 0
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
            if domains > 0:
                output += f"{tier}/{tier}/{tier}:\t{domains} ({condensed})\n"
            tier += 1
        await ctx.send(output)

    @commands.command(name = 'papers')
    async def papers(self, ctx, purple: int, red: int, white = 0):

        levels = [3331, 4943, 8367]
        average_gain = 122.5
        min_gain = 110
        max_gain = 135
        current_whites = purple * 20 + red * 5 + white

        tier = 70
        output = ""
        for level in levels:
            leylines = math.ceil((level - current_whites) / average_gain)
            condensed = math.ceil(((level - current_whites) / average_gain) / 2)
            if leylines > 0:
                output += f"{tier}:\t{leylines} ({condensed})\n"
            tier += 10
        await ctx.send(output)

    @commands.command(name = 'bondexp')
    async def bondexp(self, ctx, level: int, pixels: int):
        if not 1 <= level < 10 or not 0 <= pixels < 331:
            await ctx.send('wrong input')
            return
        levels = {1: [1000, 0],
                  2: [1550, 1000],
                  3: [2050, 2550],
                  4: [2600, 4600],
                  5: [3175, 7200],
                  6: [3750, 10375],
                  7: [4350, 14125],
                  8: [4975, 18475],
                  9: [5650, 23450]
                  }

        maxexp = 29100

        levelbarpixels = 331

        totalexp = math.floor(levels[level][1] + (pixels / levelbarpixels) * levels[level][0])
        missingexp = maxexp - totalexp

        dailygains = {'teapot': 120,
                      'grind': 300,
                      'commissions': 580,
                      'resin': 360,
                      'refresh': 120
                      }

        normal = dailygains['teapot'] + dailygains['commissions'] + dailygains['resin']

        output = '```' + 'refreshes'.ljust(12) + 'no grind'.ljust(12) + 'with grind\n'

        for i in range(4):
            gain = normal + dailygains['refresh'] * i
            withgrind = gain + dailygains['grind']

            output += str(i).ljust(12) + (str(math.ceil(missingexp/gain)) + f' ({gain})').ljust(12) + (str(math.ceil(missingexp/withgrind)) + f' ({withgrind})') + '\n'

        output += f'\ntotal exp missing: {missingexp}```'

        await ctx.send(output)

    @commands.command(name = 'grind')
    async def grind(self, ctx):
        grind = await self.config.grind()

        now = datetime.now()

        hour = int(now.strftime("%H"))

        output = now.strftime("%d/%m/%Y")

        await ctx.send(output)
