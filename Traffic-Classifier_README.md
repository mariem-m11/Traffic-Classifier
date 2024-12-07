
# Traffic Classifier

This project focuses on intelligent traffic classification using supervised machine learning algorithms and real-time data monitoring. The repository includes Python scripts, datasets, and configurations for network traffic emulation and analysis.

## Features
- Traffic classification using K-Nearest Neighbors (KNN).
- Real-time traffic monitoring with D-IGT commands.
- Support for various traffic types like VoIP, Quake3, Telnet, DNS, etc.

## Repository Structure
- `Models/`: Contains machine learning models used for traffic classification.
- `Notebooks/`: Jupyter notebooks for experimentation and visualization.
- `datasets/`: Traffic datasets used for training and testing.
- `D-IGT_cmd/`: Predefined D-IGT commands for traffic generation.
- `Knn.py`: Implementation of the K-Nearest Neighbors algorithm for classification.
- `traffic_classifier.py`: Main script for traffic classification.
- `simple_monitor_13.py`: Script for real-time traffic monitoring.

## Installation

### Requirements
- Python 3.7+
- Mininet
- Open vSwitch
- D-IGT

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/mariem-m11/Traffic-Classifier.git
   cd Traffic-Classifier
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install D-IGT:
   [D-IGT Installation Guide](https://github.com/jbucar/ditg)
4. Install Mininet:
   [Mininet Installation Guide](http://mininet.org/download/)
5. Install Open vSwitch:
   [Open vSwitch Installation Guide](https://www.openvswitch.org/download/)

## Usage

### Starting Mininet Topology
Run the following command to create a basic topology:
```bash
sudo mn --topo single,3 --mac --switch ovsk --controller remote
```

### Real-Time Traffic Prediction
Start real-time prediction:
```bash
python3 traffic_classifier.py supervised
```

### Generate Traffic with D-IGT
Execute predefined commands for different traffic types:
- **VoIP Traffic**: 
  ```bash
  ./ITGSend -a 10.0.0.1 -rp 10001 VoIP -x G.711.2 -h RTP -VAD
  ```
- **Quake3 Traffic**:
  ```bash
  ./ITGSend -a 10.0.0.1 -rp 10002 Quake3
  ```
- **Telnet Traffic**:
  ```bash
  ./ITGSend -a 10.0.0.1 -rp 10002 Telnet
  ```
- **CSa Traffic**:
  ```bash
  ./ITGSend -a 10.0.0.1 -rp 10002 CSa
  ```
- **DNS Traffic**:
  ```bash
  ./ITGSend -a 10.0.0.1 -rp 10003 DNS
  ```

## Contributing
Feel free to fork this repository, make modifications, and submit pull requests.

## License
This project is licensed under the MIT License.
