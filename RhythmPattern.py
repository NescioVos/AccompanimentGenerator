# The function returns an array of durations for given
# template given by a string and time=beats/beat_type
def get_rhythm_measure_by_template(template, beats, beat_type, part_sign):
  print "Template = " + str(template)
  print "Time = " + str(beats) + "/" + str(beat_type)
  max_duration = beats * 24
  print "Max duration = " + str(max_duration)
  whole = beat_type * 24
  print "Whole duration = " + str(whole)
  if template == 0:
    return [max_duration]
  if template == 20:
    return [max_duration / 2, max_duration / 2]

  if template < 100 or template == 116:
    note = 24
    if template == 116:
      note = whole / 16
    else:
      note = whole * (template / 10) / (template % 10)
    notes_num = max_duration / note
    res = []
    for dur in xrange(notes_num):
      res.append(note)
    if max_duration % note != 0:
      res.append(max_duration - notes_num * note)
    return res
  if template == 400:
    if beats / beat_type != 1:
      print "ERROR: 3+2 can be used with C or 4/4 or 2/2 time"
      return []
    if part_sign == "bass":
      return get_rhythm_measure_by_template(38, 4, 4, "")
    return get_rhythm_measure_by_template(18, 4, 4, "")
  print "ERROR: sorry, we cann't handle this template yet."
  return []


# measure is a list of chords
# rhythm_template is a code of template
# octave is an integer value
# returns a list of tuples (chord, octave, duration, accent)
def get_measure_for_pattern(measure, rhythm_template, octave, beat, beat_type, part_sign=""):
  pattern = get_rhythm_measure_by_template(rhythm_template, beat, beat_type, part_sign)
  if len(pattern) == 0:
    return []
  ch_mes = []
  if rhythm_template == 400:
    if len(measure) == 1:
      for pat in pattern:
        ch_mes.append((measure[0], octave, pat))
      if part_sign == "bass":
        return ch_mes
      print ch_mes[0]
      ch_mes[0] += (1,)
      ch_mes[3] += (1,)
      ch_mes[6] += (1,)
      return ch_mes
    if len(measure) == 2:
      if part_sign == "bass":
        ch_mes.append((measure[0], octave, pattern[0]))
        ch_mes.append((measure[0], octave, pattern[1]))
        ch_mes.append((measure[1], octave, pattern[2]))
      else:
        for i in xrange(6):
          ch_mes.append((measure[0], octave, pattern[i]))
        ch_mes.append((measure[1], octave, pattern[6]))
        ch_mes.append((measure[1], octave, pattern[7]))
        ch_mes[0] += (1,)
        ch_mes[3] += (1,)
        ch_mes[6] += (1,)
      return ch_mes
    if len(measure) == 3:
      if part_sign == "bass":
        for i in xrange(3):
          ch_mes.append((measure[i], octave, pattern[i]))
        return ch_mes
      for i in xrange(3):
        ch_mes.append((measure[0], octave, pattern[i]))
      for i in xrange(3, 6):
        ch_mes.append((measure[1], octave, pattern[i]))
      ch_mes.append((measure[2], octave, pattern[6]))
      ch_mes.append((measure[2], octave, pattern[7]))
      ch_mes[0] += (1,)
      ch_mes[3] += (1,)
      ch_mes[6] += (1,)
      return ch_mes
  if len(measure) == 1:
    for r in pattern:
      ch_mes.append((measure[0], octave, r))
  elif len(measure) == len(pattern):
    for i in xrange(len(measure)):
      ch_mes.append((measure[i], octave, pattern[i]))
  elif len(pattern) > len(measure):
    if len(measure) == 2:
      for i in xrange(len(pattern) / 2):
        ch_mes.append((measure[0], octave, pattern[i]))
      for i in xrange(len(pattern) / 2, len(pattern)):
        ch_mes.append((measure[1], octave, pattern[i]))
    elif len(measure) == 3:
      for i in xrange(len(pattern) - 2):
        ch_mes.append((measure[0], octave, pattern[i]))
      ch_mes.append((measure[1], octave, pattern[-2]))
      ch_mes.append((measure[2], octave, pattern[-1]))
    else:
      print "ERROR: cann't resolve this pattern yet :'("
  else:
    if len(measure) == 2:  # len(pattern) == 1
      ch_mes.append((measure[0], octave, pattern[0] / 2))
      ch_mes.append((measure[1], octave, pattern[0] / 2))
    elif len(measure) == 3:
      if len(pattern) == 1:
        if pattern[0] % 3 == 0:
          for ch in measure:
            ch_mes.append((ch, octave, pattern[0] / 3))
        elif pattern[0] % 4 == 0:
          ch_mes.append((measure[0], octave, pattern[0] / 2))
          ch_mes.append((measure[1], octave, pattern[0] / 4))
          ch_mes.append((measure[2], octave, pattern[0] / 4))
        else:
          print "ERROR: cann't parse measure " + measure[0] + ", "
          + measure[1] + ", " + measure[2] + ") for given pattern"
      else:  # len == 2
        ch_mes.append((measure[0], octave, pattern[0]))
        ch_mes.append((measure[1], octave, pattern[1] / 2))
        ch_mes.append((measure[2], octave, pattern[1] / 2))
    elif len(measure) == 4:
      if len(pattern) == 1:
        for ch in measure:
          ch_mes.append((ch, octave, pattern[0] / 2))
      elif len(pattern) == 2:
        ch_mes.append((measure[0], octave, pattern[0] / 2))
        ch_mes.append((measure[1]), octave, pattern[0] / 2)
        ch_mes.append((measure[2], octave, pattern[1] / 2))
        ch_mes.append((measure[3]), octave, pattern[2] / 2)
  return ch_mes



  # print get_rhythm_measure_by_template(0, 3, 4)
  # print get_rhythm_measure_by_template(20, 3, 4)
  # print get_measure_for_pattern(['C', 'F', 'G'], 400, 4, 4, 4)
  # print get_measure_for_pattern(['C', 'F', 'G'], 18, 4, 4, 4)
  # print get_measure_for_pattern(['C', 'G'], 14, 4, 2, 4)
  # print get_rhythm_measure_by_template(400, 3, 4)
  # print get_rhythm_measure_by_template(300, 3, 4)
