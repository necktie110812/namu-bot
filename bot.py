import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# 🎯 자동 스레드 생성 채널 3개
# =========================
CHANNEL_SETTINGS = {
    1474235445083635815: {  # 채널 1
        "thread_name": "{author}의 질문",
        "message": "위 질문은 이 스레드에 답변해주세요."
    },
    1436612356451991584: {  # 채널 2
        "thread_name": "{author}의 팀 채팅",
        "message": "팀 채팅은 이 스레드에서 해주세요."
    },
    1436609131594256436: {  # 채널 3
        "thread_name": "{author}의 클립 댓글",
        "message": "위 클립의 댓글은 여기서 작성해주세요."
    }
}

# =========================
# 👍 반응 자동 추가 채널
# =========================
REACTION_CHANNELS = [
    1436609131594256436  # 👍 달릴 채널 ID
]

# =========================
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# =========================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # 1️⃣ 자동 스레드 생성
    if message.channel.id in CHANNEL_SETTINGS:
        settings = CHANNEL_SETTINGS[message.channel.id]

        try:
            thread = await message.create_thread(
                name=settings["thread_name"].format(author=message.author.name),
                auto_archive_duration=10080
            )

            await thread.send(settings["message"])

        except Exception as e:
            print("Thread error:", e)

    # 2️⃣ 👍 자동 반응
    if message.channel.id in REACTION_CHANNELS:
        try:
            await message.add_reaction("👍")
        except Exception as e:
            print("Reaction error:", e)

    await bot.process_commands(message)

bot.run(TOKEN)