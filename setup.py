from setuptools import setup, find_packages


setup(
    name='pypdc-sis',
    version='0.1',
    packages=find_packages(),
    author='Shafiullah Qureshi
    author_email='qureshi.shafiullah@gmail.com, 
    install_requires=[
        
        'dcor'
    ],
    package_data={
        'pypdc-sis': ['data/*']
    },
    include_package_data=True
)
