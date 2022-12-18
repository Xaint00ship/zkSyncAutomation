import base58
import binascii


class Ipfs2bytes32:

    def ipfscidv0_to_byte32(self, cid):
        decoded = base58.b58decode(cid)
        sliced_decoded = decoded[2:]
        print(sliced_decoded)
        print(binascii.b2a_hex(sliced_decoded))
        return "0x" + binascii.b2a_hex(sliced_decoded).decode("utf-8")

    def byte32_to_ipfscidv0(self, hexstr):

        binary_str = binascii.a2b_hex(hexstr)
        completed_binary_str = b'\x12 ' + binary_str
        return base58.b58encode(completed_binary_str).decode("utf-8")

