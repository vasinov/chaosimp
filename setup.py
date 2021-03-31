from setuptools import setup, find_packages

setup(
    name="imp",
    version="0.1.0",
    description="Chaos engineering on AWS",
    url="https://github.com/chaosops/imp",
    author="Vasily Vasinov",
    author_email="vasinov@me.com",
    license="Apache 2.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pyyaml", "click", "boto3", "troposphere"],
    entry_points={"console_scripts": ["imp=imp.__main__:main"]}
)
