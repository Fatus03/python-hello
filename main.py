import discord
from discord import app_commands
from discord.ext import commands
import io
import contextlib
import os

# ⚙️ Cấu hình
OWNER_ID = 1285549494888300555  # ID của bạn
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

# 👋 /hello
@bot.tree.command(name="hello", description="Chào người dùng")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Xin chào {interaction.user.mention}! Tôi đang chạy bằng Railway 🤖")

# ⚡ /run — chạy code Python
@bot.tree.command(name="run", description="Chạy code Python (chỉ chủ bot được phép dùng)")
async def run(interaction: discord.Interaction, code: str):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("⛔ Bạn không có quyền dùng lệnh này.", ephemeral=True)
        return

    # Giữ output của code
    output_buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(output_buffer):
            exec(code, {})
    except Exception as e:
        await interaction.response.send_message(f"❌ Lỗi: `{e}`")
        return

    output = output_buffer.getvalue()
    if output.strip() == "":
        output = "✅ Code đã chạy nhưng không có output."
    await interaction.response.send_message(f"```py\n{output}\n```")

# 🧮 /eval — chạy biểu thức Python và trả kết quả
@bot.tree.command(name="eval", description="Tính toán biểu thức Python nhanh")
async def eval_expr(interaction: discord.Interaction, expression: str):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("⛔ Bạn không có quyền dùng lệnh này.", ephemeral=True)
        return

    try:
        result = eval(expression)
        await interaction.response.send_message(f"✅ Kết quả: `{result}`")
    except Exception as e:
        await interaction.response.send_message(f"❌ Lỗi: `{e}`")

# 🚀 Chạy bot
bot.run(os.getenv("DISCORD_TOKEN"))
