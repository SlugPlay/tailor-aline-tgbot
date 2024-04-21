import asyncio
import sys

from typing import Callable, Any, Awaitable, Union
from aiogram import Bot, Dispatcher, types, fsm, filters, F, BaseMiddleware

from aiogram.types import FSInputFile, Message, InputMediaPhoto, InputMedia, ContentType, TelegramObject
from typing import Any, Dict, Union

from config import bot
from config import flag_request

class SomeMiddleware(BaseMiddleware):
    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.01):
        self.latency = latency

    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            message: Message,
            data: dict[str, Any]
    ) -> Any:
        flag_midleware = flag_request()

        if not flag_midleware:
            await handler(message, data)
            return
        if not message.media_group_id:
            try:
                self.album_data[0].append(message)
            except KeyError:
                self.album_data[0] = [message]
                await asyncio.sleep(self.latency)

                data['_is_last'] = True
                data["album"] = self.album_data[0]
                await handler(message, data)

            if not message.media_group_id and data.get("_is_last"):
                del self.album_data[0]
                del data['_is_last']
        else:
            try:
                self.album_data[message.media_group_id].append(message)
            except KeyError:
                self.album_data[message.media_group_id] = [message]
                await asyncio.sleep(self.latency)

                data['_is_last'] = True
                data["album"] = self.album_data[message.media_group_id]
                await handler(message, data)

            if message.media_group_id and data.get("_is_last"):
                del self.album_data[message.media_group_id]
                del data['_is_last']


class SlowpokeMiddleware(BaseMiddleware):
    def __init__(self, sleep_sec: int):
        self.sleep_sec = sleep_sec

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        # Ждём указанное количество секунд и передаём управление дальше по цепочке
        # (это может быть как хэндлер, так и следующая мидлварь)
        await asyncio.sleep(self.sleep_sec)
        result = await handler(event, data)
        # Если в хэндлере сделать return, то это значение попадёт в result
        print(f"Handler was delayed by {self.sleep_sec} seconds")
        return result
