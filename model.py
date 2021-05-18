import numpy as np
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"	# Disable GPU

from keras.models import Sequential
from keras.layers import Dense

class Seq(Sequential):
	'''
	Wraps Keras Sequential model for ease of use

	'''
	def __init__(self):
		super(Seq, self).__init__()

		# input layer
		self.add(Dense(100, input_dim=12, activation='relu'))

		# hidden layer
		self.add(Dense(20, activation='relu'))

		# output layer
		self.add(Dense(2, activation='softmax'))
		self.summary()
		self.n_params = self.count_params()

	def pred(self, inputs):
		'''
		Calls model.predict

		- Args:
			inputs (array-like):
				see game.py for inputs

		Returns:
			int, 0 for left, 1 for right
		'''
		out = self.predict(inputs, verbose=0)[0]
		return np.where(out==np.max(out))[0][0]

	def _set_weights(self, ind):
			new_parameters = []
			param_idx = 0
			for i, layer in enumerate(self.get_weights()):
				num_parameters_taken = np.prod(layer.shape)
				new_parameters.append(ind[param_idx:param_idx+num_parameters_taken].reshape(layer.shape))
				param_idx += num_parameters_taken

			self.set_weights(new_parameters)