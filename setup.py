""" Not sure yet if necessary"""
from setuptools import find_packages, setup
""" This is based on course material and pwp-course-sensorhub-api-example by enkwolf """

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