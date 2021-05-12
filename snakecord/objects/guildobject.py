from .baseobject import BaseObject
from .. import rest
from ..states.channelstate import GuildChannelState
from ..templates import GuildBanTemplate, GuildPreviewTemplate, GuildTemplate
from ..utils import Snowflake, _validate_keys


class Guild(BaseObject, template=GuildTemplate):
    __slots__ = ('channels',)

    def __init__(self, *, state):
        super().__init__(state=state)
        self.channels = GuildChannelState(
            superstate=self._state.manager.channels,
            guild=self)

    async def fetch_preview(self):
        return await self._state.fetch_preview(self.id)

    async def modify(self, **kwargs):
        keys = rest.modify_guild.keys

        _validate_keys(f'{self.__class__.__name__}.modify',
                       kwargs, (), keys)

        data = await rest.modify_guild.request(
            session=self._state.manager.rest,
            fmt=dict(guild_id=self.id),
            json=kwargs)

        return self.append(data)

    async def delete(self):
        await rest.delete_guild.request(
            session=self._state.manager.rest,
            fmt=dict(guild_id=self.id))

    async def fetch_prune_count(self, days=None, include_roles=None):
        params = {}

        if days is not None:
            params['days'] = int(days)

        if include_roles is not None:
            include_roles = {
                str(Snowflake.try_snowflake(r)) for r in include_roles
            }
            params['include_roles'] = ','.join(include_roles)

        data = await rest.get_guild_prune_count.request(
            session=self._state.manager.rest,
            fmt=dict(guild_id=self.id))

        return data['pruned']

    async def begin_prune(self, **kwargs):
        keys = rest.begin_guild_prune.json

        try:
            roles = {
                Snowflake.try_snowflake(r) for r in kwargs['roles']
            }
            kwargs['roles'] = list(roles)
        except KeyError:
            pass

        _validate_keys(f'{self.__class__.__name__}.begin_prune',
                       kwargs, (), keys)

        data = await rest.begin_guild_prune.request(
            session=self._state.manager.rest,
            fmt=dict(guild_id=self.id),
            json=kwargs)

        return data['pruned']

    async def fetch_voice_regions(self):
        data = await rest.get_guild_voice_regions.request(
            session=self._state.manager.rest,
            fmt=dict(guild_id=self.id))

        return data

    async def fetch_vanity_url(self):
        # XXX: self.vanity_url = GuildVanityUrl(...);
        # await self.vanity_url.fetch()?
        pass

    def to_preview_dict(self):
        return GuildPreviewTemplate.to_dict(self)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

        channels = getattr(self, '_channels', None)
        if channels is not None:
            for channel in channels:
                channel = self._state.manager.channels.append(channel)
                self.channels.add_key(channel.id)

            del self._channels


class GuildBan(BaseObject, template=GuildBanTemplate):
    __slots__ = ('guild', 'user')

    def __init__(self, *, state, guild):
        super().__init__(state)
        self.guild = guild

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

        user = getattr(self, '_user', None)
        if user is not None:
            self.user = self._state.manager.users.append(user)
            self.id = self.user.id
            del self._user
