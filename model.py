#TODO: 
'''
1) Explore architectures
2) Create logging scheme

'''
import numpy as np

from keras.models import Sequential
from keras.layers import Dense, LeakyReLU

input_dim = 12
n_neurons = 200
hidden = 1
output_dim = 2

n_traits = (hidden>0) * input_dim * n_neurons + (hidden > 1) *\
			(n_neurons ** hidden) + n_neurons * output_dim +\
			n_neurons * hidden + output_dim + (hidden==0) *\
			input_dim * output_dim

class Seq(Sequential):
	def __init__(self):
		super(Seq, self).__init__()

		# # hidden layers
		# self.add(Dense(100, input_dim=5, activation='tanh'))
		# self.add(Dense(50, activation='tanh'))
		# self.add(Dense(10, activation='tanh'))

		# # hidden layers
		# n_neurons = 5
		# self.add(Dense(n_neurons, input_dim=5, activation='tanh'))
		# # self.add(Dense(n_neurons, activation='tanh'))
		# self.add(Dense(n_neurons, activation='tanh'))

		# hidden layers
		self.add(Dense(n_neurons, input_dim=input_dim, activation='relu'))
		for i in range(hidden-1):
			self.add(Dense(n_neurons, activation='relu'))

		# output layer
		self.add(Dense(output_dim, activation='softmax'))
		self.summary()

	def pred(self, inputs):
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