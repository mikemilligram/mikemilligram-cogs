from typing import Literal

import discord
from redbot.core import Config, commands, app_commands
from .rest import HomeAssistantAPI

class HomeAssistant(commands.Cog):
    """Home Assistant Cog"""

    def __init__(self, bot):
        self.bot = bot
        
        self.config = Config.get_conf(self, identifier=800813, force_registration=True)
        
        default_guild = {
            "url": "",
            "token": "",
            "entities": {}
        }
        
        self.config.register_guild(**default_guild)
        
    ha_slash = app_commands.Group(name="homeassistant", description="Home Assistant commands")
    
    
    @app_commands.checks.has_permissions(administrator=True)
    @ha_slash.command(name="auth")
    async def auth(self, interaction: discord.Interaction, url: str, token: str):
        """Authenticate with Home Assistant and save the configuration."""
        
        api = HomeAssistantAPI(url, token)
        success = api.authenticate()
        
        if success:
            await self.config.guild(interaction.guild).url.set(url)
            await self.config.guild(interaction.guild).token.set(token)
            await interaction.response.send_message("Authentication successful. Configuration saved.")
        else:
            await interaction.response.send_message("Authentication failed.")
            
    
    @ha_slash.command(name="unauth")
    async def unauth(self, interaction: discord.Interaction):
        """Unregister the user's Home Assistant configuration."""
        
        await self.config.guild(interaction.guild).clear()
        await interaction.response.send_message("Configuration cleared.")
        
    @commands.admin()
    @commands.command(name="changestate")
    async def change_state(self, ctx: commands.Context, entity_id: str, state: Literal["on", "off"]):
        """Change the state of an entity."""
        
        url = await self.config.guild(ctx.guild).url()
        token = await self.config.guild(ctx.guild).token()
        
        if not url or not token:
            await ctx.send("You need to authenticate first using /homeassistant auth.")
            return
        
        api = HomeAssistantAPI(url, token)
        
        try:
            api.change_state(entity_id, state)
            if state == "on":
                await ctx.send(f"Turned on.")   
            else:
                await ctx.send(f"Turned off.")

        except Exception as e:
            await ctx.send(f"Failed to change state for {entity_id}: {str(e)}")
