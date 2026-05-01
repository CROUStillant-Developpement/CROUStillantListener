import discord


class ActionRow(discord.ui.ActionRow):
    """
    Ligne d'action contenant un bouton de lien vers la fiche du restaurant.

    Hérite de :class:`discord.ui.ActionRow` et ajoute automatiquement un bouton
    pointant vers ``https://croustillant.menu/fr/restaurants/{rid}``.
    """

    def __init__(self, rid: int) -> None:
        """
        Initialise la ligne d'action avec un bouton de lien.

        :param rid: Identifiant unique du restaurant (``RID``).
        :type rid: int
        """
        super().__init__()
        self.add_item(
            discord.ui.Button(
                label="Voir sur croustillant.menu",
                style=discord.ButtonStyle.link,
                url=f"https://croustillant.menu/fr/restaurants/{rid}",
            )
        )


class NewRestaurantView(discord.ui.LayoutView):
    """
    Vue Discord pour notifier l'ajout d'un nouveau restaurant.

    Construit un :class:`discord.ui.Container` composé d'une section textuelle,
    d'une galerie d'images (image du restaurant ou bannière par défaut),
    d'un bouton de lien et d'un pied de page.
    """

    def __init__(self, content: str, image_url: str | None, footer_text: str, rid: int) -> None:
        """
        Initialise la vue de nouveau restaurant.

        :param content: Texte Markdown principal affiché dans la section.
        :type content: str
        :param image_url: URL de l'image du restaurant. Si ``None`` ou vide,
            la bannière par défaut ``https://croustillant.menu/banner-small.png``
            est utilisée.
        :type image_url: str or None
        :param footer_text: Texte affiché en pied de page (mentions légales, année).
        :type footer_text: str
        :param rid: Identifiant unique du restaurant, transmis à :class:`ActionRow`.
        :type rid: int
        """
        super().__init__()
        items = [
            discord.ui.Section(
                content,
                accessory=discord.ui.Thumbnail(media="https://croustillant.menu/logo.png")
            ),
        ]

        if image_url:
            items.append(discord.ui.MediaGallery(discord.MediaGalleryItem(media=image_url)))
        else:
            items.append(discord.ui.MediaGallery(discord.MediaGalleryItem(media="https://croustillant.menu/banner-small.png")))

        items.append(ActionRow(rid=rid))
        items.append(discord.ui.TextDisplay(content=f"-# *{footer_text}*"))

        self.add_item(discord.ui.Container(*items))


class RestaurantStateChangeView(discord.ui.LayoutView):
    """
    Vue Discord pour notifier un changement d'état d'un restaurant (activation/désactivation).

    Construit un :class:`discord.ui.Container` composé d'une section textuelle,
    d'une galerie d'images (image du restaurant ou bannière par défaut),
    d'un bouton de lien et d'un pied de page.
    """

    def __init__(self, content: str, image_url: str | None, footer_text: str, rid: int) -> None:
        """
        Initialise la vue de changement d'état.

        :param content: Texte Markdown principal affiché dans la section.
        :type content: str
        :param image_url: URL de l'image du restaurant. Si ``None`` ou vide,
            la bannière par défaut ``https://croustillant.menu/banner-small.png``
            est utilisée.
        :type image_url: str or None
        :param footer_text: Texte affiché en pied de page (mentions légales, année).
        :type footer_text: str
        :param rid: Identifiant unique du restaurant, transmis à :class:`ActionRow`.
        :type rid: int
        """
        super().__init__()
        items = [
            discord.ui.Section(
                content,
                accessory=discord.ui.Thumbnail(media="https://croustillant.menu/logo.png")
            ),
        ]

        if image_url:
            items.append(discord.ui.MediaGallery(discord.MediaGalleryItem(media=image_url)))
        else:
            items.append(discord.ui.MediaGallery(discord.MediaGalleryItem(media="https://croustillant.menu/banner-small.png")))

        items.append(ActionRow(rid=rid))
        items.append(discord.ui.TextDisplay(content=f"-# *{footer_text}*"))

        self.add_item(discord.ui.Container(*items))
