import random
from midiutil import MIDIFile
from mingus.core import progressions, intervals

from midi_python_convert import note_to_number, number_to_note

scale = "A"

royal_road = progressions.to_chords(["IV7", "V7", "iii7", "vi"], scale)

track = 0
channel = 0
time = 0  # In beats
duration = 1  # In beats
tempo = 150  # In BPM
volume = 100  # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
# automatically)
MyMIDI.addTempo(track, time, tempo)

previous_pitch = 0
carry_over = 0
for i in range(32):

    # Write down some chords
    notes = royal_road[i % 4]
    for note in notes:
        pitch = note_to_number(note, 3)
        MyMIDI.addNote(track, channel, pitch, time + i * 4, 4, 50)

    # Melodies
    bar_len = 0 + carry_over
    while bar_len < 4:
        note = random.choice(notes)
        pitch = note_to_number(note, random.choice([6, 7]))
        leap_limit = 3
        iterations = 0
        while abs(pitch - previous_pitch) > leap_limit:
            if previous_pitch == 0:
                break
            pitch = note_to_number(note, random.choice([6, 7]))
            iterations += 1
            if iterations % 100 == 0:
                leap_limit += 1
        
        duration = random.choice([0.5, 1])
        # except...
        if bar_len > 4:
            carry_over = bar_len - 4
            bar_len = 4
        else:
            carry_over = 0
        # hold note every 8 bars, unless its bar 0.
        if (i + 1) % 8 == 0 and i != 0:
            duration = 4

        MyMIDI.addNote(track, channel, pitch, time + i * 4 + bar_len, duration, 80)

        bar_len += duration
        previous_pitch = pitch

with open("song.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)