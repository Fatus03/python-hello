import discord
from discord import app_commands
from discord.ext import commands
import os, time, io, contextlib, traceback

# ======== Cấu hình cơ bản ========
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="|", intents=intents)
OWNER_ID = 123456789012345678  # <--- Thay bằng ID Discord của bạn

# ======== Khi bot khởi động ========
@bot.event
async def on_ready():
    print(f"✅ Đăng nhập thành công: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Đồng bộ {len(synced)} slash command(s).")
    except Exception as e:
        print(f"❌ Lỗi đồng bộ lệnh: {e}")

# ======== /hello ========
@bot.tree.command(name="hello", description="Chào người dùng")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"👋 Xin chào {interaction.user.mention}! Tôi đang chạy bằng **Railway** 🚀",
        ephemeral=True
    )

# ======== /help ========
@bot.tree.command(name="help", description="Hiển thị hướng dẫn sử dụng bot")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📘 Hướng dẫn dùng PythonBot",
        color=0x3498db,
        description=(
            "**/hello** → Chào bot 🤖\n"
            "**/run code:** → Chạy code Python (1 dòng hoặc nhiều dòng)\n"
            "**/eval code:** → Chạy biểu thức Python ngắn\n\n"
            "⚠️ Chỉ admin mới được dùng `/run` và `/eval` để đảm bảo an toàn."
        )
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ======== /run ========
@bot.tree.command(name="run", description="Chạy code Python trực tiếp trên Discord")
async def run(interaction: discord.Interaction, code: str):
    if interaction.user.id != OWNER_ID:
        return await interaction.response.send_message("⛔ Bạn không có quyền dùng lệnh này.", ephemeral=True)

    # Chặn lệnh nguy hiểm
    banned = ["os.", "subprocess", "open(", "eval(", "exec(", "input("]
    if any(b in code for b in banned):
        return await interaction.response.send_message("⚠️ Code chứa lệnh nguy hiểm, không được phép.", ephemeral=True)

    start = time.perf_counter()
    result = io.StringIO()
    try:
        with contextlib.redirect_stdout(result):
            exec(code, {})
        output = result.getvalue() or "✅ Không có output"
    except Exception:
        output = "❌ Lỗi:\n" + traceback.format_exc()

    elapsed = time.perf_counter() - start
    if len(output) > 1900:
        output = output[:1900] + "\n...[đã cắt bớt]"

    embed = discord.Embed(
        title="📦 Kết quả chạy code",
        description=f"```py\n{output}\n```",
        color=0x2ecc71
    )
    embed.set_footer(text=f"⏱️ Thời gian: {elapsed:.3f}s")
    await interaction.response.send_message(embed=embed)

# ======== /eval ========
@bot.tree.command(name="eval", description="Chạy biểu thức Python ngắn (vd: 2 + 2)")
async def eval_command(interaction: discord.Interaction, expression: str):
    if interaction.user.id != OWNER_ID:
        return await interaction.response.send_message("⛔ Bạn không có quyền dùng lệnh này.", ephemeral=True)

    try:
        start = time.perf_counter()
        result = eval(expression)
        elapsed = time.perf_counter() - start
        embed = discord.Embed(
            title="🧮 Kết quả Eval",
            description=f"```py\n{result}\n```",
            color=0xf1c40f
        )
        embed.set_footer(text=f"⏱️ {elapsed:.4f}s")
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message(f"❌ Lỗi: `{e}`", ephemeral=True)

# ======== Chạy bot ========
bot.run(os.getenv("DISCORD_TOKEN"))
