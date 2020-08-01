from redbot.core import commands
from redbot.core import Config
import discord
import asyncio


DIMENSIONS = {'o': 'overworld', 'n': 'nether', 'e': 'the end'}


class Minecraft(commands.Cog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lock = asyncio.Lock()
        self.config = Config.get_conf(self, identifier=141197)
        # default_member = {}
        default_guild = {
            'connections': {},
            'locations': {}
        }
        # self.config.register_member(**default_member)
        self.config.register_guild(**default_guild)

    @commands.group(aliases=['mc'])
    async def minecraft(self, ctx):
        pass

    @minecraft.group(aliases=['netherhub'])
    async def hub(self, ctx):
        pass

    @minecraft.group()
    async def location(self, ctx):
        pass

    @hub.command(name="list")
    async def hub_list(self, ctx):
        async with self.lock:
            connections = await self.config.guild(ctx.guild).connections()
        embed = discord.Embed(title="NETHER HUB")
        for connection, portals in connections.items():
            embed.add_field(name=connection.title(), value=f"\a", inline=True)
            embed.add_field(name=f"{portals[0]['x']} | {portals[0]['z']}", value="Nether", inline=True)
            embed.add_field(name = f"{portals[1]['x']} | {portals[1]['y']} | {portals[1]['z']}", value = "Overworld",
                            inline = True)
        return await ctx.send(embed=embed)

    @hub.command(name="add")
    async def hub_add(self, ctx, name: str, nether_x: int, nether_z: int, overworld_x: int, overworld_y: int,
                  overworld_z: int):
        nether_portal = {'x': nether_x, 'z': nether_z}
        overworld_portal = {'x': overworld_x, 'y': overworld_y, 'z': overworld_z}
        async with self.lock:
            connections = await self.config.guild(ctx.guild).connections()
        if name.lower() in connections.keys():
            return await ctx.send("There is already a connection with that name.")
        else:
            connections[name.lower()] = [nether_portal, overworld_portal]
        await self.config.guild(ctx.guild).connections.set(connections)
        return await ctx.send("The connection has been registered.")

    @location.command(name="list")
    async def location_list(self, ctx):
        async with self.lock:
            locations = await self.config.guild(ctx.guild).locations()
        embed = discord.Embed(title = "LOCATIONS")
        for location, coords in locations.items():
            embed.add_field(name = location.title(), value = "\a", inline = True)
            embed.add_field(name = f"{coords['x']} | {coords['y']} | {coords['z']}", value = "Coordinates",
                            inline = True)
        return await ctx.send(embed = embed)

    @location.command(name="add")
    async def location_add(self, ctx, name: str, x: int, y: int, z: int):
        location = {'x': x, 'y': y, 'z': z}
        async with self.lock:
            locations = await self.config.guild(ctx.guild).locations()
        if name.lower() in locations.keys():
            return await ctx.send("There is already a location with that name.")
        else:
            locations[name.lower()] = location
        await self.config.guild(ctx.guild).locations.set(locations)
        return await ctx.send("The location has been registered.")
