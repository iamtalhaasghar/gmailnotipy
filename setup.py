import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

__version__ = '0.0.3'
setuptools.setup(
    name="gmailnotipy",
    version=__version__,
    author="Talha Asghar",
    author_email="talhaasghar.contact@simplelogin.fr",
    description=" A command line tool which will notify when an email arrives in your Gmail inbox.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iamtalhaasghar/gmailnotipy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
    install_requires=[i for i in open('requirements.txt').readlines() if len(i)!=0],
    entry_points={'console_scripts': ['gmailnotipy = gmailnotipy:gmailnotipy.main']},
)
