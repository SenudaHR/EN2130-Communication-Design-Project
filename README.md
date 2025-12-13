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
## Ettus Research USRP N210 Setup (Alternative)

This guide explains how to set up the **Ettus Research USRP N210** using **UHD (USRP Hardware Driver)** and run the GNU Radio project.

---

### 1. Network Configuration

The USRP N210 communicates over **Gigabit Ethernet**.

* **USRP default IP:** `192.168.10.2`
* **Host PC IP:** `192.168.10.1` (or any IP in `192.168.10.x`, except `.2`)

#### Steps (Linux)

1. Connect the USRP N210 directly to your PC using a **Gigabit Ethernet** cable.
2. Set the Ethernet interface IP manually:

```bash
sudo ip addr add 192.168.10.1/24 dev eth0
sudo ip link set eth0 up
```

> Replace `eth0` with your actual Ethernet interface name (check using `ip a`).

3. Verify connectivity:

```bash
ping 192.168.10.2
```

A successful reply confirms correct network configuration.

---

### 2. Install UHD (USRP Hardware Driver)

#### a. Install Dependencies

```bash
sudo apt update
sudo apt install -y \
  git \
  cmake \
  build-essential \
  python3-dev \
  libboost-all-dev \
  libusb-1.0-0-dev
```

---

#### b. Clone and Build UHD

```bash
git clone https://github.com/EttusResearch/uhd.git
cd uhd

git checkout release_4.6   # Use a stable UHD release

mkdir build && cd build
cmake ..
make -j$(nproc)
sudo make install
sudo ldconfig
```

> ⚠️ Building UHD from source may take several minutes.

---

### 3. Download Firmware and FPGA Images

After installing UHD, download the required firmware and FPGA images:

```bash
sudo uhd_images_downloader
```

This step is **mandatory** for proper USRP operation.

---

### 4. Verify Installation

Check whether the USRP N210 is detected correctly:

```bash
uhd_find_devices
```

#### Expected Output (Example)

* Device type: `usrp2 / n210`
* IP address: `192.168.10.2`

If the device is listed, UHD is correctly installed and the network setup is successful.

---

### 5. Running the Project

#### a. Open the GNU Radio Flowgraph

1. Launch **GNU Radio Companion (GRC)**.
2. Open the main flowgraph:

```bash
cd <project-directory>
gnuradio-companion cdp.grc
```

---

### b. Configure Hardware Parameters

Inside the flowgraph, set the appropriate parameters for your SDR:

* **Center Frequency** (Tx/Rx)
* **Gain** (RF / IF / BB as applicable)
* **Sample Rate**
* **Device Type**: `USRP N210` or `bladeRF`

Ensure the correct device is selected before execution.

---

### c. Generate and Execute Python File

From GNU Radio Companion:

1. Click **Generate**
2. Click **Execute**

Or run directly from the terminal:

```bash
python3 cdp.py
```

---

### Notes

* Ensure no other application is using the Ethernet interface connected to the USRP.
* Always verify **Gigabit Ethernet** link speed for stable operation.
* Use appropriate RF front-end settings to avoid signal distortion or hardware damage.

---

### Troubleshooting

* **Device not found:**

  * Recheck IP configuration
  * Disable NetworkManager control for the Ethernet interface
* **Packet loss / underflows:**

  * Reduce sample rate
  * Confirm Gigabit Ethernet connection

---

✅ USRP N210 setup and project execution complete.


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
## License & contact
- License: (Add project license file, e.g., MIT or GPL — update LICENSE file as appropriate).
- Contact / owner: SenudaHR (repository owner). Open issues or PRs in the repo for questions and contributions.

## Acknowledgements
- Nuand bladeRF and GNU Radio projects — this work builds on their hardware and software.


```
