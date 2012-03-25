#!/usr/bin/env python
# encoding: utf-8

from distutils.command.build_py import build_py as _build_py
from distutils.errors import DistutilsError
from distutils.core import setup
from distutils.command.build_scripts import build_scripts as _build_scripts
from distutils.command.clean import clean as _clean
from distutils import log
import os.path
import sys
import unittest
import os.path
sys.path.append(os.path.join(sys.path[0],'src','main','python'))
sys.path.append(os.path.join(sys.path[0],'src','test','python'))

from webtest import urilibtest, assertiontest

VERSION_TAG = '${version}'

VERSION = '1.0-M1'

TEST_MODULES = [urilibtest,
                assertiontest,]

class DistutilsTestError (DistutilsError):
    """Unable to complite the test without errors."""
    pass

def fix_version(outfile, dry_run):
    try:
        with open(outfile) as f :
             lines = []
             to_substitute = False
             for line in f:
                 if line.find(VERSION_TAG) > -1:
                    to_substitute = True
                    line = line.replace(VERSION_TAG,VERSION)
                 lines.append(line)
        if to_substitute:
            log.info("version tag substituted in %s", os.path.basename(outfile))
            with open(outfile, 'w') as f :
                f.writelines(lines)
    except IOError:
        if not dry_run:
            raise

class clean(_clean):
    pass

class build_py(_build_py):
    """Specialized Python source builder."""

    # implement whatever needs to be different...
    def run(self):
        _build_py.run(self)
        self.test()
        self.fix_version()

    def fix_version(self):
        log.info("fix version on modules")
        modules = self.find_all_modules()
        for (package, module, _) in modules:
            if type(package) is str:
                package = package.split('.')
            elif type(package) not in (list, tuple):
                raise TypeError(
                  "'package' must be a string (dot-separated), list, or tuple")
            outfile = self.get_module_outfile(self.build_lib, package, module)
            fix_version(outfile, self.dry_run)
        
    def test(self):
        """
        Run test cases contained wihtin the test folder.
        """
        log.info("running tests")
        fail = False
        for module in TEST_MODULES:
#            tests = unittest.defaultTestLoader.loadTestsFromModule(module)
#            for test in tests:
#                result=unittest.TextTestRunner(verbosity=2).run(test)
#                fail = fail or not result.wasSuccessful()
            suite = module.suite()
            result = unittest.TextTestRunner(verbosity=2).run(suite)
            fail = fail or not result.wasSuccessful()
        if fail:
            raise DistutilsTestError('Exit the build due to a test error!')

class build_scripts(_build_scripts):

    def run(self):
        _build_scripts.run(self)
        self.fixversion()

    def fix_version(self):
        log.info("fix version on scripts")
        for script in self.scripts:
            outfile = os.path.join(self.build_dir, os.path.basename(script))
            fix_version(outfile, self.dry_run)

#cmdclass={'build_py': build_py}, used to test.
setup(cmdclass={'build_py': build_py, 'build_scripts': build_scripts},
      name='curi',
      version=VERSION,
      description='URI manipulation',
      author='Romain Gilles',
      author_email='romain dot gilles at gmail dot com',
      url='http://romain.gilles.free.fr',
      packages=['web'],
      package_dir={'':os.path.join('src', 'main', 'python')},
#      requires=['PyHamcrest'],
      scripts=[],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Software Development :: URI manipulation',
          ],
     )
