from enum import Enum
from math import sqrt
import wx
import collections


class StateType(Enum):
    Normal = 0
    Start = 1
    End = 2

    def __str__(self):
        return str(self.value)


class State:

    def __init__(self, position, state_name, radius=50, selected=False, up=True):
        self.position = position
        self.type = StateType.Normal
        self.radius = radius
        self.arcs = collections.OrderedDict()
        self.selected = selected
        self.state_name = state_name
        self.up = up
        self.current = False
        self.bad_input = False
        self.ok_input = False

    def __str__(self):
        return self.state_name

    def set_type(self, state_type):
        self.type = state_type

    def add_arc(self, arc, value):
        self.arcs[arc] = value
        
    def remove_arc(self, arc):
        if arc in self.arcs:
            self.arcs.remove(arc)

    def draw(self, dc):
        brush = wx.Brush('White', wx.SOLID)
        if self.selected:
            brush = wx.Brush('Yellow', wx.SOLID)
        if self.current:
            brush = wx.Brush('Grey', wx.SOLID)
        if self.bad_input:
            brush = wx.Brush('Red', wx.SOLID)
        if self.ok_input:
            brush = wx.Brush('Green', wx.SOLID)
        dc.SetBrush(brush)
        if self.type == StateType.Normal:
            dc.DrawCircle(self.position[0], self.position[1], self.radius)
        elif self.type == StateType.End:
            dc.DrawCircle(self.position[0], self.position[1], self.radius)
            dc.DrawCircle(self.position[0], self.position[1], self.radius - 5)
        else:
            dc.DrawCircle(self.position[0], self.position[1], self.radius)
            dc.DrawLine(self.position[0]-self.radius, self.position[1],
                        self.position[0]-2*self.radius, self.position[1]-self.radius)
            dc.DrawLine(self.position[0]-2*self.radius, self.position[1]-self.radius,
                        self.position[0]-2*self.radius, self.position[1]+self.radius)
            dc.DrawLine(self.position[0]-2*self.radius, self.position[1]+self.radius,
                        self.position[0]-self.radius, self.position[1])

        for arc in self.arcs:
            if arc.contains_arc(self):
                if arc == self:
                    dc.DrawText(self.state_name+'->'+arc.state_name+":"+self.arcs[arc], (self.position[0])-20, (self.position[1]- 100))
                    dc.DrawLine(self.position[0], self.position[1], arc.position[0], arc.position[1]-85)
                    continue
                else:
                    if arc.up:
                        self.up = False
                    if self.up:
                        dc.DrawText(self.state_name+'->'+arc.state_name+":"+self.arcs[arc], (self.position[0]+arc.position[0])/2,
                                (self.position[1]+arc.position[1])/2 + 10)
                    else:
                        dc.DrawText(self.state_name+'->'+arc.state_name+":"+self.arcs[arc], (self.position[0]+arc.position[0])/2,
                                (self.position[1]+arc.position[1])/2 - 10)
            else:
                dc.DrawText(self.state_name+'->'+arc.state_name+":"+self.arcs[arc], (self.position[0]+arc.position[0])/2,
                            (self.position[1]+arc.position[1])/2 + 10)
            dc.DrawLine(self.position[0], self.position[1], arc.position[0], arc.position[1])

        dc.DrawText(self.state_name, self.position[0], self.position[1])

    def set_selected(self, selected):
        self.selected = selected

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def is_within(self, pos):
        distance = sqrt(((pos[0] - self.position[0]) ** 2) +
                        ((pos[1] - self.position[1]) ** 2))
        return distance < self.radius

    def contains_arc(self, arc):
        return arc in self.arcs

    def set_name(self, name):
        self.state_name = name

    def set_arcValue(self, arc, value):
        self.arcs[arc] = value

    def add_new_arc_value(self, arc, value):
        self.arcs[arc] = self.arcs[arc] + ", " + value
