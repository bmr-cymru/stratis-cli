# Copyright 2016 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Miscellaneous methods to support testing.
"""

import abc
import os
import string
import subprocess

from hypothesis import strategies

from ._constants import _STRATISD
from ._constants import _STRATISD_EXECUTABLE
from ._constants import _STRATISD_RUST


def _device_list(minimum):
    """
    Get a device generating strategy.

    :param int minimum: the minimum number of devices, must be at least 0
    """
    return strategies.lists(
       strategies.text(
          alphabet=string.ascii_letters + "/",
          min_size=1
       ),
       min_size=minimum
    )


class ServiceABC(abc.ABC):
    """
    Abstract base class of Service classes.
    """

    @abc.abstractmethod
    def setUp(self):
        """
        Start the stratisd daemon with the simulator.
        """
        raise NotImplementedError()

    def tearDown(self):
        """
        Stop the stratisd simulator and daemon.
        """
        # pylint: disable=no-member
        self._stratisd.terminate()
        self._stratisd.wait()


class ServiceC(ServiceABC):
    """
    Handle starting and stopping the C service.
    """

    def setUp(self):
        env = dict(os.environ)
        env['LD_LIBRARY_PATH'] = os.path.join(_STRATISD, 'lib')

        bin_path = os.path.join(_STRATISD, 'bin')

        self._stratisd = subprocess.Popen(
           os.path.join(bin_path, _STRATISD_EXECUTABLE),
           env=env
        )


class ServiceR(ServiceABC):
    """
    Handle starting and stopping the Rust service.
    """

    def setUp(self):
        self._stratisd = subprocess.Popen(
           [os.path.join(_STRATISD_RUST, 'target/debug/stratisd'), '--sim']
        )


Service = ServiceR
