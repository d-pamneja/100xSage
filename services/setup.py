from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = [req.strip() for req in f.readlines() if req.strip()]
    
setup(
    name="100xSage",
    version="0.0.4",
    author="Dhruv Pamneja",
    author_email="dpamneja@gmail.com",
    install_requires=[requirements],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "src.agents.Resolver.config": ["*.yaml"],
    },
)