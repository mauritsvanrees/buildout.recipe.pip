Buildout for pip users
======================

So you are a Python developer and have been using ``pip`` to install packages in a ``virtualenv``.
You have been doing this for years and it is working fine.
Why would you consider using buildout?

The main reason is:
**buildout does not just install packages**.
Buildout can do much more.

Buildout is basically a ``Makefile`` for the Python world.
You can extend it with buildout recipes, which are themselves Python packages.
With those recipes you can do things like this:

- install Python packages
- install a non-Python project, running its ``configure``, ``make``, and ``make install`` steps
- create an nginx configuration file from a template
- create a script for backing up your database
- add cronjobs
- run a command

Try doing that with ``pip``!

But buildout is not here to replace ``pip``.
Buildout has a recipe that uses ``pip``.
Let's see what you can do with that.


Buildout basics
---------------

On http://www.buildout.org you can watch screen casts and read documentation on how to install and use buildout.
But let's give you the basic steps here.

- Create a virtualenv and install ``zc.buildout`` in it::

    virtualenv test
    cd test
    . bin/activate
    pip install zc.buildout

- Create a ``buildout.cfg`` file with some contents::

    [buildout]
    parts =

- Run buildout::

    bin/buildout

This will create a few directories and then quit because there is nothing to do.
So let's think up some things that we could let buildout do for us.


Install a package
-----------------

You are a ``pip`` user and have this simple ``requirements.txt`` file::

    requests

You install it by running pip::

    pip install -r requirements.txt

How does this translate into a buildout?
Update your ``buildout.cfg`` file to this::

    [buildout]
    parts = packages

    [packages]
    recipe = buildout.recipe.pip
    packages = requests

Then run buildout::

     bin/buildout

Buildout will install the ``buildout.recipe.pip`` Python package.
This recipe creates a virtualenv in the directory ``parts/packages``.
The ``packages`` name comes from the part or section name that is within square brackets.
Then it uses the ``pip`` from the new virtualenv to install the ``requests`` package.

You may be frowning now.
You have a virtualenv with buildout, and this creates another virtualenv with ``requests``.
Shouldn't those two be combined?

What is happening here is: clean separation.
If you would combine them, and buildout and ``requests`` somehow interfere with one another, you may end up with a broken environment.
By separating them, you can create multiple environments that coexist happily next to each other, for example:

- a virtualenv with Django plus your own Django add-on
- a virtualenv with Django plus your own Django add-on plus its test dependencies
- a virtualenv with Django plus a similar add-on that you want to compare
- a virtualenv with Sphinx to build your documentation

It may not even be possible to put all this in a single virtualenv, if your add-on requires newer versions that the other add-on conflicts with.
Or your add-on starts depending on a utility function from Sphinx and you don't notice that you didn't add Sphinx to the ``install_requires`` in your ``setup.py``.

Okay, you say, but it would be nice to have a Python prompt with the installed packages without needing to do ``parts/packages/bin/python``.
Sure, let's do that.


A Python interpreter with packages
----------------------------------

So you want a Python interpreter that has access to the ``requests`` package from the ``parts/packages`` virtualenv that the recipe created.
Adjust the ``buildout.cfg`` like this::

    [buildout]
    parts = packages

    [packages]
    recipe = buildout.recipe.pip
    packages = requests
    interpreter = pyrequests

This will create a file ``bin/pyrequests`` in your buildout directory, which gives you the wanted Python prompt.

TODO: write this code.


Use exact versions of packages
------------------------------

Let's say your ``requirements.txt`` file had a version pin to use an older version::

    requests==2.12.5

What is the buildout equivalent?
You specify a buildout part with version pins::

    [buildout]
    parts = packages

    [versions]
    requests = 2.12.5

    [packages]
    recipe = buildout.recipe.pip
    packages = requests
    interpreter = pyrequests

The ``versions`` section is used to constrain the versions.
The recipe creates a temporary file based on this section, and passes this to ``pip install --constraint <file>``.

The nice thing about a constraints file, is that it can be a known good set: a long list of packages that work well together.
The recipe does not install all packages in this list, but only that packages that are required.
For example, this versions section would have the same effect::

    [versions]
    requests = 2.12.5
    Plone = 5.0.6
    no_such_package = 1.0

.. We could mention ``packages = requests==2.12.5`` without a versions section as option.
   But if we allow that, we can put it in detailed documentation.
   In this document, showing all choices would be too much informatin.

TODO: ``packages = requests==2.9.1`` is ignored in favor of the versions section.
That may be unexpected.
At least it sounds doable to allow this.
But then, that does not work for the original ``zc.recipe.egg`` either.
If you try this, you actually get a version error::

    [packages]
    recipe = zc.recipe.egg
    eggs = requests==2.9.1
