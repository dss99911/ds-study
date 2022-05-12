from setuptools import setup, find_packages

setup(
    name='common-utils',
    version='0.1',
    description='Common Utils',
    author='hyun',
    author_email='dss99911@gmail.com',
    packages=find_packages(exclude=['test', 'data', 'pipeline', 'program'])
)
