import os
import discord
from discord import app_commands
from discord.ext import commands

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot đã đăng nhập với tên: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Đã sync {len(synced)} slash command(s).")
    except Exception as e:
        print(f"Lỗi sync lệnh: {e}")

# Slash command
@bot.tree.command(name="hello", description="Chào bot 👋")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Xin chào! Tôi đang chạy bằng Railway 🚄")

bot.run(TOKEN)
