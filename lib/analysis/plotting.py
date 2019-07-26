import numpy as np 
from .constants import *
import matplotlib.pyplot as plt 

def plot_vectors(*args, names=[]):
    f, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20,10))
    for arg in args:
        ax1.plot(arg[:,0])
        ax2.plot(arg[:,1])
        ax3.plot(arg[:,2])
    ax1.set_title("x component")
    ax2.set_title("y component")
    ax3.set_title("z component")
    ax1.legend(names)
    ax2.legend(names)
    ax3.legend(names)

def pad_fd(data):
	for k, v in data.items():
		if "F_human" in k:
			F_h_name = k
			F_h = v
		elif "waypoint" in k:
			n_pre = v.shape[0]
		elif "position" in k:
			n_tot = v.shape[0]
	data[F_h_name] = np.vstack((np.zeros((n_pre, F_h.shape[1])),
	 F_h, np.zeros((n_tot - n_pre - F_h.shape[0], F_h.shape[1]))))
	return data
     
def load_data(path="npz/three_drone_box_fd.npz"):
    data = np.load(path)
    processed = {}
    
    for key in data:
#         if POSITION in d: import pdb; pdb.set_trace()
        
        #if "drone" not in d or BOX not in d: continue
        try:
            name, topic = key.split("/")
        except ValueError:
            continue
        if name not in processed: processed[name] = {}
        processed[name][topic] = data[key]
    # Assume 'drone_1' always exists
    force_start = processed[DRONES[0]][WAYPOINT].shape[0]
    
    # Assume F_Human is 7D for now, 0th element is timestamp
    for obj, topics in processed.items():
        if F_HUMAN not in topics: continue
        F_human = topics[F_HUMAN]
        F_human = np.vstack((
            np.zeros((force_start,7)), 
             F_human,
             np.zeros((topics[POSITION].shape[0] - F_human.shape[0] - force_start, 7))
        ))
        processed[obj][F_HUMAN] = F_human
    return processed
