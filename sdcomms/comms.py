import os
import math
import random
from typing import Sequence, Tuple

import schemdraw
import schemdraw.elements
from schemdraw import dsp

from schemdraw.elements import Element
from schemdraw.segments import Segment, SegmentArc, SegmentCircle, SegmentPoly

from schemdraw.util import linspace


OPTcol = "#1f77b4"
RFcol = "#d62728"
OPTRFcol = "#9467bd"


class Bend90(Element):
    """A generic bend in a communications schematic.

    Creates a bend with a fixed radius.7

    Parameters
    ----------
    radius : float, default=1
        Radius of the bend

    Anchors
    -------
    in : The input point of the bend
    out : The output point of the bend
    """

    # bend with radius, theta start and theta stop, basically just a circle
    def __init__(self, radius=1, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(SegmentArc((0, 0), 2 * radius, 2 * radius, 0, 90))

        self.anchors["in"] = (radius, 0)
        self.anchors["out"] = (0, radius)
        self.elmparams["drop"] = (0, radius)


class Bend180(Element):
    """A generic bend in a communications schematic.

    Creates a bend with a fixed radius.

    Parameters
    ----------
    radius : float, default=1
        Radius of the bend
    **kwargs :
        Other Element keyword arguments.
    Anchors
    -------
    in : The input point of the bend
    out : The output point of the bend
    """

    # bend with radius, theta start and theta stop, basically just a circle
    def __init__(self, radius=1, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(SegmentArc((0, 0), 2 * radius, 2 * radius, 0, 180))

        self.anchors["in"] = (radius, 0)
        self.anchors["out"] = (-radius, 0)
        self.elmparams["drop"] = (-radius, 0)


class Rectangle(Element):
    """A rectangular block element with customizable dimensions and anchors.

    This element creates a rectangular block with configurable width, height,
    and number of anchor points on each side.

    Parameters
    ----------
    width : float, default=1
        Width of the rectangle.
    height : float, default=1
        Height of the rectangle.
    numN : int, default=1
        Number of anchor points on the North (top) edge.
    numS : int, default=1
        Number of anchor points on the South (bottom) edge.
    numE : int, default=1
        Number of anchor points on the East (right) edge.
    numW : int, default=1
        Number of anchor points on the West (left) edge.
    **kwargs :
        Other Element keyword arguments.

    Anchors
    -------
    N{i} : tuple
        Points along the top edge, from left to right, where i goes from 0 to numN-1.
        Evenly spaced along the edge.
    S{i} : tuple
        Points along the bottom edge, from left to right, where i goes from 0 to numS-1.
        Evenly spaced along the edge.
    E{i} : tuple
        Points along the right edge, from top to bottom, where i goes from 0 to numE-1.
        Evenly spaced along the edge.
    W{i} : tuple
        Points along the left edge, from top to bottom, where i goes from 0 to numW-1.
        Evenly spaced along the edge.
    """

    def __init__(
        self,
        width=1,
        height=1,
        numN=1,
        numS=1,
        numE=1,
        numW=1,
        fillcol="white",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.width = width
        self.height = height
        self.numN = numN
        self.numS = numS
        self.numE = numE
        self.numW = numW
        self.fillcol = fillcol

        self.segments.append(
            SegmentPoly(
                [
                    (0, -self.height / 2),
                    (self.width, -self.height / 2),
                    (self.width, self.height / 2),
                    (0, self.height / 2),
                    (0, -self.height / 2),
                ],
                fill=self.fillcol,
            )
        )
        self.elmparams["lblloc"] = "center"
        self.elmparams["lblofst"] = 0

        for i in range(numN):
            self.anchors[f"N{i}"] = (
                (i + 1) * self.width / (numN + 1),
                self.height / 2,
            )

        for i in range(numS):
            self.anchors[f"S{i}"] = (
                (i + 1) * self.width / (numS + 1),
                -self.height / 2,
            )

        for i in range(numE):
            self.anchors[f"E{i}"] = (
                self.width,
                ((i + 1) * self.height / (numE + 1)) - self.height / 2,
            )

        for i in range(numW):
            self.anchors[f"W{i}"] = (
                0,
                ((i + 1) * self.height / (numW + 1)) - self.height / 2,
            )

        self.elmparams["drop"] = self.anchors[f"E{numE - 1}"]


class Termination(Element):
    """A termination element.

    Parameters
    ----------
    **kwargs :
        Other Element keyword arguments.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.segments.append(Segment([(0, 0), (0.0, 0.2)], lw=2))
        self.segments.append(Segment([(0, 0), (0.0, -0.2)], lw=2))

        self.anchors["in"] = (0, 0)
        self.anchors["out"] = (0, 0)

        self.elmparams["drop"] = (0, 0)


class FBG(Element):
    """A fiber Bragg grating element.

    Parameters
    ----------
    **kwargs :
        Other Element keyword arguments.

    Anchors
    -------
    in : The input point of the FBG
    out : The output point of the FBG
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.segments.append(
            SegmentPoly(
                [
                    (0, -0.5 / 2),
                    (1, -0.5 / 2),
                    (1, 0.5 / 2),
                    (0, 0.5 / 2),
                    (0, -0.5 / 2),
                ],
            )
        )

        for i in range(4):
            self.segments.append(
                SegmentPoly(
                    [
                        (0.15 + i * 0.2, 0.5 / 2),
                        (0.15 + i * 0.2, 0.5 / 2 + 0.075),
                        (0.25 + i * 0.2, 0.5 / 2 + 0.075),
                        (0.25 + i * 0.2, 0.5 / 2),
                        (0.15 + i * 0.2, 0.5 / 2),
                    ],
                    fill=True,
                )
            )

            self.segments.append(
                SegmentPoly(
                    [
                        (0.15 + i * 0.2, -0.5 / 2),
                        (0.15 + i * 0.2, -0.5 / 2 - 0.075),
                        (0.25 + i * 0.2, -0.5 / 2 - 0.075),
                        (0.25 + i * 0.2, -0.5 / 2),
                        (0.15 + i * 0.2, -0.5 / 2),
                    ],
                    fill=True,
                )
            )

        self.anchors["in"] = (0, 0)
        self.anchors["out"] = (1, 0)

        self.elmparams["drop"] = (1, 0)
        self.label("FBG", loc="center", ofst=(0, -0.03))


class MUX(Element):
    """A generic multiplexer element.

    Parameters
    ----------
    numE : int, default=1
        Number of anchor points on the East (right) edge.
    numW : int, default=1
        Number of anchor points on the West (left) edge.
    **kwargs :
        Other Element keyword arguments.

    Anchors
    -------
    E{i} : tuple
        Points along the right edge, from top to bottom, where i goes from 0 to numE-1.
        Evenly spaced along the edge.
    W{i} : tuple
        Points along the left edge, from top to bottom, where i goes from 0 to numW-1.
        Evenly spaced along the edge.
    """

    def __init__(self, numE=1, numW=1, **kwargs):
        super().__init__(**kwargs)

        height1 = 2.5
        height2 = 1
        width = 1

        self.segments.append(
            SegmentPoly(
                [
                    (0, height1 / 2),
                    (width, height2 / 2),
                    (width, -height2 / 2),
                    (0, -height1 / 2),
                    (0, height1 / 2),
                ],
                fill="white",
            )
        )

        for i in range(numE):
            self.anchors[f"E{i}"] = (
                width,
                ((i + 1) * height2 / (numE + 1)) - height2 / 2,
            )

        for i in range(numW):
            self.anchors[f"W{i}"] = (
                0,
                ((i + 1) * height1 / (numW + 1)) - height1 / 2,
            )

        self.elmparams["drop"] = self.anchors[f"E{numE - 1}"]
        self.elmparams["lblloc"] = "center"
        self.elmparams["lblofst"] = 0

        self.label("MUX", loc="center")


class Circulator(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        radius = 0.5

        self.segments.append(SegmentCircle((0, 0), radius, fill="white"))
        self.segments.append(SegmentArc((0, 0), 1.2 * radius, 1.2 * radius, -70, 200))

        def _rotate(points, angle_degrees):
            angle_radians = math.radians(angle_degrees)
            cos_a = math.cos(angle_radians)
            sin_a = math.sin(angle_radians)

            rotated_points = []
            for x, y in points:
                x_new = x * cos_a - y * sin_a
                y_new = x * sin_a + y * cos_a
                rotated_points.append((x_new, y_new))

            return rotated_points

        arrow = [(-0.08, 0), (0.08, 0.06), (0.08, -0.06)]
        arrow_rotated = _rotate(arrow, 30)
        # shift to the new origin
        arrow_rotated = [
            (
                x + 0.6 * radius * math.cos(math.radians(-70)),
                y + 0.6 * radius * math.sin(math.radians(-70)),
            )
            for x, y in arrow_rotated
        ]
        self.segments.append(SegmentPoly(arrow_rotated, fill=True))

        self.anchors["1"] = (-radius, 0)
        self.anchors["2"] = (radius, 0)
        self.anchors["3"] = (0, -radius)

        self.elmparams["drop"] = (radius, 0)


class BS(Rectangle):
    """A beam splitter element.

    Parameters
    ----------
    width : float, default=0.3
        Width of the beam splitter.
    height : float, default=0.3
        Height of the beam splitter.
    numN : int, default=1
        Number of anchor points on the North (top) edge.
    numS : int, default=1
        Number of anchor points on the South (bottom) edge.
    numE : int, default=1
        Number of anchor points on the East (right) edge.
    numW : int, default=1
        Number of anchor points on the West (left) edge.
    **kwargs :
        Other Element keyword arguments.

    Anchors
    -------
    N{i} : tuple
        Points along the top edge, from left to right, where i goes from 0 to numN-1.
        Evenly spaced along the edge.
    S{i} : tuple
        Points along the bottom edge, from left to right, where i goes from 0 to numS-1.
        Evenly spaced along the edge.
    E{i} : tuple
        Points along the right edge, from top to bottom, where i goes from 0 to numE-1.
        Evenly spaced along the edge.
    W{i} : tuple
        Points along the left edge, from top to bottom, where i goes from 0 to numW-1.
        Evenly spaced along the edge.
    """

    def __init__(self, width=0.6, height=0.6, numN=1, numS=1, numE=1, numW=1, **kwargs):
        super().__init__(
            width=width,
            height=height,
            numN=numN,
            numS=numS,
            numE=numE,
            numW=numW,
            fillcol="white",
            **kwargs,
        )
        self.segments.append(
            Segment([(0, self.height / 2), (self.width, -self.height / 2)])
        )


class CouplerDot(Rectangle):
    """A coupler element.

    Anchors
    -------
    N0, S0, E0, W0
    """

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            width=0,
            height=0,
            numN=1,
            numS=1,
            numE=1,
            numW=1,
            **kwargs,
        )
        self.elmparams["drop"] = (0, 0)


class CouplerCirc(Element):
    """
    Anchors
    -------
    N0, S0, E0, W0
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        w, h = 0.3, 0.15
        # There's no ellipse Segment type, so draw one with a path Segment
        t = linspace(0, math.pi * 2, num=50)
        y = [(h / 2) * math.sin(t0) for t0 in t]
        x = [(w / 2) * math.cos(t0) + w / 2 for t0 in t]
        x[-1] = x[0]
        y[-1] = y[0]  # Ensure the path is actually closed
        self.segments.append(Segment(list(zip(x, y)), fill="white"))

        self.anchors["N0"] = (w / 2, h / 2)
        self.anchors["S0"] = (w / 2, -h / 2)
        self.anchors["E0"] = (w, 0)
        self.anchors["W0"] = (0, 0)
        self.elmparams["drop"] = (w, 0)


class Fiber(Rectangle):
    """A fiber element.

    Parameters
    ----------
    **kwargs :
        Other Element keyword arguments.

    Anchors
    -------
    in : The input point of the fiber
    out : The output point of the fiber
    """

    def __init__(self, **kwargs):
        super().__init__(
            width=1.1,
            height=0.9,
            fillcol="white",
            numE=1,
            numW=1,
            numN=1,
            numS=1,
            **kwargs,
        )

        self.radius = 0.3
        self.length = 1
        self.segments.append(Segment([(0.1, -0.3), (self.length, -0.3)]))
        self.segments.append(
            SegmentCircle(
                (0.05 + self.length / 2 - 0.125, self.radius - 0.3),
                self.radius,
                fill=False,
            )
        )
        self.segments.append(
            SegmentCircle(
                (0.05 + self.length / 2, self.radius - 0.3), self.radius, fill=False
            )
        )
        self.segments.append(
            SegmentCircle(
                (0.05 + self.length / 2 + 0.125, self.radius - 0.3),
                self.radius,
                fill=False,
            )
        )


class PolCtrl(Element):
    """A polarization controller element.
    Parameters
    ----------
    **kwargs :
        Other Element keyword arguments.
    Anchors
    -------
    in : The input point of the polarization controller
    out : The output point of the polarization controller
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.radius = 0.19
        self.length = self.radius * 6
        self.segments.append(Segment([(0, 0), (self.length, 0)]))
        self.segments.append(
            SegmentCircle(
                (self.length / 2 - 2 * self.radius, self.radius),
                self.radius,
                fill=False,
            )
        )
        self.segments.append(
            SegmentCircle((self.length / 2, self.radius), self.radius, fill=False)
        )
        self.segments.append(
            SegmentCircle(
                (self.length / 2 + 2 * self.radius, self.radius),
                self.radius,
                fill=False,
            )
        )
        self.elmparams["drop"] = (self.length, 0)
        self.anchors["in"] = (0, 0)
        self.anchors["out"] = (self.length, 0)


class VOA(Element):
    """A variable optical attenuator element.

    Anchors
    -------
    W : The input point of the VOA
    E : The output point of the VOA
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.width = 0.7
        self.height = 0.7

        self.segments.append(
            SegmentPoly(
                [
                    (0, self.height / 2),
                    (self.width, self.height / 2),
                    (self.width, -self.height / 2),
                    (0, -self.height / 2),
                    (0, self.height / 2),
                ],
                fill="white",
            )
        )

        self.segments.append(
            SegmentCircle((self.width / 2, 0), self.width / 3, fill=False)
        )

        self.segments.append(
            Segment(
                [
                    (0.09, -self.height / 2 + 0.09),
                    (self.width - 0.05, self.height / 2 - 0.05),
                ],
                arrow="->",
                arrowlength=0.13,
                arrowwidth=0.1,
            )
        )

        self.elmparams["drop"] = (self.width, 0)
        self.anchors["W"] = (0, 0)
        self.anchors["E"] = (self.width, 0)


class PM(Rectangle):
    """An optical phase modulator element.

    Parameters
    ----------
    width : float, default=0.5
        Width of the modulator.
    height : float, default=0.5
        Height of the modulator.
    numN : int, default=1
        Number of anchor points on the North (top) edge.
    numS : int, default=1
        Number of anchor points on the South (bottom) edge.
    numE : int, default=1
        Number of anchor points on the East (right) edge.
    numW : int, default=1
        Number of anchor points on the West (left) edge.
    **kwargs :
        Other Element keyword arguments.

    Anchors
    -------
    N{i} : tuple
        Points along the top edge, from left to right, where i goes from 0 to numN-1.
        Evenly spaced along the edge.
    S{i} : tuple
        Points along the bottom edge, from left to right, where i goes from 0 to numS-1.
        Evenly spaced along the edge.
    E{i} : tuple
        Points along the right edge, from top to bottom, where i goes from 0 to numE-1.
        Evenly spaced along the edge.
    W{i} : tuple
        Points along the left edge, from top to bottom, where i goes from 0 to numW-1.
        Evenly spaced along the edge.
    """

    def __init__(
        self,
        width=1,
        height=0.5,
        numN=1,
        numS=1,
        numE=1,
        numW=1,
        **kwargs,
    ):
        super().__init__(
            width=width,
            height=height,
            numN=numN,
            numS=numS,
            numE=numE,
            numW=numW,
            fillcol="white",
            **kwargs,
        )

        # self.segments.append(
        #     Segment([(0, self.height / 3.25), (self.width, self.height / 3.25)])
        # )
        # self.segments.append(
        #     Segment([(0, -self.height / 3.25), (self.width, -self.height / 3.25)])
        # )

        self.label("PM", loc="center", ofst=(0, -0.035))


class MZM(Rectangle):
    """A Mach-Zehnder modulator element.

    Parameters
    ----------
    width : float, default=1.5
        Width of the modulator.
    height : float, default=0.9
        Height of the modulator.
    label : str, default="MZM"
        Label of the modulator.
    numN : int, default=1
        Number of anchor points on the North (top) edge.
    numS : int, default=1
        Number of anchor points on the South (bottom) edge.
    numE : int, default=1
        Number of anchor points on the East (right) edge.
    numW : int, default=1
        Number of anchor points on the West (left) edge.
    **kwargs :
        Other Element keyword arguments.

    Anchors
    -------
    N{i} : tuple
        Points along the top edge, from left to right, where i goes from 0 to numN-1.
        Evenly spaced along the edge.
    S{i} : tuple
        Points along the bottom edge, from left to right, where i goes from 0 to numS-1.
        Evenly spaced along the edge.
    E{i} : tuple
        Points along the right edge, from top to bottom, where i goes from 0 to numE-1.
        Evenly spaced along the edge.
    W{i} : tuple
        Points along the left edge, from top to bottom, where i goes from 0 to numW-1.
        Evenly spaced along the edge.
    """

    def __init__(
        self,
        width=1.6,
        height=1,
        label="MZM",
        numN=1,
        numS=1,
        numE=1,
        numW=1,
        **kwargs,
    ):
        super().__init__(
            width=width,
            height=height,
            numN=numN,
            numS=numS,
            numE=numE,
            numW=numW,
            fillcol="white",
            **kwargs,
        )

        a = 0.15
        d = 0.7
        cx = 0.3
        cy = 0.3

        def _mzm(x, y, a, cx, cy, d):
            return [
                Segment([(x, y), (x + a, y)]),
                SegmentPoly(
                    [
                        (x + a, y),
                        (x + a + cx, y + cy),
                        (x + a + cx + d, y + cy),
                        (x + a + 2 * cx + d, y),
                        (x + a + cx + d, y - cy),
                        ((x + a + cx, y - cy)),
                        (x + a, y),
                    ],
                    fill=False,
                ),
                Segment([(x + a + 2 * cx + d, y), (x + 2 * a + 2 * cx + d, y)]),
            ]

        self.segments.extend(_mzm(0, 0, a, cx, cy, d))

        self.label(label, loc="center", ofst=(0, -0.04))


class IQM(Rectangle):
    """An IQ modulator element.

    Parameters
    ----------
    numN : int, default=1
        Number of anchor points on the North (top) edge.
    numS : int, default=1
        Number of anchor points on the South (bottom) edge.
    numE : int, default=1
        Number of anchor points on the East (right) edge.
    numW : int, default=1
        Number of anchor points on the West (left) edge.
    **kwargs :
        Other Element keyword arguments.

    Anchors
    -------
    N{i} : tuple
        Points along the top edge, from left to right, where i goes from 0 to numN-1.
        Evenly spaced along the edge.
    S{i} : tuple
        Points along the bottom edge, from left to right, where i goes from 0 to numS-1.
        Evenly spaced along the edge.
    E{i} : tuple
        Points along the right edge, from top to bottom, where i goes from 0 to numE-1.
        Evenly spaced along the edge.
    W{i} : tuple
        Points along the left edge, from top to bottom, where i goes from 0 to numW-1.
        Evenly spaced along the edge.
    """

    def __init__(
        self,
        width=2.5,
        height=1.3,
        label="IQM",
        numN=1,
        numS=1,
        numE=1,
        numW=1,
        **kwargs,
    ):
        super().__init__(
            width=width,
            height=height,
            numN=numN,
            numS=numS,
            numE=numE,
            numW=numW,
            fillcol="white",
            **kwargs,
        )

        a = 0.15
        d = 0.7
        bx = 0.3
        by = 0.3
        cx = 0.3
        cy = 0.25

        def _mzm(x, y, a, cx, cy, d):
            return [
                Segment([(x, y), (x + a, y)]),
                SegmentPoly(
                    [
                        (x + a, y),
                        (x + a + cx, y + cy),
                        (x + a + cx + d, y + cy),
                        (x + a + 2 * cx + d, y),
                        (x + a + cx + d, y - cy),
                        ((x + a + cx, y - cy)),
                        (x + a, y),
                    ],
                    fill=False,
                ),
                Segment([(x + a + 2 * cx + d, y), (x + 2 * a + 2 * cx + d, y)]),
            ]

        self.segments.append(Segment([(0, 0), (a, 0)]))
        self.segments.append(Segment([(a, 0), (a + bx, by)]))
        self.segments.extend(_mzm(a + bx, by, a, cx, cy, d))
        self.segments.append(
            Segment([(3 * a + bx + 2 * cx + d, by), (3 * a + 2 * bx + 2 * cx + d, 0)])
        )
        self.segments.append(
            Segment(
                [(3 * a + 2 * bx + 2 * cx + d, 0), (4 * a + 2 * bx + 2 * cx + d, 0)]
            )
        )
        self.segments.append(Segment([(a, 0), (a + bx, -by)]))
        self.segments.extend(_mzm(a + bx, -by, a, cx, cy, d))
        self.segments.append(
            Segment([(3 * a + bx + 2 * cx + d, -by), (3 * a + 2 * bx + 2 * cx + d, 0)])
        )

        self.segments.append(
            schemdraw.SegmentText((self.width / 2, self.height / 4 - 0.06), "I")
        )

        self.segments.append(
            schemdraw.SegmentText((self.width / 2, -self.height / 4 - 0.02), "Q")
        )


class OSA(Rectangle):
    """An optical spectrum analyzer element.

    Parameters
    ----------
    numN : int, default=1
        Number of anchor points on the North (top) edge.
    numS : int, default=1
        Number of anchor points on the South (bottom) edge.
    numE : int, default=1
        Number of anchor points on the East (right) edge.
    numW : int, default=1
        Number of anchor points on the West (left) edge.
    **kwargs :
        Other Element keyword arguments.

    Anchors
    -------
    N{i} : tuple
        Points along the top edge, from left to right, where i goes from 0 to numN-1.
        Evenly spaced along the edge.
    S{i} : tuple
        Points along the bottom edge, from left to right, where i goes from 0 to numS-1.
        Evenly spaced along the edge.
    E{i} : tuple
        Points along the right edge, from top to bottom, where i goes from 0 to numE-1.
        Evenly spaced along the edge.
    W{i} : tuple
        Points along the left edge, from top to bottom, where i goes from 0 to numW-1.
        Evenly spaced along the edge.
    """

    def __init__(self, width=2.6, height=1.1, numN=1, numS=1, numE=1, numW=1, **kwargs):
        super().__init__(
            width=width,
            height=height,
            numN=numN,
            numS=numS,
            numE=numE,
            numW=numW,
            fillcol="white",
            **kwargs,
        )

        # Display inside the screen
        disp_x_offset = 0.1
        disp_y_offset = -0.45
        disp_width = 1.2
        disp_height = 0.9

        self.segments.append(
            SegmentPoly(
                [
                    (disp_x_offset, disp_y_offset + disp_height),
                    (
                        disp_x_offset + disp_width,
                        disp_y_offset + disp_height,
                    ),
                    (disp_x_offset + disp_width, disp_y_offset),
                    (disp_x_offset, disp_y_offset),
                ],
                cornerradius=0.25,
            )
        )

        import numpy as np

        p = np.load(os.path.join(os.path.dirname(__file__), "spectrum.npy"))
        path = []
        path.extend(
            (float(p[i, 0] / 500000000) + 0.7, float(p[i, 1] / 80) + 0.8)
            for i in range(p.shape[0])
        )

        noisy_path = []
        for x, y in path:
            noise_amplitude = 0.1 * disp_height
            y_noise = noise_amplitude * (random.random() - 0.5)
            noisy_path.append((x, y + y_noise))
        path = noisy_path

        self.segments.append(Segment(path))

        self.label("OSA", loc="center", ofst=(0.65, -0.04))


class ESA(Rectangle):
    """An electrical spectrum analyzer element.

    Parameters
    ----------
    numN : int, default=1
        Number of anchor points on the North (top) edge.
    numS : int, default=1
        Number of anchor points on the South (bottom) edge.
    numE : int, default=1
        Number of anchor points on the East (right) edge.
    numW : int, default=1
        Number of anchor points on the West (left) edge.
    **kwargs :
        Other Element keyword arguments.

    Anchors
    -------
    N{i} : tuple
        Points along the top edge, from left to right, where i goes from 0 to numN-1.
        Evenly spaced along the edge.
    S{i} : tuple
        Points along the bottom edge, from left to right, where i goes from 0 to numS-1.
        Evenly spaced along the edge.
    E{i} : tuple
        Points along the right edge, from top to bottom, where i goes from 0 to numE-1.
        Evenly spaced along the edge.
    W{i} : tuple
        Points along the left edge, from top to bottom, where i goes from 0 to numW-1.
        Evenly spaced along the edge.
    """

    def __init__(self, width=2.6, height=1.1, numN=1, numS=1, numE=1, numW=1, **kwargs):
        super().__init__(
            width=width,
            height=height,
            numN=numN,
            numS=numS,
            numE=numE,
            numW=numW,
            fillcol="white",
            **kwargs,
        )

        # Display inside the screen
        disp_x_offset = 0.1
        disp_y_offset = -0.45
        disp_width = 1.2
        disp_height = 0.9

        self.segments.append(
            SegmentPoly(
                [
                    (disp_x_offset, disp_y_offset + disp_height),
                    (
                        disp_x_offset + disp_width,
                        disp_y_offset + disp_height,
                    ),
                    (disp_x_offset + disp_width, disp_y_offset),
                    (disp_x_offset, disp_y_offset),
                ],
                cornerradius=0.25,
            )
        )

        import numpy as np

        p = np.load(os.path.join(os.path.dirname(__file__), "spectrum.npy"))
        path = []
        path.extend(
            (float(p[i, 0] / 500000000) + 0.7, float(p[i, 1] / 80) + 0.8)
            for i in range(p.shape[0])
        )

        noisy_path = []
        for x, y in path:
            noise_amplitude = 0.1 * disp_height
            y_noise = noise_amplitude * (random.random() - 0.5)
            noisy_path.append((x, y + y_noise))
        path = noisy_path

        self.segments.append(Segment(path))

        self.label("ESA", loc="center", ofst=(0.65, -0.04))


class AWG(Rectangle):
    """An arbitrary waveform generator element.

    Parameters
    ----------
    numN : int, default=1
        Number of anchor points on the North (top) edge.
    numS : int, default=1
        Number of anchor points on the South (bottom) edge.
    numE : int, default=1
        Number of anchor points on the East (right) edge.
    numW : int, default=1
        Number of anchor points on the West (left) edge.
    **kwargs :
        Other Element keyword arguments.

    Anchors
    -------
    N{i} : tuple
        Points along the top edge, from left to right, where i goes from 0 to numN-1.
        Evenly spaced along the edge.
    S{i} : tuple
        Points along the bottom edge, from left to right, where i goes from 0 to numS-1.
        Evenly spaced along the edge.
    E{i} : tuple
        Points along the right edge, from top to bottom, where i goes from 0 to numE-1.
        Evenly spaced along the edge.
    W{i} : tuple
        Points along the left edge, from top to bottom, where i goes from 0 to numW-1.
        Evenly spaced along the edge.
    """

    def __init__(self, width=2.6, height=1.1, numN=1, numS=1, numE=1, numW=1, **kwargs):
        super().__init__(
            width=width,
            height=height,
            numN=numN,
            numS=numS,
            numE=numE,
            numW=numW,
            fillcol="white",
            **kwargs,
        )

        # Disaplay inside the screen
        disp_x_offset = 0.1
        disp_y_offset = -0.45
        disp_width = 1.2
        disp_height = 0.9

        self.segments.append(
            SegmentPoly(
                [
                    (disp_x_offset, disp_y_offset + disp_height),
                    (
                        disp_x_offset + disp_width,
                        disp_y_offset + disp_height,
                    ),
                    (disp_x_offset + disp_width, disp_y_offset),
                    (disp_x_offset, disp_y_offset),
                ],
                cornerradius=0.25,
            )
        )

        # Waveform on the screen
        def _make_sum_of_sines(
            length: int = 500,
        ) -> Sequence[Tuple[float, float]]:
            path = []
            for x in range(length):
                y = (
                    0.2 * disp_height * math.sin(5 * math.pi * x / length)
                    + 0.2 * disp_height * math.sin(10 * math.pi * x / length)
                    + 0.4 * disp_height * math.sin(15 * math.pi * x / length)
                )
                path.append((x / length * 0.8 * disp_width, 0.45 * y))
            return path

        path = _make_sum_of_sines()
        path = [
            (
                x + disp_x_offset + 0.1 * disp_width,
                y + disp_y_offset + disp_height / 2.1,
            )
            for x, y in path
        ]
        self.segments.append(SegmentPoly(path, fill=True))

        self.label("AWG", loc="center", ofst=(0.65, -0.04))


class Scope(Rectangle):
    """An oscilloscope element.

    Parameters
    ----------
    numN : int, default=1
        Number of anchor points on the North (top) edge.
    numS : int, default=1
        Number of anchor points on the South (bottom) edge.
    numE : int, default=1
        Number of anchor points on the East (right) edge.
    numW : int, default=1
        Number of anchor points on the West (left) edge.
    **kwargs :
        Other Element keyword arguments.

    Anchors
    -------
    N{i} : tuple
        Points along the top edge, from left to right, where i goes from 0 to numN-1.
        Evenly spaced along the edge.
    S{i} : tuple
        Points along the bottom edge, from left to right, where i goes from 0 to numS-1.
        Evenly spaced along the edge.
    E{i} : tuple
        Points along the right edge, from top to bottom, where i goes from 0 to numE-1.
        Evenly spaced along the edge.
    W{i} : tuple
        Points along the left edge, from top to bottom, where i goes from 0 to numW-1.
        Evenly spaced along the edge.
    """

    def __init__(self, width=2.6, height=1.1, numN=1, numS=1, numE=1, numW=1, **kwargs):
        super().__init__(
            width=width,
            height=height,
            numN=numN,
            numS=numS,
            numE=numE,
            numW=numW,
            **kwargs,
        )

        # Disaplay inside the screen
        disp_x_offset = 0.1
        disp_y_offset = -0.45
        disp_width = 1.2
        disp_height = 0.9

        self.segments.append(
            SegmentPoly(
                [
                    (disp_x_offset, disp_y_offset + disp_height),
                    (
                        disp_x_offset + disp_width,
                        disp_y_offset + disp_height,
                    ),
                    (disp_x_offset + disp_width, disp_y_offset),
                    (disp_x_offset, disp_y_offset),
                ],
                cornerradius=0.25,
            )
        )

        # Waveform on the screen
        def _make_noisy_sine(
            length: int = 120,
        ) -> Sequence[Tuple[float, float]]:
            path = []
            for x in range(length):
                y = 0.5 * disp_height * math.sin(
                    7 * math.pi * x / length
                ) + 0.3 * disp_height * (random.random() - 0.5)
                path.append((x / length * 0.8 * disp_width, 0.6 * y))
            return path

        path = _make_noisy_sine()
        path = [
            (x + disp_x_offset + 0.1 * disp_width, y + disp_y_offset + disp_height / 2)
            for x, y in path
        ]
        self.segments.append(Segment(path))

        self.label("DSO", loc="center", ofst=(0.65, -0.04))


class OPM(Rectangle):
    """An optical power meter element.

    Parameters
    ----------
    width : float, default=1.5
        Width of the OPM.
    height : float, default=1
        Height of the OPM.
    numN : int, default=1
        Number of anchor points on the North (top) edge.
    numS : int, default=1
        Number of anchor points on the South (bottom) edge.
    numE : int, default=1
        Number of anchor points on the East (right) edge.
    numW : int, default=1
        Number of anchor points on the West (left) edge.
    **kwargs :
        Other Element keyword arguments.

    Anchors
    -------
    N{i} : tuple
        Points along the top edge, from left to right, where i goes from 0 to numN-1.
        Evenly spaced along the edge.
    S{i} : tuple
        Points along the bottom edge, from left to right, where i goes from 0 to numS-1.
        Evenly spaced along the edge.
    E{i} : tuple
        Points along the right edge, from top to bottom, where i goes from 0 to numE-1.
        Evenly spaced along the edge.
    W{i} : tuple
        Points along the left edge, from top to bottom, where i goes from 0 to numW-1.
        Evenly spaced along the edge.
    """

    def __init__(
        self,
        width=1,
        height=1,
        numN=1,
        numS=1,
        numE=1,
        numW=1,
        fillcol="white",
        **kwargs,
    ):
        super().__init__(
            width=width,
            height=height,
            numN=numN,
            numS=numS,
            numE=numE,
            numW=numW,
            fillcol=fillcol,
            **kwargs,
        )

        # Arc
        self.segments.append(
            SegmentArc(
                (self.width / 2, -0.1),
                0.95,
                1,
                theta1=30,
                theta2=150,
                fill=False,
            )
        )

        # Arrow
        self.segments.append(
            Segment(
                [(self.width / 2, 0), (0.7, 0.325)],
                arrow="->",
                arrowlength=0.2,
                arrowwidth=0.15,
            )
        )

        self.label("OPM", loc="center", ofst=(0, -0.275))

        # # Fill circle at the beginning of the arrow
        # self.segments.append(
        #     SegmentCircle((self.width / 2, -self.height / 5), 0.05, fill=True)
        # )


class PD(Rectangle):
    """A photodetector element.

    Parameters
    ----------
    width : float, default=1
        Width of the photodetector.
    height : float, default=1
        Height of the photodetector.
    numN : int, default=1
        Number of anchor points on the North (top) edge.
    numS : int, default=1
        Number of anchor points on the South (bottom) edge.
    numE : int, default=1
        Number of anchor points on the East (right) edge.
    numW : int, default=1
        Number of anchor points on the West (left) edge.
    **kwargs :
        Other Element keyword arguments.

    Anchors
    -------
    N{i} : tuple
        Points along the top edge, from left to right, where i goes from 0 to numN-1.
        Evenly spaced along the edge.
    S{i} : tuple
        Points along the bottom edge, from left to right, where i goes from 0 to numS-1.
        Evenly spaced along the edge.
    E{i} : tuple
        Points along the right edge, from top to bottom, where i goes from 0 to numE-1.
        Evenly spaced along the edge.
    W{i} : tuple
        Points along the left edge, from top to bottom, where i goes from 0 to numW-1.
        Evenly spaced along the edge.
    """

    def __init__(self, width=1, height=1, numN=1, numS=1, numE=1, numW=1, **kwargs):
        super().__init__(
            width=width,
            height=height,
            numN=numN,
            numS=numS,
            numE=numE,
            numW=numW,
            **kwargs,
        )

        self.segments.append(
            Segment(
                [
                    (self.width / 2, -self.height / 2),
                    (self.width / 2, -self.height / 2 + 0.3),
                ]
            )
        )
        self.segments.append(
            SegmentPoly(
                [
                    (self.width / 4 - 0.05, -self.height / 2 + 0.3),
                    (self.width / 2, self.height / 2 - 0.35),
                    (3 * self.width / 4 + 0.05, -self.height / 2 + 0.3),
                ],
                fill=True,
            )
        )
        self.segments.append(
            Segment(
                [
                    (self.width / 4 - 0.05, self.height / 2 - 0.35),
                    (3 * self.width / 4 + 0.05, self.height / 2 - 0.35),
                ]
            )
        )
        self.segments.append(
            Segment(
                [
                    (self.width / 2, self.height / 2 - 0.35),
                    (self.width / 2, self.height / 2),
                ]
            )
        )


class LD(Rectangle):
    """A laser diode/device element.

    Parameters
    ----------
    width : float, default=1
        Width of the photodetector.
    height : float, default=1
        Height of the photodetector.
    numN : int, default=1
        Number of anchor points on the North (top) edge.
    numS : int, default=1
        Number of anchor points on the South (bottom) edge.
    numE : int, default=1
        Number of anchor points on the East (right) edge.
    numW : int, default=1
        Number of anchor points on the West (left) edge.
    **kwargs :
        Other Element keyword arguments.

    Anchors
    -------
    N{i} : tuple
        Points along the top edge, from left to right, where i goes from 0 to numN-1.
        Evenly spaced along the edge.
    S{i} : tuple
        Points along the bottom edge, from left to right, where i goes from 0 to numS-1.
        Evenly spaced along the edge.
    E{i} : tuple
        Points along the right edge, from top to bottom, where i goes from 0 to numE-1.
        Evenly spaced along the edge.
    W{i} : tuple
        Points along the left edge, from top to bottom, where i goes from 0 to numW-1.
        Evenly spaced along the edge.
    """

    def __init__(self, width=1.5, height=1.4, numN=1, numS=1, numE=1, numW=1, **kwargs):
        super().__init__(
            width=width,
            height=height,
            numN=numN,
            numS=numS,
            numE=numE,
            numW=numW,
            fillcol="white",
            **kwargs,
        )

        def _rotate(points, angle_degrees, center=(0, 0), shiftx=0):
            angle_radians = math.radians(angle_degrees)
            cos_a = math.cos(angle_radians)
            sin_a = math.sin(angle_radians)
            cx, cy = center

            rotated_points = []
            for x, y in points:
                # Translate to origin
                x_translated = x - cx
                y_translated = y - cy

                # Rotate
                x_new = x_translated * cos_a - y_translated * sin_a
                y_new = x_translated * sin_a + y_translated * cos_a

                # Translate back
                x_final = x_new + cx
                y_final = y_new + cy

                rotated_points.append((x_final + shiftx, y_final))

            return rotated_points

        ww = 1
        xshift = 0.25
        ypos = 0.15

        horiz1 = [(0.1, ypos), (ww - 0.1, ypos)]
        horiz2 = [(0.2, ypos), (ww - 0.2, ypos)]

        for i in range(4):
            _horiz1 = _rotate(horiz1, 45 * i, center=(ww / 2, ypos), shiftx=xshift)
            self.segments.append(Segment(_horiz1))
            _horiz2 = _rotate(
                horiz2, (45 / 2) + 45 * i, center=(ww / 2, ypos), shiftx=xshift
            )
            self.segments.append(Segment(_horiz2))

        self.label("Laser", loc="center", ofst=(0, -0.5))

        # self.segments.append(
        #     Segment(
        #         [
        #             (self.width / 2, -self.height / 2 + 0.1),
        #             (self.width / 2, -self.height / 2 + 0.25),
        #         ]
        #     )
        # )
        # self.segments.append(
        #     SegmentPoly(
        #         [
        #             (self.width / 4, -self.height / 2 + 0.25),
        #             (self.width / 2, self.height / 2 - 0.45),
        #             (3 * self.width / 4, -self.height / 2 + 0.25),
        #         ],
        #         fill=True,
        #     )
        # )
        # self.segments.append(
        #     Segment(
        #         [
        #             (self.width / 4, self.height / 2 - 0.45),
        #             (3 * self.width / 4, self.height / 2 - 0.45),
        #         ]
        #     )
        # )
        # self.segments.append(
        #     Segment(
        #         [
        #             (self.width / 2, self.height / 2 - 0.45),
        #             (self.width / 2, self.height / 2 - 0.25),
        #         ]
        #     )
        # )

        # x_ofst = 0.62
        # y_ofst = 0.22

        # self.segments.append(
        #     Segment(
        #         [
        #             (0.0 + x_ofst, 0.0 + y_ofst),
        #             (self.height / 6 + x_ofst, self.height / 6 + y_ofst),
        #         ],
        #         arrow="->",
        #         arrowlength=0.15,
        #         arrowwidth=0.09,
        #         lw=1.15,
        #     )
        # )

        # x_ofst = 0.7
        # y_ofst = 0.15

        # self.segments.append(
        #     Segment(
        #         [
        #             (0.0 + x_ofst, 0.0 + y_ofst),
        #             (self.height / 6 + x_ofst, self.height / 6 + y_ofst),
        #         ],
        #         arrow="->",
        #         arrowlength=0.15,
        #         arrowwidth=0.09,
        #         lw=1.15,
        #     )
        # )
