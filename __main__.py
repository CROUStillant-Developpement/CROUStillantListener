import asyncio
import asyncpg

from utils.logger import Logger
from utils.views import NewRestaurantView, RestaurantStateChangeView
from discord import Webhook
from os import environ
from aiohttp import ClientSession
from dotenv import load_dotenv
from json import loads
from datetime import datetime
from pytz import timezone


load_dotenv(dotenv_path=".env")


class Listener:
    """
    Écoute les notifications PostgreSQL et les publie sur Discord via un webhook.

    Utilise ``asyncpg`` pour s'abonner aux canaux ``insert`` et ``actif_change``
    de la base de données, puis envoie un message Discord formaté pour chaque
    événement reçu.
    """

    def __init__(self) -> None:
        """
        Initialise le listener sans établir de connexion.

        La session HTTP et le webhook Discord sont créés à la demande lors du
        premier appel à :meth:`createWebhook`.
        """
        self.session: ClientSession | None = None
        self.webhook: Webhook | None = None

        self.logger = Logger("listener")


    def createWebhook(self) -> None:
        """
        Initialise la session HTTP ``aiohttp`` et le webhook Discord.

        Si une session existe déjà elle est réutilisée ; sinon une nouvelle
        :class:`aiohttp.ClientSession` est créée. Le webhook est construit à
        partir de la variable d'environnement ``DISCORD_WEBHOOK``.
        """
        if not self.session:
            self.session = ClientSession()

        self.webhook = Webhook.from_url(environ["DISCORD_WEBHOOK"], session=self.session)


    async def postNewRestaurants(self, connection: asyncpg.Connection, _pid: int, channel: str, data: str) -> None:
        """
        Callback déclenché lors d'une notification sur le canal ``insert``.

        Désérialise la charge utile JSON, construit un embed Discord via
        :class:`~utils.views.NewRestaurantView` et l'envoie sur le webhook.

        :param connection: Connexion PostgreSQL active transmise par ``asyncpg``.
        :type connection: asyncpg.Connection
        :param _pid: Identifiant du processus PostgreSQL émetteur de la notification (non utilisé).
        :type _pid: int
        :param channel: Nom du canal de notification (``insert``).
        :type channel: str
        :param data: Charge utile JSON de la notification contenant les colonnes du restaurant.
        :type data: str
        """
        self.logger.info(f"Notification reçue: [{channel}] {data}")

        data = loads(data)

        if not self.webhook:
            self.createWebhook()

        if data.get("horaires", None):
            horaires = loads(data.get("horaires"))
        else:
            horaires = []

        horaires_str = f"\n- Horaires : `{' '.join(horaires)}`" if horaires else ""

        year = datetime.now(tz=timezone('Europe/Paris')).year

        view = NewRestaurantView(
            content=f"## Nouveau restaurant détecté !\n\n**{data.get('nom')}**\n\n- Adresse : `{data.get('adresse', '') if data.get('adresse') else '-'}`\n- Téléphone : `{data.get('telephone') if data.get('telephone') else '-'}`\n- Email : `{data.get('email') if data.get('email') else '-'}`{horaires_str}\n- Zone : `{data.get('zone', '')}`\n- Latitude : `{data.get('latitude', '')}`\n- Longitude : `{data.get('longitude', '')}`\n- Ouvert : `{'Oui' if data.get('ouvert', False) else 'Non'}`",
            image_url=data.get("image_url", None),
            footer_text=f"CROUStillant Développement © 2022 - {year} | Tous droits réservés.",
            rid=data.get('rid')
        )

        await self.webhook.send(view=view)


    async def postRestaurantStateChange(self, connection: asyncpg.Connection, _pid: int, channel: str, data: str) -> None:
        """
        Callback déclenché lors d'une notification sur le canal ``actif_change``.

        Désérialise la charge utile JSON, construit un embed Discord via
        :class:`~utils.views.RestaurantStateChangeView` et l'envoie sur le webhook.

        :param connection: Connexion PostgreSQL active transmise par ``asyncpg``.
        :type connection: asyncpg.Connection
        :param _pid: Identifiant du processus PostgreSQL émetteur de la notification (non utilisé).
        :type _pid: int
        :param channel: Nom du canal de notification (``actif_change``).
        :type channel: str
        :param data: Charge utile JSON de la notification contenant les colonnes du restaurant.
        :type data: str
        """
        self.logger.info(f"Notification reçue: [{channel}] {data}")

        data = loads(data)

        if not self.webhook:
            self.createWebhook()

        is_active = data.get('actif', False)
        state_text = "actif" if is_active else "inactif"

        year = datetime.now(tz=timezone('Europe/Paris')).year

        view = RestaurantStateChangeView(
            content=f"## Restaurant {'activé' if is_active else 'désactivé'} !\n\n**{data.get('nom')}**\n\n- Adresse : `{data.get('adresse', '') if data.get('adresse') else '-'}`\n- Zone : `{data.get('zone', '')}`\n- État : `{state_text}`",
            image_url=data.get("image_url", None),
            footer_text=f"CROUStillant Développement © 2022 - {year} | Tous droits réservés.",
            rid=data.get('rid')
        )

        await self.webhook.send(view=view)


    async def run(self) -> None:
        """
        Établit la connexion PostgreSQL et démarre la boucle d'écoute.

        Se connecte à la base de données à partir des variables d'environnement
        ``POSTGRES_DATABASE``, ``POSTGRES_USER``, ``POSTGRES_PASSWORD``,
        ``POSTGRES_HOST`` et ``POSTGRES_PORT``, puis enregistre les callbacks
        :meth:`postNewRestaurants` et :meth:`postRestaurantStateChange` sur leurs
        canaux respectifs. La boucle tourne indéfiniment jusqu'à interruption.

        :raises asyncpg.PostgresConnectionError: Si la connexion à la base échoue.
        """
        self.logger.info("Connection en cours...")

        conn = await asyncpg.connect(
            database=environ["POSTGRES_DATABASE"],
            user=environ["POSTGRES_USER"],
            password=environ["POSTGRES_PASSWORD"],
            host=environ["POSTGRES_HOST"],
            port=environ["POSTGRES_PORT"]
        )
        await conn.add_listener('insert', self.postNewRestaurants)
        await conn.add_listener('actif_change', self.postRestaurantStateChange)

        self.logger.info("Écoute des notifications...")

        while True:
            await asyncio.sleep(1)


if __name__ == "__main__":
    listener = Listener()
    asyncio.run(listener.run())
