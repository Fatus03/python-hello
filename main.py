import discord
from discord import app_commands
from discord.ext import commands
import os

# 🧩 Khởi tạo bot với intents mặc định
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="|", intents=intents)

# 🟢 Khi bot khởi động
@bot.event
async def on_ready():
    print(f"✅ Đã đăng nhập thành công dưới tên: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Đã đồng bộ {len(synced)} slash command(s).")
    except Exception as e:
        print(f"❌ Lỗi đồng bộ lệnh: {e}")

# 👋 Lệnh chào /hello
@bot.tree.command(name="hello", description="Chào người dùng")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Xin chào! Tôi đang chạy bằng Railway 🤖")

# 💻 Lệnh chạy code /run
@bot.tree.command(name="run", description="Chạy code Python trực tiếp trên Discord")
async def run(interaction: discord.Interaction, code: str):
    try:
        local_vars = {}
        exec(code, {}, local_vars)  # chạy code
        result = local_vars.get("result", "✅ Đã chạy xong!")  # nếu có biến 'result' thì hiển thị
        await interaction.response.send_message(f"💡 Kết quả: `{result}`")
    except Exception as e:
        await interaction.response.send_message(f"❌ Lỗi: `{e}`")

# 🚀 Chạy bot bằng token từ biến môi trường
bot.run(os.getenv("DISCORD_TOKEN"))
