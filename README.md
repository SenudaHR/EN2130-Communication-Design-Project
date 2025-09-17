# EN2130-Communication-Design-Project
Two-Way Digital Paging System Using Software Defined Radios
## QPSK with Stop-and-Wait ARQ (GNU Radio + BladeRF)

This project implements a **reliable wireless communication system** using **QPSK modulation** and a **Stop-and-Wait ARQ protocol**.  
It is built in **GNU Radio Companion (GRC)** with custom embedded Python blocks, and tested with **BladeRF 2.9 Micro** SDR hardware.

---

## 📑 Features
- **QPSK Modulation/Demodulation**
  - Bandwidth-efficient (2 bits/symbol)
  - Gray-coded constellation mapping
- **Packet Handling**
  - CRC-32 error detection
  - Addressing (accept/reject based on destination address)
  - Length tagging for proper packetization
- **ARQ Mechanism**
  - Stop-and-Wait ARQ with ACK feedback
  - Retransmission on missing/failed ACK
- **Synchronization**
  - Symbol synchronization (`pfb_clock_sync_ccf`)
  - Carrier recovery (`costas_loop_cc`)
  - Linear equalizer for multipath mitigation
- **Hardware**
  - Compatible with BladeRF SDRs
  - Adjustable RF/IF/TX gains via GUI

---

## 📂 Project Structure

---

## 🔧 How It Works
1. **Transmission**
   - Read text file → segment into PDUs (1500-byte MTU)
   - Add address + CRC
   - Convolutional encoding + QPSK modulation
   - Transmit via BladeRF

2. **Reception**
   - BladeRF captures baseband signal
   - Symbol synchronization + Costas loop carrier recovery
   - Equalizer corrects multipath/frequency offset
   - Demodulation → decoding → CRC check

3. **ARQ Feedback**
   - If CRC + address are correct → send **ACK** back
   - If ACK not received → retransmit last frame
   - Implements **Stop-and-Wait ARQ**

---

## 🖥️ Requirements
- [GNU Radio 3.10+](https://wiki.gnuradio.org)
- [BladeRF drivers & SoapySDR](https://github.com/Nuand/bladeRF)
- Python 3.8+
- Qt5 (for GUI)

