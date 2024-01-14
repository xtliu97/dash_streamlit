import os
from setuptools import setup, find_packages


def get_version() -> str:
    with open(os.path.join("dash_streamlit", "__init__.py")) as f:
        for line in f:
            if line.startswith("__version__"):
                return eval(line.split("=")[-1])


setup(
    name="dash_streamlit",
    version=get_version(),
    packages=find_packages(),
    description="A python package build on streamlit to make it easier to manage callbacks and layout.",
    author="xtliu97",
    author_email="mielionsk@outlook.com",
    install_requires=["streamlit"],
)
