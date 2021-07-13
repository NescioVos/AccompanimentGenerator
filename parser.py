#!/usr/bin/python
import sys
import tokens

import PartAttributes as PA

Buffer = ""
# Attributes consist of
# Flags:
# 0 - default
# 1 - instrumental
# 1<<1 - acoustic (no drums, no bass)
# 1<<2 + violin
# 1<<3 + 2 violins
# 1<<4 + viola. For acoustic string quartet 0x3a. For acoustic string trio 0x36
# 1<<5 + cello
# 1<<6 + piano
######################
Attributes = {"Flags": 0, "Clef": {"key": "G", "line": 2}, "KeyAlt": 0, "Mode": "major",
              "Tempo": 90, "Time": {"beats": 4, "beat_type": 4}, "Rhythm": 0,
              "Bass_r": 1, "Guitar_r": 1, "Def_duration": 16, "AmericanNotation": 0}
Chain = []
OutFile = "out.xml"


def print_tabs():
  global Buffer
  Buffer += tokens.print_tabs()


def next_level():
  global Buffer
  Buffer += tokens.next_level()


def prev_level():
  global Buffer
  Buffer += tokens.prev_level()


def parse_key(key):
  global Attributes
  if not (key[0] in "ABCDEFGHabcdefgh"):
    print "Error in key signature"
    return
  if len(key) > 1:
    if key[1] != 's' and key[1] != 'b' and key[1] != 'm':
      print "Error in key signature"
      return
    if key[1] == 'm':
      Attributes["Mode"] == "minor"
    if len(key) > 2:
      if key[1] == 'm':
        print "Error in key signature"
        return
      if key[2] != 'm':
        print "Error in key signature"
        return
      if len(key) > 3:
        print "Error in key signature. Appendix symbols in tail."
        return
      #  print "Key = "+key
  if key[-1] == "m":
    Attributes["Mode"] = "minor"
  if key == "C" or key == "Am":
    return
  if key == "G" or key == "Em":
    Attributes["KeyAlt"] = 1
    return
  if key == "D" or key == "Hm":
    Attributes["KeyAlt"] = 2
    return
  if key == "A" or key == "Fsm":
    Attributes["KeyAlt"] = 3
    return
  if key == "E" or key == "Csm":
    Attributes["KeyAlt"] = 4
    return
  if key == "H" or key == "Gsm":
    Attributes["KeyAlt"] = 5
    return
  if key == "Fs" or key == "Dsm":
    Attributes["KeyAlt"] = 6
    return
  if key == "Cs" or key == "Asm":
    Attributes["KeyAlt"] = 7
    return
  if key == "F" or key == "Dm":
    Attributes["KeyAlt"] = -1
    return
  if key == "B" or key == "Gm":
    Attributes["KeyAlt"] = -2
    return
  if key == "Eb" or key == "Cm":
    Attributes["KeyAlt"] = -3
    return
  if key == "Ab" or key == "Fm":
    Attributes["KeyAlt"] = -4
    return
  if key == "Db" or key == "Bm":
    Attributes["KeyAlt"] = -5
    return
  if key == "Gb" or key == "Ebm":
    Attributes["KeyAlt"] = -6
    return
  print "Key signature is rarely used. Use simple instead."


def parse_tempo(tempo):
  global Attributes
  Attributes["Tempo"] = int(tempo)


def parse_time(time):
  global Attributes
  t_list = time.split('-')
  if len(t_list) == 1:
    if time == "c" or time == "C" or time == "4":
      return
    Attributes["Time"]["beats"] = int(time)
    return
  if len(t_list) == 2:
    Attributes["Time"]["beats"] = int(t_list[0])

    Attributes["Time"]["beat_type"] = int(t_list[1])
    return
  print "Error in parsing time signature"


