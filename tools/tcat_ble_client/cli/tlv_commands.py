"""
  Copyright (c) 2024, The OpenThread Authors.
  All rights reserved.

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are met:
  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.
  3. Neither the name of the copyright holder nor the
     names of its contributors may be used to endorse or promote products
     derived from this software without specific prior written permission.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
  POSSIBILITY OF SUCH DAMAGE.
"""

# from abc import abstractmethod
# from ble.ble_connection_constants import BBTC_SERVICE_UUID, BBTC_TX_CHAR_UUID, \
#     BBTC_RX_CHAR_UUID
# from ble.ble_stream import BleStream
# from ble.ble_stream_secure import BleStreamSecure
# from ble import ble_scanner
# from tlv.tlv import TLV
# from tlv.tcat_tlv import TcatTLVType
# from cli.command import Command, CommandResultNone, CommandResultTLV
# from dataset.dataset import ThreadDataset
# from utils import select_device_by_user_input
# from os import path
# from time import time
# from secrets import token_bytes
# from hashlib import sha256
# import hmac
# import binascii

from .base_commands import BleCommand, DataNotPrepared, CommandResultTLV
from ble.ble_stream_secure import BleStreamSecure
from enum import StrEnum
from tlv.tlv import TLV
from tlv.tcat_tlv import TcatTLVType


class TlvTreeCommands(StrEnum):
    LIST = "list"
    SEND = "send"


class TlvCommand(BleCommand):

    def get_log_string(self) -> str:
        return 'Sending custom TLV message...'

    def get_help_string(self) -> str:
        return 'Send custom TLV message.'

    async def execute_default(self, args, context):
        bless: BleStreamSecure = context['ble_sstream']

        # print(self.get_log_string())
        try:
            data = self.prepare_data(args, context)
            if data:
                response = await bless.send_with_resp(data)
                if not response:
                    return
                tlv_response = TLV.from_bytes(response)
                return CommandResultTLV(tlv_response)
            return None
        except DataNotPrepared as err:
            print('Command failed', err)

    def prepare_data(self, args, context):
        cmd = TlvTreeCommands(args[0])
        if cmd == TlvTreeCommands.LIST:
            list_tlv = "\n".join([f"{tlv.value:#x}\t{tlv.name}"
                                  for tlv in TcatTLVType])
            print(f"\n{list_tlv}")
            return None
        elif cmd == TlvTreeCommands.SEND:
            tlv_type = TcatTLVType(int(args[1], 16))
            tlv_value = bytes()
            try:
                tlv_value = bytes.fromhex(args[2])
            except IndexError:
                pass
            data = TLV(tlv_type.value, tlv_value).to_bytes()
            return data
