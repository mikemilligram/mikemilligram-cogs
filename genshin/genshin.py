import discord
from redbot.core import commands, app_commands
from redbot.core import Config
from datetime import datetime, timedelta
import math
import json
import re
import requests
from bs4 import BeautifulSoup


class Genshin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=3547)
        default_global = {

        }
        default_guild = {
            'achievements': {},
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

    @app_commands.command(name='bondexp')
    @app_commands.choices(res=[
        app_commands.Choice(name="1920x1080 - Full HD", value=1920),
        app_commands.Choice(name="2560x1440 - 2K", value=2560)
    ])
    async def bondexp(self, interaction: discord.Interaction, level: int, pixels: int, res: int):
        level_bar_pixels = 331 * (res / 1920)
        if not 1 <= level < 10 or not 0 <= pixels < level_bar_pixels:
            await interaction.response.send_message('invalid input', ephemeral=True)
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

        totalexp = math.floor(levels[level][1] + (pixels / level_bar_pixels) * levels[level][0])
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

        await interaction.response.send_message(output)

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

    @app_commands.command(name='achievements update')
    async def update(self, interaction: discord.Interaction):
        base_url = "https://genshin-impact.fandom.com"
        url = f"{base_url}/wiki/Wonders_of_the_World"
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')

        wonders = {}
        rows = soup.find('table').findAll('tr')

        for row in rows[1:]:
            elements = row.findAll('td')
            tier = re.match(r'.*\(Tier_(\d)\).*', elements[0].find('a').get('href').strip())
            name = elements[0].text.strip() + f" ({tier[1]})" if tier else elements[0].text.strip()
            achievement = {
                'name': elements[0].text.strip(),
                'description': elements[1].text.strip(),
                'requirements': elements[2].text.strip(),
                'hidden': elements[3].text.strip(),
                'type': elements[4].text.strip(),
                'version': elements[5].text.strip(),
                'reward': elements[6].text.strip(),
                'link': base_url + elements[0].find('a').get('href').strip(),
                'tier': tier[1] if tier else 0
            }
            wonders[name] = achievement

        await self.config.guild(interaction.guild).achievements.set(wonders)

        await interaction.response.send_message(f"Achievements have been updated, Total Achievements (Wonders of the "
                                                f"World): {len(wonders.keys())}")

    @app_commands.command(name='achievements list')
    async def list(self, interaction: discord.Interaction):
        achievements = await self.config.guild(interaction.guild).achievements()
        await interaction.response.send_message(len(achievements.keys()))

    # async def test(self, interaction: discord.Interaction[discord.InteractionType.component]):
    #     await interaction.response.send_message(discord.ActionRow([discord.Button(discord.ComponentType.button)]))
