from redbot.core import commands
from redbot.core import Config
from datetime import datetime, timedelta
import math


class Genshin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=3547)
        default_global = {

        }
        default_guild = {
            'grind': 0,
            'date': ""
        }
        default_member = {
            'uid': 0,
            'achievements': {}
        }
        self.config.register_global(**default_global)
        self.config.register_guild(**default_guild)
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
        if output == "":
            spare = current_bronze - levels[4]
            gold = math.floor(spare / 9)
            await ctx.send(f"you'll have about {gold} gold books left over.")
        else:
            await ctx.send(output)

    @commands.command(name='papers')
    async def papers(self, ctx, purple: int, red: int, white=0):

        levels = [3331, 4943, 8367]
        average_gain = 122.5
        current_whites = purple * 20 + red * 5 + white

        tier = 70
        output = ""
        for level in levels:
            leylines = math.ceil((level - current_whites) / average_gain)
            condensed = math.ceil(((level - current_whites) / average_gain) / 2)
            if leylines > 0:
                output += f"{tier}:\t{leylines} ({condensed})\n"
            tier += 10
        if output == "":
            spare = current_whites - levels[2]
            purple = math.floor(spare / 20)
            await ctx.send(f"you'll have about {purple} purples left over.")
        else:
            await ctx.send(output)

    @commands.command(name='bondexp')
    async def bondexp(self, ctx, level: int, pixels: int, res: str = "1080"):
        levelbarpixels = 331
        if res == "2k":
            levelbarpixels = 442
        if not 1 <= level < 10 or not 0 <= pixels < levelbarpixels:
            await ctx.send('wrong input')
            return
        levels = {
            1: [1000, 0],
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

        for i in range(7):
            gain = normal + dailygains['refresh'] * i
            withgrind = gain + dailygains['grind']

            output += str(i).ljust(12) + (str(math.ceil(missingexp / gain)) + f' ({gain})').ljust(12) + (
                    str(math.ceil(missingexp / withgrind)) + f' ({withgrind})') + '\n'

        output += f'\ntotal exp missing: {missingexp}```'

        await ctx.send(output)

    @commands.command(name='grind')
    async def grind(self, ctx, events: int = 1):

        if not 0 < events < 10:
            await ctx.send('wrong input')
            return

        grind = await self.config.guild(ctx.guild).grind()
        last_date = await self.config.guild(ctx.guild).date()
        now = datetime.now()
        hour = int(now.strftime("%H"))

        if hour < 11:
            now -= timedelta(1)
        formatted_date = now.strftime("%d/%m/%Y")

        if formatted_date == last_date:
            if grind >= 10:
                await ctx.send("today's bond exp grind has already been completed.")
                return
            grind += events
        else:
            grind = events

        if grind < 5:
            second_line = "I" * grind
        elif grind < 10:
            second_line = "IIIII " + "I" * (grind - 5)
        else:
            second_line = "**IIIII IIIII**"

        output = f'{formatted_date}\n{second_line}'

        await self.config.guild(ctx.guild).grind.set(grind)
        await self.config.guild(ctx.guild).date.set(formatted_date)

        await ctx.send(output)

    @commands.command(name='reset')
    async def grind_reset(self, ctx):
        await self.config.guild(ctx.guild).grind.set(0)

        await ctx.send("today's bond exp grind has been reset.")

    @commands.group(name='genshin')
    async def genshin(self, ctx):
        pass
