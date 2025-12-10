# EN2130-Communication-Design-Project
## 📡 Two-Way Digital Paging System Using Software Defined Radios

> **Core Concept:** This project is a comprehensive **Software-Defined Radio (SDR) platform** that implements a complete digital communication protocol stack. It integrates **QPSK** physical layer transmission, **Go-Back-N ARQ** for reliable data transfer, and **AES-128 encryption** for secure communications through intuitive user interfaces.

---

## ✨ System Architecture and Core Features

### Protocol Stack Overview 🧱
The system follows a 5-layer model based on the TCP/IP stack:

| Layer | Key Components | Core Functionality |
| :--- | :--- | :--- |
| **Application** | WhatsApp-style GUI | Message input/output, Delivery status display, Multi-sender management. |
| **Transport** | **Go-Back-N ARQ** | Sequence numbering, ACK handling, Retransmission management. |
| **Network** | Addressing | Node addressing, Packet routing, Multi-node support (up to 256 stations). |
| **Data Link** | CRC32 Checker | Frame formatting, CRC32 error checking, Packet deduplication. |
| **Physical** | QPSK Modulator/Demodulator | **QPSK Modulation**, Carrier recovery, **Symbol Synchronization**. |

### Data Flow Chains
* **Transmitter Chain:** GUI $\rightarrow$ ARQ Protocol $\rightarrow$ CRC Append / AES-128 Encryption $\rightarrow$ Addressing $\rightarrow$ **QPSK Modulator** $\rightarrow$ Channel.
* **Receiver Chain:** Channel $\rightarrow$ **QPSK Demodulator / Symbol Synchronization** $\rightarrow$ Address Checker $\rightarrow$ AES-128 Decryption $\rightarrow$ CRC32 Checker / ACK Handler $\rightarrow$ Multi-Sender GUI.


---

## 🔑 Key Technical Components

### 1. Physical Layer DSP ⚙️

| Component | Function | Implementation Detail |
| :--- | :--- | :--- |
| **QPSK Modulation/Demodulation** | Encodes and decodes 2 bits per symbol. | Uses a rectangular constellation with **4-ary arity**. |
| **Pulse Shaping (RRC Filter)** | Reduces Inter-Symbol Interference (ISI). | Implemented using a **Root-Raised Cosine (RRC) filter** within a Polyphase Filter Bank (PFB). |
| **Symbol Synchronization** | Corrects symbol timing error ($\epsilon$). | Achieved using the `digital_symbol_sync_xx` block to reliably determine the correct sampling instant. |
| **Carrier Recovery** | Corrects phase and fine frequency offset. | Implemented using the **Costas Loop** (`digital_costas_loop_cc_0`). |
| **Adaptive Equalization** | Mitigates channel distortion (ISI). | Uses a **Linear Equalizer** with the **Constant Modulus Algorithm (CMA)** for adaptation. |

### 2. Transport and Data Link Layers

* **Go-Back-N ARQ:** The sender retransmits from the first unacknowledged frame if an ACK timeout occurs or a CRC failure is reported by the receiver.
* **Packet Framing:** Frames include a 64-bit Access Code, Packet Length, Sender Address, Sequence ID, CRC-32, and an **AES-128 Encrypted Payload**.

### 3. Security: Dynamic AES-128 Encryption

* **Encryption Standard:** **AES-128** is used for payload security (`epy_block_5`/`epy_block_6`).
* **Key Management:** The encryption key is **dynamically calculated** based on the receiver's address. This ensures that only the intended recipient possesses the correct key for decryption.

### 4. Hardware and Channelization (FDMA)

* **SDR Hardware:** **Dual bladeRF 2.0 Setup** (Nuand).
* **FDMA:** **Frequency Division Multiple Access** is used for full-duplex operation:
    * **Data Channel (Upstream):** 2.4 GHz ISM Band.
    * **ACK Channel (Downstream):** 5.8 GHz ISM Band.
    * This prevents contention and enables simultaneous Tx/Rx operations.

---

## 🚀 Installation & Usage

### Prerequisites
* **Operating System:** **Ubuntu** is highly recommended, as **Nuand bladeRF 2.0 drivers** were noted as unstable on Windows.
* GNU Radio Companion 3.10+
* Python 3.x, PyQt5, Cryptodome, SoapySDR.

### Downloading Nuand bladeRF Drivers (Linux/Ubuntu)

The official `libbladeRF` library provides the necessary drivers and utilities.

1.  **Install Dependencies:**
    ```bash
    sudo apt install git build-essential cmake libusb-1.0-0-dev
    ```
2.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/Nuand/bladeRF.git](https://github.com/Nuand/bladeRF.git)
    cd bladeRF/host
    ```
3.  **Build and Install:**
    ```bash
    mkdir build && cd build
    cmake ../
    make
    sudo make install
    ```
4.  **Configure udev Rules (for non-root access):**
    ```bash
    sudo cp ../libraries/libbladeRF/platform/linux/99-libbladerf.rules /etc/udev/rules.d/
    sudo udevadm control --reload-rules
    # Re-plug the bladeRF device after this step.
    ```
5.  **Install Gr-OSMOSDR:** This provides the GNU Radio source/sink blocks for the hardware.
    ```bash
    # (Follow standard gr-osmosdr build process, ensuring bladeRF support is enabled)
    ```

### Running the System
1.  Open `cdp.grc` in GNU Radio Companion.
2.  Ensure hardware parameters (e.g., center frequency, gain) are correctly set.
3.  Execute the flowgraph:
    ```bash
    python3 cdp.py
    ```

---

## 📊 Performance and Challenges

| Metric | Value | Units |
| :--- | :--- | :--- |
| **Data Rate** | **175** | **Bps** |
| Sample Rate | 1.2 | MHz |
| Synchronization Bits | 10,000 | bits |
| Modulation | QPSK | N/A |
| Max Distance |15(?)| m |

### Synchronization Challenge Resolution
* **Issue:** Short messages led to receiver failure as the timing loops couldn't lock.
* **Solution:** A preamble of **$\approx 10,000$ random synchronization bits** was prepended to every message.
* **Impact:** While guaranteeing lock, this significantly **decreased the effective data rate** to 175 Bps.

---

## 🤝 Future Works

* **Data Rate Optimization:** Finding better synchronization methods using **fewer bits**.
* **Multimedia Support:** Adding support for Video, image, PDF, and voice transmission.
* **Collision Avoidance:** Implementing **CSMA/CA** (Carrier Sense Multiple Access with Collision Avoidance).
* **Priority Handling:** Implementing priority-based message handling for emergency messages.
