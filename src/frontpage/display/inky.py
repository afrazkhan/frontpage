from PIL import Image, ImageDraw, ImageFont
from jinja2 import Environment, PackageLoader
from html import unescape

class Inky():
    """ TODO """

    def __init__(self, logger, config, page, mock):
        if config is None:
            logger.error('This command can only be used with configuration present in ~/.config/frontpage.yaml')
            logger.error('The only available command line option available is --page')

        self.logger = logger
        self.config = config
        self.page = page

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
        self.font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Times New Roman.ttf', 14)
        self.draw = ImageDraw.Draw(self.image)
        self.templates = Environment(loader=PackageLoader('frontpage.display', 'templates/'), trim_blocks=True, lstrip_blocks=True)


    def create_image(self, coords: tuple, text: str, filename: str = None):
        """ Write <text> at <coords>, and save to <filename> """

        filename = filename or './current_happenings.png'

        self.draw.multiline_text(coords, text, font=self.font, fill=(0, 0, 0))
        self.image.save(filename)

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

        if self.page == 'front':
            from frontpage.gather.google import Google
            this_google = Google(self.logger, self.config, self.config['country_codes'], self.config['number_of_items'])
            web_trends = unescape(this_google.main())

            from frontpage.gather.news import News
            this_news = News(self.logger, self.config, 2)
            the_news = unescape(this_news.main())

            from frontpage.gather.weather import Weather
            this_weather = Weather(self.logger, self.config, self.config.get('city'), self.config.get('coords'))
            the_weather = unescape(this_weather.main())

            page = self.templates.get_template("frontpage.j2")
            rendered_page = page.render({
                'web_trends': web_trends,
                'news': the_news,
                'weather': the_weather
            })

            formatted_page = self.fit_display(rendered_page, self.font, self.dimensions)

            self.create_image((5,5), formatted_page)

    def main(self):
        """ Main method for this class """

        self.render_page()
