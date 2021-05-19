from .baseobject import BaseObject, BaseTemplate
from .. import rest
from ..utils import (JsonArray, JsonField, JsonTemplate, Snowflake,
                     _validate_keys)
from ..utils import JsonArray, JsonField

import sys

module_path = sys.path.pop(0)
module = sys.modules.pop('snakecord')
# This will import the snakecord from site packages
# because that's where the emojis module is.
# This is only needed when snakecord.emojis and snakecord
# are not in the same module (during development).
# Will remove later

from snakecord.emojis import ALL_CATEGORIES

sys.path.insert(0, module_path)
sys.modules['snakecord'] = module

__all__ = ('GuildEmoji',)


GuildEmojiTemplate = JsonTemplate(
    name=JsonField('name'),
    role_ids=JsonArray('roles'),
    required_colons=JsonField('required_colons'),
    managed=JsonField('managed'),
    animated=JsonField('animated'),
    available=JsonField('available'),
    __extends__=(BaseTemplate,)
)


class GuildEmoji(BaseObject, template=GuildEmojiTemplate):
    __slots__ = ('guild', 'user')

    def __json_init__(self, *, state, guild):
        super().__json_init__(state=state)
        self.guild = guild
        self.user = None

    @property
    def roles(self):
        return [self.guild.roles.get(r) for r in self.role_ids]

    async def modify(self, **kwargs):
        keys = rest.modify_guild_emoji.json

        try:
            roles = Snowflake.try_snowflake_set(kwargs['roles'])
            kwargs['roles'] = tuple(roles)
        except KeyError:
            pass

        _validate_keys(f'{self.__class__.__name__}.modify',
                       kwargs, (), keys)

        data = await rest.modify_guild_emoji.request(
            session=self.state.manager.rest,
            fmt=dict(guild_id=self.guild.id, emoji_id=self.id),
            json=kwargs)

        self.update(data)

        return self

    async def delete(self):
        await rest.delete_guild_emoji.request(
            session=self.state.manager.rest,
            fmt=dict(guild_id=self.guild.id, emoji_id=self.id))

    def update(self, data, *args, **kwargs):
        super().update(data, *args, **kwargs)

        user = data.get('user')
        if user is not None:
            self.user = self.state.manager.users.append(user)


class BuiltinEmoji:
    def __init__(self, category, data):
        self.category = category

        self.surrogates = data[0]
        self.names = data[1]
        self.unicode_version = data[2]

        self.diversity_children = []
        for child in data[3]:
            self.diversity_children.append(
                BuiltinEmoji(category, child))

    def store(self, cache):
        cache[self.surrogates] = self

        for child in self.diversity_children:
            child.store(cache)


BUILTIN_EMOJIS = {}

for category, emojis in ALL_CATEGORIES.items():
    for data in emojis:
        emoji = BuiltinEmoji(category, data)
        emoji.store(BUILTIN_EMOJIS)
