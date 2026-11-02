# dev.py
"""Contains internal dev commands"""

import importlib
import re
import sys

import discord
from discord.commands import SlashCommandGroup, Option
from discord.ext import commands

import database
from resources import functions, settings, views


class DevCog(commands.Cog):
    """Cog with internal dev commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    dev = SlashCommandGroup(
        "dev",
        "Development commands",
        guild_ids=settings.DEV_GUILDS,
        default_member_permissions=discord.Permissions(administrator=True)
    )

    # Commands
    @dev.command()
    @commands.is_owner()
    async def cache(self, ctx: discord.ApplicationContext):
        """Shows cache size"""
        from cache import messages
        cache_size = sys.getsizeof(messages._MESSAGE_CACHE)
        channel_count = len(messages._MESSAGE_CACHE)
        message_count = 0
        for channel_messages in messages._MESSAGE_CACHE.values():
            message_count += len(channel_messages)
            cache_size += sys.getsizeof(channel_messages)
            for message in channel_messages:
                cache_size += sys.getsizeof(message)
        await ctx.respond(
            f'Cache size: {cache_size / 1024:,.2f} KB\n'
            f'Channel count: {channel_count:,}\n'
            f'Message count: {message_count:,}\n'
        )

    @dev.command()
    @commands.is_owner()
    async def reload(
        self,
        ctx: discord.ApplicationContext,
        modules: Option(str, 'Cogs or modules to reload'),
    ) -> None:
        """Reloads cogs or modules"""
        modules = modules.split(' ')
        actions = []
        for module in modules:
            name_found = False
            cog_name = f'cogs.{module}' if not 'cogs.' in module else module
            try:
                cog_status = self.bot.reload_extension(cog_name)
            except:
                cog_status = 'Error'
            if cog_status is None:
                actions.append(f'+ Extension \'{cog_name}\' reloaded.')
                name_found = True
            if not name_found:
                for module_name in sys.modules.copy():
                    if module == module_name:
                        module = sys.modules.get(module_name)
                        if module is not None:
                            importlib.reload(module)
                            actions.append(f'+ Module \'{module_name}\' reloaded.')
                            name_found = True
            if not name_found:
                actions.append(f'- No loaded cog or module with the name \'{module}\' found.')

        message = ''
        for action in actions:
            message = f'{message}\n{action}'
        await ctx.respond(f'```diff\n{message}\n```')

    @dev.command()
    @commands.is_owner()
    async def shutdown(self, ctx: discord.ApplicationContext):
        """Shuts down the bot"""
        view = views.ConfirmCancelView(ctx)
        interaction = await ctx.respond(f'**{ctx.author.name}**, are you **SURE**?', view=view)
        view.interaction = interaction
        await view.wait()
        if view.value is None:
            await functions.edit_interaction(interaction, content=f'**{ctx.author.name}**, you didn\'t answer in time.',
                                             view=None)
        elif view.value == 'confirm':
            await functions.edit_interaction(interaction, content='Shutting down.', view=None)
            await self.bot.close()
        else:
            await functions.edit_interaction(interaction, content='Shutdown aborted.', view=None)


    @dev.command(name='sync-commands')
    @commands.is_owner()
    async def sync_commands(self, ctx: discord.ApplicationContext) -> None:
        """Manually sync commands"""
        await ctx.defer()
        if settings.DEBUG_MODE:
            #await self.bot.sync_commands(commands=[], guild_ids=settings.DEV_GUILDS)
            await self.bot.sync_commands(guild_ids=settings.DEV_GUILDS, force=True)
        else:
            #await self.bot.sync_commands(commands=[], force=False)
            await self.bot.sync_commands(force=True)
        await ctx.respond('Done')

    @dev.command(name='test')
    @commands.is_owner()
    async def test_command(self, ctx: discord.ApplicationContext) -> None:
        """Manually sync commands"""
        test = functions.format_string(None)
        pass

    @dev.command()
    @commands.is_owner()
    async def add_code(
        self,
        ctx: discord.ApplicationContext,
        code: Option(str, 'Code to add'),
        content: Option(str, 'Content of the code'),
        temporary: Option(bool, 'Whether the code is temporary or permanent', default=True),
    ) -> None:
        """Adds a code to the database"""

        await database.insert_code(code, content, temporary)
        await ctx.respond('Done')

    @dev.command()
    @commands.is_owner()
    async def delete_code(
        self,
        ctx: discord.ApplicationContext,
        code: Option(str, 'Code to delete'),
    ) -> None:
        """Adds a code to the database"""

        await database.delete_code(code)
        await ctx.respond('Done')

    @dev.command(name='migrate-database')
    @commands.is_owner()
    async def dev_migrate_users(
        self,
        ctx: discord.ApplicationContext,
    ) -> None:
        """Migrates the users table to a new one with encrypted user ids"""

        def quotes(name: str) -> str:
            return '"' + name.replace('"', '""') + '"'
        
        await ctx.defer()

        database.ERG_DB.create_function("uid_hash", 1, lambda value: database.create_hash(value))
        db_create_users_sql = database.ERG_DB.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='users'").fetchone()[0]
        db_extras_users = [
            record[0] for record in database.ERG_DB.execute(
                "SELECT sql FROM sqlite_master WHERE tbl_name='users' "
                "AND type IN ('index','trigger') AND sql IS NOT NULL"
            )
        ]

        try:
            database.ERG_DB.execute("BEGIN")

            # Migrate table "users"
            new_sql_users = re.sub(r'^CREATE TABLE\s+\S+', 'CREATE TABLE users_new', db_create_users_sql, flags=re.IGNORECASE)
            new_sql_users, number_of_replacements = re.subn(r'\buser_id\b\s+INTEGER\b', 'user_id_hash TEXT',
                                                            new_sql_users, flags=re.IGNORECASE)
            if number_of_replacements != 1:
                raise Exception("Column user_id not found in table 'users', check db_create_users_sql")
            database.ERG_DB.execute(new_sql_users)

            insert_columns = "user_id_hash, tt, ascended, quick_trade_enabled"
            select_columns = "uid_hash(user_id), tt, ascended, quick_trade_enabled"
            database.ERG_DB.execute(f"INSERT INTO users_new ({insert_columns}) SELECT {select_columns} FROM users")

            users_count_old = database.ERG_DB.execute("SELECT COUNT(*) FROM users").fetchone()[0]
            users_count_new = database.ERG_DB.execute("SELECT COUNT(*) FROM users_new").fetchone()[0]
            if users_count_old != users_count_new:
                raise Exception(f"Row count mismatch: Found {users_count_old} old reminders, but only migrated {users_count_new} reminders.")

            database.ERG_DB.execute("DROP TABLE users")
            database.ERG_DB.execute("ALTER TABLE users_new RENAME TO users")

            for sql in db_extras_users:
                database.ERG_DB.execute(sql.replace('user_id', 'user_id_hash'))

            # Commit
            database.ERG_DB.execute("COMMIT")
            database.ERG_DB.execute("VACUUM")
            answer = f'Done.'
        except Exception as error:
            database.ERG_DB.execute("ROLLBACK")
            answer = f'Migration failed:\n```{str(error)}```'

        await ctx.respond(answer)


# Initialization
def setup(bot):
    bot.add_cog(DevCog(bot))