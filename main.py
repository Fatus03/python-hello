import discord
from discord import app_commands
from discord.ext import commands
import os

# 🧠 Khởi tạo bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="|", intents=intents)

# 🟢 Khi bot khởi động
@bot.event
async def on_ready():
    print(f"✅ Đã đăng nhập thành công dưới tên: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Đã đồng bộ {len(synced)} lệnh slash command(s).")
    except Exception as e:
        print(f"❌ Lỗi đồng bộ lệnh: {e}")

# 👋 Lệnh chào /hello
@bot.tree.command(name="hello", description="Chào người dùng")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Xin chào! Tôi đang chạy bằng Railway 🤖")

# 🧩 Lệnh chạy code /run
@bot.tree.command(name="run", description="Chạy code Python trực tiếp trên Discord")
async def run(interaction: discord.Interaction, code: str):
    try:
        # Tạo môi trường an toàn để chạy code
        local_vars = {}
        exec(f"result = {code}", {}, local_vars)
        result = local_vars["result"]
        await interaction.response.send_message(f"✅ Kết quả: `{result}`")
    except Exception as e:
        await interaction.response.send_message(f"❌ Lỗi: `{e}`")

# 🚀 Chạy bot
bot.run(os.getenv("DISCORD_TOKEN"))
