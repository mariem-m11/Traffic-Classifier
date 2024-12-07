######################################################traffic_slicer.py######################################################
#!/usr/bin/python

# Importing libraries
from prettytable import PrettyTable
import subprocess
import sys
import signal
import os
import numpy as np
import pickle

# Ryu command
cmd = "sudo ryu run simple_monitor_13.py"

flows = {}  # Dictionary to store flow information
TIMEOUT = 15 * 60  # 15 minutes

# Define slices and their priorities
slices = {
    "game": {"priority": 1, "flows": []},
    "voice": {"priority": 2, "flows": []},
    "other": {"priority": 3, "flows": []}  # Includes pin, DNS, telnet
}

class Flow:
    def __init__(self, time_start, datapath, inport, ethsrc, ethdst, outport, packets, bytes):
        self.time_start = time_start
        self.datapath = datapath
        self.inport = inport
        self.ethsrc = ethsrc
        self.ethdst = ethdst
        self.outport = outport
        self.forward_packets = packets
        self.forward_bytes = bytes
        self.forward_delta_packets = 0
        self.forward_delta_bytes = 0
        self.forward_inst_pps = 0.00
        self.forward_avg_pps = 0.00
        self.forward_inst_bps = 0.00
        self.forward_avg_bps = 0.00
        self.forward_status = "ACTIVE"
        self.forward_last_time = time_start
        self.reverse_packets = 0
        self.reverse_bytes = 0
        self.reverse_delta_packets = 0
        self.reverse_delta_bytes = 0
        self.reverse_inst_pps = 0.00
        self.reverse_avg_pps = 0.00
        self.reverse_inst_bps = 0.00
        self.reverse_avg_bps = 0.00
        self.reverse_status = "INACTIVE"
        self.reverse_last_time = time_start

    def updateforward(self, packets, bytes, curr_time):
        self.forward_delta_packets = packets - self.forward_packets
        self.forward_packets = packets
        if curr_time != self.time_start:
            self.forward_avg_pps = packets / float(curr_time - self.time_start)
        if curr_time != self.forward_last_time:
            self.forward_inst_pps = self.forward_delta_packets / float(curr_time - self.forward_last_time)

        self.forward_delta_bytes = bytes - self.forward_bytes
        self.forward_bytes = bytes
        if curr_time != self.time_start:
            self.forward_avg_bps = bytes / float(curr_time - self.time_start)
        if curr_time != self.forward_last_time:
            self.forward_inst_bps = self.forward_delta_bytes / float(curr_time - self.forward_last_time)
        self.forward_last_time = curr_time

        if self.forward_delta_bytes == 0 or self.forward_delta_packets == 0:
            self.forward_status = "INACTIVE"
        else:
            self.forward_status = "ACTIVE"

    def updatereverse(self, packets, bytes, curr_time):
        self.reverse_delta_packets = packets - self.reverse_packets
        self.reverse_packets = packets
        if curr_time != self.time_start:
            self.reverse_avg_pps = packets / float(curr_time - self.time_start)
        if curr_time != self.reverse_last_time:
            self.reverse_inst_pps = self.reverse_delta_packets / float(curr_time - self.reverse_last_time)

        self.reverse_delta_bytes = bytes - self.reverse_bytes
        self.reverse_bytes = bytes
        if curr_time != self.time_start:
            self.reverse_avg_bps = bytes / float(curr_time - self.time_start)
        if curr_time != self.reverse_last_time:
            self.reverse_inst_bps = self.reverse_delta_bytes / float(curr_time - self.reverse_last_time)
        self.reverse_last_time = curr_time

        if self.reverse_delta_bytes == 0 or self.reverse_delta_packets == 0:
            self.reverse_status = "INACTIVE"
        else:
            self.reverse_status = "ACTIVE"

#def printclassifier(model):
#    x = PrettyTable()
#    x.field_names = ["Flow ID", "Src MAC", "Dest MAC", "Traffic Type", "Slice", "Priority"]

#    for key, flow in flows.items():
 #       features = np.asarray([
  #          flow.forward_delta_packets, flow.forward_delta_bytes, flow.forward_inst_pps,
   #         flow.forward_avg_pps, flow.forward_inst_bps, flow.forward_avg_bps,
    #        flow.reverse_delta_packets, flow.reverse_delta_bytes, flow.reverse_inst_pps,
     #       flow.reverse_avg_pps, flow.reverse_inst_bps, flow.reverse_avg_bp



        # Add flow to the appropriate slice
     #   slices[slice_name]["flows"].append(flow)
       
    #    x.add_row([key, flow.ethsrc, flow.ethdst, traffic_type, slice_name, slices[slice_name]["priority"]])


def printclassifier(model):
    x = PrettyTable()
    x.field_names = ["Flow ID", "Src MAC", "Dest MAC", "Traffic Type", "Slice", "Priority"]

    for key, flow in flows.items():
        features = np.asarray([
            flow.forward_delta_packets, flow.forward_delta_bytes, flow.forward_inst_pps,
            flow.forward_avg_pps, flow.forward_inst_bps, flow.forward_avg_bps,
            flow.reverse_delta_packets, flow.reverse_delta_bytes, flow.reverse_inst_pps,
            flow.reverse_avg_pps, flow.reverse_inst_bps, flow.reverse_avg_bps
        ]).reshape(1, -1)
       
        label = model.predict(features.tolist())
        traffic_type = str(label[0]).strip()  # Ensure it's a string and stripped

        # Use a dictionary to map label to slice and traffic_type
        traffic_dict = {
            "dns": ("dns", "other"),
            "game": ("game", "game"),
            "ping": ("ping", "other"),
            "quake": ("quake", "game"),
            "telnet": ("telnet", "other"),
            "voice": ("voice", "voice"),
        }

        traffic_type, slice_name = traffic_dict.get(traffic_type, ("unknown", "other"))

        # Add flow to the appropriate slice
        slices[slice_name]["flows"].append(flow)
       
        x.add_row([key, flow.ethsrc, flow.ethdst, traffic_type, slice_name, slices[slice_name]["priority"]])
   
    print(x)




