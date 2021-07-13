#!/usr/python

import RhythmPattern as RP

CurLevel = 0
# Notes in european notation
NoteMap = {'AF': 8, 'A': 9, 'AS': 10, 'B': 10, 'CF': 11, 'C': 0, 'CS': 1, 'DF': 1,
           'D': 2, 'DS': 3, 'EF': 3, 'E': 4, 'FF': 4, 'ES': 5, 'F': 5, 'FS': 6, 'GF': 6,
           'G': 7, 'GS': 8, 'H': 11, 'HF': 10, 'HS': 0}
NoteArray = [['C', 'HS'], ['CS', 'DF'], ['D'], ['DS', 'EF'], ['E', 'FF'],
             ['F', 'ES'], ['FS', 'GF'], ['G'], ['GS', 'AF'], ['A'], ['B', 'HF'],
             ['H', 'CF']]

KeyArray = [0, 0, 0, 0, 0, 0, 0]

DrumSet = {'snare':{'C', 5}, 'bass':{'F', 4}, 'hihat':{'G', 5, 'x'}, 'cymbal':{'G', 5, 'diamond'}}

def print_tabs():
  buf = ""
  for i in xrange(CurLevel):
    buf += " "
  return buf


def next_level():
  global CurLevel
  CurLevel += 1
  return print_tabs()


def prev_level():
  global CurLevel
  CurLevel -= 1
  return print_tabs()


def increment_level():
  global CurLevel
  CurLevel += 1


def decrement_level():
  global CurLevel
  CurLevel -= 1


# All parameters must be strings
def printOneLineToken(tokenstr, valstr, attributes=dict({})):
  buf = "<" + tokenstr
  if len(attributes) != 0:
    for attr in attributes.keys():
      buf += " " + str(attr) + "=\"" + str(attributes[attr]) + "\""
  buf += ">" + valstr + "</" + tokenstr + ">\n"
  return buf


def multilineEnd(tokenstr):
  return "</" + tokenstr + ">\n"


def multilineBegin(tokenstr, attributes=dict({})):
  buf = "<" + tokenstr
  if len(attributes) != 0:
    for attr in attributes.keys():
      buf += " " + str(attr) + "=\"" + str(attributes[attr]) + "\""
  buf += ">\n"
  return buf


# attributes is a library of string parameters and values
def printAttrToken(tokenstr, attributes):
  buf = "<" + tokenstr + " "
  for attr in attributes:
    buf += str(attr) + "=\"" + str(attributes[attr]) + "\" "
  buf += "/>\n"
  return buf


def printSimpleToken(tokenstr):
  return "<" + tokenstr + "/>\n"


#############################
####   Library of tokens
#############################
def print_duration(val):
  return printOneLineToken("duration", str(val))


def print_divisions(val):
  return printOneLineToken("divisions", str(val))


def print_clef_sign(key):
  return printOneLineToken("sign", key)


def print_clef_line(line):
  return printOneLineToken("line", str(line))


# Note
def note_begin():
  return multilineBegin("note")


def note_end():
  return multilineEnd("note")


def pitch_begin():
  return multilineBegin("pitch")


def pitch_end():
  return multilineEnd("pitch")


def key_begin():
  return multilineBegin("key")


def key_end():
  return multilineEnd("key")


def clef_begin(number=0):
  if number == 0:
    return multilineBegin("clef")
  return multilineBegin("clef", {"number": number})


def clef_end():
  return multilineEnd("clef")


def print_step(note):
  return printOneLineToken("step", note)


def print_octave(octave_no):
  return printOneLineToken("octave", str(octave_no))


def print_alter(alter_val):
  return printOneLineToken("alter", str(alter_val))


def mark_as_chord():
  return printSimpleToken("chord")


def print_fifths(val):
  return printOneLineToken("fifths", str(val))


def print_mode(val):
  return printOneLineToken("mode", val)


def time_begin():
  return multilineBegin("time")


def time_end():
  return multilineEnd("time")


def print_beats(val):
  return printOneLineToken("beats", str(val))


def print_beats_type(val):
  return printOneLineToken("beat-type", str(val))


# Score
def print_part_name(part):
  return printOneLineToken("part-name", part)


def score_part_begin(attributes):
  return multilineBegin("score-part", attributes)


