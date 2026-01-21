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
    print(f"✅ Bot đã đăng nhập với tên: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔄 Đã đồng bộ {len(synced)} slash command(s)")
    except Exception as e:
        print(f"⚠️ Lỗi sync: {e}")

# ---- Lệnh kiểm tra bot ----
@bot.tree.command(name="hello", description="Kiểm tra bot hoạt động")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Xin chào! Tôi đang chạy bằng Railway ", ephemeral=True)

# ---- Lệnh chạy code Python ----
@bot.tree.command(name="run", description="Chạy code Python trực tiếp trong Discord")
@app_commands.describe(code="Nhập đoạn code Python cần chạy")
async def run(interaction: discord.Interaction, code: str):
    await interaction.response.defer(ephemeral=True)
    str_obj = io.StringIO()

    try:
        with contextlib.redirect_stdout(str_obj):
            exec(code)
    except Exception as e:
        output = f"Lỗi: {e}"
    else:
        output = str_obj.getvalue()

    if not output.strip():
        output = "✅ Code chạy thành công (không có kết quả print)."
    
    # Giới hạn độ dài để tránh spam
    if len(output) > 1500:
        output = output[:1500] + "\n... (đã rút gọn kết quả)"
    
    await interaction.followup.send(f"📤 **Kết quả:**\n```\n{output}\n```", ephemeral=True)

# ---- Chạy bot ----
if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("⚠️ Không tìm thấy biến môi trường DISCORD_TOKEN. Hãy thêm nó trong Railway → Variables.")