# Function to print flow attributes when collecting training data
def printflows(traffic_type,f):
    for key,flow in flows.items():

        outstring = '\t'.join([
        str(flow.forward_packets),
        str(flow.forward_bytes),
        str(flow.forward_delta_packets),
        str(flow.forward_delta_bytes),
        str(flow.forward_inst_pps),
        str(flow.forward_avg_pps),
        str(flow.forward_inst_bps),
        str(flow.forward_avg_bps),
        str(flow.reverse_packets),
        str(flow.reverse_bytes),
        str(flow.reverse_delta_packets),
        str(flow.reverse_delta_bytes),
        str(flow.reverse_inst_pps),
        str(flow.reverse_avg_pps),
        str(flow.reverse_inst_bps),
        str(flow.reverse_avg_bps),
        str(traffic_type)])
        f.write(outstring+'\n')
       




def run_ryu(p, model=None):
    time = 0
    while True:
        out = p.stdout.readline()
        if out == "" and p.poll() is not None:
            break
        if out != "" and out.startswith(b"data"):
            fields = out.split(b"\t")[1:]
            fields = [f.decode("utf-8") for f in fields]
            unique_id = hash("".join([fields[1], fields[3], fields[4]]))
            if unique_id in flows:
                flows[unique_id].updateforward(int(fields[6]), int(fields[7]), int(fields[0]))
            else:
                rev_unique_id = hash("".join([fields[1], fields[4], fields[3]]))
                if rev_unique_id in flows:
                    flows[rev_unique_id].updatereverse(int(fields[6]), int(fields[7]), int(fields[0]))
                else:
                    flows[unique_id] = Flow(int(fields[0]), fields[1], fields[2], fields[3], fields[4], fields[5], int(fields[6]), int(fields[7]))
            if model is not None and time % 10 == 0:
                printclassifier(model)
        time += 1

def printHelp():
    print("\nUsage: sudo python traffic_classifier.py [subcommand] [options]")
    print("\n\tSUBCOMMANDS: 'logistic', 'kmeans', 'svm', 'Randomforest'")
    return


if __name__ == '__main__':
    SUBCOMMANDS = ('train', 'logistic', 'kmeans', 'knearest', 'svm', 'Randomforest', 'gaussiannb')

    if len(sys.argv) < 2:
        print("ERROR: Incorrect # of args")
        print()
        printHelp()
        sys.exit();
    else:
        if len(sys.argv) == 2:
            if sys.argv[1] not in SUBCOMMANDS:
                print("ERROR: Unknown subcommand argument.")
                print("       Currently subaccepted commands are: %s" % str(SUBCOMMANDS).strip('()'))
                print()
                printHelp()
                sys.exit();

    if len(sys.argv) == 1:
        # Called with no arguments
        printHelp()
    elif len(sys.argv) >= 2:
        if sys.argv[1] == "train":
            if len(sys.argv) == 3:
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) #start Ryu process
                traffic_type = sys.argv[2]
                f = open(traffic_type+'_training_data.csv', 'w') #open training data output file
                signal.signal(signal.SIGALRM, alarm_handler) #start signal process
                signal.alarm(TIMEOUT) #set for 15 minutes
                try:
                    headers = 'Forward Packets\tForward Bytes\tDelta Forward Packets\tDelta Forward Bytes\tForward Instantaneous Packets per Second\tForward Average Packets per second\tForward Instantaneous Bytes per Second\tForward Average Bytes per second\tReverse Packets\tReverse Bytes\tDelta Reverse Packets\tDelta Reverse Bytes\tDeltaReverse Instantaneous Packets per Second\tReverse Average Packets per second\tReverse Instantaneous Bytes per Second\tReverse Average Bytes per second\tTraffic Type\n'
                    f.write(headers)
                    run_ryu(p,traffic_type=traffic_type,f=f)
                except Exception:
                    print('Exiting')
                    os.killpg(os.getpgid(p.pid), signal.SIGTERM) #kill ryu process on exit
                    f.close()
            else:
                print("ERROR: specify traffic type.\n")

        else:
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) #start ryu process
            if sys.argv[1] == 'logistic':
                infile = open('models/LogisticRegression','rb')
            elif sys.argv[1] == 'kmeans':
                infile = open('models/KMeans_Clustering','rb')
            elif sys.argv[1] == 'svm':
                infile = open('models/SVC','rb')
            elif sys.argv[1] == 'kneighbors':
                infile = open('models/KNeighbors','rb')
            elif sys.argv[1] == 'Randomforest':
                infile = open('models/RandomForestClassifier','rb')
            elif sys.argv[1] == 'gaussiannb':
                infile = open('models/GaussianNB','rb')
   

            model = pickle.load(infile) #unload previously trained ML model (refer to Jupyter notebook for details)
            infile.close()
            run_ryu(p,model=model)
    sys.exit();

