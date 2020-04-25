import codecs
import os
import re
from distutils.core import setup

import setuptools  # noqa

here = os.path.abspath(os.path.dirname(__file__))


def read(*file_paths, default=""):
    # intentionally *not* adding an encoding option to open
    try:
        return codecs.open(os.path.join(here, *file_paths), "r").read()
    except Exception:
        return default


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="zelenium",
    version=find_version("zelenium", "__init__.py"),
    packages=["zelenium"],
    url="https://github.com/zeburek/zelenium",
    license="GNU General Public License v3 (GPLv3)",
    author="Parviz Khavari",
    author_email="me@parviz.pw",
    description=(
        "New Selenium framework for Python with base pages and elements"
    ),
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Testing",
    ],
)
