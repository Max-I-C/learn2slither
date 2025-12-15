# Trying to understand how works already build neuronal networks to be able to after recreate my own neuronal network for this project #
import numpy as np
from keras import Sequential, layers

model = Sequential()
model.add(layers.Input(shape=(1,)))
model.add(layers.Dense(3))
model.add(layers.Dense(64))
model.add(layers.Dense(1))

entree = np.array([1, 2, 3, 4, 5], dtype=float)
sortie = np.array([2, 4, 6, 8, 10], dtype=float)

model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(entree, sortie, epochs=1000, verbose=0)

while True:
    x = float(input('Nombre : '))
    prediction = model.predict(np.array([[x]]), verbose=0)
    print('Predi :', prediction[0][0])