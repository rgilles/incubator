#!/usr/bin/env python
# encoding: utf-8
#
# Copyright 2012 Romain Gilles
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from distutils.cmd import Command
from distutils.command.build_py import build_py as _build_py
from distutils.errors import DistutilsError
from distutils.core import setup
from distutils.command.build_scripts import build_scripts as _build_scripts
from distutils.command.clean import clean as _clean
from distutils import log
import fnmatch
from ftplib import FTP
from shutil import rmtree
from subprocess import  Popen
import sys
from time import sleep
import unittest
import os

PYTHON_CACHE = "__pycache__"
sys.path.append(os.path.join(sys.path[0], 'src', 'main', 'python'))
sys.path.append(os.path.join(sys.path[0], 'src', 'test', 'python'))
from webtest import urilibtest, assertiontest, itest, curilibtest
from webtest.webserver import DEFAULT_PORT_NUMBER

MANIFEST_FILE_NAME = "MANIFEST"

VERSION_TAG = '${version}'

VERSION = '1.0-SNAPSHOT'

TEST_MODULES = [urilibtest,
                assertiontest,
                curilibtest,
                ]
ITEST_MODULES = [itest]

class DistutilsTestError(DistutilsError):
    """Unable to complite the test without errors."""
    pass


def fix_version(outfile, dry_run):
    try:
        with open(outfile) as f:
            lines = []
            to_substitute = False
            for line in f:
                if line.find(VERSION_TAG) > -1:
                    to_substitute = True
                    line = line.replace(VERSION_TAG, VERSION)
                lines.append(line)
        if to_substitute:
            log.info("version tag substituted in %s", os.path.basename(outfile))
            with open(outfile, 'w') as f:
                f.writelines(lines)
    except IOError:
        if not dry_run:
            raise


class Deploy(Command):
    description = "publish distribution archive to the remote repository"
    user_options = [
        ('user=', 'u',
         "user name"),
        ('password=', 'p',
         "password"),
        ('dist-dir=', 'd',
         "directory to put final built distributions in "
         "[default: dist]"),
        ('server=', 's', "ftp url where distribution archives have to be published. [default: freeperso.free.fr]" )
    ]

    def initialize_options(self):
        self.user = None
        self.password = None
        self.dist_dir = None
        self.server = None

    def finalize_options(self):
        self.set_undefined_options('bdist',
            ('dist_dir', 'dist_dir'))
        if self.dist_dir is None:
            self.dist_dir = "dist"

        if self.server is None:
            self.server = "ftpperso.free.fr"

        if self.user is None:
            self.user = input("user: ")

        if self.password is None:
            self.password = input("password: ")

    def get_dist_files(self):
        if self.distribution.dist_files is not None and len(self.distribution.dist_files) > 0:
            for _, _, file_path in self.distribution.dist_files:
                yield file_path
        else:
            base_dir = self.distribution.get_fullname()
            for file in os.listdir(self.dist_dir):
                file_path = os.path.join(self.dist_dir, file)
                if os.path.isfile(file_path) and fnmatch.fnmatch(file, "{0}.*".format(base_dir)):
                    yield file_path

    def run(self):
        # Figure out which sub-commands we need to run.
        log.info("start publishing on server [%s]: ", self.server)
        if not os.path.isdir(self.dist_dir):
            log.info("no distribution to publish cannot find distribution folder '%s'", self.dist_dir)
            return

        with FTP(self.server) as ftp:
            ftp.login(self.user, self.password)
            ftp.cwd("curi")
            for file_path in self.get_dist_files():
                log.info("publish file: '%s'", file_path)
                #toto test dry-run mode
                if self.dry_run:
                    log.info("send stor action: 'STOR %s'", os.path.basename(file_path))
                else:
                    ftp.storbinary("STOR {0}".format(os.path.basename(file_path)), open(file_path, 'rb'))


class Clean(_clean):
    def run(self):
        super().run()
        if os.path.isfile(MANIFEST_FILE_NAME):
            log.info("remove generated manifest file")
            os.remove(MANIFEST_FILE_NAME)
        if os.path.isdir(PYTHON_CACHE):
            log.info("remove python cache directory: %s", PYTHON_CACHE)
            rmtree(PYTHON_CACHE)


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
        test()


class Test(Command):
    description = "Launch test use cases"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        test()


def test(test_modules=TEST_MODULES, message="running tests"):
    """
    Run test cases contained wihtin the test folder.
    """
    log.info(message)
    fail = False
    for module in test_modules:
        suite = module.suite()
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        fail = fail or not result.wasSuccessful()
    if fail:
        raise DistutilsTestError('Exit due to a test error!')


class Verify(Command):
    description = "Verify package by running the integration tests agains a local http server"
    user_options = [
        ('port=', 'p',
         "port number for the http server (default: {0})".format(DEFAULT_PORT_NUMBER)),
    ]

    def initialize_options(self):
        self.port = None

    def finalize_options(self):
        if self.port is None:
            self.port = DEFAULT_PORT_NUMBER
        else:
            self.port = int(self.port)

    def run(self):
        #startup the web server
        log.info("integration test run on port %d", self.port)
        p = Popen(
            "python {0} --port={1}".format(os.path.join("src", "test", "python", "webtest", "webserver.py"), self.port),
            shell=True)
        try:
            # p = Process(target=webserver.start, args=(self.port,))
            # process based solution does not work :(
            # p.start()
            log.info("wait 2s server startup...") #todo replace it by synchro mechanism
            sleep(2)
            test(ITEST_MODULES, "running integration tests")
        finally:
            log.info("shutdown the web server")
            p.terminate()


class build_scripts(_build_scripts):
    def run(self):
        _build_scripts.run(self)
        self.fix_version()

    def fix_version(self):
        log.info("fix version on scripts")
        for script in self.scripts:
            outfile = os.path.join(self.build_dir, os.path.basename(script))
            fix_version(outfile, self.dry_run)

#cmdclass={'build_py': build_py}, used to test.
setup(
    cmdclass={'build_py': build_py, 'build_scripts': build_scripts, 'clean': Clean, 'deploy': Deploy, 'verify': Verify,
              'test': Test},
    name='curi',
    version=VERSION,
    description='URI manipulation',
    author='Romain Gilles',
    author_email='romain dot gilles at gmail dot com',
    url='http://romain.gilles.free.fr',
    packages=['web'],
    package_dir={'': os.path.join('src', 'main', 'python')},
    #      requires=['PyHamcrest'],
    scripts=[os.path.join('src', 'main', 'scripts', 'curi.py'), os.path.join('src', 'main', 'scripts', 'curi')],
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
