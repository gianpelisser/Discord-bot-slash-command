# import asyncio
# from typing import Optional
import discord
# from discord import app_commands
from discord.ext import commands
# import aiohttp
import os
import config

TOKEN = open("bot_token.txt", "r").read()  # Get the Token in the txt file (Notepad)
guild_id = config.guild_id


class Aclient(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=config.client_prefix,
                         intents=intents,
                         help_command=None)
        self.synced = False  # we use this so the bot doesn't sync commands more than once
        # Start empty Cogs
        self.initial_extensions = []
        # Folder name with extensions (Cogs)
        cogs_path_name = "cogs"
        # Get all files in the Cogs folder
        folders = [filename for filename in os.listdir(cogs_path_name)]
        # Find and loads all Cogs in the extension. Variable-list: initial-extensions
        i = 0
        for item in folders:
            if not item.startswith("__"):
                if folders[i].endswith('.py'):
                    current_file_name = folders[i]
                    cog = f'cogs.{current_file_name[:-3]}'
                    self.initial_extensions.append(cog)
                    print(f"Cog found: {cog}")
            i += 1

    async def setup_hook(self) -> None:
        try:
            for extension in self.initial_extensions:
                await self.load_extension(extension)
                print(f'Cog Loaded: {extension}')
            if not self.synced:
                try:
                    synced_count = await self.tree.sync()
                    # synced_count = await self.tree.sync(guild=discord.Object(id=guild_id))  # for specific guild
                    print(f"[ {len(synced_count)} ] synchronized command(s).")
                except Exception as e:
                    print(f"Error syncing command(s): {e}")
                self.synced = True
        except Exception as e:
            print(e)

    async def on_command_error(self, ctx, error):
        await ctx.reply(error, ephemeral=True)

    async def on_ready(self):
        await self.wait_until_ready()

        # print('-=-' * 24)
        print('-=-' * 10, '[ Vortex ]', '-=-' * 10)
        # print("Bot esta Online e Pronto!")
        print(f"BOT: {self.user.name} | Online - Ping: {int(self.latency * 100)}")
        print(f"ID: {self.user.id}")
        print('-=-' * 8, f'[ {self.user.name} ]', '-=-' * 8)
        print()  # Prints a blank space.


bot = Aclient()


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return


@bot.hybrid_command(name="ping", with_app_command=True, description='Ping')
# @app_commands.guilds(discord.Object(id=guild_id))
@commands.has_permissions(administrator=True)
async def cmd_ping(ctx: commands.Context):
    await ctx.defer(ephemeral=True)
    await ctx.reply(f"_Pong_\n"
                    f"\n**Ping:** {int(bot.latency*100)}")


if __name__ == "__main__":
    bot.run(TOKEN)
