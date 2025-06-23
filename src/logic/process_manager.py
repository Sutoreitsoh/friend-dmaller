import asyncio
import os
import time
import discord

class ProcessManager:
    def __init__(self, token_manager, message_manager):
        self.token_manager = token_manager
        self.message_manager = message_manager
        self.is_running = False

    def start_process(self):
        if self.is_running:
            self.log_action("Processus déjà en cours.")
            return

        self.is_running = True
        tokens = self.token_manager.read_tokens()
        if not tokens:
            self.log_action("Aucun token trouvé.")
            self.complete_process()
            return

        token = tokens[0]
        message = self.message_manager.read_messages()
        delay = float(os.getenv("DELAY_SECONDS", "2"))

        asyncio.run(self._run_discord(token, message, delay))

    async def _run_discord(self, token, message, delay):
        client = discord.Client(intents=discord.Intents.all(), self_bot=True)
        self.log_action("Connexion Discord...")

        @client.event
        async def on_ready():
            self.log_action(f"Connecté en tant que {client.user} ({client.user.id})")
            friends = [u for u in client.user.friends]
            self.log_action(f"Récupération de {len(friends)} amis.")
            success, failed = 0, 0
            for friend in friends:
                if not self.is_running:
                    break
                try:
                    await friend.send(message)
                    self.log_action(f"{friend} DM avec succès")
                    success += 1
                except Exception as e:
                    self.log_action(f"Erreur DM {friend}: {e}")
                    failed += 1
                await asyncio.sleep(delay)
            self.log_action(f"Friend Dmall terminé | {success} DM avec succès / {len(friends)} total / {failed} failed")
            await client.close()
            self.complete_process()

        try:
            await client.start(token, bot=False)
        except Exception as e:
            self.log_action(f"Erreur Discord: {e}")
            self.complete_process()

    def complete_process(self):
        self.is_running = False
        self.log_action("Process completed.")

    def halt_process(self):
        self.is_running = False
        self.log_action("Process halted by Panic Button.")

    def log_action(self, message):
        print(message)
        with open('logs/app.log', 'a', encoding='utf-8') as log_file:
            log_file.write(f"{message}\n")