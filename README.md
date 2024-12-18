
# Traffic Classifier

The main objective of this project is to develop and implement a robust 
machine learning-based traffic classification system, capable of accurately identifying 
different types of network traffic flows based on packet information. This 
system will be deployed in a software-defined network environment using Open 
vSwitch (OVS) and will use traffic data generated by a traffic generation tool.

## Features
- Traffic classification using deep learning and machine learning models.
- Real-time traffic monitoring with D-IGT commands.
- Support for various traffic types like VoIP, Quake3, Telnet, DNS, etc.
- Network slicing: Prioritization of traffic into slices such as gaming, voice, and other types to enhance Quality of Service (QoS).

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

## Installation Steps

### Install Required Tools and Libraries

1. **Install Python 3 and Pip**  
   Ensure you have Python 3 installed. Check with:
   ```bash
   python3 --version
   pip3 --version
   ```

2. **Install Required Python Packages**
   Use `pip` to install the required Python libraries:
   ```bash
   pip3 install numpy
   pip3 install prettytable
   pip3 install scikit-learn

   ```

3. **Install D-ITG**
   Download and compile D-ITG:
   ```bash
   git clone https://github.com/jbucar/ditg.git
   cd ditg
   make
   sudo make install
   ```

4. **Install Mininet**
   Download and install Mininet:
   ```bash
   sudo apt-get install mininet
   ```

5. **Install Open vSwitch**
   Install Open vSwitch:
   ```bash
   sudo apt-get install openvswitch-switch
   ```

6. **Install Ryu**
   Install Ryu Controller:
   ```bash
   pip3 install ryu
   ```


## Usage

### Starting Mininet Topology
Run the following command to create a basic topology:
```bash
sudo mn --topo single,3 --mac --controller remote --switch ovs,protocols=OpenFlow13
```

### Real-Time Traffic Prediction
Start real-time prediction:
```bash
python3 traffic_classifier.py kneighbors
```

### Generate Traffic with D-IGT
Start the Receiver :

```bash
   ITGRecv -l /tmp/receiver1.log
```
Execute predefined commands for generating different traffic types:
- **VoIP Traffic**: 
  ```bash
   ITGSend -a 10.0.0.1 -rp 10001 VoIP -x G.711.2 -h RTP -VAD
  ```
- **Quake3 Traffic**:
  ```bash
   ITGSend -a 10.0.0.1 -rp 10002 Quake3
  ```
- **Telnet Traffic**:
  ```bash
   ITGSend -a 10.0.0.1 -rp 10002 Telnet
  ```
- **CSa Traffic**:
  ```bash
   ITGSend -a 10.0.0.1 -rp 10002 CSa
  ```
- **DNS Traffic**:
  ```bash
   ITGSend -a 10.0.0.1 -rp 10003 DNS
  ```

## Contributing
Feel free to fork this repository, make modifications, and submit pull requests.

## License
This project is licensed under the MIT License.
