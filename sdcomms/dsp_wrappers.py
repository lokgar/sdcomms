from schemdraw.dsp import Filter as DSPFilter
from .comms import OPTcol


class Filter(DSPFilter):
    """Filter

    Args:
        response: Filter response ('lp', 'bp', 'hp', or 'notch') for
            low-pass, band-pass, high-pass, and notch/band-stop filters

    Anchors:
        * N
        * S
        * E
        * W
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("fill", "white")
        super().__init__(*args, **kwargs)
