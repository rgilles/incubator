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
__author__ = 'Romain Gilles'


def iterable(value):
    return hasattr(value, '__iter__') or hasattr(value, '__getitem__')


def is_class(type_):
    return hasattr(type_, "__base__")

class IllegalArgumentError (AssertionError):
    pass

def raise_illegal_argument(message):
    raise IllegalArgumentError(message)

def assert_that_argument_is_not_none(argument, argument_name):
    if argument is None:
        raise_illegal_argument("{0} must be not None".format(argument_name))

def assert_that_argument_type_is(argument, class_or_type_or_tuple, argument_name):
    """
    Return whether an object is an instance of a class or of a subclass thereof.
    With a type as second argument, return whether that is the object's type.
    The form using a tuple, isinstance(x, (A, B, ...)), is a shortcut for
    isinstance(x, A) or isinstance(x, B) or ... (etc.).
    """
    if not isinstance(argument, class_or_type_or_tuple):
        raise_illegal_argument("{0} type must be{1}: {2}".format(argument_name, "" if is_class(class_or_type_or_tuple) else " one of",str(class_or_type_or_tuple)))