def score_part_end():
  return multilineEnd("score-part")


# measure
def measure_begin(measure_id):
  return multilineBegin("measure", {"number": measure_id})


def measure_end():
  return multilineEnd("measure")


# measure
def attributes_begin():
  return multilineBegin("attributes", {})


def attributes_end():
  return multilineEnd("attributes")


def articulations_begin():
  return multilineBegin("articulations", {})


def articulations_end():
  return multilineEnd("articulations")


def notations_begin():
  return multilineBegin("notations", {})


def notations_end():
  return multilineEnd("notations")

FirstStaff=1

def print_predirective(tempo_val, tempo_text=""):
  global FirstStaff
  if FirstStaff != 1:
    return ""
  buf = ""
  buf += multilineBegin("direction", {"directive":"yes", "placement":"above"})
  buf += next_level()
  buf += multilineBegin("direction-type")
  buf += next_level()
  if len(tempo_text) > 0:
    buf += printOneLineToken("words", tempo_text, {"default-y":15, "font-weight":"bold"})
  else:
    buf += multilineBegin("metronome",
                          {"default-y":15, "font-weight":"bold", "font-family":"EngraverTextT"})
    buf += next_level()
    buf += printOneLineToken("beat-unit", "quarter")
    buf += print_tabs()
    buf += printOneLineToken("per-minute", str(tempo_val))
    buf += prev_level()
    buf += multilineEnd("metronome")
  buf += prev_level()
  buf += multilineEnd("direction-type")
  buf += print_tabs()
  buf += printAttrToken("sound", {"tempo":tempo_val})
  buf += prev_level()
  buf += multilineEnd("direction")
  FirstStaff = 0
  return buf


def print_header():
  buf = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n"
  buf += "<!DOCTYPE score-partwise PUBLIC\n\t\"-//Recordare//DTD MusicXML 3.0 Partwise//EN\"\n\t\"http://www.musicxml.org/dtds/partwise.dtd\">\n"
  return buf

def print_score_instrument(ID, part_name):
  buf = multilineBegin("score-instrument", {"id":"P"+str(ID)+"-I"+str(ID)})
  buf += next_level()
  buf += printOneLineToken("instrument-name", "ARIA Player")
  sound = "keyboard.piano"
  virtual_name = "005. Keyboards/Steinway Piano"
  if part_name == "pad":
    sound = "synth.pad"
    virtual_name = "014. GM/Warm Pad"
  elif part_name == "bass":
    sound = "pluck.bass.electric"
    virtual_name = "011. Jazz/Jazz Fretted Bass KS"
  elif part_name == "vocal":
    sound = "voice.vocals"
    virtual_name = "009. Choir/Choir Ahs"
  elif part_name == "guitar":
    sound = "pluck.guitar.acoustic"
    virtual_name = "011. Jazz/Acoustic Guitar KS"
  elif part_name == "cello":
    sound = "strings.cello"
    virtual_name = "007. Solo Strings/3. Cello/Cello Solo KS"
  buf += print_tabs()
  buf += printOneLineToken("instrument-sound", sound)
  buf += print_tabs()
  buf += multilineBegin("virtual-instrument")
  buf += next_level()
  buf += printOneLineToken("virtual-library", "Garritan Instruments for Finale")
  buf += print_tabs()
  buf += printOneLineToken("virtual-name", virtual_name)
  buf += prev_level()
  buf += multilineEnd("virtual-instrument")
  buf += prev_level()
  buf += multilineEnd("score-instrument")
  # Print MIDI config
  buf += print_tabs()
  buf += printOneLineToken("midi-device", "Bank 1")
  buf += print_tabs()
  buf += multilineBegin("midi-instrument", {"id":"P"+str(ID)+"-I"+str(ID)})
  buf += next_level()
  buf += printOneLineToken("midi-channel", str(ID+1))
  buf += print_tabs()
  buf += printOneLineToken("midi-program", str(1))
  buf += print_tabs()
  buf += printOneLineToken("volume", str(80))
  buf += print_tabs()
  buf += printOneLineToken("pan", str(80))
  buf += prev_level()
  buf += multilineEnd("midi-instrument")
  return buf

