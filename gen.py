import sys
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
from music21 import *
import os
import random 
# load ascii text and covert to lowercase

xmls = os.listdir("./xml")
notes = []

for file in xmls:
    song =  converter.parse("./xml/"+file)
    solo = song[1]
    for measure in solo:
        if type(measure) is stream.Measure:
            for el in measure:
                if type(el) is note.Note:
                    p = el.pitch.midi
                    if len(notes) > 0:
                        if p == notes[-1]:
                            if el.tie is None or el.tie == "start":
                                notes.append(p)
                        else:
                            notes.append(p)
                    else:
                        notes.append(p)
                elif type(el) is note.Rest:
                    if len(notes) > 0:
                        if notes[-1] is not -1:
                            notes.append(-1)


# s = stream.Stream()

# for n in notes:
# 	s.append(note.Note(midi=n))
# s.show()

pitches = sorted(set(notes))


notes_to_int = dict((c, i) for i, c in enumerate(pitches))
int_to_notes = dict((i, c) for i, c in enumerate(pitches))


n_notes = len(notes)
n_pitches = len(pitches)



seq_length = 100

dataX = []
dataY = []
for i in range(0, n_notes - seq_length, 1):
	seq_in = notes[i:i + seq_length]
	seq_out = notes[i + seq_length]
	dataX.append([notes_to_int[n] for n in seq_in])
	dataY.append(notes_to_int[seq_out])

n_patterns = len(dataX)
X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
# normalize
X = X / float(n_pitches)
# one hot encode the output variable
y = np_utils.to_categorical(dataY)

# define the LSTM model
model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]),return_sequences=True))
model.add(Dropout(0.1))
model.add(LSTM(256))
model.add(Dropout(0.1))
model.add(Dense(y.shape[1], activation='softmax'))
# load the network weights
filename = "w.hdf5"
model.load_weights(filename)
model.compile(loss='categorical_crossentropy', optimizer='adam')
# pick a random seed
start = numpy.random.randint(0, len(dataX)-1)
pattern = dataX[start]



solocode = []

def sample_val(pred):
    s = numpy.argsort(prediction[0])
    s = s[-2:len(s)]
    return random.choice(s)

for i in range(500):
    x = numpy.reshape(pattern, (1, len(pattern), 1))
    x = x / float(n_pitches)
    prediction = model.predict(x, verbose=0)
    index = sample_val(prediction)
    result = int_to_notes[index]
    solocode.append(result)
    pattern.append(index)
    pattern = pattern[1:len(pattern)]

s = stream.Stream()
for n in solocode:
	if n is not -1:
		temp = note.Note(midi=n)
		temp.quarterLength = 0.5
		s.append(temp)
	else:
		s.append(note.Rest(quarterLength = .5))

s.show()