from setuptools import setup

# This will create a package to distribute a python program.
# run python setup.py bdist_wheel to create a wheel.
# pip3 install dist/snapshotalyzer_3000-0.1-py3-none-any.whl
# this install the the package and its dependencies in your environment

setup(
    name='snapshotalyzer-3000',
    version='0.1',
    author="Mike McKee",
    author_email="networkmike42@gmail.com",
    description="SnapshotAlyzer 3000 is a tool to manage AWS EC2 snpashots",
    license="GPLv3+",
    packages=['shotty'],
    url="https://github.com/networkmike42/snaphotanyzer-30000",
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        shotty=shotty.shotty:cli
    '''
)
#shotty = <directory>.name:execution
