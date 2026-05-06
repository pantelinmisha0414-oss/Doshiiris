import discord
import os
from discord.ext import commands


# Токен берём из Render переменной окружения
TOKEN = os.getenv("DISCORD_TOKEN")

# Интенты (ВАЖНО для команд и модерации)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


# -----------------------
# БОТ ЗАПУСТИЛСЯ
# -----------------------
@bot.event
async def on_ready():
    print(f"Бот запущен как {bot.user}")


# -----------------------
# !ping
# -----------------------
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


# -----------------------
# !whoami (КТО Я)
# -----------------------
@bot.command()
async def whoami(ctx):
    user = ctx.author

    embed = discord.Embed(
        title="Информация о тебе 😄",
        color=0x00ffcc
    )

    embed.add_field(name="Имя", value=user.name, inline=False)
    embed.add_field(name="ID", value=user.id, inline=False)
    embed.add_field(
        name="Дата создания аккаунта",
        value=user.created_at.strftime("%Y-%m-%d"),
        inline=False
    )

    await ctx.send(embed=embed)


# -----------------------
# !ban (бан)
# -----------------------
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"⛔ {member} забанен. Причина: {reason}")


# -----------------------
# !mute (таймаут)
# -----------------------
@bot.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, minutes: int):
    duration = discord.utils.utcnow() + discord.timedelta(minutes=minutes)
    await member.edit(timed_out_until=duration)
    await ctx.send(f"🔇 {member} замьючен на {minutes} минут")


# -----------------------
# !unmute
# -----------------------
@bot.command()
@commands.has_permissions(moderate_members=True)
async def unmute(ctx, member: discord.Member):
    await member.edit(timed_out_until=None)
    await ctx.send(f"🔊 {member} размьючен")

@bot.command()
async def helpme(ctx):
    embed = discord.Embed(
        title="📜 Список команд бота",
        color=0x00ffcc
    )

    embed.add_field(name="!ping", value="Проверка бота", inline=False)
    embed.add_field(name="!whoami", value="Информация о тебе", inline=False)
    embed.add_field(name="!ban @user причина", value="Забанить пользователя", inline=False)
    embed.add_field(name="!mute @user минуты", value="Замьютить пользователя", inline=False)
    embed.add_field(name="!unmute @user", value="Размьютить пользователя", inline=False)

    await ctx.send(embed=embed)


# -----------------------
# ОБЯЗАТЕЛЬНО ДЛЯ КОМАНД
# -----------------------
bot.run(TOKEN)
