#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pmt
import zlib
import time
from gnuradio import gr

class crc_forwarder(gr.basic_block):
    """
    CRC32 Checker + Dedup + Forwarder (Message Reassembler)
    - Input : [sender_addr | seq_id | payload | crc32]
    - Output: [sender_addr | full_message] (only when END marker)
    - END marker = valid packet with empty payload
    - Adds parameter 'retry_limit' to retransmit ACKs multiple times
    """

    def __init__(self, retry_limit=1):
        gr.basic_block.__init__(
            self,
            name="CRC32 Dedup + Forwarder",
            in_sig=[],
            out_sig=[]
        )

        self.retry_limit = max(1, int(retry_limit))  # ensure >= 1

        self.received_ids = set()
        self.buffers = {}

        # Ports
        self.message_port_register_in(pmt.intern("in"))
        self.message_port_register_out(pmt.intern("out"))
        self.message_port_register_out(pmt.intern("ack_out"))

        self.set_msg_handler(pmt.intern("in"), self._handle_msg)

        print(f"[CRC32] Receiver initialized (retry_limit={self.retry_limit})")

    def _send_ack(self, ack_data):
        """Send ACK multiple times based on retry_limit."""
        ack_vec = pmt.init_u8vector(len(ack_data), list(ack_data))
        ack_pdu = pmt.cons(pmt.PMT_NIL, ack_vec)

        for i in range(self.retry_limit):
            self.message_port_pub(pmt.intern("ack_out"), ack_pdu)
            print(f"[ACK] Retransmit {i+1}/{self.retry_limit}")
            time.sleep(0.01)  # short delay (optional)

    def _handle_msg(self, msg):
        if not pmt.is_pair(msg):
            return
        vec = pmt.cdr(msg)
        if not pmt.is_u8vector(vec):
            return

        data = bytearray(pmt.u8vector_elements(vec))
        if len(data) < 6:
            print("[CRC32] Frame too short")
            return

        sender_addr = data[0]
        pkt_id = data[1]
        payload = data[2:-4]
        recv_crc = int.from_bytes(data[-4:], "big")

        calc_crc = zlib.crc32(bytes([sender_addr, pkt_id]) + payload) & 0xFFFFFFFF

        if calc_crc != recv_crc:
            print(f"[CRC32] FAIL (Addr=0x{sender_addr:02X}, ID={pkt_id})")
            return

        print(f"[CRC32] OK (Addr=0x{sender_addr:02X}, ID={pkt_id})")

        # --- Build ACK ---
        ack_data = bytearray([sender_addr, 0xAA, pkt_id])
        ack_crc = zlib.crc32(ack_data) & 0xFFFFFFFF
        ack_data += ack_crc.to_bytes(4, 'big')

        print(f"[ACK] Sending ACK with retry limit {self.retry_limit}")
        self._send_ack(ack_data)

        # Dedup
        if (sender_addr, pkt_id) in self.received_ids:
            print(f"[Forward] Duplicate packet ID={pkt_id}, ignored")
            return
        self.received_ids.add((sender_addr, pkt_id))

        # END MARKER
        if len(payload) == 0:
            if sender_addr in self.buffers and self.buffers[sender_addr]:
                full_payload = b''.join(self.buffers[sender_addr])
                forward_bytes = bytes([sender_addr]) + full_payload

                out_vec = pmt.init_u8vector(len(forward_bytes), list(forward_bytes))
                out_msg = pmt.cons(pmt.PMT_NIL, out_vec)
                self.message_port_pub(pmt.intern("out"), out_msg)

                print(f"[Forward] Reassembled {len(full_payload)} bytes")

            else:
                print(f"[Forward] END marker received but no data")

            self.buffers[sender_addr] = []
            return

        # Buffering
        if sender_addr not in self.buffers:
            self.buffers[sender_addr] = []

        self.buffers[sender_addr].append(payload)
        total_len = sum(len(p) for p in self.buffers[sender_addr])
        print(f"[Buffer] Addr 0x{sender_addr:02X}, ID {pkt_id}, +{len(payload)} bytes (total {total_len})")

