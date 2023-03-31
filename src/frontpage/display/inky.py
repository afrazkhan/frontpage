from PIL import Image, ImageDraw, ImageFont
from jinja2 import Environment, PackageLoader
from html import unescape
from importlib import resources
import datetime

class InkyDisplay():
    """ TODO """

    def __init__(self, logger, config, page, mock):
        if config is None:
            logger.error('This command can only be used with configuration present in ~/.config/frontpage.yaml')
            logger.error('The only available command line option available is --page')

        self.logger = logger
        self.config = config
        self.page = page
        self.mock = mock
        self.image_location = '/tmp/current_happenings.png'

        try:
            from inky.auto import auto # pylint: disable=import-error,unused-import
            self.display = auto(ask_user=True)

        except ModuleNotFoundError:
            logger.warning('Non-linux systems are not supported. We will only generate the image to be displayed')

        self.dimensions = (600, 448)
        self.image = Image.new('RGB', self.dimensions, 'white')
        with resources.path('resources', 'Academy Engraved LET Fonts.ttf') as path:
            self.title_font = ImageFont.truetype(str(path), 40)
        with resources.path('resources', 'Times New Roman.ttf') as path:
            self.font = ImageFont.truetype(str(path), 14)
            self.subtitle_font = ImageFont.truetype(str(path), 20)
        self.draw = ImageDraw.Draw(self.image)
        self.templates = Environment(loader=PackageLoader('frontpage.display', 'templates/'), trim_blocks=True, lstrip_blocks=True)


    def draw_global_titles(self):
        """
        Draw all the hardcoded positioned titles that go at the to of all pages
        """

        title = "The Daily Pantaloon"
        blurb = "All the news that's fit to print, and lots that's not"
        now = datetime.datetime.now()
        title_size = self.draw.textsize(title, font=self.title_font)
        self.draw.text(((self.dimensions[0]-title_size[0])/2, 5), title, font=self.title_font, fill=(0, 0, 0))
        blurb_size = self.draw.textsize(blurb, font=self.font)
        self.draw.text(((self.dimensions[0]-blurb_size[0])/2, 40), blurb, font=self.font, align='center', fill=(0, 0, 0))
        self.draw.text((465, 40), now.strftime('%A %e %b %Y'), font=self.font, align='center', fill=(0, 0, 0))

    def draw_frontpage(self, text: str, weather_icon: str, filename: str = None):
        """ Fill in the frontpage, and save it to a PNG """

        self.draw_global_titles()

        # Draw the hardcoded titles for the frontpage
        self.draw.text((20, 65), "Web Trends", font=self.subtitle_font, fill=(0, 0, 0))
        self.draw.text((20, 305), "Weather", font=self.subtitle_font, align='center', fill=(0, 0, 0))

        # Fill in the text
        self.draw.multiline_text((20, 100), text, font=self.font, fill=(0, 0, 0))

        with resources.path('resources.icons', f"{weather_icon}.png") as path:
            with Image.open(path, 'r') as image:
                weather_icon_image = image.resize((100, 100))
        self.image.paste(weather_icon_image, (465, 320), mask=weather_icon_image)

        self.image.save(filename or self.image_location)

    def fit_display(self, text: str, font: ImageFont, dimensions: tuple, padding: int = 5) -> str:
        """
        Make <text> fit on display of <dimensions>

        Robbed from here:
        https://stackoverflow.com/questions/11159990/write-text-to-image-with-max-width-in-pixels-python-pil
        """

        max_width = dimensions[0] - (padding*2)
        text_lines = text.split('\n')
        text_lines = []
        text_line = []
        text = text.replace('\n', ' [br] ')
        words = text.split()

        for word in words:
            if word == '[br]':
                text_lines.append(' '.join(text_line))
                text_line = []
                continue
            text_line.append(word)
            space_size = font.getsize(' '.join(text_line))
            if space_size[0] > max_width:
                text_line.pop()
                text_lines.append(' '.join(text_line))
                text_line = [word]

        if len(text_line) > 0:
            text_lines.append(' '.join(text_line))

        return '\n'.join(text_lines)

    def render_page(self):
        """ Render a page """

        if self.mock:
            with resources.path('resources', 'sample_text.txt') as path:
                with open(path, 'r') as file:
                    formatted_page = file.read()

            self.draw_frontpage(formatted_page, weather_icon='01d')

            return

        if self.page == 'front':
            from frontpage.gather.google import Google
            this_google = Google(self.logger, self.config, self.config['country_codes'], self.config['number_of_items'])
            web_trends = unescape(this_google.main())

            from frontpage.gather.weather import Weather
            this_weather = Weather(self.logger, self.config, self.config.get('city'), self.config.get('coords'))
            the_weather = unescape(this_weather.main())

            from frontpage.gather.news import News
            this_news = News(self.logger, self.config, 2)
            the_news = unescape(this_news.main())

            page = self.templates.get_template("frontpage.j2")
            rendered_page = page.render({
                'web_trends': web_trends,
                'news': the_news,
                'weather': the_weather
            })

            formatted_page = self.fit_display(rendered_page, self.font, self.dimensions)
            self.draw_frontpage(formatted_page, weather_icon=the_weather['weather'][0]['icon'])

    def main(self):
        """ Main method for this class """

        self.render_page()

        try:
            self.display.set_image(self.image)
            self.display.show()
        except AttributeError:
            self.logger.warning(f"""Not talking to Inky actual, because we're not on Linux. The image file has still
been written out to {self.image_location} though""")
