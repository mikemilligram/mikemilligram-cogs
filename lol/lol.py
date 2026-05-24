from redbot.core import commands, app_commands, Config
from redbot.core.utils.views import ConfirmView
from redbot.core.utils.menus import menu
from urllib import request
import json
import discord
import random


class LoL(commands.Cog):
    """League of Legends Cog"""
    
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=120701)
        default_global = {
            'sources': {
                'champs': ""
            },
            'champs': []
        }
        default_member = {
            'champs': []
        }
        self.config.register_global(**default_global)
        self.config.register_member(**default_member)
        
        
    @commands.group(name='champs')
    async def champs(self, ctx):
        pass
    
    
    @commands.is_owner()
    @champs.command(name='setsource')
    async def set_source(self, ctx, source: str):
        """set the source for the list of champs"""
        await self.config.sources.champs.set(source)
        await ctx.send("source has been set")


    @champs.command(name='list')
    async def champs_list(self, ctx):
        champ_list = await self.config.member(ctx.author).champs()
        pages = []
        for i in range(0, len(champ_list), 10):
            embed = discord.Embed(title=f"your champs - {len(champ_list)}", description="\n".join(champ_list[i:i+10]))
            embed.set_footer(text="Page {}/{}".format(i//10+1, (len(champ_list)-1)//10+1))
            pages.append(embed)
        if champ_list:
            await menu(ctx, pages, timeout=60)
        else:
            await ctx.send("your champs list is empty")   

    champs_slash = app_commands.Group(name="champs", description="League of Legends commands")

      
    @app_commands.checks.has_permissions(administrator=True)
    @champs_slash.command(name='update')
    async def champs_update(self, interaction: discord.Interaction):
        source = await self.config.sources.champs()
        with request.urlopen(source) as url:
            data = json.loads(url.read().decode())
        champ_list = list(data['data'].keys())
        await self.config.champs.set(champ_list)
        await interaction.response.send_message("global champs list has been updated")
        
    
    @champs_slash.command(name='reset')
    async def champs_reset(self, interaction: discord.Interaction):
        champs = await self.config.champs()
        await self.config.member(interaction.user).champs.set(champs)
        await interaction.response.send_message("your champs list has been reset")
        
    
    @champs_slash.command(name='remove')
    async def champs_remove(self, interaction: discord.Interaction, champ: str):
        champ_list = await self.config.member(interaction.user).champs()
        if champ in champ_list:
            champ_list.remove(champ)
            await self.config.member(interaction.user).champs.set(champ_list)
            await interaction.response.send_message(f"{champ} has been removed from your list")
        else:
            await interaction.response.send_message(f"{champ} is not on your list")
            
    
    @champs_slash.command(name='add')
    async def champs_add(self, interaction: discord.Interaction, champ: str):
        champ_list = await self.config.member(interaction.user).champs()
        if champ not in champ_list:
            champs = await self.config.champs()
            if champ not in champs:
                await interaction.response.send_message(f"{champ} is not a valid champion")
                return
            champ_list.append(champ)
            await self.config.member(interaction.user).champs.set(champ_list)
            await interaction.response.send_message(f"{champ} has been added to your list")
        else:
            await interaction.response.send_message(f"{champ} is already on your list")
                 
    
    @champs_slash.command(name='random')
    async def champs_random(self, interaction: discord.Interaction):
        champ_list = await self.config.member(interaction.user).champs()
        if champ_list:
            champ = random.choice(champ_list)
            view = ConfirmView(interaction.user, disable_buttons=True)
            view.confirm_button.style = discord.ButtonStyle.red
            view.message = await interaction.response.send_message(f"your random champion is {champ}, confirm to remove them from your list", view=view)
            await view.wait()
            if view.result:
                champ_list.remove(champ)
                await self.config.member(interaction.user).champs.set(champ_list)
                await interaction.edit_original_response(content=f"{champ} has been removed from your list")
            else:
                await interaction.edit_original_response(content=f"{champ} has not been removed from your list")
                pass
            
        else:
            await interaction.response.send_message("your champs list is empty")
