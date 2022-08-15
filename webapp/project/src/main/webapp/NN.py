from keras.models import Sequential
from keras.layers.core import Dense
from tensorflow.keras.optimizers import Adam


def neuron(X_train, y_train):
    model = Sequential()
    model.add(Dense(8, input_dim=12, activation='relu'))
    model.add(Dense(5,activation='relu'))
    model.add(Dense(5,activation='relu'))
    model.add(Dense(1,activation='linear'))

    model.compile(loss='mean_squared_error',
                  optimizer=Adam(),metrics=['accuracy'])
    
    model.fit(X_train, y_train,
              batch_size=10,
              epochs=2000,
              verbose=0)
    return model
