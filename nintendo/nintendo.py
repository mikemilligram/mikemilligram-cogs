from redbot.core import commands
from redbot.core import Config
import discord


class Nintendo(commands.Cog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = Config.get_conf(self, identifier=1806)
        default_member = {
            'switchcode': 'This user has not registered a switch code'
        }
        self.config.register_member(**default_member)

    @commands.group()
    async def switch(self, ctx):
        pass

    @switch.command(name='set', help = 'register or change your nintendo switch code')
    async def set_code(self, ctx, code: str):
        await self.config.member_from_ids(ctx.guild.id, ctx.author.id).switchcode.set(code)
        await ctx.send("your switch code has been set")

    @switch.command(name='show', help = "display your own or someone else's switch code")
    async def display_code(self, ctx, member: discord.Member = None):
        user = member if member else ctx.author
        code = await self.config.member_from_ids(ctx.guild.id, user.id).switchcode()
        name = user.nick if user.nick else user.name
        await ctx.send(f"{name}'s switch code: " + code)

    @switch.command(name='list', help = "display the codes of everyone in the server")
    async def list_codes(self, ctx):
        users = await self.config.all_members(ctx.guild)
        embed = discord.Embed(title = 'switch codes')
        for userid, data in users.items():
            user = self.bot.get_user(userid)
            name = user.nick if user.nick else user.name
            embed.add_field(name = name, value = data['switchcode'])
        await ctx.send(embed=embed)
