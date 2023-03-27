from PIL import Image, ImageDraw
from jinja2 import Environment, FileSystemLoader, PackageLoader

class Inky():
    """ TODO """

    def __init__(self, logger, config, page, mock):
        self.logger = logger
        self.config = config
        self.page = page

        # if mock:
        #     from inky import InkyMockPHAT as InkyPHAT # pylint: disable=import-error,unused-import
        # else:
        #     from inky import InkyPHAT # pylint: disable=import-error,unused-import
        if not mock:
            from inky import InkyPHAT # pylint: disable=import-error,unused-import
            self.display = InkyPHAT('black')

        self.dimensions = (600, 448)
        self.image = Image.new('RGB', self.dimensions, 'black')
        self.draw = ImageDraw.Draw(self.image)

        self.templates = Environment(loader=PackageLoader('frontpage.display', 'templates/'), trim_blocks=True, lstrip_blocks=True)


    def create_image(self, coords, text, filename=None):
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
            web_trends = this_google.main()

            from frontpage.gather.news import News
            this_news = News(self.logger, self.config, 2)
            the_news = this_news.main()

            from frontpage.gather.weather import Weather
            this_weather = Weather(self.logger, self.config, self.config.get('city'), self.config.get('coords'))
            the_weather = this_weather.main()

            rendered_page = page.render({
                'web_trends': web_trends,
                'news': the_news,
                'weather': the_weather
            })

            print(rendered_page)
