import os
import io
import asyncio
import contextlib
import discord
from discord.ext import commands

# ===== Cấu hình cơ bản =====
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== Biến toàn cục =====
OWNER_ID = int(os.getenv("OWNER_ID", "0"))  # Thay bằng ID Discord của bạn
user_env = {}  # môi trường lưu biến tạm


# ===== Hàm chạy code Python =====
async def execute_python(code: str) -> str:
    """Chạy code Python trong môi trường an toàn, trả kết quả."""
    # Redirect output
    output_buffer = io.StringIO()
    with contextlib.redirect_stdout(output_buffer):
        try:
            # Hạn chế timeout 5 giây
            exec_namespace = user_env.copy()
            code = code.strip("` ")
            task = asyncio.create_task(run_code(code, exec_namespace))
            await asyncio.wait_for(task, timeout=5.0)
            user_env.update(exec_namespace)
        except asyncio.TimeoutError:
            return "⏱ Code chạy quá 5 giây và đã bị dừng."
        except Exception as e:
            return f"⚠️ Lỗi: {type(e).__name__}: {e}"
    return output_buffer.getvalue() or "✅ Code chạy xong."


async def run_code(code, env):
    """Thực thi code thật trong exec()"""
    exec(code, env)


# ===== Sự kiện khởi động =====
@bot.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập với tên: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Đã đồng bộ {len(synced)} lệnh slash command(s)")
    except Exception as e:
        print(f"Lỗi sync: {e}")


# ===== Lệnh kiểm tra bot =====
@bot.tree.command(name="hello", description="Kiểm tra bot hoạt động")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(
        "🤖 Xin chào! Tôi đang hoạt động như một Colab mini trên Discord!", ephemeral=True
    )


# ===== Lệnh chạy code Python =====
@bot.tree.command(name="run", description="Chạy code Python trực tiếp")
async def run(interaction: discord.Interaction, *, code: str):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ Bạn không có quyền chạy lệnh này.", ephemeral=True)
        return

    await interaction.response.defer(thinking=True)

    result = await execute_python(code)

    # Nếu kết quả quá dài, gửi file
    if len(result) > 1900:
        file = discord.File(io.BytesIO(result.encode()), filename="output.txt")
        await interaction.followup.send("📄 Output quá dài, xem file đính kèm:", file=file)
    else:
        await interaction.followup.send(f"```\n{result}\n```")


# ===== Lệnh reset môi trường =====
@bot.tree.command(name="reset", description="Xóa sạch biến môi trường code tạm thời")
async def reset_env(interaction: discord.Interaction):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ Bạn không có quyền.", ephemeral=True)
        return
    user_env.clear()
    await interaction.response.send_message("🧹 Đã xóa sạch môi trường code!", ephemeral=True)


# ===== Chạy bot =====
if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("⚠️ Không tìm thấy biến môi trường DISCORD_TOKEN trong Railway.")
