from setuptools import setup, find_packages
import os
if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    version = os.environ['CI_JOB_ID']

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='mobi_logic',
    # url='https://github.com/jladan/package_demo',
    author='Mariusz Masztalerczuk',
    author_email='mariusz@masztalerczuk.com',
    # Needed to actually package jjjsomething
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    # Needed for dependencies
    # install_requires=['numpy'],
    # *strongly* suggested for sharing
    version=version,
    # The license can be anything you like
    license='MIT',
    description='Bussiness logic for mobi stats',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)
