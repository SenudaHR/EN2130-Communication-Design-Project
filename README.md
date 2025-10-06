# EN2130-Communication-Design-Project
Two-Way Digital Paging System Using Software Defined Radios
## 📡 System Overview

This project implements a complete digital communication system featuring:

- **Dual-channel QPSK modulation/demodulation**
- **Go-Back-N ARQ protocol** for reliable data transfer
- **AES-128 encryption** for secure communications
- **WhatsApp-style GUI interfaces** for message sending and reception
- **Real-time signal visualization** with constellation plots and spectrum analysis
- **Simulated channel models** with configurable impairments

## 🏗️ System Architecture

### Transmitter Chain
Message GUI → ARQ Protocol → AES Encryption → Header Formatting → QPSK Modulation → Channel
### Receiver Chain  
Channel → Symbol Sync → Costas Loop → Equalization → QPSK Demodulation → CRC Check → AES Decryption → Message Display



### ARQ Protocol Features
- **Go-Back-N sliding window protocol**
- **Sequence numbering and ACK mechanisms**
- **Configurable retry limits and timeout settings**
- **End-of-message markers for packet reassembly**

## 🔧 Key Components

### Signal Processing Blocks
- **QPSK Modulator/Demodulator** with root-raised cosine filtering
- **Digital Symbol Synchronization** with polyphase filter banks
- **Costas Loop** for carrier phase and frequency recovery
- **Linear Equalizer** with CMA adaptive algorithm
- **Channel Model** with configurable noise, frequency offset, and timing drift

### Protocol Stack
- **`epy_block_2_0`**: Go-Back-N ARQ protocol implementation
- **`epy_block_4_0`**: CRC32 checking, deduplication, and message reassembly
- **`epy_block_0`/`epy_block_3`**: Address-based packet routing
- **Header Formatter**: Packet framing with access codes

### Security
- **`epy_block_5`/`epy_block_6`**: AES-128-CBC encryption/decryption
- **Configurable encryption keys** and initialization vectors

### User Interfaces
- **`epy_block_0_1_0`**: WhatsApp-style message sender with delivery status
- **`epy_block_3_1`**: Multi-sender message viewer with contact list
- **Real-time visualization**: Constellation plots, spectrum analyzers, time sinks

## 🚀 Installation & Usage

### Prerequisites
- GNU Radio Companion 3.10+
- Python 3.x
- PyQt5
- Cryptodome (for AES encryption)
- SoapySDR (for hardware support)

### Running the System
1. Open `cdp.grc` in GNU Radio Companion
2. Ensure all Python blocks are properly configured
3. Set desired parameters in the control panels
4. Execute the flowgraph

### Hardware Support
The system supports BladeRF SDR hardware with configurable:
- Center frequencies
- Sample rates
- RF gain settings
- Bandwidth configurations

## 🎛️ GUI Controls

### Channel Control Tab
- Noise voltage adjustment
- Frequency offset correction
- Timing offset compensation

### Receiver Control Tab
- Phase loop bandwidth tuning
- Equalizer adaptation rate
- Timing recovery settings

### Visualization Tabs
- **Constellation**: Real-time QPSK constellation display
- **Symbols**: Time-domain symbol visualization
- **Spectrum**: Frequency domain analysis

## 📊 Performance Features

- **Adaptive Equalization**: Compensates for channel distortions
- **Carrier Recovery**: Automatic frequency and phase correction
- **Timing Recovery**: Robust symbol timing synchronization
- **Error Detection**: CRC32 checksum verification
- **Packet Reassembly**: Message reconstruction from fragments

## 🔒 Security Implementation

The system uses AES-128-CBC encryption with:
- Configurable encryption keys
- Initialization vectors
- Secure packet encapsulation
- End-to-end encryption between GUI interfaces

## 🐛 Troubleshooting

### Common Issues
1. **Python import errors**: Ensure all required packages are installed
2. **SDR hardware not detected**: Verify SoapySDR drivers and connections
3. **GUI not loading**: Check PyQt5 installation and dependencies
4. **Poor reception**: Adjust channel parameters and equalizer settings

### Performance Optimization
- Adjust loop bandwidths for faster convergence
- Modify equalizer taps for specific channel conditions
- Tune ARQ parameters for network characteristics
- Optimize sample rates for hardware capabilities

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.



---

**Note**: This system is designed for educational and research purposes. Ensure compliance with local regulations when transmitting radio signals.


