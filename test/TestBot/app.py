from aiogram import executor
from handlers import dp
from typing import Optional
import aiohttp

class AsyncSession:
    def __init__(self) -> None:
        self._session: Optional[aiohttp.ClientSession] = None
    async def get_session(self) -> aiohttp.ClientSession:
        if self._session is None:
            new_session = aiohttp.ClientSession()
            self._session = new_session
        return self._session
    async def close(self) -> None:
        if self._session is None:
            return None
        await self._session.close()

async def on_startup(dp):
    aSession = AsyncSession()
    dp.bot['aSession'] = aSession

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)