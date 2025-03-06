import discord
from discord.ext import commands
import asyncio
import time

INVITE_LINK = "https://discord.gg/95cppXTqa3" # JOIN MY DISCORD SERVER (YOU CAN CHANGE THE INVITE LINK ONLY IS A REMINDER AFTER SPAM (ONLY U CAN SEE THE REMINDER))

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        self.command_cooldowns = {} 

    async def setup_hook(self):
        try:
            await self.tree.sync()
            print("Commands synced successfully.")
        except Exception as e:
            print(f"Error syncing commands: {e}")

bot = MyBot()

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")
    await bot.setup_hook()

@bot.tree.command(name="spamcustom", description="Sends your custom message wherever you want")
async def spamcustom(interaction: discord.Interaction, text: str):

    try:
        user_id = interaction.user.id
        cooldown_time = 4 # YOUR CUSTOM COLDOWN

        last_used = bot.command_cooldowns.get(user_id, 0)
        time_since_last_use = time.time() - last_used

        if time_since_last_use < cooldown_time:
            remaining_time = cooldown_time - time_since_last_use

            embed = discord.Embed(
                title="⏳ Cooldown Active",
                description=f"Please wait **{remaining_time:.1f} seconds** before using this command again.",
                color=discord.Color.from_rgb(255, 0, 0) 
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        bot.command_cooldowns[user_id] = time.time()

        embed = discord.Embed(
            title="Join Our Discord!",
            description=f"Don't forget to join our community: [Click here to join]({INVITE_LINK})",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

        # Spam message settings
        num_responses = 10
        interval_ms = 150
        interval = interval_ms / 1000.0

        for _ in range(num_responses):
            await asyncio.sleep(interval)
            await interaction.followup.send(text, ephemeral=False)

    except discord.Forbidden:
        print("The bot lacks permissions to send messages.")
    except discord.HTTPException as e:
        print(f"HTTP error occurred")
    except Exception as e:
        print(f"Unexpected error")

bot.run("YOUR BOT TOKEN")
