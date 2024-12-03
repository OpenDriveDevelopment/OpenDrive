from setuptools import setup, find_packages

setup(
    name="OpenDrive",
    version="0.1.3",
    author="OpenDrive systems",
    author_email="tu.email@ejemplo.com",
    description="OpenDrive Framework allows developers to work on detection, perception, and decision-making components, facilitating the creation of custom autonomous systems.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/OpenDriveDevelopment/OpenDrive",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=[
        "opencv-python>=4.5.0,<5.0.0",
        "tensorflow>=2.9.0",
        "ultralytics>=8.0.0",
        "quixstreams>=3.0.0",
    ],
)
