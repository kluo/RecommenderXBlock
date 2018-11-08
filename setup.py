"""Setup for recommender XBlock."""

import os
import subprocess
from setuptools.command.install import install as _install
from setuptools import setup


class XBlockInstall(_install):
    """Custom XBlock install command."""

    def run(self):
        _install.run(self)
        self.compile_translations()

    def compile_translations(self):
        """
        Compiles textual translations files(.po) to binary(.mo) files.
        """
        self.announce('Compiling translations')
        try:
            for dirname, _, files in os.walk(os.path.join('recommender', 'translations')):
                for fname in files:
                    if os.path.splitext(fname)[1] == '.po':
                        po_path = os.path.join(dirname, fname)
                        mo_path = os.path.splitext(po_path)[0] + '.mo'
                        self.announce('Compiling translation at %s' % po_path, 4)
                        self.announce('CALLING MSGFMT FROM DIR: %s' % self.install_lib, 4)
                        subprocess.check_call(['msgfmt', po_path, '-o', mo_path], cwd=self.install_lib)
                        self.announce('FINISHED CALLING THE MSGFMT!!!', 4)
            self.announce('FINISHED THE COMPILING', 4)
        except Exception as ex:
            self.announce('Translations compilation failed: %s' % repr(ex), 4)
            self.announce("FORCED INTO HERE EVEN WITH NO BAD SYNTAX", 4)
            #self.announce('BAD SYNTAX FAIL: %s', ex.message)
         self.announce('HERE COMES THE BAD SYNTAX OUTSIDE THE CLAUSE', 4)
         self.announce('blah %s', 'random')

def package_data(pkg, root_list):
    """Generic function to find package_data for `pkg` under `root`."""
    data = []
    for root in root_list:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='recommender-xblock',
    version='1.2',
    description='recommender XBlock',   # TODO: write a better description.
    packages=[
        'recommender',
    ],
    entry_points={
        'xblock.v1': [
            'recommender = recommender:RecommenderXBlock',
        ]
    },
    package_data=package_data("recommender", ["static", "translations"]),
    cmdclass={
        'install': XBlockInstall,
    },
)
