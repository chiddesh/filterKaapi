from setuptools import setup, find_packages

setup(
    name="kaapi-lang",  # Package name on PyPI
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "kaapi=kaapi_lang.cli:main",
        ],
    },
    python_requires=">=3.7",
    description="FilterKaapi: A Tamil-inspired programming language",
    author="Chiddesh",
    author_email="your_email@example.com",
    url="https://github.com/chiddesh/filterKaapi",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
