from setuptools import setup, find_packages

# 确保打包时包含包内的所有数据文件
include_package_data = (True,)

# 读取 README 文件
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name="ytest",
    version="0.1.0",
    author="leo",
    author_email="your.email@example.com",
    description="auto api test",
    url="https://github.com/leoyyer/ytest",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={
        "ytest": [
            "utils/initializer/demo_suite.xlsx",
            "utils/initializer/demo_api.xlsx",
        ],  # 指定需要打包的文件
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "allure-pytest==2.13.5",
        "allure-python-commons==2.13.5",
        "attrs==23.1.0",
        "certifi==2022.12.7",
        "charset-normalizer==3.1.0",
        "click==8.1.7",
        "enum34==1.1.10",
        "exceptiongroup==1.1.1",
        "idna==3.4",
        "importlib-resources==5.12.0",
        "iniconfig==2.0.0",
        "Jinja2==3.1.2",
        "jsonpath==0.82",
        "jsonschema==3.2.0",
        "lxml==4.9.2",
        "MarkupSafe==2.1.2",
        "namedlist==1.8",
        "packaging==23.1",
        "pkgutil_resolve_name==1.3.10",
        "pluggy==1.0.0",
        "py==1.11.0",
        "pydantic==1.10.7",
        "PyMySQL==1.0.2",
        "pyrsistent==0.19.3",
        "pytest==6.2.5",
        "PyYAML==6.0",
        "requests==2.28.2",
        "six==1.16.0",
        "toml==0.10.2",
        "tomli==2.0.1",
        "typing_extensions==4.5.0",
        "urllib3==1.26.15",
        "xlrd==1.2.0",
        "xlutils==2.0.0",
        "xlwt==1.3.0",
        "zipp==3.15.0",
        "pandas==2.2.2"

    ],
    entry_points={
        'console_scripts': [
            'ytest=ytest.__main__:main',
        ]
    }
)
