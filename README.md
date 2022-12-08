# Weather-Getter CLI Tool
A CLI tool for to get the weather based on street address input.

## Installation
This has only been tested in a BASH environment. However, it is _expected_ to work on other systems, per it was written deliberately only using built-in modules in a relatively "not old" version of python3 (3.8.10). 

As well, I have left off the `.py` file extension per this is intended to be used as a CLI tool.

To install:
- clone repository: `git clone https://github.com/gresco/weather-getter.git`
- then either
  - run it directly with `cd weather-getter; chmod +x weather-getter && ./weather-getter` 
  - or install it in your $PATH by running `cd weather-getter/ && sudo install weather-getter /usr/local/bin`

## Usage
Please run `weather-getter help` to see syntax and examples.

# Considerations
This iteration has not been robustly tested and may prove fragile for certain edge cases. Howbeit, I did try to account for the empty dataset (when the address is not found by census.gov) and when implemented the crudest of pattern checks against the address string (checking for commas).

The script accounts for more unhandled exceptions that I came across. But, I also did not write any testing around zip codes, secondary address lines, or other edge-cases. 

I considered running this via Docker, but for brevity's sake I never got around to it. as a CLI tool I think Docker would help more with tightening the development feedback loop as well as easy of testing against different versions of Python. For something this lightweight and focused I feel okay with 

If I had more time, I would probably have created a virtenv/dockerized container and brought in non-built-in modules like:
- [Click](https://click.palletsprojects.com/en/8.1.x/) for CLI args and flags.
- [Colorama](https://pypi.python.org/pypi/colorama) for text effects.
- [i18naddress](https://pypi.org/project/google-i19n-address/) for address validation and normalization.

