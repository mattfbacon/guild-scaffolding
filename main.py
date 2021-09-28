import discord
import json
import asyncio

"""
Creates channels, categories, and roles automatically based on structured data.

For each category, a channel category will be created, a helper role will be created for the category, and a voice channel will be added to the category.

Then, for each item in the category, a channel and role will be created. This role, the helper role for the category, as well as every role in roles_to_add_to_all, will have view access to the channel. @everyone will not be able to view the channel.

Take care to make sure that you will not reach the role/channel limit. Your guild will look very weird if the bot fails halfway through due to such limits.
"""

token = # your bot token
guild_id = # the guild to operate on

roles_to_add_to_all = [
    # roles that will have access to all channels
]

data = None
"""
roles.json has this format:
[
  {
    "name": "the category name",
    "items": [ "each", "item", "in", "the", "category" ]
  }
]
"""
with open('roles.json', 'r') as f:
    data = json.load(f)


def title_to_kebab(string):
    return string.lower().replace(' ', '-')


async def set_chan_permissions(chan, default_role, channel_role, category_role,
                               universal_roles):
    await asyncio.gather(
        chan.set_permissions(default_role, view_channel=False),
        *([chan.set_permissions(channel_role, view_channel=True)]
          if not isinstance(channel_role, list) else [
              chan.set_permissions(role, view_channel=True)
              for role in channel_role
          ]), chan.set_permissions(category_role, view_channel=True), *[
              chan.set_permissions(universal_role, view_channel=True)
              for universal_role in universal_roles
          ])


async def make_topic_channel(guild, universal_roles, category, helper_role,
                             color, name):
    await asyncio.sleep(0.03)  # rate-limiting
    channel_role = await guild.create_role(name=f'{name} ({category.name})',
                                           colour=color,
                                           mentionable=False)
    await asyncio.sleep(0.03)  # rate-limiting
    chan = await guild.create_text_channel(title_to_kebab(name),
                                           category=category)
    await asyncio.sleep(0.03)  # rate-limiting
    await set_chan_permissions(chan, guild.default_role, channel_role,
                               helper_role, universal_roles)

    return channel_role


async def make_category_voice_channel(guild, universal_roles, category,
                                      category_role, channel_roles):
    await asyncio.sleep(0.03)  # rate-limiting
    chan = await guild.create_voice_channel(category.name + ' Voice',
                                            category=category)

    await asyncio.sleep(0.03)  # rate-limiting
    await set_chan_permissions(chan, guild.default_role, channel_roles,
                               category_role, universal_roles)

    return chan


async def make_topic_category(guild, universal_roles, category_data):
    category_color = discord.Colour.random()
    await asyncio.sleep(0.03)  # rate-limiting
    category, category_role = await asyncio.gather(
        guild.create_category_channel(category_data['name']),
        guild.create_role(name=category_data['name'] + ' Helper',
                          colour=category_color,
                          mentionable=False))
    await asyncio.sleep(0.03)  # rate-limiting
    topic_roles = list(await asyncio.gather(*[
        make_topic_channel(guild, universal_roles, category, category_role,
                           category_color, channel_name)
        for channel_name in category_data['items']
    ]))
    await asyncio.sleep(0.03)  # rate-limiting
    await make_category_voice_channel(guild, universal_roles, category,
                                      category_role, topic_roles)
    return category


async def do_the_thing(client):
    guild = client.get_guild(guild_id)
    universal_roles = [
        guild.get_role(role_id) for role_id in roles_to_add_to_all
    ]
    await asyncio.gather(*[
        make_topic_category(guild, universal_roles, category_data)
        for category_data in data
    ])


class MyClient(discord.Client):
    async def on_ready(self):
        print("logged in")
        await do_the_thing(self)


if __name__ == "__main__":
    client = MyClient(
        intents=discord.Intents(guilds=True, guild_messages=True))
    client.run(token)
