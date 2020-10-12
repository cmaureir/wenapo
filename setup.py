import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wenapo",
    version="0.0.1",
    author="Cristián Maureira-Fredes",
    author_email="cmaureirafredes@gmail.com",
    description="Wrap, and spell checker for PO files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cmaureir/wenapo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "polib",
        "pyspellchecker",
        "docutils",
    ],
    entry_points={"console_scripts": ["wenapo=wenapo:main"]},
    python_requires=">=3.6",
)
