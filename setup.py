import setuptools


setuptools.setup(
    name="tab2dict",
    version="0.0.1",
    description="tab2dict supports data handing in developing scientific software.",
    long_description="`tab2dict` supports data handling in developing of scientific software (i.e., models). "
    "It can convert predefined input tables (`.xlsx` or `.csv`) into `TabDict` instances. "
    "Then, the items therein can be fetched by `TabKey` instances.",
    long_description_content_type="text/markdown",
    url="https://github.com/SongminYu/tab2dict",
    author="Songmin Yu, Zhanyi Hou",
    author_email="songmin.yu@outlook.com",
    license="MIT",
    # For classifiers, refer to:
    # https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering",
    ],
    packages=setuptools.find_namespace_packages(include=["tab2dict", "tab2dict.*"]),
    install_requires=[
        "pandas",
        "openpyxl",
    ],
    python_requires=">=3.8",
    include_package_data=True,
)
