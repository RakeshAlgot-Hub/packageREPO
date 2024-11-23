from setuptools import setup, find_packages

setup(
    name="emailyen",
    version="0.1",
    description="A simple email sending system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="RakeshAiYensi",
    author_email="rakesh@aiyensi.com",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "emailyen": ["EmailTemplates/*.html"],
    },
    install_requires=[
        "fastapi>=0.115.5",
        "uvicorn>=0.30.6",
        "sendgrid>=6.11.0",
        "email-validator>=2.2.0",
        "setuptools>=66.1.0" 
        "ddtrace>=2.12.0"
    ],
    python_requires=">=3.10",
)
