# coding=utf-8

from distutils.core import setup

setup(
    name='pyrst',
    version='0.50',
    packages=['pyrst'],
    url='https://github.com/rbonedata/pyrst',
    license='Apache 2.0',
    author='Chris von Csefalvay',
    author_email='chris@chrisvoncsefalvay.com',
    description='Pyrst is a Python client for Birst\'s API.',
    install_requires=['suds', 'pandas', 'PyYAML', 'wsgiref'],
    classifiers=['Development Status :: 3 - Alpha']
)
