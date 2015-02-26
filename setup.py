# coding=utf-8

from distutils.core import setup

setup(
    name='pyrst',
    version='0.5.3',
    packages=['pyrst'],
    url='https://github.com/rbonedata/pyrst',
    license='Apache 2.0',
    keywords=['BI', 'business intelligence', 'api', 'birst'],
    author='Chris von Csefalvay',
    author_email='chris@chrisvoncsefalvay.com',
    description='Pyrst is a Python client for Birst\'s API.',
    install_requires=['suds', 'pandas', 'PyYAML'],
    classifiers=["Development Status :: 3 - Alpha"]
)
