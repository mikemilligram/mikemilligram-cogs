from redbot.core import commands
from redbot.core import Config
import discord


class Stonks(commands.Cog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = Config.get_conf(self, identifier=19836)
        default_member = {
            'turnips': {
                'last_pattern': -1,
                'sunday': 0,
                'prices': {
                    '11': 0, '12': 0, '21': 0, '22': 0, '31': 0, '32': 0,
                    '41': 0, '42': 0, '51': 0, '52': 0, '61': 0, '62': 0,
                }
            }
        }
        self.config.register_member(**default_member)

    @commands.command()
    async def stonk(self, ctx):
        await ctx.send("here is one (1) stonk for you")

    @commands.command(help='weekday: 1 = monday, 2 = tuesday...\ntime: 1 = am, 2 = pm')
    async def turnips(self, ctx, weekday: str, time: str, price: int):
        if 0 < int(weekday) < 7 and 0 < int(time) < 3 and 1000 > price > 0:
            ts = weekday+time
            await self.config.member_from_ids(ctx.guild.id, ctx.author.id).turnips.prices.set_raw(ts, value=price)
            await ctx.send("<:turnip:707177818756218910>")
        else:
            await ctx.send("<:fubk:706516580368121867>")

    @commands.command()
    async def list(self, ctx, member: discord.Member = None):
        if member is not None:
            turnips = await self.config.member(member).turnips()
        else:
            turnips = await self.config.member(ctx.author).turnips()
        name = (member.display_name if member is not None else ctx.author.display_name)
        header = name + "'s turnip prices"
        await ctx.send(embed=discord.Embed(colour=discord.Colour.from_rgb(0,255,0), title=header, description='```' + get_overview(turnips) + '```'))

    @commands.command()
    async def link(self, ctx, member: discord.Member = None):
        if member is not None:
            turnips = await self.config.member(member).turnips()
        else:
            turnips = await self.config.member(ctx.author).turnips()
        await ctx.send(get_link(turnips))

    @commands.command()
    async def pattern(self, ctx, pattern: int):
        if 0 <= pattern <= 3:
            await self.config.member_from_ids(ctx.guild.id, ctx.author.id).turnips.last_pattern.set(pattern)
            await ctx.send("<:turnip:707177818756218910>")
        else:
            await ctx.send("<:fubk:706516580368121867>")

    @commands.command()
    async def resetpattern(self, ctx):
        await self.config.member_from_ids(ctx.guild.id, ctx.author.id).turnips.last_pattern.set(-1)
        await ctx.send("<:turnip:707177818756218910>")

    @commands.command()
    async def islandprice(self, ctx, price: int):
        if price > 0:
            await self.config.member_from_ids(ctx.guild.id, ctx.author.id).turnips.sunday.set(price)
            await ctx.send("<:turnip:707177818756218910>")
        else:
            await ctx.send("<:fubk:706516580368121867>")

    @commands.command()
    async def reset(self, ctx):
        await self.config.member_from_ids(ctx.guild.id, ctx.author.id).clear()
        await ctx.send("<:turnip:707177818756218910>")


weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
times = ['am', 'pm']
patterns = ['fluctuating', 'large spike', 'decreasing', 'small spike']

def get_link(turnips):
    baseurl = "https://turnipprophet.io/?prices="
    prices = get_prices(turnips)
    baseurl += str(turnips['sunday']) if turnips['sunday'] > 0 else ''
    for p in prices:
        baseurl += '.' + str(p)
    pattern = turnips['last_pattern']
    baseurl += "&pattern=" + str(pattern) if pattern >= 0 else ''
    return baseurl


def get_prices(turnips):
    prices = []
    for day in range(1, 7):
        for time in range(1, 3):
            price = turnips['prices'][str(day) + str(time)]
            prices.append(price if price > 0 else '')
    return prices


def get_overview(turnips):
    prices = get_prices(turnips)
    string = 'island price: ' + (str(turnips['sunday']) if turnips['sunday'] > 0 else '') + '\n\n'
    for day in range(1, 7):
        string += (weekdays[day - 1] + ' ').ljust(15) + times[0] + ': ' + str(prices[day * 2 - 2]).ljust(5)
        string += times[1] + ': ' + str(prices[day * 2 - 1]) + '\n'
    string += "\nlast week's pattern: " + (patterns[turnips['last_pattern']] if turnips['last_pattern'] >= 0 else 'unknown')
    return string