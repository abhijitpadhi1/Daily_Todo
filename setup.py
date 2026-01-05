from setuptools import setup, find_packages

setup(
    name="daily-todo",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "jinja2",
        "python-dateutil",
    ],
    entry_points={
        "console_scripts": [
            "todo=app.cli:main",
        ]
    },
)