def print_part_list(part_list, attributes):
  buf = multilineBegin("part-list")
  increment_level()
  for i in xrange(len(part_list)):
    buf += print_tabs()
    buf += score_part_begin({"id": "P" + str(i)})
    buf += next_level()
    buf += print_part_name(str(part_list[i]))
    buf += print_tabs()
    buf += print_score_instrument(i, part_list[i])
    buf += prev_level()
    buf += score_part_end()
  buf += prev_level()
  buf += multilineEnd("part-list")
  return buf


def print_simple_note(step, octave, duration, alteration=0, chord=0, voice=0, accent=0):
  buf = note_begin()
  buf += next_level()
  if chord != 0:
    buf += mark_as_chord()
    buf += print_tabs()
  buf += pitch_begin()
  buf += next_level()
  buf += print_step(step)
  if alteration != 0:
    buf += print_tabs()
    buf += print_alter(alteration)
  buf += print_tabs()
  buf += print_octave(octave)
  buf += prev_level()
  buf += pitch_end()

  buf += print_tabs()
  buf += print_duration(duration)

  #<voice>
  if voice != 0:
    buf += print_tabs()
    buf += printOneLineToken("voice", str(voice))
  #FIXME: print accidental here!!!
  #<type>
  #<accidentals>
  if is_accidental(step, alteration) != 0:
    acc_words = ["flat", "natural", "sharp"]
    acc_word = acc_words[alteration+1]
    buf += print_tabs()
    buf += printOneLineToken("accidental", acc_word)
  #staff
  if voice != 0:
    buf += print_tabs()
    buf += printOneLineToken("staff", str(voice))
  #<beam>
  #<notations>
  if accent != 0:
    buf += print_tabs()
    buf += notations_begin()
    buf += next_level()
    buf += articulations_begin()
    buf += next_level()
    buf += printAttrToken("accent", {"default-x": -1, "default-y": 55})  # , "placement":"below"})
    buf += prev_level()
    buf += articulations_end()
    buf += prev_level()
    buf += notations_end()

  buf += prev_level()
  buf += note_end()
  return buf


def print_rest(duration, voice=0):
  buf = note_begin()
  buf += next_level()
  buf += printSimpleToken("rest")
  buf += print_tabs()
  buf += print_duration(duration)
  if voice != 0:
    buf += print_tabs()
    buf += printOneLineToken("staff", str(voice))
    #   buf += print_tabs()
  #  buf += printOneLineToken("voice", str(voice))
  buf += prev_level()
  buf += note_end()
  return buf


#######################
#######################
## Interval arithmetics
#######################

# interval is a number of half-tones
# return a pair tuple of note and octave
# FIXME: european notation!
def get_interval(note, octave, interval):
  print note
  if len(note) > 2 or not (note[0] in "ABCDEFGHabcdefhg"):
    print "ERROR in get_interval: invalid note"
    return ""
  if interval / 12 + octave > 6:
    print "ERROR in get_interval: invalid interval value or octave"
    return ""
  note = note.upper()
  note = convert_to_eu(note)
  # Calculate absolute value in 12-tones system
  note_num = NoteMap[note] + interval
  new_octave = octave
  if note_num > 12:
    new_octave += note_num / 12
  note_num = note_num % 12
  note_arr = NoteArray[note_num]
  if len(note_arr) == 1 or len(note_arr[0]) == 1:
    return (note_arr[0], new_octave)
  if len(note) == 1 or note[1] == 'S':
    return (note_arr[0], new_octave)

  return (note_arr[1], new_octave)


# get notes for american notation for B
def get_note_alteration(note, us_notation=0):
  if us_notation == 0 and note == 'B':
    return -1
  if len(note) == 1:
    return 0
  if note[1] == 'S':
    return 1
  return -1


def convert_to_us(note):
  if note[0] == 'H':
    return 'B' + note[1:]
  if note[0] == 'B':
    return 'BF' + note[1:]
  return note


def convert_to_eu(note):
  if note[0] != 'B':
    return note
  if note == 'B':
    return 'H'
  if note == 'BF':
    return 'B'
  if note == 'BS':  # FIXME: simplify
    return 'C'
  return note


