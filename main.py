import os
import discord
from discord.ext import commands
from discord import app_commands
import io
import contextlib

# ---- Cấu hình intents ----
intents = discord.Intents.default()
intents.message_content = True

# ---- Tạo bot ----
bot = commands.Bot(command_prefix="!", intents=intents)

# ---- Khi bot khởi động ----
@bot.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔗 Đã đồng bộ {len(synced)} slash command(s)")
    except Exception as e:
        print(f"⚠️ Lỗi sync: {e}")

# ---- Lệnh /hello kiểm tra bot ----
@bot.tree.command(name="hello", description="Kiểm tra bot hoạt động")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Xin chào! Tôi đang chạy bằng Railway 🚄", ephemeral=True)

# ---- Lệnh /run để chạy code Python ----
@bot.tree.command(name="run", description="Chạy code Python trực tiếp")
@app_commands.describe(code="Đoạn code Python bạn muốn chạy")
async def run(interaction: discord.Interaction, code: str):
    # Chặn code nguy hiểm
    blacklist = ["import os", "import sys", "open(", "exec(", "eval(", "subprocess", "shutil"]
    if any(x in code for x in blacklist):
        await interaction.response.send_message("⚠️ Đoạn code này có thể gây hại, mình không thể chạy!", ephemeral=True)
        return

    # Chạy code và bắt đầu kết quả
    with contextlib.redirect_stdout(io.StringIO()) as f:
        try:
            exec(code)
            output = f.getvalue()
        except Exception as e:
            output = f"Lỗi: {e}"

    if output.strip() == "":
        output = "✅ Đã chạy xong (không có kết quả in ra)."

    await interaction.response.send_message(f"**Kết quả:**\n```\n{output}\n```")

# ---- Chạy bot ----
if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("⚠️ Không tìm thấy DISCORD_TOKEN. Hãy thêm nó trong Railway → Variables.")