# Rhythm:
# 0 -> 0
# 0-2 -> 20
# 1-2 -> 12
# 1-3 -> 13
# 1-4 -> 14
# 1-8 -> 18
# 1-6 -> 16
# 1-16 -> 116
# 3-8 -> 38
# clave -> 300
# 3+2 ->  400
# bossa -> 500
def parse_rhythm(rhythm):
  global Attributes
  if len(rhythm) == 1 and rhythm != '0':
    print "Error in parsing rhythm template. No template " + rhythm + " found."
    return
  if rhythm == '0':
    Attributes['Rhythm'] = 0
    return
  if len(rhythm) > 4:
    if rhythm == 'clave':
      Attributes['Rhythm'] = 300
      return
    if rhythm == 'bossa':
      Attributes['Rhythm'] = 500
      return
    print "Error in parsing rhythm template. No template " + rhythm + " found."
    return
  r_list = rhythm.split('-')
  if len(r_list) == 2:
    if r_list[0] == '0':
      if r_list[1] == '2':
        Attributes['Rhythm'] = 20
        return
      else:
        print "Error in parsing rhythm template. No template " + rhythm + " found."
        return
    if r_list[1] != '2' and r_list[1] != '4' and r_list[1] != '8' and r_list[1] != '16':
      print "Error in parsing rhythm template. No template " + rhythm + " found."
      return
    if r_list[0].isdigit() and r_list[1].isdigit() and int(r_list[1]) != 0:
      Attributes['Rhythm'] = int(r_list[0] + r_list[1])
      return
    print "Error in parsing rhythm template. No template " + rhythm + " found."
    return
  if rhythm == "3+2":
    Attributes['Rhythm'] = 400
    return
  print "Error in parsing rhythm template. No template " + rhythm + " found."


# Call this function after all parameters was parsed
# Validate returns 0 if all OK and 1 else
def validate():
  global Attributes
  if Attributes['Rhythm'] > 200 and (Attributes['Time']['beats'] != 4 or Attributes['Time']['beats-type'] != 4):
    print "Error in validating rhythm template with time-beats."
    return 1
  if Attributes['Rhythm'] == 400:
    Attributes['Def_duration'] = 8
    Attributes['Guitar_r'] = 1
    Attributes['Bass_r'] = 3
    return 0
  if Attributes['Rhythm'] == 0 and Attributes['Time']['beats'] == 4 and Attributes['Time']['beats-type'] == 4:
    Attributes['Def_duration'] = 4
    Attributes['Guitar_r'] = 4
    Attributes['Bass_r'] = 4
    return 0

  return 0


# This is comma-separated chord chain.
# Each sequence between commas are measures.
# All chord in chain will be set in accordance with rhythm template.
# Chords in measure are separated by /
def parse_chain(chain_str):
  global Chain
  print "PARSE CHAIN"
  tmp_chain = chain_str.split(",")
  for measure in tmp_chain:
    m_chords = measure.split("/")
    for chord in m_chords:
      if not (chord[0] in "ABCDEFGHRabcdefghr"):
        print "Error in parsing chord " + chord
        return
      for c in chord[1:]:
        if not (c in "795FKMSfkms"):
          print "Error in parsing chord " + chord
          return
    Chain.append(m_chords)


def print_help():
  print "MusicXML song generator ver. 0.1"
  print "-o [file] -- specify output"
  print "-i -- instrumental, without vocals"
  print "-a -- acoustic, without drum"
  print "-v -- with violin"
  print "-V -- with 2 violins"
  print "-A -- with viola"
  print "-c -- with cello"
  print "-p -- with piano"
  print "-q -- generate quartet = -a -V -A -c"
  print "-t -- generate string trio = -a -v -A -c"
  print "-n -- use american notation. It means that B means Ti note instead of Ti-flat"
  print "-K [Key][s|b][m] -- key of the track"
  print "-T [tempo] -- tempo of the track"
  print "-B [beats]-[type] -- beats of the track"
  print "-R [rhythm] - rhythm template of the track. Values could be "
  print "   0 for whole measure independent from beats"
  print "   0-2 half measure independent from beats"
  print "   1-2 -- half note, available for 4/4 and 2/2"
  print "   1-3 -- triples"
  print "   1-4 -- quarts"
  print "   1-8 -- eights"
  print "   1-16 -- sixteens"
  print "   3-8  -- quarts with points"
  print "   clave -- 3-8 and halves available only for 4/4"
  print "   3+2 -- bass is 3-8 and rhythm is 1-8, available only for 4/4"
  print "   bossa -- bossa style"


