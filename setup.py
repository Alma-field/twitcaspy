import re
from setuptools import find_packages, setup

VERSION_FILE = "twitcaspy/__init__.py"
with open(VERSION_FILE) as version_file:
    match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                      version_file.read(), re.MULTILINE)

if match:
    version = match.group(1)
else:
    raise RuntimeError(f"Unable to find version string in {VERSION_FILE}.")

with open("README.md") as readme_file:
    long_description = readme_file.read()

tests_require = [
    "nose>=1.3.7,<2",
    "vcrpy>=4.1.1,<5",
    "python-dotenv>=0.17.1,<1",
]

examples_require = [
    "flask>=2.0.1,<3"
]

setup(
    name="twitcaspy",
    version=version,
    description="Twitcasting library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Alma-field",
    author_email="",
    url="https://github.com/Alma-field/twitcaspy",
    project_urls={
        "Documentation": "https://github.com/Alma-field/twitcaspy/blob/master/README.md",
        "Issue Tracker": "https://github.com/Alma-field/twitcaspy/issues",
        "Source Code": "https://github.com/Alma-field/twitcaspy",
    },
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "requests>=2.25.1,<3",
        "requests_oauthlib>=1.3.0,<2",
    ],
    tests_require=tests_require,
    extras_require={
        "test": tests_require,
        "example": examples_require,
    },
    test_suite="nose.collector",
    keywords="twitcasting library",
    python_requires=">=3.7",
    classifiers=[
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
    zip_safe=True,
)
