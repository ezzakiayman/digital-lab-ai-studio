"""Find a genuinely quiet PCM location before adding pedagogical silence."""
from array import array
import math
import sys


def quiet_cut(pcm, rate, sample_width, channels, before, after):
    if sample_width != 2:
        return None
    width = sample_width * channels
    count = len(pcm) // width
    radius = max(1, round(.04 * rate))
    first, last = max(radius, round(before * rate)), min(count-radius, round(after * rate))
    if first > last:
        return None
    midpoint = min(last, max(first, round((before+after)/2*rate)))
    candidates = {midpoint, first, last, *range(first,last+1,max(1,round(.005*rate)))}
    for sample in sorted(candidates,key=lambda n:abs(n-midpoint)):
        values = array('h', pcm[(sample-radius)*width:(sample+radius)*width])
        if sys.byteorder != 'little':
            values.byteswap()
        if not values:
            continue
        rms = math.sqrt(sum(v*v for v in values)/len(values))/32768
        peak = max(abs(v) for v in values)/32768
        if rms <= 10**(-55/20) and peak <= .01:
            return sample
    return None
