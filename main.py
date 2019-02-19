import re
import pprint

class Scale:
    #Setting inital values
    MUSIC_NOTES = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
    def __init__(self, notes, key, tuning="EADGBE"):
        self.scaleNotes = notes
        self._key = key
        self._tuning = self.noteFilter(tuning)
        self.fretBoard = self.makeFretboard(tuning)

    @property
    def scaleNotes(self):
        return str(self._scaleNotes)

    @scaleNotes.setter
    def scaleNotes(self, string):
        print(self.noteFilter(string))
        self._scaleNotes = self.noteFilter(string)


    #Print the fretboard in a more readable way
    def viewFull(self):
        for string in range(len(self.fretBoard)):
            for fret in range(len(self.fretBoard[string])):
                if len(self.fretBoard[string][fret]) == 2:
                    print("{}---".format(self.fretBoard[string][fret]), end="")
                else:
                    print("{}----".format(self.fretBoard[string][fret]), end="")
            print()

    def viewScale(self):
        for string in range(len(self.fretBoard)):
            for fret in range(len(self.fretBoard[string])):
                if self.fretBoard[string][fret] in self.scaleNotes:
                    if len(self.fretBoard[string][fret]) == 2:
                        print("{}---".format(self.fretBoard[string][fret]), end="")
                    else:
                        print("{}----".format(self.fretBoard[string][fret]), end="")
                else:
                    print("0----", end="")
            print()

    
    @property
    def tuning(self):
        return self._tuning

    #When tuning changes, update the fretboard too
    @tuning.setter
    def tuning(self, tuning):
        if len(tuning) != 6:
            raise Exception("Tuning must consist of 6 notes. Only sharps")
        self._tuning = tuning
        self.fretBoard = self.makeFretboard(tuning)
    
    #Extract notes from string and return list
    def noteFilter(self, noteString):
        noteArray = list(filter(None, re.split("([A-Z]#)|([A-Z])",noteString)))
        return noteArray

    #Create fretboard
    def makeFretboard(self, tuning):
        fretBoard = [[0 for i in range(13)] for i in range(6)]

        #Find noteoffset and use it to add onto the current notes
        #This allows for alternate tunings
        noteOffset = [self.getNoteIndex(self.tuning[i]) for i in range(len(self.tuning))]

        for string in range(len(fretBoard)):
            for fret in range(len(fretBoard[string])):
                fretBoard[string][fret] = self.MUSIC_NOTES[(fret+noteOffset[string]) % len(self.MUSIC_NOTES)]
        fretBoard.reverse()
        return fretBoard

    def export(self):
        pass

    @property
    def key(self):
        return self._key

    def getNoteIndex(self, note):
        return self.MUSIC_NOTES.index(note)

    @key.setter
    def key(self, value):
        noteDiff = abs(self.getNoteIndex(self._key) - self.getNoteIndex(value))
        for i in range(len(self._scaleNotes)):
            noteIndex = self.getNoteIndex(self._scaleNotes[i])
            newNote = self.MUSIC_NOTES[(noteIndex+noteDiff) % len(self.MUSIC_NOTES)]
            self._scaleNotes[i] = newNote
        self._key = value
        print("Changed key")


scale = Scale("ABCDEFG", "A")
scale.key = "B"
scale.viewScale()

while 1:
    notes = input("Scale:")
    key = input("Key:")
    tuning = input("Tuning:")

    scale.notes = notes
    scale.key = key
    scale.tuning = tuning

    scale.viewScale()