# Return a tuple of (Note, alteration, mode, bass, notes_num)
# This works with american
def parse_chord(chord_str):
  mode = "major"
  notes_num = 3
  bass = 0
  chord_str = chord_str.upper()
  note = chord_str[0]
  tmp = chord_str[1:]
  alt = 0
  for ch in tmp:
    if ch == 'S':
      alt = 1
    if ch == 'F':
      alt = -1
    if ch == 'M':
      mode = "minor"
    if ch == '7':
      notes_num = 4
    if ch == '5':
      bass = 2
    if ch == '3':
      bass = 1
    if ch == '9':
      notes_num = 5
  return (note, alt, mode, bass, notes_num)

# FIXME: US notation
def is_accidental(note, alt):
  global KeyArray
  note_id = NoteMap[note]/2 + NoteMap[note]%2
  if note == "B":
    note_id = 6
  if KeyArray[note_id] != alt:
    return 1
  return 0

# print chord for piano right hand or similar
# chord_sig is chord signature string
# prev_chord_sig is a previous chord to make voice leading more smooth
#  if prev_chord_sig is "" chord will be written in a 3-5 form
# octave is a desirable octave for lowest note
def print_chord(chord_sig, prev_chord_sig, octave, duration, us_notation=0, accent=0, voice=0):
  int1 = 4
  int2 = 3
  int3 = 0
  chTuple = parse_chord(convert_to_us(chord_sig))
  if len(chTuple) != 5:
    print "ERROR: error in parsing chord signature"
    return ""
  alt = chTuple[1]
  minor = 0
  if chTuple[2] == "minor":
    minor = 1
  notes_num = 3
  bass = chTuple[3]
  notes_num = chTuple[4]
  buf = ""
  note = chTuple[0]
  buf += print_simple_note(note, octave, duration, alt, 0, voice, accent)

  if alt == -1:
    note += 'F'
  if alt == 1:
    note += 'S'

  interval_arr = [4, 3]
  if minor == 1:
    interval_arr = [3, 4]
    if notes_num > 3:
      interval_arr.append(3)
  else:
    if notes_num > 3:
      interval_arr.append(4)

  for interval in interval_arr:
    third = get_interval(note, octave, interval)
    alt = get_note_alteration(third[0], us_notation)
    buf += print_tabs()
    buf += print_simple_note(convert_to_us(third[0])[0], third[1], duration, alt, 1, voice, 0)
    note = third[0][0]
    octave = third[1]
    if alt == 1:
      note += "S"
    elif alt == -1:
      note += "F"
  return buf

def print_ending_barline():
  buf = multilineBegin("barline", {"location":"right"})
  buf += next_level()
  buf += printOneLineToken("bar-style", "light-heavy")
  buf += prev_level()
  buf += multilineEnd("barline")
  return buf


def print_part_attributes(attributes):
  global FirstStaff
  buf = attributes_begin()
  buf += next_level()

  buf += print_divisions(attributes.BeatType * 6)
  buf += next_level()

  buf += key_begin()
  buf += next_level()

  buf += print_fifths(attributes.Fifths)
  buf += print_tabs()
  buf += print_mode(attributes.Mode)

  buf += prev_level()
  buf += key_end()

  buf += prev_level()

  buf += time_begin()
  buf += next_level()
  buf += print_beats(attributes.Beats)
  buf += print_tabs()
  buf += print_beats_type(attributes.BeatType)
  buf += prev_level()
  buf += time_end()

  # FIXME: dirty hack
  if attributes.StavesNum == 2:
    buf += print_tabs()
    buf += printOneLineToken("staves", str(attributes.StavesNum))
    clefs = [("G", 2), ("F", 4)]
    for i in xrange(attributes.StavesNum):
      buf += print_tabs()
      buf += clef_begin(i + 1)
      buf += next_level()
      buf += print_clef_sign(clefs[i][0])
      buf += print_tabs()
      buf += print_clef_line(clefs[i][1])
      buf += prev_level()
      buf += clef_end()
  else:
    buf += print_tabs()
    buf += clef_begin()
    buf += next_level()
    buf += print_clef_sign(attributes.Clef_key)
    buf += print_tabs()
    buf += print_clef_line(attributes.Clef_line)
    buf += prev_level()
    buf += clef_end()

  buf += prev_level()
  buf += attributes_end()

  if FirstStaff == 1 :
    buf += print_tabs()
    buf += print_predirective(attributes.Tempo)
  return buf


