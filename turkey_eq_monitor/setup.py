from setuptools import setup
import json
import os


def read_pipenv_dependencies(fname):
    """Получаем из Pipfile.lock зависимости по умолчанию."""
    filepath = os.path.join(os.path.dirname(__file__), fname)
    with open(filepath) as lockfile:
        lockjson = json.load(lockfile)
        return [dependency for dependency in lockjson.get('default')]


setup(
    name='turkey_eq_monitor',
    version='1.0',
    description='Package for practical work on Turkey_EQ.',
    license='MIT',
    url='https://github.com/dzhoshua/turkey_eq_monitor.git',
    packages=['turkey_eq_monitor'],
    install_requires=[*read_pipenv_dependencies('Pipfile.lock')],
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
    python_requires='>=3.10',
)