# -i -- instrumental, without vocals
# -a -- acoustic, without drum and bass
# -v -- with violin
# -V -- with 2 violins
# -A -- with viola
# -c -- with cello
# -p -- with piano
# -q -- generate quartet = -a -V -A
# -t -- generate string trio = -a -v -A
# -K [Key][s|b][m] -- key of the track
# -T [tempo] -- tempo of the track
# -B [beats]-[type] -- beats of the track
# -R [rhythm] - rhythm template of the track. Values could be
#   0 for whole measure independent from beats
#   0-2 half measure independent from beats
#   1-2 -- half note, available for 4/4 and 2/2
#   1-3 -- triples
#   1-4 -- quarts
#   1-8 -- eights
#   1-16 -- sixteens
#   3-8  -- quarts with points
#   clave -- 3-8 and halves available only for 4/4
#   3+2 -- bass is 3-8 and rhythm is 1-8, available only for 4/4
#   bossa -- bossa style
def parse_command_line(c_list):
  flags = 0
  global Attributes
  global OutFile
  cur_param = ""
  for el in c_list:
    if el[0] == "-" and len(el) == 2:
      if el == "-i":
        print "Do not generate vocals"
        flags |= 1
      if el == "-a":
        print "Do not generate drums"
        flags |= 1 << 1
      if el == "-v":
        print "Add violin to score"
        flags |= 1 << 2
      if el == "-V":
        print "Add 2 violins to score"
        flags |= 1 << 3
        continue
      if el == "-A":
        print "Add viola to score"
        flags |= 1 << 4
        continue
      if el == "-c":
        print "Add cello to score"
        flags |= 1 << 5
        continue
      if el == "-p":
        print "Add piano to score"
        flags |= 1 << 6
        continue
      if el == "-q":
        print "Add string quartet to score"
        flags |= 0x3a
      if el == "-t":
        print "Add string trio to score"
        flags |= 0x36
      if el == "-h":
        print_help()
        return 1
      if el == "-n":
        print "Use american notation"
        Attributes["AmericanNotation"] = 1
      else:
        cur_param = el[1]
        continue
    else:
      if cur_param == "o":
        OutFile = el
        cur_param = ""
        continue
      if cur_param == "K":
        parse_key(el)
        cur_param = ""
        continue
      if cur_param == "T":
        parse_tempo(el)
        cur_param = ""
        continue
      if cur_param == "B":
        parse_time(el)
        cur_param = ""
        continue
      if cur_param == "R":
        parse_rhythm(el)
        cur_param = ""
        continue
      else:  # chain
        print "PC!!"
        parse_chain(el)
        break  # ignore all attributes after chain
  Attributes["Flags"] = flags
  print Attributes
  return 0


def score_begin():
  global Buffer
  Buffer += "<score-partwise version=\"3.0\">\n"


def score_end():
  global Buffer
  Buffer += "</score-partwise>\n"


def print_part_list(part_list):
  global Attributes
  global Buffer
  if not (Attributes["Flags"] & 1):  # not instrumental
    part_list.append("Vocal")
  if Attributes["Flags"] & 1<<3:
    part_list.append("Violin1")
    part_list.append("Violin2")
  elif Attributes["Flags"] & 1<<2:
    part_list.append("Violin")

  if Attributes["Flags"] & 1<<4:
    part_list.append("Viola")

  if Attributes["Flags"] & 1<<5:
    part_list.append("Cello")
  if Attributes["Flags"] & 1<<6:
    part_list.append("Piano")
  part_list += ["Pad"]
  part_list += ["Guitar"]
  if not (Attributes["Flags"] & 2):  # not acoustic
    part_list.append("Bass")
    part_list.append("Drum Set")

  Buffer += tokens.print_part_list(part_list, Attributes)


# rhythm_pattern is a list of durations for chords in a measure
def print_pad_part():
  global Chain
  global Buffer
  global Attributes
  pad = PA.PartAttributes('G', 2, 0, Attributes["Tempo"], 4, Attributes["Mode"], Attributes["KeyAlt"],
                          Attributes["Time"]["beats"], Attributes["Time"]["beat_type"])

  Buffer += tokens.print_simple_chord_chain(Chain, pad, Attributes["AmericanNotation"])


def print_bass_part():
  global Chain
  global Buffer
  global Attributes
  bass = PA.PartAttributes("F", 4, Attributes["Rhythm"], Attributes["Tempo"], 2, Attributes["Mode"], Attributes["KeyAlt"],
                           Attributes["Time"]["beats"], Attributes["Time"]["beat_type"])

  Buffer += tokens.print_simple_bass(Chain, bass, Attributes["AmericanNotation"])


