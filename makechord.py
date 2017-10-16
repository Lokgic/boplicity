from music21 import *

billie = "|F7   |Bb7   |F7   |F7   |Bb7   |Bb7   |F7   |A-7 D7 |G-7   |C7   |F7   |C7   |"

chords_dict = {'F7':"F A C E-","Bb7": "B- D F A-","A-7": "A C E G","D7": "D F# A C","G-7": "G B- D F","C7": "C E G B-"}

billie = billie.split('|')

st = stream.Stream()

for bar in billie:
	data = bar.split()
	n_chords = len(data)
	for i in data:
		c = chord.Chord(chords_dict[i])
		c.quarterLength = 4/n_chords
		st.append(c)
