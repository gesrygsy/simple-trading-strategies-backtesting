import sys

if sys.version_info < (3, 8):
    sys.exit(
        'ERROR: Requires Python 3.8 or above'
    )

if __name__ == '__main__':
    from setuptools import setup, find_packages

    setup(
        name='simple-trading-strategies-backtesting',
        description='Trading Strategies Backtest for Forex',
        packages=find_packages(),
        author='gesrygsy',
        version='0.1',
        install_requires=[
            'numpy>=1.23.0',
            'pandas>=1.5.2',
            'matplotlib>=3.6.2',
        ],
        python_requires='>=3.8',
    )