# from setup_reqs import use_setuptools
# use_setuptools()
import os
from setuptools import setup, find_packages
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "package_signer",
    version = "0.9",
    author = "JustaGist",
    author_email = "saifksidhik@gmail.com",
    description = ("Convenience package for inserting comment signature on top of files in a package."),
    license = "BSD",
    keywords = "signature, package signer",
    # url = "https://bitbucket.org/justagist/reinfor_learn",
    packages=find_packages(),
    scripts=['scripts/sign_package'],
    long_description=read('README.md'),
    classifiers=[],
    package_data={'': ['config/sample_signature.txt']},
    include_package_data=True,
    #     "Development Status :: 3 - Alpha",
    #     "Topic :: Utilities",
    #     "License :: OSI Approved :: BSD License",
    # ],
)

