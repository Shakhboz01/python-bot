from typing import Callable, Dict, Awaitable, Any
from aiogram.types import TelegramObject, Update
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from database import get_user

class AdminCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user = getattr(event, "from_user", None)
        if user:
            user_id = user.id
            db_user = await get_user(user_id)
            if not db_user or not db_user["is_admin"]:
                await event.answer("🚫 You do not have permission to access this feature.")
                return
        return await handler(event, data)