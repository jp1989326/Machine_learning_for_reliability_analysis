from __future__ import division, print_function, absolute_import

import tflearn
from tflearn.data_utils import to_categorical, pad_sequences
from tflearn.datasets import imdb

# IMDB Dataset loading
train, val, test = imdb.load_data(path='imdb.pkl', maxlen=200,
                                  n_words=20000)
trainX, trainY = train
valX, valY = val
testX, testY = test

# Data preprocessing
# Sequence padding
trainX = pad_sequences(trainX, maxlen=200, value=0.)
testX = pad_sequences(testX, maxlen=200, value=0.)
# Converting labels to binary vectors
trainY = to_categorical(trainY, nb_classes=2)
valY = to_categorical(valY, nb_classes=2)
testY = to_categorical(testY, nb_classes=2)

# Network building
net = tflearn.input_data([None, 200])
net = tflearn.embedding(net, input_dim=20000, output_dim=128)
net = tflearn.lstm(net, 128)
net = tflearn.dropout(net, 0.5)
net = tflearn.fully_connected(net, 2, activation='softmax')
net = tflearn.regression(net, optimizer='adam',
                         loss='categorical_crossentropy')

# Training
model = tflearn.DNN(net, clip_gradients=0., tensorboard_verbose=0)
model.fit(trainX, trainY, validation_set=(testX, testY), show_metric=True,
          batch_size=128)