[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)

# Frontpage

> Application for displaying newspaper style pages on a 7" Inky Impression

Creates newspaper style pages for the [Inky Impression 5.7" ePaper display](https://shop.pimoroni.com/products/inky-impression-5-7) (currently only a frontpage). Designed to be used with something like a cronjob which would refresh the page for you every n hours, or the buttons on the side (not ready yet).

Bear in mind that whilst it would be easy to make the dimensions of the display options to be specified in the CLI, the way in which the pages are rendered — using hardcoded positions for the section titles — means this wouldn't be useful. For this reason, it's specifically designed to be used with the 5.7" version of the display.

## Usage

The CLI is documents itself well, but the quickstart (presuming you've [set up your Raspberry Pi for use with the Inky device already](https://github.com/pimoroni/inky#installation)) is:

1. Create a configuration file at `~/.config/frontpage.yaml` (see the [sample file](./sample_configuration.yaml)). For the `openweather_token`, you don't need to subscribe to anything, a personal account with a token generated on [this page](https://home.openweathermap.org/api_keys) is enough
1. `pip install .`
1. `fp display inky`

This will display the frontpage by default, which is an overview of information available in greater detail on the dedicated pages.

The option for displaying the other pages is `-p`, but those are not yet implemented. You can still see the information they would provide with:

```shell
fp gather [google | news | weather]
```
