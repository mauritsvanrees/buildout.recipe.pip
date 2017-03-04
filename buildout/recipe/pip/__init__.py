# -*- coding: utf-8 -*-
"""Recipe pip"""
from subprocess import call

import logging
import os
import tempfile
import virtualenv
import zc.buildout

logger = logging.getLogger('buildout.recipe.pip')


class Recipe(object):
    """zc.buildout recipe for creating a virtualenv and installing with pip."""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        env_dir = os.path.join(self.buildout['buildout']['parts-directory'], self.name)
        if not os.path.exists(env_dir):
            virtualenv.create_environment(env_dir)
        # Find lib/python2.7/site-packages.  Or for Python 3 or PyPy.
        # I read somewhere that on Windows it is lib/site-packages.
        path = os.path.join(env_dir, 'lib')
        if 'site-packages' in os.listdir(path):
            path = os.path.join(path, 'site-packages')
        else:
            path = os.path.join(path, os.listdir(path)[0], 'site-packages')
        if not os.path.isdir(path):
            raise zc.buildout.UserError(
                'virtualenv path {} not found'.format(path))
        self.options['env_dir'] = env_dir
        self.options['path'] = path

    def install(self):
        """Installer"""
        self.options['env_dir'] = env_dir
        self.options.created(env_dir)

        pip_script = os.path.join(self.options['env_dir'], 'bin', 'pip')
        packages = self.options.get('packages', self.options.get('eggs'), '').split()
        if not packages:
            return self.options.created()

        pip_args = [
            # Command:
            'install',
            # Compile py files to pyc.
            '--compile',
            '--no-binary', 'zc.recipe.egg',  # Maybe use canonicalize_name.
            '--disable-pip-version-check',
        ]
        # Get the version constraints.
        versions = self.buildout.versions
        with tempfile.NamedTemporaryFile() as constraints_file:
            # Get version constraints.
            if versions is not None:
                for name, version in versions.items():
                    if 'dev' in version:
                        # Could not find a version that satisfies the requirement
                        # zc.buildout==>=2.6.0.dev0
                        logger.warn('Ignoring dev constraint %s = %s',
                                    name, version)
                        continue
                    # Collecting zc.recipe.egg==>=2.0.0a3 fails for me, even
                    # when it is already installed as dev version.  Pip says it
                    # can't find it in a list that does actually contain it...
                    if '>=' in version:
                        logger.warn('Ignoring ">=" constraint %s = %s',
                                    name, version)
                        continue
                    constraints_file.write('{0}=={1}\n'.format(name, version))
            constraints_file.seek(0)
            # Constrain versions using the given constraints file.
            pip_args.extend(['--constraint', constraints_file.name])

            pip_args.extend(packages)
            pip_command = [pip_script]
            pip_command.extend(pip_args)
            call(pip_command)

        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.
        return self.options.created()

    def update(self):
        """Updater"""
        # For now do the same as on install.
        return self.install()


class Scripts(object):
    """zc.buildout recipe for creating scripts.

    This uses distlib.scripts.ScriptMaker.

    Current goal: turn the ./bin/instance script in a working
    ./instance script.

    We have a bin/instance script that has been created with
    plone.recipe.zope2instance, which is based on zc.recipe.egg.  The
    way we use it in our test buildout.cfg results in a script that only
    has the Zope2 egg plus dependencies, and uses the python with which
    buildout was run.  You can start it with 'bin/instance fg' and
    create a plain Zope site.

    The Scripts class replaces the shebang line with one that has a
    shebang line for the Python from the virtualenv/pip part.

    In the end we probably want to replace plone.recipe.zope2instance
    with a recipe that is not based on zc.recipe.egg.
    """

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options

    def install(self):
        # XXX We would like to use the distlib package that is in the
        # virtualenv, as that would make things much easier, for example
        # finding the right executable for a shebang line.
        from distlib.scripts import ScriptMaker
        bin_dir = self.buildout['buildout']['bin-directory']
        buildout_dir = self.buildout['buildout']['directory']
        maker = ScriptMaker(bin_dir, buildout_dir)  # source dir, target dir

        # Set the Python executable for the script.
        executable = os.path.join(self.options['env-dir'], 'bin', 'python')
        maker.executable = executable

        # Allow to overwrite previous scripts.
        maker.clobber = True

        # Make a copy of the script.
        maker.make('instance')

        return ('instance',)
