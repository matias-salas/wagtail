from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

class TitleAndTextBlock(blocks.StructBlock):
    """Title and text and nothing else"""

    title = blocks.CharBlock(required=True, help_text="Add your title")
    text = blocks.TextBlock(required=True, help_text="Add additional text")

    class Meta:  # noqa
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Titulo & Texto"

class RichTextBlock(blocks.RichTextBlock):
    """Richtext with all the features"""

    class Meta:  # noqa
        template = "streams/richtext_block.html"
        icon = "doc-full"
        label = "Texto enriquecido" 

class SimpleRichTextBlock(blocks.RichTextBlock):
    """Richtext without (limited) all the features"""

    def __init__(
        self, required=True, help_text="Add text", editor="default", features=None, **kwargs
    ):
        super().__init__(**kwargs)
        self.features = ["bold", "italic", "link"]

    class Meta:  # noqa
        template = "streams/richtext_block.html"
        icon = "edit"
        label = "Texto enriquecido simple"




class CTABlock(blocks.StructBlock):
    """A simple call to action section"""

    title = blocks.CharBlock(required=True, max_length=60)
    text = blocks.RichTextBlock(required=True, features=["bold", "italic"])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(required=True, default="Learn More", max_length=40)

    class Meta:  # noqa
        template = "streams/cta_block.html"
        icon = "placeholder"
        label = "Call to Action"

class CardBlock(blocks.StructBlock):
    """An image and text and button"""

    title = blocks.CharBlock(required=True, max_length=60)
    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=True, help_text="Imagen de 500x500px")),
                ("title", blocks.CharBlock(required=True, max_length=40)),
                ("text", blocks.TextBlock(required=True, max_length=200)),
                ("button_page", blocks.PageChooserBlock(required=False)),
                ("button_url", blocks.URLBlock(required=False, help_text="Si el boton de arriba esta seleccionado, este no se tomara en cuenta")),
                ("button_text", blocks.CharBlock(required=True, max_length=40, default="Learn More")),
            ]
        )
    )

    class Meta:  # noqa
        template = "streams/card_block.html"
        icon = "placeholder"
        label = "Tarjetas"