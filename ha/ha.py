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
            "entities": {
                "satellite": ""
            }
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
            await interaction.response.send_message("Authentication successful. Configuration saved.", ephemeral=True)
            self.api = api
        else:
            await interaction.response.send_message("Authentication failed.", ephemeral=True)
            
    
    @ha_slash.command(name="reconnect")
    async def reconnect(self, interaction: discord.Interaction):
        url = await self.config.guild(interaction.guild).url()
        token = await self.config.guild(interaction.guild).token()
        
        if not url or not token:
            await interaction.response.send_message("You need to authenticate first using /homeassistant auth.", ephemeral=True)
            return
        
        api = HomeAssistantAPI(url, token)
        if not api.authenticate():
            await interaction.response.send_message("Please reauthenticate using /homeassistant auth", ephemeral=True)
        else:
            self.api = api
            await interaction.response.send_message("Successfully reconnected", ephemeral=True)
    
    
    @ha_slash.command(name="unauth")
    async def unauth(self, interaction: discord.Interaction):
        """Unregister the user's Home Assistant configuration."""
        
        await self.config.guild(interaction.guild).clear()
        await interaction.response.send_message("Configuration cleared.", ephemeral=True)
        

    @commands.command(name="service")
    async def call_service(self, ctx: commands.Context, domain: str, entity: str, service: str):
        """Call a service within a specific domain."""
        api = await api_instance(self, ctx)
        
        try:
            api.call_service(domain, entity, service)
            await ctx.tick()

        except Exception as e:
            await ctx.react_quietly("❌")
            

    @commands.group(name="light")
    async def light(self, ctx: commands.Context):
        """Light control commands."""
        pass
    
    @light.command(name="on")
    async def light_on(self, ctx: commands.Context, *entities: str):
        """Turn on one or more light entities."""
        api = await api_instance(self, ctx)
        try:
            api.light_on(entities)
            await ctx.tick()

        except Exception as e:
            await ctx.react_quietly("❌")
        
    
    @light.command(name="off")
    async def light_off(self, ctx: commands.Context, *entities: str):
        """Turn off one or more light entities."""
        api = await api_instance(self, ctx)
        
        try:
            api.light_off(entities)
            await ctx.tick()

        except Exception as e:
            await ctx.react_quietly("❌")
        
        
    @light.command(name="morse")
    async def light_morse(self, ctx: commands.Context, message: str, *entities: str):
        """Send a message in Morse code using the specified light entities."""
        # api = await api_instance(self, ctx)
        
        await self.api.light_morse(message, *entities)
                    
            
    @app_commands.checks.has_permissions(administrator=True)
    @ha_slash.command(name="set_satellite", description="Set the device ID for Home Assistant Satellite announcements.")
    async def set_satellite(self, interaction: discord.Interaction, device_id: str):
        """Set the device ID for Home Assistant Satellite announcements."""
        
        await self.config.guild(interaction.guild).entities.set_raw("satellite", value=device_id)
        await interaction.response.send_message(f"Satellite device ID set to `{device_id}`.", ephemeral=True)


    @commands.command(name="say")
    async def say(self, ctx: commands.Context, *, message: str):
        """Announce a message using a media player entity."""
        device_id = await self.config.guild(ctx.guild).entities.satellite()
        api = await api_instance(self, ctx)
        
        try:
            api.announce(message, device_id)
            await ctx.tick()

        except Exception as e:
            await ctx.react_quietly("❌")
            
            
async def api_instance(ha: HomeAssistant, ctx: commands.Context) -> HomeAssistantAPI:
    """Helper function to create an API instance with the current configuration."""
    url = await ha.config.guild(ctx.guild).url()
    token = await ha.config.guild(ctx.guild).token()
    
    if not url or not token:
        await ctx.send("You need to authenticate first using /homeassistant auth.")
        return
    
    return HomeAssistantAPI(url, token)
