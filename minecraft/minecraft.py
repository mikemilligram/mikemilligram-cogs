from redbot.core import commands
from redbot.core import Config
import discord


class Minecraft(commands.Cog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = Config.get_conf(self, identifier=141197)
        # default_member = {
        #
        # }
        # default_guild = {
        #
        # }
        # self.config.register_member(**default_member)
        # self.config.register_guild(**default_guild)

    @commands.group(aliases=['mc'])
    async def minecraft(self, ctx):
        pass

    @minecraft.group(aliases=['nether', 'hub'])
    async def nether_hub(self, ctx):
        pass

    @minecraft.group()
    async def locations(self, ctx):
        pass

    @nether_hub.command()
    async def list(self, ctx):
        async with self.lock:
            data = await self.config.guild(ctx.guild).all()

    @nether_hub.command()
    async def add(self, ctx, name: str, nether_x: int, nether_z: int, overworld_x: int, overworld_y: int, overworld_z: int):
        nether_portal = {x: nether_x, z: nether_z}
        overworld_portal = {x: overworld_x, y: overworld_y, z: overworld_z}
        async with self.lock:
            data = await self.config.guild(ctx.guild).all()
        if name in data['connections'].keys():
            return await ctx.send("There is already a connection with that name")
        else:
            data['connections'][name] = {nether_portal: overworld_portal}
        await self.config.guild(ctx.guild).connections.set(data['connection'])
