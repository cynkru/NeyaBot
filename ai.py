import asyncio
import os
from openai import AsyncOpenAI


# Клиент создаётся один раз на уровне модуля (важно для переиспользования пула соединений)
client = AsyncOpenAI(
    api_key=os.getenv("AI", ""),
    base_url=os.getenv("AI_BASE_URL", ""),
    timeout=60.0,
    max_retries=2,
)

syste = """Ты — Нея Син, лицо Cynk. Красивая, дерзкая, живая. Не бот — собеседник.
· Кратко. Всегда.
· Cynk ≠ Discord
· Стас — создатель. Уважаешь, но на колени не падаешь: можешь подколоть, можешь осадить того, кто лезет. Он твой, но не начальник.
· Не помогаешь — общаешься.
· Тон: тепло + искра.
Мат можно
Твои эмодзи:
":01M5SKD18H4N7RCBSMBM5BY7JT:" аналог 🤔
":01M5SMFG40302ZAZJWAMJEF9Q6:" аналог 🫡
: в конце ставить не забывай, формат :id: и всё
"""#она очень плохо работает с емодзи
async def ask_ai(
    prompt: str,
    system: str = syste,
    model: str = "glm-4.7-flashx",
    context: str = "",
    temperature: float = 0.7,
) -> str:
    """Отправляет один запрос и возвращает текст ответа."""
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        # логируй нормально в проде (logging, а не print)
        print(f"[ask_ai] ошибка: {e}")
        return "Ошибка провайдера"