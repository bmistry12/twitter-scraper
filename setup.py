from setuptools import setup

# Where the magic happens:
setup(
    name='TwitterScraper',
    version='1.0',
    description='Twitter Scraper',
	long_description=open('README.md').read(),
    author='bmistry12',
    # python_requires='3.5.0',
    py_modules=['twitter_data'],
    install_requires=['tweepy', 'simplejson', 'hvac', 'textblob', 'pandas'],
    include_package_data=True,
)
