import copy
import enum
import operator
from datetime import datetime

from ..utils import (JsonArray, JsonField, JsonObject, JsonTemplate)

__all__ = ('EmbedThumbnail', 'EmbedVideo', 'EmbedImage',
           'EmbedProvider', 'EmbedAuthor', 'EmbedFooter',
           'EmbedField', 'Embed')


class EmbedType(enum.Enum):
    RICH = 'rich'
    IMAGE = 'image'
    VIDEO = 'video'
    GIFV = 'gifv'
    ARTICLE = 'article'
    LINK = 'link'


EmbedThumbnail = JsonTemplate(
    url=JsonField('url'),
    proxy_url=JsonField('proxy_url'),
    height=JsonField('height'),
    width=JsonField('width')
).default_object('EmbedThumbnail')


EmbedVideo = JsonTemplate(
    url=JsonField('url'),
    proxy_url=JsonField('proxy_url'),
    height=JsonField('height'),
    width=JsonField('width')
).default_object('EmbedVideo')


EmbedImage = JsonTemplate(
    url=JsonField('url'),
    proxy_url=JsonField('proxy_url'),
    height=JsonField('height'),
    width=JsonField('width')
).default_object('EmbedImage')


EmbedProvider = JsonTemplate(
    name=JsonField('name'),
    url=JsonField('url')
).default_object('EmbedProvider')


EmbedAuthor = JsonTemplate(
    name=JsonField('name'),
    url=JsonField('url'),
    icon_url=JsonField('icon_url'),
    proxy_icon_url=JsonField('proxy_icon_url')
).default_object('EmbedAuthor')


EmbedFooter = JsonTemplate(
    text=JsonField('text'),
    icon_url=JsonField('icon_url'),
    proxy_icon_url=JsonField('proxy_icon_url')
).default_object('EmbedFooter')


EmbedField = JsonTemplate(
    name=JsonField('name'),
    value=JsonField('value'),
    inline=JsonField('inline')
).default_object('EmbedField')


EmbedTemplate = JsonTemplate(
    title=JsonField('title'),
    type=JsonField(
        'type', EmbedType, operator.attrgetter('value'),
        default=EmbedType.RICH
    ),
    description=JsonField('description'),
    url=JsonField('url'),
    timestamp=JsonField(
        'timestamp', datetime.fromisoformat, datetime.isoformat
    ),
    color=JsonField('color'),
    footer=JsonField('footer', object=EmbedFooter),
    image=JsonField('image', object=EmbedImage),
    thumbnail=JsonField('thumbnail', object=EmbedThumbnail),
    video=JsonField('video', object=EmbedVideo),
    provider=JsonField('provider', object=EmbedProvider),
    author=JsonField('author', object=EmbedAuthor),
    fields=JsonArray('fields', object=EmbedField)
)


class Embed(JsonObject, template=EmbedTemplate):
    def to_builder(self):
        return EmbedBuilder.from_embed(self)


