import glob, os, argparse, rosbag
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--files', nargs='+', required=True)
parser.add_argument('--npz_dir', required=True)
args = parser.parse_args()

NOT_PROCESSING = set()
def to_npy_array(msg, t):
	if msg._type == "std_msgs/Float32MultiArray":
		return np.array([t.to_time()] + list(msg.data))
	elif msg._type == "geometry_msgs/Wrench":
		return np.array([t.to_time()] + get_xyz(msg.force) + get_xyz(msg.torque))
	elif msg._type == "std_msgs/Int32":
		return np.array([t.to_time()] + [msg.data])
	elif msg._type == "geometry_msgs/Twist":
		return np.array([t.to_time()] + get_xyz(msg.linear) + get_xyz(msg.angular))
	elif msg._type == "geometry_msgs/Pose":
		return np.array([t.to_time()] + get_xyz(msg.position) + get_xyz(msg.orientation) + [msg.orientation.w])	
	else:
		if msg._type not in NOT_PROCESSING:
			print("Not processing type {}".format(msg._type))
			NOT_PROCESSING.add(msg._type)
		return None

def get_xyz(val):
	return [val.x, val.y, val.z]

if __name__ == "__main__":
	for file in args.files:
		print("Processing File {}".format(file))
		name = file.split("/")[-1]
		name = name.split(".")[0] + ".npz"
		bag = rosbag.Bag(file)
		data = {}
		for topic, msg, t in bag.read_messages():
			if topic not in data:
				data[topic] = []
			val = to_npy_array(msg, t)
			if val is not None:
				data[topic].append(val)
		for t, v in data.items():
			data[t] = np.array(v)
		print("Saving file {}".format(name))
		np.savez("{}/{}".format(args.npz_dir, name), **data)
