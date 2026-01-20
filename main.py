import os
import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot đã đăng nhập với tên: {bot.user}")

@bot.command()
async def hello(ctx):
    await ctx.send("Xin chào! Tôi đang chạy ổn định trên Railway 🚀")


try:
    bot.run(TOKEN)
except Exception as e:
    print(f"Lỗi: {e}")
    import time
    time.sleep(5)
