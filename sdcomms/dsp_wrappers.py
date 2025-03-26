from schemdraw.dsp import Filter as DSPFilter
from .comms import OPTcol, OPTfill


class Filter(DSPFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("fill", OPTfill)
        kwargs.setdefault("color", OPTcol)
        super().__init__(*args, **kwargs)
