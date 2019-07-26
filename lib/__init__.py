import sys

REQUIRED_FOLDERS = [
        "./Multi_Drone_Control/src/drone_controller/src/"
        ]

for f in REQUIRED_FOLDERS:
    sys.path.insert(0, f)

