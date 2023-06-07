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
import win32com.client
import io
import os
import pythoncom
#import numpy as np
import pandas as pd
from openpyxl import load_workbook
from openpyxl.drawing.image import Image as xlimg
from PIL import Image
#from scipy.signal import savgol_filter
from pyarrow import csv
from bokeh.plotting import figure, Column
from bokeh.layouts import layout
from bokeh.io.export import get_screenshot_as_png
#from bokeh.io import export_png
from bokeh.models import (
    LinearAxis, Range1d, ColumnDataSource, TableColumn, DataTable, PointDrawTool, PanTool, ResetTool, SaveTool,
    WheelZoomTool, BoxZoomTool, UndoTool, CrosshairTool, Span, HoverTool, CustomJS, RangeSlider
    )


def save_setting(ratio, xlen, ylen, gap, cx, cy):
    columns = ['setting']
    index = ['ratio', 'xlen', 'ylen', 'gap', 'cx', 'cy']
    data = [[ratio], [xlen/ratio], [ylen/ratio], [gap/ratio], [cx/ratio], [cy/ratio]]
    setdata = pd.DataFrame(data, columns = columns, index = index)
    save_setting = convert_df(setdata)
    st.download_button(label="Download setting file as csv", data=save_setting, file_name='setting.csv', mime='text/csv')

@st.cache_data  
def cutimg(cx, cy, xlen, ylen, gap, img):
    cut_img1 = img.crop((cx,cy,cx+xlen,cy+ylen))
    cut_img2 = img.crop((cx,cy+gap,cx+xlen,cy+ylen+gap))
    cut_img3 = img.crop((cx,cy+gap*2,cx+xlen,cy+ylen+gap*2))
    return cut_img1, cut_img2, cut_img3


def showcutimg(cut_img1, cut_img2, cut_img3):
    st.image(cut_img1, caption='frame')
    st.image(cut_img2, caption='fixed')
    st.image(cut_img3, caption='moving')


def stroke_calculate(df_stroke, sensor):
    if sensor == 0: m, f = 0, 0
    elif sensor >= df_stroke['sensor'].values.tolist()[-1]:
        s = df_stroke.index[df_stroke['sensor'] <= sensor].tolist()[-1]
        m = sensor/df_stroke['sensor'][s]*df_stroke['moving'][s]
        f = sensor/df_stroke['sensor'][s]*df_stroke['fixed'][s]
    else:
        s = df_stroke.index[df_stroke['sensor'] >= sensor].tolist()[0]
        m = sensor/df_stroke['sensor'][s]*df_stroke['moving'][s]
        f = sensor/df_stroke['sensor'][s]*df_stroke['fixed'][s]
    return m, f


def bokeh_to_excel(p, sheet, cell):
    img = get_screenshot_as_png(p, width=600, height=300)
    buf = io.BytesIO()
    img.save(buf, format='png')
    img = Image.open(buf).crop((0,0,570,300))
    img.save(buf, format='png')
    img = Image.open(buf)
    img = xlimg(img)
    sheet.add_image(img, cell)
    return


def img_to_excel(img, sheet, cell):
    img = img.resize((570, int(570 / img.width * img.height)))
    buf = io.BytesIO()
    img.save(buf, format='png')
    img = Image.open(buf)
    img = xlimg(img)
    sheet.add_image(img, cell)


@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')


@st.cache_data
def upload_large_csv(data, skip_rows, delimiter):
    read_options = csv.ReadOptions(skip_rows = skip_rows, autogenerate_column_names = True)
    parse_options = csv.ParseOptions(delimiter=delimiter)
    dataframe = csv.read_csv(data, read_options = read_options, parse_options = parse_options).to_pandas()
    return dataframe


@st.cache_data  
def transparent(_image):
    img = _image.convert("RGBA")
    datas = img.getdata()
     
    newData = []
    cutOff = 150
     
    for item in datas:
        if item[0] >= cutOff and item[1] >= cutOff and item[2] >= cutOff:
            newData.append((255, 255, 255, 0))
            # RGB의 각 요소가 모두 cutOff 이상이면 transparent하게 바꿔줍니다.
        else:
            newData.append(item)
            # 나머지 요소는 변경하지 않습니다.
     
    img.putdata(newData)
    return img


@st.cache_data  
def mergeimg(image11, image21, image31, movint, fixint):
    image11.paste(image21, (fixint*-1,0), image21)
    image11.paste(image31, (movint,0), image31)
    return image11


@st.cache_data
def movimg(df_stroke, sensor, ratio, frame, fixed, moving):
    if sensor == 0:
        m, f = 0, 0
    elif sensor >= df_stroke['sensor'].values.tolist()[-1]:
        s = df_stroke.index[df_stroke['sensor'] <= sensor].tolist()[-1]
        m = sensor/df_stroke['sensor'][s]*df_stroke['moving'][s]
        f = sensor/df_stroke['sensor'][s]*df_stroke['fixed'][s]
    else:
        s = df_stroke.index[df_stroke['sensor'] >= sensor].tolist()[0]
        m = sensor/df_stroke['sensor'][s]*df_stroke['moving'][s]
        f = sensor/df_stroke['sensor'][s]*df_stroke['fixed'][s]
   
    movint = int(m*ratio)
    fixint = int(f*ratio)

    #st.image(mergeimg(frame, fixed, moving, movint, fixint))
    return_img = mergeimg(frame, fixed, moving, movint, fixint)
    return return_img


def find_extention(file):
    extention = format(file).split('.')[1].split("'")[0].lower()
    return extention


def pdf_down(buf):
    dir1 = 'C:/Users/kjc/.spyder-py3/pages/excel_temp2.xlsx'
    dir2 = 'C:/Users/kjc/.spyder-py3/pages/excel_temp2.pdf'
    wb = load_workbook(buf)
    wb.save(dir1)
    excel = win32com.client.Dispatch("Excel.Application", pythoncom.CoInitialize())
    excel.Visible = False
    wb = excel.Workbooks.Open(dir1)
    wb.Worksheets("sheet1").Select()
    wb.ActiveSheet.ExportAsFixedFormat(0, dir2)
    wb.Close(False)
    with open(dir2, 'rb') as f:
        st.download_button('download', data = f, file_name="report.pdf")
    os.remove(dir1)
    os.remove(dir2)
    return

 
def excel_down(buf):
    st.download_button('download excel', data = buf, file_name="report.xlsx")


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