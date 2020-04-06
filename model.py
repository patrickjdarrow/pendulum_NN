#TODO: 
'''
1) Explore architectures
2) Create logging scheme

'''
import numpy as np

from keras.models import Sequential
from keras.layers import Dense

class Seq(Sequential):
	def __init__(self):
		super(Seq, self).__init__()
		self.add(Dense(5, input_dim=5, activation='relu'))
		self.add(Dense(5, activation='relu'))
		self.add(Dense(3, activation='softmax'))

	def pred(self, inputs):
		out = self.predict(inputs, verbose=0)[0]
		return np.where(out==np.max(out))[0][0]