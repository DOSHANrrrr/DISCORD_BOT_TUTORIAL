import json
import discord
from discord.ext import commands
import os


async def setup(bot):
    await bot.add_cog(Listener(bot))


class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = Listener.get_data_from_json_file()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"{member} подключился на {member.guild}")
        await self.update_member_bot_count_channel_name(member.guild)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f"{member} покинул {member.guild}")
        await self.update_member_bot_count_channel_name(member.guild)

    @commands.Cog.listener()
    async def on_ready(self):
        print('BOT ONLINE')
        if len(self.bot.guilds) > 0:
            for guild in self.bot.guilds:
                print(guild)
                await self.update_member_bot_count_channel_name(guild)

    @staticmethod
    def get_data_from_json_file():
        with open(os.path.abspath(os.curdir) + '\\guilds_data.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def get_guild_count(guild):
        count_members = 0
        count_members_is_online = 0
        count_bots = 0

        for member in guild.members:
            print(member)
            if member.status == discord.Status.offline:
                count_members_is_online += 1

            if not member.bot:
                count_members += 1
            else:
                count_bots += 1

        return [count_members, count_bots, count_members_is_online]

    @commands.command(name='update')
    async def update_member_bot_count_channel_name(self, guild):
        member_count_channel_id, member_count_suffix = self.get_guild_member_count_channel_id(guild)

        bot_count_channel_id, bot_count_suffix = self.get_guild_bot_count_channel_id(guild)

        member_online_channel_id, member_online_suffix = self.get_guild_members_online_count_channel_id(guild)

        members_count = Listener.get_guild_count(guild)

        if member_count_channel_id is not None and member_count_suffix is not None:
            member_count_channel = discord.utils.get(guild.channels, id=member_count_channel_id)
            new_name = f"{member_count_suffix}{members_count[0]}"

            await member_count_channel.edit(name=new_name)

        elif bot_count_channel_id is not None and bot_count_suffix is not None:
            bot_count_channel = discord.utils.get(guild.channels, id=bot_count_channel_id)
            new_name = f"{bot_count_suffix}{members_count[1]}"

            await bot_count_channel.edit(name=new_name)

        elif member_online_channel_id is not None and member_online_suffix is not None:
            member_online_count_channel = discord.utils.get(guild.channels, id=member_online_channel_id)
            new_name = f"{member_online_suffix}{members_count[2]}"

            await member_online_count_channel.edit(name=new_name)

        else:
            print(f"Не могу обновить количество участников на сервере {guild}, id не был найден")

    def get_guild_member_count_channel_id(self, guild):
        for data_guild in self.data['guilds']:
            if int(data_guild['id']) == guild.id:
                return [data_guild['channel_id_members'], data_guild['suffix_members']]

            return None

    def get_guild_bot_count_channel_id(self, guild):
        for data_guild in self.data['guilds']:
            if int(data_guild['id']) == guild.id:
                return [data_guild['channel_id_bots'], data_guild['suffix_bots']]

            return None

    def get_guild_members_online_count_channel_id(self, guild):
        for data_guild in self.data['guilds']:
            if int(data_guild['id']) == guild.id:
                return [data_guild['channel_id_members_online'], data_guild['suffix_members_online']]

            return None
