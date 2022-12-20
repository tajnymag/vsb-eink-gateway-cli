from setuptools import setup, find_packages

setup(
    name='eink-gateway-cli',
    version='1.0.0',
    description='Command line interface for VSB E-Ink Gateway API',
    url='https://github.com/tajnymag/vsb-eink-gateway-cli',
    author='Marek Lukáš',
    author_email='marek.lukas.st@vsb.cz',
    license='MIT',
    platforms='any',
    packages=find_packages(),
    install_requires=[],
    entry_points={'console_scripts': ['eink-gateway-cli=eink_gateway_cli.cli:main']},
)