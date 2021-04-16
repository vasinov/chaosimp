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
    url="https://github.com/chaosops-oss/chaosimp",
    author="Vasily Vasinov",
    author_email="vasinov@me.com",
    license="Apache 2.0",
    install_requires=[
        "pyyaml>=5",
        "click>=7",
        "boto3>=1.17",
        "cfn_flip>=1",
        "troposphere>=2.7.1",
        "pyhumps>=1"
    ],
    entry_points={
        "console_scripts": ["imp=chaosimp.__main__:main"]
    }
)
