from setuptools import setup, find_packages

setup(
    name="kaapi-lang",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "kaapi=kaapi_lang.cli:main",
        ],
    },
    python_requires=">=3.7",
    description="FilterKaapi: A Tamil-inspired programming language",
    author="chiddesh",
    author_email="chiddesh@example.com",
    url="https://github.com/chiddesh/filterKaapi.git",
)
