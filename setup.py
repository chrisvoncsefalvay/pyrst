# coding=utf-8

from distutils.core import setup

__version__ = "0.6.3a"

long_descr = open("README").read()

setup(
    name='pyrst',
    version=__version__,
    packages=['pyrst'],
    url='https://github.com/rbonedata/pyrst',
    license='Apache 2.0',
    keywords=['BI', 'business intelligence', 'api', 'birst'],
    author='Chris von Csefalvay',
    author_email='chris@chrisvoncsefalvay.com',
    description='Pyrst is a Python client for Birst\'s API.',
    long_description=long_descr,
    install_requires=['suds', 'pandas', 'PyYAML'],
    classifiers=["Development Status :: 3 - Alpha",
                 "Environment :: Console",
                 "Intended Audience :: Financial and Insurance Industry",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: Apache Software License",
                 "Operating System :: OS Independent",
                 "Topic :: Office/Business :: Financial"],
    entry_points = {
        "console_scripts": ['pyrst = pyrst.pyrst_cli:main']
    }
)
