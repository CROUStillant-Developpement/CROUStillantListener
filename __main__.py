import asyncio
import asyncpg

from utils.logger import Logger
from discord import Embed, Webhook
from os import environ
from aiohttp import ClientSession
from dotenv import load_dotenv
from json import loads


load_dotenv(dotenv_path=".env")


class Listener:
    """
    Listener, détecte les nouveaux restaurants et les notifie sur Discord.
    """
    def __init__(self) -> None:
        self.session = None
        self.webhook = None

        self.logger = Logger("listener")


    def createWebhook(self):
        if not self.session:
            self.session = ClientSession()

        self.webhook = Webhook.from_url(environ["DISCORD_WEBHOOK"], session=self.session)


    async def postNewRestaurants(self, connection, pid, channel, data: str):
        self.logger.info(f"Notification reçue: [{channel}] {data}")

        data = loads(data)

        if not self.webhook:
            self.createWebhook()

        horaires = loads(data.get("horaires", "[]"))

        embed = Embed(
            title=f"{data.get('nom')}",
            description=f"""
- Adresse : `{data.get('adresse', '')}`
- Téléphone : `{data.get('telephone', '')}`
- Email : `{data.get('email', '')}`
- Horaires : `{' '.join(horaires)}`
- Zone : `{data.get('zone', '')}`
- Latitude : `{data.get('latitude', '')}`
- Longitude : `{data.get('longitude', '')}`
- Ouvert : `{'Oui' if data.get('ouvert', False) else 'Non'}`
            """,
            color=0x6A9056
        )
        embed.add_field(
            name="\u2060",
            value=f"*Retrouvez le ici : https://google.fr/maps/place/{data.get('latitude', '')},{data.get('longitude', '')}*",
            inline=False
        )
        embed.set_author(name="Nouveau restaurant détecté !")
        embed.set_footer(text="CROUStillant Développement © 2022 - 2024 | Tous droits réservés.", icon_url="https://github.com/CROUStillant-Developpement/CROUStillantAssets/raw/main/logo.png")
        embed.set_image(url=data.get("image_url", None))

        await self.webhook.send(embed=embed, username='CROUStillant', avatar_url="https://github.com/CROUStillant-Developpement/CROUStillantAssets/raw/main/logo.png")


    async def run(self):
        self.logger.info("Connection en cours...")

        conn = await asyncpg.connect(
            database=environ["POSTGRES_DATABASE"], 
            user=environ["POSTGRES_USER"], 
            password=environ["POSTGRES_PASSWORD"], 
            host=environ["POSTGRES_HOST"],
            port=environ["POSTGRES_PORT"]
        )
        await conn.add_listener('insert', self.postNewRestaurants)

        self.logger.info("Écoute des notifications...")

        while True:
            await asyncio.sleep(1)


if __name__ == "__main__":
    listener = Listener()
    asyncio.run(listener.run())
