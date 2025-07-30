#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="oceansecurity-news",
    version="1.0.0",
    author="海之安（中国）科技有限公司",
    author_email="contact@oceansecurity.cn",
    description="海之安网络安全新闻系统 - 全球安全资讯聚合平台",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oceansecurity/news-system",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "feedparser>=6.0.10",
        "zhipuai>=2.0.0",
        "crawl4ai>=0.2.0",
        "lxml>=4.9.0",
        "python-dateutil>=2.8.0",
    ],
    entry_points={
        "console_scripts": [
            "oceansec-news=scripts.run_glm_news:main",
        ],
    },
)
