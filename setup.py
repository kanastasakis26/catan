from setuptools import setup, find_packages

setup(
    name='Catan Monte Carlo',
    version='0.0',
    packages=find_packages(),
    install_requires=[
        'click==7.1.1',
        'cycler==0.10.0',
        'decorator==4.4.2',
        'kiwisolver==1.2.0',
        'matplotlib==3.2.1',
        'networkx==2.4',
        'numpy==1.22.0',
        'pyparsing==2.4.7',
        'python-dateutil==2.8.1',
        'six==1.14.0',
        'SQLAlchemy==1.3.16'
    ],
    entry_points='''
        [console_scripts]
        catan=catan.cli:cli
    '''
)