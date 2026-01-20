import os
import discord
from discord.ext import commands

# Lấy token bot từ biến môi trường Railway
TOKEN = os.getenv("TOKEN")

# Tạo intents (bật message_content để bot đọc tin nhắn)
intents = discord.Intents.default()
intents.message_content = True

# Tạo bot với prefix "!"
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập với tên: {bot.user}")

@bot.command()
async def hello(ctx):
    await ctx.send("Xin chào! Tôi đang chạy trên Railway 🚄")

# Chạy bot
bot.run(TOKEN)