class EmbedBuilder:
    def __init__(self, **kwargs):
        self.embed = Embed.unmarshal({'fields': []})
        self.set_title(kwargs.get('title'))
        self.set_type(kwargs.get('type'))
        self.set_description(kwargs.get('description'))
        self.set_url(kwargs.get('url'))
        self.set_timestamp(kwargs.get('timestamp'))
        self.set_color(kwargs.get('color'))

    def set_title(self, title):
        if title is not None and not isinstance(title, str):
            raise TypeError(
                'title should be a string or None, '
                'got {.__class__.__name__!r}'.format(title))

        self.embed.title = title

    def clear_title(self):
        self.embed.title = None

    def set_type(self, type):
        self.embed.type = EmbedType(type)

    def clear_type(self):
        self.embed.type = None

    def set_description(self, description):
        if description is not None and not isinstance(description, str):
            raise TypeError(
                'description should be a str or None, got '
                '{.__class__.__name__!r}'.format(description))

        self.embed.description = description

    def clear_description(self):
        self.embed.description = None

    def set_url(self, url):
        if url is not None and not isinstance(url, str):
            raise TypeError(
                'url should be a str or None, got '
                '{.__class__.__name__!r}'.format(url))

        self.embed.url = url

    def clear_url(self):
        self.embed.url = None

    def set_timestamp(self, timestamp):
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        elif isinstance(timestamp, (int, float)):
            timestamp = datetime.fromtimestamp(timestamp)

        if timestamp is not None and not isinstance(timestamp, datetime):
            raise TypeError(
                'timestamp should be a str, int, float, datetime or None, ',
                'got {.__class__.__name__!r}'.format(timestamp))

        self.embed.timestamp = timestamp

    def clear_timestamp(self):
        self.embed.timestamp = None

    def set_color(self, color):
        if color is not None and not isinstance(color, int):
            raise TypeError(
                'color should be an int, got '
                '{.__clas__.__name__!r}'.format(color))

        self.embed.color = color

    def clear_color(self):
        self.embed.color = None

    def set_footer(self, text, icon_url=None, proxy_icon_url=None):
        if not isinstance(text, str):
            raise TypeError(
                'text should be a str, got '
                '{.__class__.__name__!r}'.format(text))

        if icon_url is not None and not isinstance(icon_url, str):
            raise TypeError(
                'icon_url should be a str or None, got '
                '{.__class__.__name__!r}'.format(icon_url))

        if proxy_icon_url is not None and not isinstance(proxy_icon_url, str):
            raise TypeError(
                'proxy_icon_url should be a str or None, got '
                '{.__class__.__name__!r}'.format(proxy_icon_url))

        self.embed.foooter = EmbedFooter.unmarshal({
            'text': text,
            'icon_url': icon_url,
            'proxy_icon_url': proxy_icon_url
        })

    def clear_footer(self):
        self.embed.footer = None

    def _attachment(self, url=None, proxy_url=None, height=None, width=None):
        if url is not None and not isinstance(url, str):
            raise TypeError(
                'url should be a str or None, got '
                '{.__class__.__name__!r}'.format(url))

        if proxy_url is not None and not isinstance(proxy_url, str):
            raise TypeError(
                'proxy_url should be a str or None, got '
                '{.__class__.__name__!r}'.format(proxy_url))

        if height is not None and not isinstance(height, int):
            raise TypeError(
                'height should be an int or None, got '
                '{.__class__.__name__!r}'.format(height))

        if width is not None and not isinstance(width, int):
            raise TypeError(
                'width should be an int or None, got '
                '{.__class__.__name__!r}'.format(width))

        return {
            'url': url,
            'proxy_url': proxy_url,
            'height': height,
            'width': width
        }

    def set_image(self, url=None, proxy_url=None, height=None, width=None):
        self.embed.image = EmbedImage.unmarshal(
            self._attachment(url, proxy_url, height, width))

    def clear_image(self):
        self.embed.image = None

    def set_thumbnail(self, url=None, proxy_url=None, height=None, width=None):
        self.embed.thumbnail = EmbedThumbnail.unmarshal(
            self._attachment(url, proxy_url, height, width))

    def clear_thumbnail(self):
        self.embed.thumbnail = None

    def set_video(self, url=None, proxy_url=None, height=None, width=None):
        self.embed.video = EmbedImage.unmarshal(
            self._attachment(url, proxy_url, height, width))

    def clear_video(self):
        self.embed.video = None

    def set_provider(self, name=None, url=None):
        if name is not None and not isinstance(name, str):
            raise TypeError(
                'name should be a str or None, got '
                '{.__class__.__name__}'.format(name))

        if url is not None and not isinstance(url, str):
            raise TypeError(
                'url should be a str or None, got '
                '{.__class__.__name__}'.format(url))

        self.embed.provider = EmbedProvider.unmarshal({
            'name': name,
            'url': url
        })

    def clear_provider(self):
        self.embed.provider = None

    def set_author(self, name, icon_url=None, proxy_icon_url=None):
        if not isinstance(name, str):
            raise TypeError(
                'name should be a str, got '
                '{.__class__.__name__!r}'.format(name))

        if icon_url is not None and not isinstance(icon_url, str):
            raise TypeError(
                'icon_url should be a str or None, got '
                '{.__class__.__name__!r}'.format(icon_url))

        if proxy_icon_url is not None and not isinstance(proxy_icon_url, str):
            raise TypeError(
                'proxy_icon_url should be a str or None, got '
                '{.__class__.__name__!r}'.format(proxy_icon_url))

        self.embed.foooter = EmbedAuthor.unmarshal({
            'name': name,
            'icon_url': icon_url,
            'proxy_icon_url': proxy_icon_url
        })

    def clear_author(self):
        self.embed.author = None

    def _field(self, name, value, inline=None):
        if not isinstance(name, str):
            raise TypeError(
                'name should be a str, got '
                '{.__class__.__name__!r}'.format(name))

        if not isinstance(value, str):
            raise TypeError(
                'value should be a str, got '
                '{.__class__.__name__!r}'.format(value))

        if inline is not None and not isinstance(inline, bool):
            raise TypeError(
                'inline should be a bool or None, got '
                '{.__class__.__name__!r}'.format(inline))

        return EmbedField.unmarshal({
            'name': name,
            'value': value,
            'inline': inline
        })

    def add_field(self, name, value, inline=None):
        self.embed.fields.append(self._field(name, value, inline))

    def pop_field(self, index):
        return self.embed.fields.pop(index)

    def insert_field(self, index, name, value, inline=None):
        self.embed.fields.insert(index, self._field(name, value, inline))

    def extend_fields(self, *fields):
        for field in fields:
            self.add_field(*field)

    def clear_fields(self):
        self.embed.fields.clear()

    @classmethod
    def from_embed(cls, embed):
        self = cls.__new__(cls)
        self.embed = copy.copy(embed)
        return self
