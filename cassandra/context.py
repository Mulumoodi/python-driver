# Copyright DataStax, Inc.
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

from cassandra.registry import MessageCodecRegistry
from cassandra.protocol import ProtocolHandler

__all__ = ['DriverContext']


class SingletonProvider(object):
    _obj = None
    _provider = None
    _args = None
    _kwargs = None

    def __init__(self, provider, *args, **kwargs):
        self._provider = provider
        self._args = args
        self._kwargs = kwargs

    def __call__(self):
        if self._obj is None:
            self._obj = self._provider(*self._args, **self._kwargs)
        return self._obj


class DriverContext(object):

    _message_codec_registry = None
    # the default protocol handler
    _protocol_handler = None

    def __init__(self):
        self._message_codec_registry = SingletonProvider(MessageCodecRegistry.factory)
        self._protocol_handler = SingletonProvider(
            ProtocolHandler,
            self._message_codec_registry().encoders,
            self._message_codec_registry().decoders)

    @property
    def message_codec_registry(self):
        return self._message_codec_registry()

    @property
    def protocol_handler(self):
        return self._protocol_handler()
