import discord
from discord import app_commands
from discord.ext import commands
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Đã đăng nhập thành công dưới tên: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔁 Đã đồng bộ {len(synced)} slash command(s).")
    except Exception as e:
        print(f"❌ Lỗi đồng bộ lệnh: {e}")

@bot.tree.command(name="hello", description="Chào người dùng")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Xin chào! Tôi đang chạy bằng Railway 🚆")

@bot.tree.command(name="run", description="Chạy code Python trực tiếp")
async def run(interaction: discord.Interaction, code: str):
    try:
        result = eval(code)
        await interaction.response.send_message(f"✅ Kết quả: `{result}`")
    except Exception as e:
        await interaction.response.send_message(f"⚠️ Lỗi: `{e}`")

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
