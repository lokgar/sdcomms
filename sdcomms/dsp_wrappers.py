from schemdraw.dsp import (
    Filter as DSPFilter,
    Adc as DSPAdc,
    Dac as DSPDac,
    Multiplexer as DSPMultiplexer,
)

OPT = "#154d76"
OPTfill = "white"
RF = "#8b0000"
RFfill = "white"
OPTRF = "#663399"
OPTRFfill = "white"


class Filter(DSPFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("fill", OPTfill)
        kwargs.setdefault("color", OPT)
        super().__init__(*args, **kwargs)
