import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zendesk_search",
    version="1.0.0",
    author="Sendhil",
    author_email="sendhildz@gmail.com",
    description="Zendesk Search",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sendhilg/zendesk-search",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
