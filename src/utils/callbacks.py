class ContourCallback(object):
    def __init__(self, actor, renWin, contour_filter):
        self.renWin = renWin
        self.actor = actor
        self.contour_filter = contour_filter

    def __call__(self, caller, ev):
        value = caller.GetSliderRepresentation().GetValue()
        self.contour_filter.SetValue(0, value)
        self.renWin.Render()


class OpacityCallback(object):
    def __init__(self, actor, renWin, point, piecewise):
        self.renWin = renWin
        self.actor = actor
        self.point = point
        self.piecewise = piecewise

    def __call__(self, caller, ev):
        value = caller.GetSliderRepresentation().GetValue()
        self.piecewise.RemoveAllPoints()
        self.piecewise.AddPoint(0, 0)
        self.piecewise.AddPoint(self.point, value)
        self.piecewise.AddPoint(self.point + 1, value)
        self.piecewise.AddPoint(255, 0)
        self.renWin.Render()
