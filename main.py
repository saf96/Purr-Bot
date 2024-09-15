import discord
from discord.ext import tasks, commands
import random
from dotenv import load_dotenv
import os
from webserver import keep_alive

# Load environment variables from a .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Define the intents
intents = discord.Intents.default()
intents.members = True  # Enable Server Members Intent
intents.presences = True  # Enable Presence Intent
intents.message_content = True  # Enable Message Content Intent

# Initialize the bot with the defined intents
bot = commands.Bot(command_prefix='!', intents=intents)

# List of cat-themed self-care reminders
reminders = [
    "🐾 Drink some water, lovely hooman! Hydration is key to feeling good. 🐱",
    "🐾 Don't forget, you are loved and appreciated. Keep being wonderful! 🐱",
    "🐾 Have you checked your space for any stray cups or mugs? Let's keep it tidy! 🐱",
    "🐾 Take a deep breath, you're doing your best, and that's all that matters! 🐱",
    "🐾 Stretch out those paws, a good stretch can make you feel amazing! 🐱",
    "🐾 Remember, it's okay to take breaks. You deserve some rest. 🐱",
    "🐾 You're capable of more than you know! Keep going, I'm proud of you. 🐱",
    "🐾 Have you eaten recently? Make sure to have a snack if you're hungry! 🐱",
    "🐾 Look outside! A little sunshine or fresh air might brighten your day. 🐱",
    "🐾 It’s okay to ask for help if you need it. You don’t have to do everything alone. 🐱",
    "🐾 You’ve got this! Whatever you're working on, I'm cheering you on. 🐱",
    "🐾 Just a reminder: you’re doing amazing, no matter how small your progress feels. 🐱",
]

# Initialize the user ID for daily reminders
daily_reminder_user_id = None

# Function to send reminders every 4 hours
@tasks.loop(hours=4)
async def send_reminders():
    for guild in bot.guilds:
        channel = discord.utils.get(guild.text_channels, name="general")  # Change "general" to your preferred channel name
        if channel:
            reminder = random.choice(reminders)
            await channel.send(reminder)

@tasks.loop(hours=24)  # Run this task once a day
async def daily_water_reminder():
    if daily_reminder_user_id is None:
        return

    for guild in bot.guilds:
        member = guild.get_member(daily_reminder_user_id)
        if member:
            channel = discord.utils.get(guild.text_channels, name="general")  # Change "general" to your preferred channel name
            if channel:
                await channel.send(f"Hey {member.mention}, it's time to drink some water! 🐾💧")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    send_reminders.start()  # Start the reminder task
    daily_water_reminder.start()  # Start the daily water reminder task

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Ensure the message is in a guild (server)
    if message.guild is None:
        return

    # Process commands if any exist in the message
    await bot.process_commands(message)

@bot.command(name='selfcare')
async def selfcare(ctx):
    reminder = random.choice(reminders)
    await ctx.send(reminder)

@bot.command(name='hydrate')
async def hydrate(ctx):
    await ctx.send("🐾 Time to drink some water! Your body will thank you. 🐱")

@bot.command(name='stop')
async def stop(ctx):
    await ctx.send("🐾 I'll stop reminding you now. Take care, friend! 🐱")
    await bot.close()

@bot.command(name='setdailyreminder')
async def set_daily_reminder(ctx, user: discord.User):
    global daily_reminder_user_id
    daily_reminder_user_id = user.id
    await ctx.send(f"Daily water reminder set for {user.mention}. I'll remind them to drink water once a day! 🐱💧")

# keep bot alive
keep_alive()

# Run the bot with the token
bot.run(TOKEN)
