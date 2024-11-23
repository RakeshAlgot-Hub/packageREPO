from setuptools import setup, find_packages

setup(
    name="logyen",
    version="0.1",
    description="A simple login system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="RakeshAiYensi",
    author_email="rakesh@aiyensi.com",
    packages=find_packages(),
    install_requires=["fastapi>=0.115.0", "python-keycloak>=4.6.2", "pymongo>=3.12", "uvicorn>=0.30.6", "pydantic>=2.8.2", "requests>=2.20.0", "jwcrypto>=1.5.4", "ddtrace>=2.12.0"],
    python_requires=">=3.10",
)
