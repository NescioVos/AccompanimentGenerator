# Class fields:
# Clef_key: string
# Clef_line: int
# Rhythm: int (code of pattern)
# Tempo: int
# Octave: int
# Mode: major or minor
# Beats: int 
# BeatType: int
# StavesNum: int
class PartAttributes:
  def __init__(self, clef_key, clef_line, rhythm, tempo, octave, mode, fifths, time_beats, time_beats_ty, staves=1):
    self.Clef_key = clef_key
    self.Clef_line = clef_line
    self.Rhythm = rhythm
    self.Octave = octave
    self.Mode = mode
    self.Fifths = fifths
    self.Beats = time_beats
    self.BeatType = time_beats_ty
    self.StavesNum = staves
    self.Tempo = tempo

  def setClef(self, key, line):
    self.Clef_key = key
    self.Clef_line = line

  def setRythm(self, rhythm):
    self.Rythm = rhythm

  def setOctave(self, octave):
    self.Octave = octave

  def setMode(self, mode):
    self.Mode = mode

  def setFifths(self, fifths):
    self.Fifths = fifths

# Unit tests must be commented 
# pa = PartAttributes("G", 2, 0, 4, "major", 0)
# print pa.Clef_key
# print pa.Clef_line
# print pa.Mode
# print pa.Octave
# print pa.Rhythm
# pa.setClef("F", 4)
# print pa.Clef_key
# print pa.Clef_line
