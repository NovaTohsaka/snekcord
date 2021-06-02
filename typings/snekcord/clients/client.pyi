from typing import Any, Iterator

from ..manager import Manager
from ..objects.baseobject import BaseObject
from ..states.basestate import BaseState
from ..states.channelstate import ChannelState
from ..states.guildstate import GuildState


class Client:
    manager: Manager

    def __init__(self, token: str, **kwargs) -> None: ...
    @property
    def rest(self) -> Any: ...
    @property
    def channels(self) -> ChannelState: ...
    @property
    def guilds(self) -> GuildState: ...
    @property
    def invites(self) -> BaseState: ...
    @property
    def stages(self) -> BaseState: ...
    @property
    def members(self) -> Iterator[BaseObject]: ...
    @property
    def messages(self) -> Iterator[BaseObject]: ...
    @property
    def roles(self) -> Iterator[BaseObject]: ...
    @property
    def emojis(self) -> Iterator[BaseObject]: ...
