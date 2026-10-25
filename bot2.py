from stoat import Client, Message
import stoat
from ai import ask_ai
import asyncio
from stoat.ext.commands import Context

statuses = [
    "Я не бот",
    "Сижу, слежу за Стасом",
    "Отвечаю на умные сообщения"
]


class MyClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._status_task = None

    async def on_ready(self, _, /):
        print('Logged on as', self.me)
        await self.me.edit(status=stoat.UserStatusEdit(presence=stoat.Presence.focus))

        if self._status_task is None or self._status_task.done():
            self._status_task = asyncio.create_task(self.rotate_status())

    async def rotate_status(self):
        while True:
            for status in statuses:
                await self.me.edit(status=stoat.UserStatusEdit(text=status, presence=stoat.Presence.focus))
                await asyncio.sleep(10)
            await asyncio.sleep(10)

    async def on_message(self, message: Message, /):
        # 1. Игнорируем сообщения от самого бота
        if message.author_id == self.me.id:
            return

        repl = False
        last=""
        for i in message.replies:
            m = await message.channel.fetch_message(i)
            if m.author_id == self.me.id:
                repl = True
                last = m.content
        # 2. Проверяем, упомянут ли бот в сообщении
        if f'<@{self.me.id}>' in message.content or repl:
            # 3. Убираем упоминание из текста
            text = message.content.replace(f'<@{self.me.id}>', '').strip()

            if not text:
                text = "Привет"

            # 4. Получаем пользователя
            user = self.get_user(message.author_id)
            if user.bot:
                pass
            name = user.display_name or user.name if user else "Unknown"
            # 5. Показываем "печатает" и вызываем AI
            async with message.channel.typing():
                msg = await message.channel.send("Хмм :01M5SKD18H4N7RCBSMBM5BY7JT:")
                ans = await ask_ai(
                    f"Контекст: Имя: {name}. \n Сообщение: {text}",
                    context=last if last else ""
                )
                await msg.edit(content=ans)
            

client = MyClient(token='', http_base='https://api.cynk.space', websocket_base='wss://ws.cynk.space')
client.run()