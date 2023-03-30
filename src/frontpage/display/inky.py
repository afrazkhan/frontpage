from PIL import Image, ImageDraw, ImageFont
from jinja2 import Environment, PackageLoader
from html import unescape
import importlib.resources as resources

class Inky():
    """ TODO """

    def __init__(self, logger, config, page, mock):
        if config is None:
            logger.error('This command can only be used with configuration present in ~/.config/frontpage.yaml')
            logger.error('The only available command line option available is --page')

        self.logger = logger
        self.config = config
        self.page = page
        self.mock = mock

        try:
            if mock:
                from inky import InkyMockPHAT as InkyPHAT # pylint: disable=import-error,unused-import
            else:
                from inky import InkyPHAT # pylint: disable=import-error,unused-import

            self.display = InkyPHAT('white')
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


    def create_image(self, text: str, weather_icon: str, filename: str = None):
        """ Write <text> at <coords>, and save to <filename> """

        # Draw all the hardcoded positioned titles
        self.draw.text((230, 5), "The Daily", font=self.title_font, fill=(0, 0, 0))
        self.draw.text((175, 40), "All the news that's fit to print, and lots that's not", font=self.font, align='center', fill=(0, 0, 0))
        self.draw.text((20, 65), "Web Trends", font=self.subtitle_font, fill=(0, 0, 0))
        self.draw.text((20, 305), "Weather", font=self.subtitle_font, align='center', fill=(0, 0, 0))

        # Fill in the text
        self.draw.multiline_text((20, 100), text, font=self.font, fill=(0, 0, 0))

        with resources.path('resources.icons', f"{weather_icon}.png") as path:
            with Image.open(path, 'r') as image:
                weather_icon_image = image.resize((100, 100))
        self.image.paste(weather_icon_image, (465, 320), mask=weather_icon_image)

        self.image.save(filename or './current_happenings.png')

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
            w, h = font.getsize(' '.join(text_line))
            if w > max_width:
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

            self.create_image(formatted_page, weather_icon='01d')

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
            print(formatted_page)

            self.create_image(formatted_page, weather_icon=the_weather['weather'][0]['icon'])

    def main(self):
        """ Main method for this class """

        self.render_page()