# chord_dur is a list of tuples (chord,octave,duration, accent) in a measure
def print_chord_measure(chord_dur, us_notation=0, voice=0):
  buf = ""
  for chord in (chord_dur):
    accent = 0
    if len(chord) > 3:
      accent = chord[3]
      print "FOUND accent" + str(chord[3])
    buf += print_tabs()
    buf += print_chord(chord[0], "", chord[1], chord[2], us_notation, accent, voice)
  return buf


# FIXME: chain with whole notes
# Attributes of class PartAttributes
def print_simple_chord_chain(chain, attributes, us_notation=0):
  buf = ""
  count = 2
  init_key_array(attributes.Fifths)
  buf += print_tabs()
  buf += measure_begin(1)
  buf += next_level()
  buf += print_part_attributes(attributes)
  mTuple = RP.get_measure_for_pattern(chain[0], attributes.Rhythm, attributes.Octave, attributes.Beats,
                                      attributes.BeatType)
  buf += print_chord_measure(mTuple, us_notation)
  buf += prev_level()
  buf += measure_end()

  for measure in chain[1:]:
    buf += print_tabs()
    buf += measure_begin(count)
    increment_level()
    if len(measure) == 1 and measure[0].upper() == "R":
      buf += print_tabs()
      buf += print_rest(attributes.Beats * 24)
    else:
      mTuple = RP.get_measure_for_pattern(measure, attributes.Rhythm, attributes.Octave, attributes.Beats,
                                          attributes.BeatType)
      buf += print_chord_measure(mTuple, us_notation)
    if count == len(chain):
      buf += print_tabs()
      buf += print_ending_barline()
    buf += prev_level()
    buf += measure_end()
    count += 1
  return buf


def print_simple_bass(chain, attributes, us_notation=0):
  buf = ""
  count = 2
  init_key_array(attributes.Fifths)
  # print attributes in the first measure only
  buf += print_tabs()
  buf += measure_begin(1)
  buf += next_level()
  buf += print_part_attributes(attributes)
  mTuple = RP.get_measure_for_pattern(chain[0], attributes.Rhythm, attributes.Octave, attributes.Beats,
                                      attributes.BeatType, "bass")
  for ch in mTuple:
    note = ch[0]
    if us_notation == 0:
      note = convert_to_us(ch[0])
    chTuple = parse_chord(note)
    # FIXME: handle non-zero bass value
    buf += print_tabs()
    note = chTuple[0]
    buf += print_simple_note(note, ch[1], ch[2], chTuple[1], 0)
  buf += prev_level()
  buf += measure_end()

  for measure in chain[1:]:
    buf += print_tabs()
    buf += measure_begin(count)
    increment_level()
    if len(measure) == 1 and measure[0].upper() == "R":
      buf += print_tabs()
      buf += print_rest(attributes.Beats * 24)
    else:
      mTuple = RP.get_measure_for_pattern(measure, attributes.Rhythm, attributes.Octave, attributes.Beats,
                                          attributes.BeatType, "bass")
      for ch in mTuple:
        note = ch[0]
        if us_notation == 0:
          note = convert_to_us(ch[0])
        chTuple = parse_chord(note)
        # FIXME: handle non-zero bass value
        buf += print_tabs()
        note = chTuple[0]
        print "Bass note = "+note
        print "Alt = "+str(chTuple[1])
        buf += print_simple_note(note, ch[1], ch[2], chTuple[1], 0)
    if count == len(chain):
      buf += print_tabs()
      buf += print_ending_barline()
    buf += prev_level()
    buf += measure_end()
    count += 1
  return buf


def print_rests(num, attributes, voices=0):
  buf = ""
  # print attributes in the first measure only
  buf += print_tabs()
  buf += measure_begin(1)
  buf += next_level()
  buf += print_part_attributes(attributes)
  if voices != 0:
    for voice in xrange(voices):
      buf += print_tabs()
      buf += print_rest(attributes.Beats * 24, voice + 1)
  else:
    buf += print_tabs()
    buf += print_rest(attributes.Beats * 24)
  buf += prev_level()
  buf += measure_end()
  for i in xrange(1, num):
    buf += print_tabs()
    buf += measure_begin(i + 1)
    increment_level()
    if voices != 0:
      for voice in xrange(voices):
        buf += print_tabs()
        buf += print_rest(attributes.Beats * 24, voice + 1)
    else:
      buf += print_tabs()
      buf += print_rest(attributes.Beats * 24)
    if i == num-1:
      buf += print_tabs()
      buf += print_ending_barline()
    buf += prev_level()
    buf += measure_end()
  return buf

