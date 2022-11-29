import discord
from discord import app_commands
from discord.ext import commands
import config


class Ping(commands.Cog):
    def __int__(self, bot: commands.Bot):
        self.bot = bot

    # On Message
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if not message.author.bot:
            mention = f'<@{config.client_id}>'
            if mention in message.content:
                member = message.author
                return await message.channel.send(f"{member.mention}\n"
                                                  f"Did you mention me?\n"
                                                  f"You can use slash commands. (/)\n"
                                                  f"\nFor old-fashioned commands.\n"
                                                  f"My prefix is **{config.client_prefix}**")  # Change prefix config.py
            # fim mention
            if '*command1' in message.content:
                return await message.channel.send(f"Comando personalizado.", delete_after=30)
    # fim on_message

    # comando de barra (Slash)
    @app_commands.command(name="fale", description="O que eu deveria dizer?")
    async def say_fale(self, interaction: discord.Interaction, mensagem_para_repetir: str):
        await interaction.response.send_message(f'{mensagem_para_repetir}', ephemeral=False)


async def setup(bot):
    await bot.add_cog(Ping(bot), guilds=[])
    # await bot.add_cog(Ping(bot))
