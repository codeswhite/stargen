import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stargen",
    version="0.8.4",
    author="Max G",
    author_email="max3227@gmail.com",
    description="Interactive wordlists generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    python_requires='>=3.8',
    install_requires=[
        'interutils',
        'pyfiglet',
    ],
    entry_points={
        'console_scripts': [
            'stargen = stargen:main',
        ],
    }
)
