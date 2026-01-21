import os
import discord
from discord.ext import commands
from discord import app_commands

# ---- Cấu hình intents ----
intents = discord.Intents.default()
intents.message_content = True  # Cho phép đọc nội dung tin nhắn

# ---- Tạo bot ----
bot = commands.Bot(command_prefix="!", intents=intents)

# ---- Sự kiện khởi động ----
@bot.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập với tên: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔁 Đã đồng bộ {len(synced)} slash command(s).")
    except Exception as e:
        print(f"❌ Lỗi sync: {e}")

# ---- Slash command ví dụ ----
@bot.tree.command(name="hello", description="Kiểm tra bot hoạt động")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Xin chào! Tôi đang chạy bằng Railway 🚄", ephemeral=True)

# ---- Chạy bot ----
if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")

    if token:
        try:
            bot.run(token)
        except Exception as e:
            print(f"❌ Lỗi khi khởi động bot: {e}")
    else:
        print("⚠️ Không tìm thấy biến môi trường DISCORD_TOKEN. Hãy thêm nó trong Railway → Variables.")
