from .manager import UserClientManager
from ...utils.events import EventPusher


class UserClient(EventPusher):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.manager = UserClientManager(loop=self.loop)

    async def start(self, *args, **kwargs) -> None:
        await self.manager.start(*args, **kwargs)
