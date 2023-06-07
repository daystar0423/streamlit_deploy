# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 19:24:05 2023

@author: kjc
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 19:36:36 2023

@author: kjc
"""
import streamlit as st
import pandas as pd
from pyarrow import csv
from bokeh.plotting import figure, Column
from bokeh.layouts import layout
from bokeh.models import (
    LinearAxis, Range1d, ColumnDataSource, TableColumn, DataTable, PointDrawTool, PanTool, ResetTool, SaveTool,
    WheelZoomTool, BoxZoomTool, UndoTool, CrosshairTool, Span, HoverTool, CustomJS, RangeSlider
    )






















def upload_large_csv(data, skip_rows, delimiter):
    read_options = csv.ReadOptions(skip_rows = skip_rows, autogenerate_column_names = True)
    parse_options = csv.ParseOptions(delimiter=delimiter)
    dataframe = csv.read_csv(data, read_options = read_options, parse_options = parse_options).to_pandas()
    return dataframe















 



def plot_bokeh(title):
    TOOLTIPS = [("x", "@x"), ("y", "@y")]
    p = figure(title=title, tools=[], tooltips = TOOLTIPS)
    p.add_tools(PanTool())
    p.add_tools(ResetTool())
    p.add_tools(SaveTool())
    p.add_tools(WheelZoomTool())
    p.add_tools(WheelZoomTool(dimensions='width'))
    p.add_tools(WheelZoomTool(dimensions='height'))
    p.add_tools(BoxZoomTool())
    p.add_tools(BoxZoomTool(dimensions='width'))
    p.add_tools(BoxZoomTool(dimensions='height'))
    p.add_tools(UndoTool())
    p.add_tools(CrosshairTool())
    p.legend.location = "top_right"
    p.yaxis.visible = False
    return p


def show_bokeh(p):
    p.legend.click_policy="hide"
    st.bokeh_chart(p, use_container_width=True)


def show_bokeh_with_dot(p, x_list, y_list):
    p.legend.click_policy="hide"
   
    point = ColumnDataSource(data=dict(x=x_list,y=y_list))
    columns = [TableColumn(field="x", title="x")]
    table = DataTable(source=point, columns=columns, editable=True, height=50)
    r = p.scatter(x='x', y='y', source=point, color='red', size=8)
    p.add_tools(PointDrawTool(renderers=[r]))
   
    range_slider = RangeSlider(
        title="x range ",
        start=p.x_range.start,
        end=p.x_range.end,
        step=0.01,
        value=(p.x_range.start, p.x_range.end),
        orientation = 'horizontal',
        sizing_mode = "stretch_width",
    )
    range_slider.js_link("value", p.x_range, "start", attr_selector=0)
    range_slider.js_link("value", p.x_range, "end", attr_selector=1)
    layout1 = layout([range_slider], [p])
    st.bokeh_chart(Column(layout1, table), use_container_width=True)


def base_xaxis(p, x1, x2, label, color):
    p.x_range = Range1d(x1, x2)
    p.xaxis.axis_label = label
    p.xaxis.axis_label_text_color = color
    return


def base_yaxis(p, y1, y2, label, color):
    p.y_range = Range1d(y1, y2)
    p.yaxis.axis_label = label
    p.yaxis.axis_label_text_color = color
    return


def add_line_chart(p, x, y, y1, y2, legend_label, width, alpha, color, axis_label, axis_direction, axis_visible):
    p.extra_y_ranges[legend_label] = Range1d(y1, y2)
    ax1 = LinearAxis(y_range_name = legend_label, axis_label = axis_label, axis_label_text_color = color)
    p.line(x, y, y_range_name = legend_label, line_width = width, alpha=alpha, legend_label=legend_label, color=color)
    if axis_visible == True:
        p.add_layout(ax1, axis_direction)
