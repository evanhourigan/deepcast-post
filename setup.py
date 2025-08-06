from setuptools import setup, find_packages

setup(
    name="deepcast-post",
    version="0.1.0",
    description="A CLI tool for generating deepcast breakdowns from diarized transcripts using OpenAI API.",
    author="Evan Hourigan",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "deepcast=deepcast_post.cli:main",
        ],
    },
    python_requires=">=3.9",
) 