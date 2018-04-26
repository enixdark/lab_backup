import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
# with open(os.path.join(here, 'README.md')) as f:
#     README = f.read()
# with open(os.path.join(here, 'CHANGES.txt')) as f:
#     CHANGES = f.read()

requires = [

]

tests_require = [
    'pytest',
    'pytest-cov',
    'Faker',
    'factory-boy >= 2.8.1'
]

setup(
    name='app',
    version='0.0',
    description='app',
    # long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
    ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={},
)
