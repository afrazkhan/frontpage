from PIL import Image, ImageDraw, ImageFont
from jinja2 import Environment, PackageLoader
import textwrap
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

        # if mock:
        #     from inky import InkyMockPHAT as InkyPHAT # pylint: disable=import-error,unused-import
        # else:
        #     from inky import InkyPHAT # pylint: disable=import-error,unused-import
        if not mock:
            try:
                from inky import InkyPHAT # pylint: disable=import-error,unused-import
                self.display = InkyPHAT('black')
            except ModuleNotFoundError:
                logger.error('Non-linux systems are not supported, though you can pass --mock to only generate the image')
                import sys
                sys.exit(1)

        self.dimensions = (600, 448)
        self.image = Image.new('RGB', self.dimensions, 'white')
        self.font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Times New Roman.ttf', 14)
        self.draw = ImageDraw.Draw(self.image)
        self.templates = Environment(loader=PackageLoader('frontpage.display', 'templates/'), trim_blocks=True, lstrip_blocks=True)


    def create_image(self, coords: tuple, text: str, filename: str = None):
        """ Write <text> at <coords>, and save to <filename> """

        filename = filename or './current_happenings.png'

        self.draw.multiline_text(coords, text)
        self.image.save(filename)

    def render_page(self):
        """ Render a page """

        if self.page == 'front':
            page = self.templates.get_template("frontpage.j2")

            from frontpage.gather.google import Google
            this_google = Google(self.logger, self.config, self.config['country_codes'], self.config['number_of_items'])
            web_trends = unescape(this_google.main())

            from frontpage.gather.news import News
            this_news = News(self.logger, self.config, 2)
            the_news = unescape(this_news.main())

            from frontpage.gather.weather import Weather
            this_weather = Weather(self.logger, self.config, self.config.get('city'), self.config.get('coords'))
            the_weather = unescape(this_weather.main())

            rendered_page = page.render({
                'web_trends': web_trends,
                'news': the_news,
                'weather': the_weather
            })

            self.create_image((5,5), rendered_page)

    def temporary_debugging(self):
        """ Delete me :) """

        web_trends = [{'NL': [{'title': 'Van Kooten en De Bie', 'summary': 'De VPRO gaat maandagavond een speciale uitzending over Van Kooten en De Bie herhalen, als eerbetoon aan de overleden komiek en schrijver Wim de Bie (83).'}, {'title': 'Gibraltar', 'summary': 'Traditiegetrouw blikt VI aan de hand van cijfers en feiten vooruit op het EK-kwalificatieduel van Oranje van maandagavond met Gibraltar.'}, {'title': 'Micha Wertheim', 'summary': 'Cabaretier Micha Wertheim gaat voor omroep BNNVara de oudejaarsconference 2023 verzorgen. Een traditionele &#39;oudejaars&#39; à la Wim Kan, Freek de Jonge...'}]}]
        page = self.templates.get_template("frontpage.j2")
        rendered_page = unescape(page.render({'web_trends': web_trends}))
        import pdb; pdb.set_trace() # pylint: disable=multiple-statements,no-member


    def main(self):
        """ Main method for this class """

        self.render_page()
