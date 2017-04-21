We'll start by creating a buildout that uses the recipe::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... index = https://pypi.python.org/simple
    ... parts = test1
    ...
    ... [test1]
    ... recipe = buildout.recipe.pip
    ... packages = requests
    ... """)

Running the buildout gives us::

    >>> print 'start', system(buildout)
    start...Installing test1.
    ...
    Collecting requests
      Downloading requests...whl...
    Installing collected packages: requests
    Successfully installed requests...

The result is a virtualenv::

    >>> ls('parts', 'test1')
    l  .Python
    d  bin
    d  include
    d  lib

We can pin specific versions::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = test1
    ... versions = versions
    ...
    ... [test1]
    ... recipe = buildout.recipe.pip
    ... packages = requests
    ...
    ... [versions]
    ... requests = 2.8.1
    ... """)

Running the buildout gives us::

    >>> print 'start', system(buildout)
    start Updating test1...
    Collecting requests==2.8.1...
      Downloading requests...2.8.1...whl...
    Installing collected packages: requests
      Found existing installation: requests...
        Uninstalling requests...
          Successfully uninstalled requests...
    Successfully installed requests...
