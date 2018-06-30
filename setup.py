from setuptools import setup, find_packages

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='mobi_logic',
    # url='https://github.com/jladan/package_demo',
    author='Mariusz Masztalerczuk',
    author_email='mariusz@masztalerczuk.com',
    # Needed to actually package something
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    # Needed for dependencies
    # install_requires=['numpy'],
    # *strongly* suggested for sharing
    version='0.1.10',
    # The license can be anything you like
    license='MIT',
    description='Bussiness logic for mobi stats',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)
