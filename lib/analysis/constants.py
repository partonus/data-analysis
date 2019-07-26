import numpy as np 

T_STEP = 0.1
BOX = "box"
DRONES = ["drone_1", "drone_2", "drone_3"]
F_HUMAN = "F_human"
FD_OBS = "Fd_obs"
EXTERNAL_FORCE = "external_force" # box to drone force
VELOCITY = "velocity"
WAYPOINT = "waypoint"
CONTROL = "control"
POSITION = "position"
SIMULATOR_FULL_STATE = "simulator_full_state"

#PHYSICAL PARAMETERS
L = 0.033
M = 0.032
INERTIA_XX = 16e-6
INERTIA_YY = INERTIA_XX
INERTIA_ZZ = 29e-6
K = 0.01

# DYNAMICS
# X_{t+1} = AX_t + BU_t + B_GRAV
GRAVITY = 9.81
A = np.zeros((12,12))
A[0:3,3:6] = np.eye(3)
A[3,7] = GRAVITY
A[4,6] = -GRAVITY
A[6:9,9:12] = np.eye(3)
A = np.eye(12) + T_STEP * A

B = np.zeros((12, 4))
B[5,:] = 1 / M * np.array([1, 1, 1, 1])
B[9:12,:] = np.array([[L, -L, -L, L], [-L, -L, L, L], [K, -K, K, -K]])
B[9,:] = B[9,:] / INERTIA_XX
B[10,:] = B[10,:] / INERTIA_YY
B[11,:] = B[11,:] / INERTIA_ZZ
B = T_STEP * B

B_GRAV = np.zeros((12,1))
B_GRAV[5] = -GRAVITY

BOX_MASS = 0.01
