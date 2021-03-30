from setuptools import setup

setup(
    name = "imp",
    version = "0.1.0",
    description = "Chaos engineering on AWS",
    url = "https://github.com/chaosops/imp",
    author = "Vasily Vasinov",
    author_email = "vasinov@me.com",
    license = "Apache 2.0",
    packages = ["imp"],
    include_package_data = True,
    install_requires = ["click", "boto3"],
    entry_points = {"console_scripts": ["imp=imp.__main__:main"]},
)
