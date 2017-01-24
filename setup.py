# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


version = '1.0'

long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    open('CONTRIBUTORS.rst').read()
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    open('CHANGES.rst').read()
)

tests_require = [
    'zope.testing',  # XXX Switch to pytest or nosetests?
    'zc.buildout[test]',
]

setup(
    name='buildout.recipe.pip',
    version=version,
    description="Use pip to install packages in a virtualenv per part.",
    long_description=long_description,
    # Get more strings from
    # https://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',
        'Framework :: Buildout',
        'Framework :: Buildout :: Recipe',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        # TODO: check with Python 3.
    ],
    keywords='buildout pip install virtualenv wheel package',
    author='Maurits van Rees',
    author_email='maurits@vanrees.org',
    url='https://github.com/mauritsvanrees/buildout.recipe.pip',
    license='ZPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['buildout', 'buildout.recipe'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'distlib',
        'setuptools',
        'zc.buildout',
        'virtualenv',
        'pip',  # XXX Maybe use the one in the virtualenv.
    ],
    tests_require=tests_require,
    extras_require=dict(tests=tests_require),
    test_suite='buildout.recipe.pip.tests.test_docs.test_suite',
    entry_points={
        'zc.buildout': [
            'default = buildout.recipe.pip:Recipe',
            'scripts = buildout.recipe.pip:Scripts',
        ],
    },
)
