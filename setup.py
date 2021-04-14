import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="chaosimp",
    version="0.1.0",
    description="Chaos engineering on AWS",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/chaosops/imp",
    author="Vasily Vasinov",
    author_email="vasinov@me.com",
    license="Apache 2.0",
    install_requires=[
        "pyyaml",
        "click",
        "boto3",
        "cfn_flip",
        "troposphere @ git+https://github.com/cloudtools/troposphere@master",  # until v2.7.1 is released
        "pyhumps>=1.6.0"
    ],
    entry_points={
        "console_scripts": ["imp=chaosimp.__main__:main"]
    }
)