def print_cello_part():
  global Chain
  global Buffer
  global Attributes
  cello = PA.PartAttributes("F", 4, Attributes["Rhythm"], Attributes["Tempo"], 2, Attributes["Mode"], Attributes["KeyAlt"],
                            Attributes["Time"]["beats"], Attributes["Time"]["beat_type"])
  Buffer += tokens.print_rests(len(Chain), cello)


def print_vocal_part():
  global Chain
  global Buffer
  global Attributes
  vocal = PA.PartAttributes("G", 2, Attributes["Rhythm"], Attributes["Tempo"], 4, Attributes["Mode"], Attributes["KeyAlt"],
                            Attributes["Time"]["beats"], Attributes["Time"]["beat_type"])
  Buffer += tokens.print_rests(len(Chain), vocal)


def print_piano_part():
  global Chain
  global Buffer
  global Attributes
  piano = PA.PartAttributes("G", 2, Attributes["Rhythm"], Attributes["Tempo"], 2, Attributes["Mode"], Attributes["KeyAlt"],
                            Attributes["Time"]["beats"], Attributes["Time"]["beat_type"], 2)
  #Buffer += tokens.print_rests(len(Chain), piano, 2)
  Buffer += tokens.print_2staff_part(Chain, piano, Attributes["AmericanNotation"])

def print_drums_part():
  global Chain
  global Buffer
  global Attributes
  drums = PA.PartAttributes("percussion", 3, Attributes["Rhythm"], Attributes["Tempo"], 0, Attributes["Mode"],
                            0, Attributes["Time"]["beats"], Attributes["Time"]["beat_type"])
  Buffer += tokens.print_rests(len(Chain), drums)

def print_viola_part():
  global Chain
  global Buffer
  global Attributes
  viola = PA.PartAttributes("C", 3, Attributes["Rhythm"], Attributes["Tempo"], 4, Attributes["Mode"], Attributes["KeyAlt"],
                            Attributes["Time"]["beats"], Attributes["Time"]["beat_type"])
  Buffer += tokens.print_rests(len(Chain), viola)

def print_violin_part():
  global Chain
  global Buffer
  global Attributes
  violin = PA.PartAttributes("G", 2, Attributes["Rhythm"], Attributes["Tempo"], 4, Attributes["Mode"], Attributes["KeyAlt"],
                            Attributes["Time"]["beats"], Attributes["Time"]["beat_type"])
  Buffer += tokens.print_rests(len(Chain), violin)

def print_guitar_part():
  global Chain
  global Buffer
  global Attributes
  guitar = PA.PartAttributes("G", 2, Attributes["Rhythm"], Attributes["Tempo"], 4, Attributes["Mode"], Attributes["KeyAlt"],
                            Attributes["Time"]["beats"], Attributes["Time"]["beat_type"])
  Buffer += tokens.print_simple_chord_chain(Chain, guitar, Attributes["AmericanNotation"])


def print_part(part_name):
  if part_name == "Pad":
    print_pad_part()
    return
  if part_name == "Bass":
    print_bass_part()
    return
  if part_name == "Cello":
    print_cello_part()
    return
  if part_name == "Vocal":
    print_vocal_part()
    return
  if part_name == "Piano":
    print_piano_part()
    return
  if part_name == "Drum Set":
    print_drums_part()
    return
  if part_name == "Viola":
    print_viola_part()
    return
  if part_name == "Violin" or part_name[0:-1] == "Violin":
    print_violin_part()
    return
  if part_name == "Guitar":
    print_guitar_part()
    return
  print "Here must be writing of " + part_name


def print_parts(part_list):
  global Buffer
  for i in xrange(len(part_list)):
    print_tabs()
    Buffer += "<part id=\"P" + str(i) + "\">\n"
    tokens.increment_level()
    print_part(part_list[i])
    prev_level()
    Buffer += "</part>\n"


def print_musXML_to_Buf():
  global Buffer
  global Attributes
  Buffer += tokens.print_header()
  score_begin()
  next_level()

  part_list = []
  print_part_list(part_list)
  print_parts(part_list)
  #
  prev_level()
  score_end()


# main
res = parse_command_line(sys.argv[1:])
if res == 1:
  exit(0)
print_musXML_to_Buf()
f = open(OutFile, 'w')
f.write(Buffer)
f.close()
# print Buffer
print "Chain is"
print Chain