def print_2staff_part(chain, attributes, us_notation=0):
  buf = ""
  count = 2
  init_key_array(attributes.Fifths)
  buf += print_tabs()
  buf += measure_begin(1)
  buf += next_level()
  buf += print_part_attributes(attributes)
  mTuple1 = RP.get_measure_for_pattern(chain[0], attributes.Rhythm, 4, attributes.Beats,
                                      attributes.BeatType)
  buf += print_chord_measure(mTuple1, us_notation, 1)

  buf += print_tabs()
  buf += multilineBegin("backup")
  buf += next_level()
  buf += print_duration(attributes.Beats*24)
  buf += prev_level()
  buf += multilineEnd("backup")

  mTuple2 = RP.get_measure_for_pattern(chain[0], attributes.Rhythm, 2, attributes.Beats,
                                      attributes.BeatType, "bass")
  for ch in mTuple2:
    note = ch[0]
    if us_notation == 0:
      note = convert_to_us(ch[0])
    chTuple = parse_chord(note)
    # FIXME: handle non-zero bass value
    buf += print_tabs()
    note = chTuple[0]
    buf += print_simple_note(note, ch[1], ch[2], chTuple[1], 0, 2)
  buf += prev_level()
  buf += measure_end()


  for measure in chain[1:]:
    buf += print_tabs()
    buf += measure_begin(count)
    increment_level()
    if len(measure) == 1 and measure[0].upper() == "R":
      buf += print_tabs()
      buf += print_rest(attributes.Beats * 24, 2)
    else:
      mTuple1 = RP.get_measure_for_pattern(measure, attributes.Rhythm, 4, attributes.Beats,
                                          attributes.BeatType)
      buf += print_chord_measure(mTuple1, us_notation, 1)

      buf += print_tabs()
      buf += multilineBegin("backup")
      buf += next_level()
      buf += print_duration(attributes.Beats*24)
      buf += prev_level()
      buf += multilineEnd("backup")

      mTuple2 = RP.get_measure_for_pattern(measure, attributes.Rhythm, 2, attributes.Beats,
                                          attributes.BeatType, "bass")
      for ch in mTuple2:
        note = ch[0]
        if us_notation == 0:
          note = convert_to_us(ch[0])
        chTuple = parse_chord(note)
        # FIXME: handle non-zero bass value
        buf += print_tabs()
        note = chTuple[0]
        buf += print_simple_note(note, ch[1], ch[2], chTuple[1], 0, 2)
    if count == len(chain):
      buf += print_tabs()
      buf += print_ending_barline()
    buf += prev_level()
    buf += measure_end()
    count += 1
  return buf


def print_drumkit_part(chain, attributes, us_notation=0):
  buf = ""
  return buf
# Unit tests
# attr = PA.PartAttributes("G", 2, 400, 4, "minor", 0, 4, 4)
# print print_simple_bass([["Am"],["Dm"],["E", "Am"]], attr, 0)
# print print_part_attributes(attr)
# print print_simple_chord_chain([["Am"],["Dm"],["E", "Am"]], attr, 0)

# print print_chord('Em', "", 4, 24)
def init_key_array(fifths):
  global KeyArray
  KeyArray = [0, 0, 0, 0, 0, 0, 0]
  cur = 6
  step = 3
  val = -1
  if fifths > 0:
    cur = 3
    val = 1
    step = 4
  iterations = abs(fifths)
  for i in xrange(iterations):
    KeyArray[cur] = val
    cur = (cur+step)%7

#init_key_array(2)
#print KeyArray
#print "B"
#print is_accidental("B", -1)
#print "A#"
#print is_accidental("A", 1)
#print "F#"
#print is_accidental("F", 1)
#print "G"
#print is_accidental("B", 0)
#print "Eb"
#print is_accidental("E", -1)

