import sys, os

REQUIRED_FOLDERS = [ # relative path
        "Multi_Drone_Control/src/drone_controller/src/"
        ]

for f in REQUIRED_FOLDERS:
    sys.path.insert(0, os.path.dirname(__file__) + "/" + f)

