def detect_text_emotion(text):

    t=text.lower()

    if any(w in t for w in [
      "sad","failed","hurt","depressed"
    ]):
        return "sad"

    if any(w in t for w in [
      "angry","furious","mad"
    ]):
        return "angry"

    if any(w in t for w in [
      "stressed","panic","worried"
    ]):
        return "stressed"

    return "neutral"



def detect_voice_emotion(stats):

    if not stats:
        return None

    volume=stats.get(
      "volume",
      0
    )

    duration=stats.get(
      "duration",
      0
    )


    if volume>0.6 and duration<2:
        return "angry"


    if duration>5 and volume<0.2:
        return "sad"


    return None



def combine_emotion(
   text,
   stats=None
):

    v=detect_voice_emotion(
      stats
    )

    if v:
       return v

    return detect_text_emotion(
       text
    )