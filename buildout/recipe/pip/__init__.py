# -*- coding: utf-8 -*-
"""Recipe pip"""
from subprocess import call

import os
import virtualenv


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options

    def install(self):
        """Installer"""
        env_dir = os.path.join(self.buildout['buildout']['parts-directory'], self.name)
        if not os.path.exists(env_dir):
            virtualenv.create_environment(env_dir)
        pip_script = os.path.join(env_dir, 'bin', 'pip')
        packages = self.options.get('packages', self.options.get('eggs'), '').split()
        if not packages:
            return tuple()
        pip_command = [pip_script, 'install']
        pip_command.extend(packages)
        call(pip_command)

        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.
        return tuple()

    def update(self):
        """Updater"""
        pass
