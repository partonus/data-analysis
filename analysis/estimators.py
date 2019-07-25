from abc import abstractmethod, ABC
import scipy.signal
import numpy as np 

class Estimator(ABC):

	@abstractmethod
	def update_estimate(self, y, u):
		raise NotImplementedError("Not Implemented!")

	@abstractmethod
	def get_trajectory(self):
		raise NotImplementedError("Not Implemented!")

class Linear_Observer(Estimator):

	def __init__(self, A, B, Bg, x_init, C=np.eye(12)):
		self.x_est = x_init
		self.Fd_est = np.zeros(3)
		self.x_est_traj = [x_init]
		self.Fd_est_traj = []

		# SYSTEM DYNAMICS
		self.A = A
		self.B = B
		self.C = C
		self.Bg = Bg

		# OBSERVER MATRICS CONSTRUCTION
		Cd = np.zeros((12,3))
		self.A_obs = np.block([[A,Bd],[np.zeros((3,12)),np.eye(3)]])
		self.B_obs = np.block([[B],[np.zeros((3,4))]])
		self.Bg_obs = np.block([[Bg.reshape((12,1))],[np.zeros((3,1))]])
		self.C_obs = np.block([[C,Cd]])
		poles = np.array([93.,94,95,96,97,98,99,100,101,102,103,104,105,106,107])/130
		sys = scipy.signal.place_poles(self.A_obs.transpose(), self.C_obs.transpose(), poles)
		self.L_obs = sys.gain_matrix.transpose()

	def update_estimate(self, y, u):
		x_obs = np.hstack((self.x_est, self.Fd_est))

		x_obs = np.dot(self.A_obs, x_obs) + \
					 np.dot(self.B_obs, u) + \
					 self.Bg_obs - \
					 self.L_obs.dot(np.dot(self.C, self.x_est) - y)

		self.x_est = x_obs[:12]
		self.Fd_est = x_obs[12:15]
		self.x_est_traj.append(self.x_est)
		self.Fd_est_traj.append(self.Fd_est)

		return self.Fd_est, self.x_est
