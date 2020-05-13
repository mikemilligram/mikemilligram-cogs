from redbot.core import commands
from redbot.core import Config
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu
from redbot.core.data_manager import bundled_data_path
import discord
import json
import copy


class ACTracker(commands.Cog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = Config.get_conf(self, identifier=4469)
        self.data = bundled_data_path(self)
        default_global = {
            'fish': get_json(str(self.data) + '/fish.json'),
            'bugs': get_json(str(self.data) + '/bugs.json'),
            'fossils': get_json(str(self.data) + '/fossils.json')
        }
        default_member = {
            'donated_fish': {},
            'donated_bugs': {},
            'donated_fossils': {}
        }
        self.config.register_global(**default_global)
        self.config.register_member(**default_member)

    @commands.group()
    async def donate(self, ctx):
        pass

    @donate.command(name='fish')
    async def donate_fish(self, ctx, fish_id: int):
        fish_data = await self.config.fish()
        if 0 < fish_id <= len(fish_data):
            fish = await self.config.member(ctx.author).donated_fish()
            if str(fish_id) not in fish.keys():
                await self.config.member(ctx.author).donated_fish.set_raw(fish_id, value=1)
                await ctx.send('you donated one (1) ' + fish_data[str(fish_id)]['name'].lower())
            else:
                await ctx.send("you already donated this, idiot")
        else:
            await ctx.send("<:fubk:702961960786067522>")

    @donate.command(name='bug')
    async def donate_bug(self, ctx, bug_id: int):
        bug_data = await self.config.bugs()
        if 0 < bug_id <= len(bug_data):
            bugs = await self.config.member(ctx.author).donated_bugs()
            if str(bug_id) not in bugs.keys():
                await self.config.member(ctx.author).donated_bugs.set_raw(bug_id, value=1)
                await ctx.send('you donated one (1) ' + bug_data[str(bug_id)]['name'].lower())
            else:
                await ctx.send("you already donated this, idiot")
        else:
            await ctx.send("<:fubk:702961960786067522>")

    @donate.command(name='fossil')
    async def donate_fossil(self, ctx, fossil_id: int):
        fossil_data = await self.config.fossils()
        if 0 < fossil_id <= len(fossil_data):
            fossils = await self.config.member(ctx.author).donated_fossils()
            if str(fossil_id) not in fossils.keys():
                await self.config.member(ctx.author).donated_fossils.set_raw(fossil_id, value=1)
                await ctx.send('you donated one (1) ' + fossil_data[str(fossil_id)]['name'].lower())
            else:
                await ctx.send("you already donated this, idiot")
        else:
            await ctx.send("<:fubk:702961960786067522>")

    @commands.group(name='undonate')
    async def undonate(self, ctx):
        pass

    @undonate.command(name='fish')
    async def undonate_fish(self, ctx, fish_id: int):
        fish_data = await self.config.fish()
        if 0 < fish_id <= len(fish_data):
            fish = await self.config.member(ctx.author).donated_fish()
            if str(fish_id) in fish.keys():
                await self.config.member(ctx.author).donated_fish.clear_raw(fish_id)
                await ctx.send('you undonated one (1) ' + fish_data[str(fish_id)]['name'].lower())
                return

        # bad input
        await ctx.send("<:fubk:702961960786067522>")

    @undonate.command(name='bug')
    async def undonate_bug(self, ctx, bug_id: int):
        bug_data = await self.config.bugs()
        if 0 < bug_id <= len(bug_data):
            bugs = await self.config.member(ctx.author).donated_bugs()
            if str(bug_id) in bugs.keys():
                await self.config.member(ctx.author).donated_bugs.clear_raw(bug_id)
                await ctx.send('you undonated one (1) ' + bug_data[str(bug_id)]['name'].lower())
                return

            # bad input
            await ctx.send("<:fubk:702961960786067522>")

    @undonate.command(name='fossil')
    async def undonate_fossil(self, ctx, fossil_id: int):
        fossil_data = await self.config.fossils()
        if 0 < fossil_id <= len(fossil_data):
            fossils = await self.config.member(ctx.author).donated_fossils()
            if str(fossil_id) in fossils.keys():
                await self.config.member(ctx.author).donated_fossils.clear_raw(fossil_id)
                await ctx.send('you undonated one (1) ' + fossil_data[str(fossil_id)]['name'].lower())
                return

        # bad input
        await ctx.send("<:fubk:702961960786067522>")

    @commands.group()
    async def list(self, ctx):
        pass

    @list.command(name='bugs')
    async def list_bugs(self, ctx):
        bugs = await self.config.member(ctx.author).donated_bugs()
        bugs_data = await self.config.bugs()
        overview = get_overview('bug', bugs, bugs_data)
        await menu(ctx, overview, controls=copy.deepcopy(DEFAULT_CONTROLS))

    @list.command(name='fish')
    async def list_fish(self, ctx):
        fish = await self.config.member(ctx.author).donated_fish()
        fish_data = await self.config.fish()
        overview = get_overview('fish', fish, fish_data)
        await menu(ctx, overview, controls=copy.deepcopy(DEFAULT_CONTROLS))

    @list.command(name='fossils')
    async def list_fossils(self, ctx):
        fossils = await self.config.member(ctx.author).donated_fossils()
        fossil_data = await self.config.fossils()
        overview = get_overview_fossils(fossils, fossil_data)
        await menu(ctx, overview, controls=copy.deepcopy(DEFAULT_CONTROLS))

    @commands.group()
    async def show(self, ctx):
        pass

    @show.command(name='bug')
    async def show_bug(self, ctx, bug_id: int):
        bug_data = await self.config.bugs()
        if 0 < bug_id <= len(bug_data):
            embed = get_detail('bug', bug_id, bug_data)
            await ctx.send(embed=embed)
        else:
            await ctx.send("<:fubk:702961960786067522>")

    @show.command(name='fish')
    async def show_fish(self, ctx, fish_id: int):
        fish_data = await self.config.fish()
        if 0 < fish_id <= len(fish_data):
            embed = get_detail('fish', fish_id, fish_data)
            await ctx.send(embed=embed)
        else:
            await ctx.send("<:fubk:702961960786067522>")

    @show.command(name='fossil')
    async def show_fossil(self, ctx, fossil_id: int):
        fossil_data = await self.config.fossils()
        if 0 < fossil_id <= len(fossil_data):
            embed = get_detail('fossil', fossil_id, fossil_data)
            await ctx.send(embed=embed)
        else:
            await ctx.send("<:fubk:702961960786067522>")

    @commands.group(name='month')
    async def month_critters(self, ctx):
        pass

    @month_critters.command(name='fish')
    async def month_fish(self, ctx, month: str, southern: bool = False):
        fish_data = await self.config.fish()
        donated_fish = await self.config.member(ctx.author).donated_fish()
        if month in MONTHS.keys():
            overview = get_overview('fish', donated_fish, get_critters_by_month(fish_data, month, southern=southern))
            await menu(ctx, overview, controls=copy.deepcopy(DEFAULT_CONTROLS))
        else:
            await ctx.send("<:fubk:702961960786067522>")

    @month_critters.command(name='bugs')
    async def month_bugs(self, ctx, month: str, southern: bool = False):
        bugs_data = await self.config.bugs()
        donated_bugs = await self.config.member(ctx.author).donated_bugs()
        if month in MONTHS.keys():
            overview = get_overview('bugs', donated_bugs, get_critters_by_month(bugs_data, month, southern=southern))
            await menu(ctx, overview, controls=copy.deepcopy(DEFAULT_CONTROLS))
        else:
            await ctx.send("<:fubk:702961960786067522>")

    @commands.group(name='new')
    async def new_critters(self, ctx):
        pass

    @new_critters.command(name='fish')
    async def new_fish(self, ctx, month: str, southern: bool = False):
        fish_data = await self.config.fish()
        donated_fish = await self.config.member(ctx.author).donated_fish()
        if month in MONTHS.keys():
            overview = get_overview('fish', donated_fish, get_critters_by_month(fish_data, month, new=True,southern=southern))
            await menu(ctx, overview, controls=copy.deepcopy(DEFAULT_CONTROLS))
        else:
            await ctx.send("<:fubk:702961960786067522>")

    @new_critters.command(name='bugs')
    async def new_bugs(self, ctx, month: str, southern: bool = False):
        bugs_data = await self.config.bugs()
        donated_bugs = await self.config.member(ctx.author).donated_bugs()
        if month in MONTHS.keys():
            overview = get_overview('fish', donated_bugs,
                                    get_critters_by_month(bugs_data, month, new=True, southern=southern))
            await menu(ctx, overview, controls=copy.deepcopy(DEFAULT_CONTROLS))
        else:
            await ctx.send("<:fubk:702961960786067522>")

    @commands.group(name='missing')
    async def missing(self, ctx):
        pass

    @missing.command(name='fish')
    async def missing_fish(self, ctx):
        fish_data = await self.config.fish()
        donated_fish = await self.config.member(ctx.author).donated_fish()
        overview = get_overview('fish', donated_fish, filter_missing(donated_fish, fish_data))
        await menu(ctx, overview, controls=copy.deepcopy(DEFAULT_CONTROLS))

    @missing.command(name='bugs')
    async def missing_bugs(self, ctx):
        bugs_data = await self.config.bugs()
        donated_bugs = await self.config.member(ctx.author).donated_bugs()
        overview = get_overview('bugs', donated_bugs, filter_missing(donated_bugs, bugs_data))
        await menu(ctx, overview, controls=copy.deepcopy(DEFAULT_CONTROLS))

    @missing.command(name='fossils')
    async def missing_fossils(self, ctx):
        fossils_data = await self.config.fossils()
        donated_fossils = await self.config.member(ctx.author).donated_fossils()
        overview = get_overview_fossils(donated_fossils, filter_missing(donated_fossils, fossils_data))
        await menu(ctx, overview, controls=copy.deepcopy(DEFAULT_CONTROLS))

    @commands.command(name='progress')
    async def progress(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        name = user.nick if user.nick else user.name
        embed = discord.Embed(title=f"{name}'s progress")
        fish = await self.config.fish()
        bugs = await self.config.bugs()
        fossils = await self.config.fossils()
        donated_fish = await self.config.member(user).donated_fish()
        donated_bugs = await self.config.member(user).donated_bugs()
        donated_fossils = await self.config.member(user).donated_fossils()
        embed.add_field(name='fish', value=f'{len(donated_fish)} / {len(fish)}')
        embed.add_field(name='bugs', value=f'{len(donated_bugs)} / {len(bugs)}')
        embed.add_field(name='fossils', value=f'{len(donated_fossils)} / {len(fossils)}')
        await ctx.send(embed=embed)


MONTHS = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7,
          'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12}


def get_json(filename: str):
    file = open(filename)
    data = json.load(file)
    file.close()
    return data


def get_overview(collectible_type: str, donations: dict, data: dict):
    pages = []
    embed = discord.Embed(title=f'{collectible_type} tracker')
    page = []
    counter = 1
    for i, d in data.items():
        page.append(('✅' if i in donations.keys() else '❌') + f' {i} ' + d['name'].lower())
        if counter % 10 == 0:
            embed.add_field(name=f'{collectible_type} time', value='\n'.join(page))
            pages.append(embed)
            page = []
            embed = discord.Embed(title=f'{collectible_type} tracker')
        counter += 1
    if len(page) > 0:
        embed.add_field(name=f'{collectible_type} time', value='\n'.join(page))
        pages.append(embed)

    return pages


def get_detail(typ: str, cid: int, data: dict):
    collectible = data[str(cid)]
    embed = discord.Embed(title=collectible["name"])
    if typ in ['fish', 'bug']:
        embed.add_field(name='location', value=collectible['location'])
        if typ == 'fish':
            embed.add_field(name='size', value=collectible['size'])
        embed.add_field(name='time', value=collectible['time'])
    if typ in ['fossil']:
        embed.add_field(name='fossil class', value=f'{collectible["class"]}')
    embed.add_field(name='price', value=f'{collectible["price"]} bells')
    if typ in ['fish', 'bug']:
        embed.add_field(name='northern hs', value=collectible['northern'])
        embed.add_field(name='southern hs', value=collectible['southern'])

    return embed


def get_overview_fossils(donations: dict, data: dict):
    bundled = {}
    for f_id, info in data.items():
        if info['class'] == 'Standalone':
            info['id'] = f_id
            bundled[info['name']] = [info]
            continue
        elif info['class'] not in bundled.keys():
            bundled[info['class']] = []
        info['id'] = f_id
        bundled[info['class']].append(info)

    page = []
    embed = discord.Embed(title=f'fossil tracker')
    counter = 1
    for name, parts in bundled.items():
        fossil = []
        for part in parts:
            fossil.append(('✅' if part['id'] in donations.keys() else '❌') + f' {part["id"]} ' + part['name'].lower())
        embed.add_field(name=name, value='\n'.join(fossil))
        if counter % 9 == 0:
            page.append(embed)
            embed = discord.Embed(title=f'fossil tracker')
        counter += 1

    if len(embed.fields) > 0:
        page.append(embed)

    return page


def get_critters_by_month(data: dict, month: str, new: bool = False, southern: bool = False):
    hs = 'southern' if southern else 'northern'
    if month in MONTHS:
        by_month = {}
        for name, info in data.items():
            if MONTHS[month] in info[hs]:
                if new:
                    if MONTHS[month] == 1:
                        last = 12
                    else:
                        last = MONTHS[month] - 1
                    if last in info[hs]:
                        continue

                by_month[name] = info
        data = by_month

    return data


def filter_missing(donated: dict, data: dict):
    missing = {}
    for c_id, info in data.items():
        if c_id not in donated.keys():
            missing[c_id] = info

    return missing
