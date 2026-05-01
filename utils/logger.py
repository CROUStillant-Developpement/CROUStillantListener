import logging


class Logger:
    """
    Wrapper autour de :class:`logging.Logger` avec un formatage horodaté standardisé.

    Chaque instance est associée à un nom de fichier/module qui apparaît dans le
    préfixe des messages (``CROUStillant - <file>``). Un handler console est
    automatiquement ajouté à l'initialisation.
    """

    def __init__(self, file: str) -> None:
        """
        Initialise le logger et attache un handler console.

        :param file: Nom du module ou fichier source, intégré dans le nom du logger.
        :type file: str
        """
        self.file = file

        self.logger = logging.getLogger(f"CROUStillant - {self.file}")
        self.logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler()
        dt_fmt = '%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        self.logger.info("Logger initialisé !")


    def info(self, message: str) -> None:
        """
        Enregistre un message au niveau ``INFO``.

        :param message: Contenu du message à enregistrer.
        :type message: str
        """
        self.logger.info(message)


    def warning(self, message: str) -> None:
        """
        Enregistre un message au niveau ``WARNING``.

        :param message: Contenu du message à enregistrer.
        :type message: str
        """
        self.logger.warning(message)


    def error(self, message: str) -> None:
        """
        Enregistre un message au niveau ``ERROR``.

        :param message: Contenu du message à enregistrer.
        :type message: str
        """
        self.logger.error(message)


    def critical(self, message: str) -> None:
        """
        Enregistre un message au niveau ``CRITICAL``.

        :param message: Contenu du message à enregistrer.
        :type message: str
        """
        self.logger.critical(message)


    def debug(self, message: str) -> None:
        """
        Enregistre un message au niveau ``DEBUG``.

        :param message: Contenu du message à enregistrer.
        :type message: str
        """
        self.logger.debug(message)
