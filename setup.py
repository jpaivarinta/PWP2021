""" Not sure yet if necessary"""
from setuptools import find_packages, setup
""" 
Source and help from
https://github.com/enkwolf/pwp-course-sensorhub-api-example and
https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/
"""
setup(
    name="cryptomonitor",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask",
        "flask-restful",
        "flask-sqlalchemy",
        "SQLAlchemy",
        ]
)