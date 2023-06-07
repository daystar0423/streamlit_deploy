# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 19:22:48 2023

@author: kjc
"""

import my
import streamlit as st
import numpy as np
from scipy.signal import savgol_filter
import importlib
importlib.reload(my)


""" auto_chart v1.0
def auto_chart(file, show): # v1.0
    extention = my.find_extention(file)
    if extention == 'csv':
        df0 = my.upload_large_csv(file, 8, ',')
    else:
        df0 = my.upload_large_csv(file, 8, '\t')

    def idx_for_ms(ms):
        array = df0['f0'].to_numpy()
        didx_dt = (len(array) - 1) / (array[-1] - array[0])
        idx = int(didx_dt * ms / 1000)
        return idx
       
    for i in range(len(df0.columns)):
       
        array = df0.iloc[:,i].to_numpy()
        try:
            array = savgol_filter(array, 75, 8)
        except:
            continue
       
        if i == 0:
            time0 = array * 1000
            st.write('ch'+str(i),': time')
            continue
           
        _min = min(array)
        _max = max(array)
        abs_max = max(abs(array))
        _med = (_min + _max) / 2
           
        if np.mean(array[:100]) < _max * 0.2: # current, coil, trv / NO : stroke, main
            if abs(np.mean(array[-100:])) > abs_max * 0.1:
                dfv = array - np.mean(array[:100])
                trv1 = savgol_filter(dfv, 100, 8)
                st.write('ch'+str(i),': dfv')
            elif _max * 0.2 < abs(_min):
                if max(abs(array[idx_for_ms(1):] - array[:-idx_for_ms(1)])) > abs(max(array)):
                    dfe = array - np.mean(array[:100])
                    st.write('ch'+str(i),': didt')
                else:
                    dfi = array - np.mean(array[:100])
                    ibr1 = savgol_filter(dfi, 100, 8)
                    st.write('ch'+str(i),': current')
            else:
                dfc = array - np.mean(array[:100])
                sol1 = savgol_filter(dfc, 100, 8)
                st.write('ch'+str(i),': coil')
        elif (np.where(array < (_max - (_max - _min)*0.8))[0][0] - np.where(array < (_max - (_max - _min)*0.2))[0][0]) < idx_for_ms(3):
            dfm = array - np.mean(array[:100])
            mc1 = savgol_filter(dfm, 100, 8)
            st.write('ch'+str(i),': mian contact')
        else:
            dfs = array - np.mean(array[:100])
            str1 = savgol_filter(dfs, 300, 1)
            st.write('ch'+str(i),': stroke')
           
    x1 = time0
    if 'ibr1' in vars(): y1 = ibr1
    if 'str1' in vars(): y2 = str1
    if 'sol1' in vars(): y3 = sol1
    if 'mc1'  in vars(): y4 = mc1
   
    end_idx = len(x1)
    if 'dfe' in vars():
        e_list0 = dfe.tolist()
        t_list0 = time0.tolist()
        time1 = []
        ibro = []
        ibr = []
       
        for i in range(end_idx):
            if i == 0:
                ibro.append(e_list0[i])
            else:
                ibro.append(ibro[i-1] + e_list0[i])
            if i % 100 == 0:
                time1.append(t_list0[i])
                ibr.append(ibro[i])
        x2 = time1
        y6 = ibr
   
   
    #if 'trv1' in vars(): y5 = trv1
    if 'dfv' in vars():
        ncz = np.where( dfv>= abs(10))[0][0]
        pst = ncz / end_idx
        v_list0 = dfv
        t_list0 = time0
        time2 = []
        trv = []
        for i in range(end_idx):
            if end_idx * (pst - 0.05) <= i <= end_idx * (pst + 0.05):
                if i % 2 == 0:
                    time2.append(t_list0[i])
                    trv.append(v_list0[i])
            elif i % 1000 == 0:
                time2.append(t_list0[i])
                trv.append(v_list0[i])
        x3 = time2
        y5 = trv
   
    test1 = 1
    test2 = 2
    test3 = 3
   
    return_list = {'test1' : test1, 'test2' : test2, 'test3' : test3}
   
    p = my.plot_bokeh('osc')
    my.base_xaxis(p, min(x1), max(x1), 'time [ms]', 'black')
   
    if 'y1' in vars():
        my.base_yaxis(p, min(y1)*1.2, max(y1)*1.2, '', 'black')
        my.add_line_chart(p, x1, y1, min(y1)*1.2, max(y1)*1.2, 'current', 0.5, 1, 'red', 'A', 'left', False)
    if 'y2' in vars():
        my.add_line_chart(p, x1, y2, min(y2)*1.2, abs(min(y2))*0.2, 'stroke', 0.5, 1, 'green', 'V', 'left', False)
    if 'y3' in vars():
        my.add_line_chart(p, x1, y3, max(y3)*-0.1, max(y3)*10, 'coil', 0.5, 1, 'blue', 'V', 'left', False)
    if 'y4' in vars():
        my.add_line_chart(p, x1, y4, min(y4)*10, abs(min(y4))*1, 'main', 0.5, 1, 'purple', 'V', 'left', False)
    if 'y5' in vars():
        my.add_line_chart(p, x3, y5, min(y5)*1.2, max(y5)*1.2, 'trv', 2, 1, 'pink', 'V', 'left', False)
    if 'y6' in vars():
        my.base_yaxis(p, min(y6)*1.2, max(y6)*1.2, '', 'black')
        my.add_line_chart(p, x2, y6, min(y6)*1.2, max(y6)*1.2, 'current', 0.5, 1, 'red', 'A', 'left', False)
   
   
    if show == True:
        if 'y1' in vars():
            my.show_bokeh_with_dot(p, [x1[1000]], [y1[1000]])
        else:
            my.show_bokeh_with_dot(p, [], [])
    return p
"""


""" auto_chart v1.1
def auto_chart(file, show, full_stroke, ct_sep_per): # v1.1
    extention = my.find_extention(file)
    if extention == 'csv':
        df0 = my.upload_large_csv(file, 8, ',')
    else:
        df0 = my.upload_large_csv(file, 8, '\t')

    def idx_for_ms(ms):
        array = df0['f0'].to_numpy()
        didx_dt = (len(array) - 1) / (array[-1] - array[0])
        idx = int(didx_dt * ms / 1000)
        return idx
    
    eff_col_num = 1
    for i in range(len(df0.columns)):
        
        array = df0.iloc[:,i].to_numpy()
        
        try: array = savgol_filter(array, 75, 8)
        except: continue

        if i == 0:
            time0 = array * 1000
            continue
        
        eff_col_num += 1
        
        _min = min(array)
        _max = max(array)
        abs_max = max(abs(array))
           
        if np.mean(array[:100]) < _max * 0.2: # current, coil, trv / NO : stroke, main
            if abs(np.mean(array[-100:])) > abs_max * 0.1:
                vars() ['ch' + str(i)] = 3 #'trv'
                vars() ['trv'] = df0['f'+str(i)]
                #dfv = array - np.mean(array[:100])
                #trv1 = savgol_filter(dfv, 100, 8)
                #st.write('ch'+str(i),': dfv')
            elif _max * 0.2 < abs(_min):
                if max(abs(array[idx_for_ms(1):] - array[:-idx_for_ms(1)])) > abs(max(array)):
                    vars() ['ch' + str(i)] = 4 #'Rogowski'
                    vars() ['Rogowski'] = df0['f'+str(i)]
                    #dfe = array - np.mean(array[:100])
                    #st.write('ch'+str(i),': didt')
                else:
                    vars() ['ch' + str(i)] = 0
                    vars() ['current'] = df0['f'+str(i)]
            else:
                dfc = array - np.mean(array[:100])
                vars() ['ch' + str(i)] = 2 #'coil'
                vars() ['coil'] = df0['f'+str(i)]
        elif (np.where(array < (_max - (_max - _min)*0.8))[0][0] - np.where(array < (_max - (_max - _min)*0.2))[0][0]) < idx_for_ms(3):
            vars() ['ch' + str(i)] = 5 #'main contact'
            vars() ['main_contact'] = df0['f'+str(i)]
        else:
            vars() ['ch' + str(i)] = 1 #'stroke'
            vars() ['stroke'] = df0['f'+str(i)]
    
    for i in range(1, eff_col_num):
        vars()['ckch'+str(i)] = st.radio('ch' + str(i) + ' :', ('current', 'stroke', 'coil', 'trv', 'Rogowski', 'main', 'none'),
             horizontal=True, index = vars()['ch' + str(i)])
        
    for i in range(1, eff_col_num):
        match vars()['ckch'+str(i)]:
            case 'current': dfi = df0['f' + str(i)]
            case 'stroke': dfs = df0['f' + str(i)]
            case 'coil': dfc = df0['f' + str(i)]
            case 'trv': dfv = df0['f' + str(i)]
            case 'Rogowski': dfe = df0['f' + str(i)]
            case 'main': dfm = df0['f' + str(i)]

             
    end_idx = len(time0) 
    
    if 'dfs' in vars():
        dfs = dfs - np.mean(dfs[:100]) 
        str1 = savgol_filter(dfs, 300, 1) 
        v_end_str = np.mean(str1[-100:])
        y2 = str1   
      
    x1 = time0
    if 'dfi' in vars():
        dfi = dfi - np.mean(dfi[:100])
        ibr1 = savgol_filter(dfi, 100, 8)
        y1 = ibr1
        
        maxibr = max(abs(ibr1))
        idx_bfcz = end_idx - np.where(abs(ibr1[::-1]) >= maxibr*0.35)[0][0]
        idx_precz = np.where(abs(ibr1[idx_bfcz:]) <= maxibr*0.0125)[0][0] + idx_bfcz
        dididx = abs((ibr1[idx_precz] - ibr1[idx_precz - 5]))/5
        idx_cz = idx_precz + int(maxibr*0.0125 / dididx)
        v_ct_sep = abs(v_end_str * ct_sep_per / 100)
        idx_sep = np.where(abs(str1) > v_ct_sep)[0][0]

    if 'dfc' in vars():
        dfc = dfc - np.mean(dfc[:100]) 
        sol1 = savgol_filter(dfc, 100, 8)
        idx_sol_start = np.where(abs(sol1) >= max(abs(sol1))*0.15)[0][0]
        y3 = sol1
        
    if 'dfm'  in vars():
        dfm = dfm - np.mean(dfm[-100:])
        mc1 = savgol_filter(dfm, 100, 8)
        y4 = mc1
        
        maxmct = max(abs(mc1))
        idx_bfsep = end_idx - np.where(abs(mc1[::-1]) >= maxmct*0.5)[0][0]
        st.write(idx_bfsep)
        st.write(end_idx)
        topen = x1[idx_bfsep] - x1[idx_sol_start]
        v_end_str = np.mean(str1[-100:])
        ratio_ctsep = abs(str1[idx_bfsep] / v_end_str)
        idx_str40 = np.where(abs(str1) >= abs(v_end_str)*0.40)[0][0]
        idx_str75 = np.where(abs(str1) >= abs(v_end_str)*0.75)[0][0]
        drdt = abs(round(   (str1[idx_str75] - str1[idx_str40]) / (x1[idx_str75] - x1[idx_str40]) / v_end_str, 2))
        
        if min(str1) < v_end_str * 1.005: v_undershoot = abs((min(str1) - v_end_str) / v_end_str)
        else: v_undershoot = 0
        try:
            idx_start_rebound = idx_bfsep + np.where((str1[idx_bfsep + 10 : ] - str1[idx_bfsep : -10]) > 0)[0][0]
            v_rebound_max = max(str1[idx_start_rebound:])
            if v_rebound_max > v_end_str * 0.995: v_rebound = abs((v_end_str - v_rebound_max) / v_end_str)
            else: v_rebound = 0
        except: st.empty()
        
    if 'dfe' in vars():
        e_list0 = savgol_filter((dfe).tolist(), 80, 8)
        t_list0 = time0.tolist()
        time1 = [];  ibro = [];  ibr = []
        for i in range(end_idx):
            if i == 0: ibro.append(e_list0[i])
            else: ibro.append(ibro[i-1] + e_list0[i])
            if i % 100 == 0: time1.append(t_list0[i]); ibr.append(ibro[i])
        
        ibr = ((np.array(ibr) - np.mean(ibr[:100]))/10).tolist()
        maxibr = max(abs(np.array(ibr)))
        ibra = np.array(ibro) * 0.1
        trva = savgol_filter((dfv).tolist(), 10, 8)
        
        tbfcz = end_idx - np.where(abs(ibra[::-1]) >= maxibr*0.35)[0][0]
        tpre1ka = np.where(abs(ibra[tbfcz:]) <= maxibr*0.0125)[0][0] + tbfcz
        tcz = np.where(abs(trva[tpre1ka:]) <= 0.1)[0][0] + tpre1ka
        varc = max(trva[tpre1ka:tcz])
        idx_per_time = (end_idx - 1) / (t_list0[-1] - t_list0[0])
        time400us = int(0.4 * idx_per_time)
        rrrv = max(abs(trva[tcz:tcz+time400us] - trva[tcz-10:tcz+time400us-10])) * idx_per_time / 10000
        vwith = max(abs(trva[tcz:tcz+time400us]))
        time8ms = int(8 * idx_per_time)
        ibrlast = max(abs(ibra[tpre1ka - time8ms :tpre1ka])) / 1000 / 1.41421356237
        ibrbflast = max(abs(ibra[tpre1ka - time8ms * 2 :tpre1ka - - time8ms])) / 1000 / 1.41421356237
        time15us = int(0.015 * idx_per_time)
        didt = max(abs(ibra[tcz-time15us:tcz]-ibra[tcz-time15us-10:tcz-10])) * idx_per_time / 10000
        pst = tcz / end_idx
        
        x2 = time1;  y6 = ibr
        
    if 'dfv' in vars():

        v_list0 = trva;   t_list0 = time0
        time2 = [];   trv = []
        for i in range(end_idx):
            if end_idx * (pst - 0.05) <= i <= end_idx * (pst + 0.05):
                if i % 2 == 0: time2.append(t_list0[i]);   trv.append(v_list0[i])
            elif i % 1000 == 0:
                time2.append(t_list0[i]);   trv.append(v_list0[i])
        x3 = time2;   y5 = trv
   
    p = my.plot_bokeh('osc')
    my.base_xaxis(p, min(x1), max(x1), 'time [ms]', 'black')
   
    if 'y1' in vars():
        my.base_yaxis(p, min(y1)*1.2, max(y1)*1.2, '', 'black')
        my.add_line_chart(p, x1, y1, min(y1)*1.2, max(y1)*1.2, 'current', 0.5, 1, 'red', 'A', 'left', False)
    if 'y2' in vars():
        my.add_line_chart(p, x1, y2, min(y2)*1.2, abs(min(y2))*0.2, 'stroke', 0.5, 1, 'green', 'V', 'left', False)
    if 'y3' in vars():
        my.add_line_chart(p, x1, y3, max(y3)*-0.1, max(y3)*10, 'coil', 0.5, 1, 'blue', 'V', 'left', False)
    if 'y4' in vars():
        my.add_line_chart(p, x1, y4, max(y4)*-10, max(y4)*1.2, 'main', 0.5, 1, 'purple', 'V', 'left', False)
    if 'y5' in vars():
        my.add_line_chart(p, x3, y5, min(y5)*1.2, max(y5)*1.2, 'trv', 0.6, 1, 'violet', 'V', 'left', False)
    if 'y6' in vars():
        my.base_yaxis(p, min(y6)*1.2, max(y6)*1.2, '', 'black')
        my.add_line_chart(p, x2, y6, min(y6)*1.2, max(y6)*1.2, 'current', 0.5, 1, 'red', 'A', 'left', False)
   
    if show == True:
        if 'y1' in vars(): my.show_bokeh_with_dot(p, [x1[idx_cz]], [y1[idx_cz]])
        else: my.show_bokeh_with_dot(p, [], [])
    
    if 'dfe' in vars():
        st.write('di/dt : ' + str(round(didt, 2)) + ' A/us')
        st.write('du/dt : ' + str(round(rrrv, 2))+ ' kV/us')
        st.write('varc : ' + str(round(varc, 2))+ ' kV')
        st.write('vpeak : ' + str(round(vwith, 2))+ ' kV')
        st.write('ibr_bf_last : ' + str(round(ibrbflast, 2))+ ' kArms')
        st.write('ibr_last : ' + str(round(ibrlast, 2))+ ' kArms')
        st.write('ibr(avg) : ' + str(round(ibrbflast*0.5 + ibrlast*0.5, 2))+ ' kArms')
    if 'dfm'  in vars():
        st.write('open time : ' + str(round(topen, 2)) + ' ms')
        st.write('sliding : ' + str(round(ratio_ctsep * full_stroke, 2)) + ' mm [' + str(round(ratio_ctsep * 100, 2)) + ' %]')
        st.write('speed : ' + str(round(drdt * full_stroke, 2))+ ' m/s')
        st.write('undershoot : ' + str(round(v_undershoot * full_stroke, 2))+ ' mm')
        st.write('rebound : ' + str(round(v_rebound * full_stroke, 2))+ ' mm')
    if 'dfi' in vars():
        topen = x1[idx_sep] - x1[idx_sol_start]
        tarc = x1[idx_cz] - x1[idx_sep]
        tbr = x1[idx_cz] - x1[idx_sol_start]
        vr_str_cz = abs(str1[idx_cz] / v_end_str)
        
        st.write('open time : ' + str(round(topen, 2)) + ' ms')
        st.write('arcing time : ' + str(round(tarc, 2)) + ' ms')
        st.write('breaking time : ' + str(round(tbr, 2)) + ' ms')
        st.write('stroke at current zero : ' + str(round(vr_str_cz * full_stroke, 2)) + ' mm')
    return 
"""


def auto_chart(file, show, full_stroke, ct_sep_per): # v1.2
    extention = my.find_extention(file)
    if extention == 'csv':
        df0 = my.upload_large_csv(file, 8, ',')
    else:
        df0 = my.upload_large_csv(file, 8, '\t')

    def idx_for_ms(ms):
        array = df0['f0'].to_numpy()
        didx_dt = (len(array) - 1) / (array[-1] - array[0])
        idx = int(didx_dt * ms / 1000)
        return idx
   
    eff_col_num = 1
    for i in range(len(df0.columns)):
       
        array = df0.iloc[:,i].to_numpy()
       
        try: array = savgol_filter(array, 75, 8)
        except: continue

        if i == 0:
            time0 = array * 1000
            continue
       
        eff_col_num += 1
       
        _min = min(array)
        _max = max(array)
        abs_max = max(abs(array))
           
        if np.mean(array[:100]) < _max * 0.2: # current, coil, trv / NO : stroke, main
            if abs(np.mean(array[-100:])) > abs_max * 0.1:
                vars() ['ch' + str(i)] = 3 #'trv'
                vars() ['trv'] = df0['f'+str(i)]
            elif _max * 0.2 < abs(_min):
                if max(abs(array[idx_for_ms(1):] - array[:-idx_for_ms(1)])) > abs(max(array)):
                    vars() ['ch' + str(i)] = 4 #'Rogowski'
                    vars() ['Rogowski'] = df0['f'+str(i)]
                else:
                    vars() ['ch' + str(i)] = 0
                    vars() ['current'] = df0['f'+str(i)]
            else:
                vars() ['ch' + str(i)] = 2 #'coil'
                vars() ['coil'] = df0['f'+str(i)]
        elif (np.where(array < (_max - (_max - _min)*0.8))[0][0] - np.where(array < (_max - (_max - _min)*0.2))[0][0]) < idx_for_ms(3):
            vars() ['ch' + str(i)] = 5 #'main contact'
            vars() ['main_contact'] = df0['f'+str(i)]
        else:
            vars() ['ch' + str(i)] = 1 #'stroke'
            vars() ['stroke'] = df0['f'+str(i)]
    for i in range(1, eff_col_num):
        vars()['ckch'+str(i)] = st.radio('ch' + str(i) + ' :',
            ('current', 'stroke', 'coil', 'trv', 'Rogowski', 'main', 'other1', 'other2', 'none'),
             horizontal=True, index = vars()['ch' + str(i)])
    for i in range(1, eff_col_num):
        match vars()['ckch'+str(i)]:
            case 'current': dfi = df0['f' + str(i)]
            case 'stroke': dfs = df0['f' + str(i)]
            case 'coil': dfc = df0['f' + str(i)]
            case 'trv': dfv = df0['f' + str(i)]
            case 'Rogowski': dfe = df0['f' + str(i)]
            case 'main': dfm = df0['f' + str(i)]
            case 'other1': dfo1 = df0['f' + str(i)]
            case 'other2': dfo2 = df0['f' + str(i)]

    end_idx = len(time0)
    x1 = time0
    if 'dfs' in vars():
        dfs = dfs - np.mean(dfs[:100])
        str1 = savgol_filter(dfs, 300, 1)
        y2 = str1
        
        v_end_str = np.mean(str1[-100:])
        v_ct_sep = abs(v_end_str * ct_sep_per / 100)
        idx_sep = np.where(abs(str1) > v_ct_sep)[0][0]
        idx_str40 = np.where(abs(str1) >= abs(v_end_str)*0.40)[0][0]
        idx_str75 = np.where(abs(str1) >= abs(v_end_str)*0.75)[0][0]
        drdt = abs(round( (str1[idx_str75] - str1[idx_str40]) / (x1[idx_str75] - x1[idx_str40]) / v_end_str, 2) )
        if min(str1) < v_end_str * 1.005: v_undershoot = abs((min(str1) - v_end_str) / v_end_str)
        else: v_undershoot = 0
        try:
            idx_start_rebound = idx_str40 + np.where((str1[idx_str40 + 10 : ] - str1[idx_str40 : -10]) > 0)[0][0]
            v_rebound_max = max(str1[idx_start_rebound:])
            if v_rebound_max > v_end_str * 0.995: v_rebound = abs((v_end_str - v_rebound_max) / v_end_str)
            else: v_rebound = 0
        except: st.empty()
    
    if 'dfi' in vars():
        dfi = dfi - np.mean(dfi[:100])
        ibr1 = savgol_filter(dfi, 100, 8)
        y1 = ibr1
       
        maxibr = max(abs(ibr1))
        idx_bfcz = end_idx - np.where(abs(ibr1[::-1]) >= maxibr*0.35)[0][0]
        idx_precz = np.where(abs(ibr1[idx_bfcz:]) <= maxibr*0.0125)[0][0] + idx_bfcz
        dididx = abs((ibr1[idx_precz] - ibr1[idx_precz - 5]))/5
        idx_cz = idx_precz + int(maxibr*0.0125 / dididx)
        
    if 'dfc' in vars():
        dfc = dfc - np.mean(dfc[:100])
        sol1 = savgol_filter(dfc, 100, 8)
        idx_sol_start = np.where(abs(sol1) >= max(abs(sol1))*0.05)[0][0]
        y3 = sol1
       
    if 'dfm'  in vars():
        dfm = dfm - np.mean(dfm[-100:])
        mc1 = savgol_filter(dfm, 100, 8)
        y4 = mc1
       
        maxmct = max(abs(mc1))
        idx_bfsep = end_idx - np.where(abs(mc1[::-1]) >= maxmct*0.5)[0][0]
        if 'dfs' in vars():
            ratio_ctsep = abs(str1[idx_bfsep] / v_end_str)
            
    if 'dfe' in vars():
        e_list0 = savgol_filter((dfe).tolist(), 80, 8)
        t_list0 = time0.tolist()
        time1 = [];  ibro = [];  ibr = []
        for i in range(end_idx):
            if i == 0: ibro.append(e_list0[i])
            else: ibro.append(ibro[i-1] + e_list0[i])
            if i % 100 == 0: time1.append(t_list0[i]); ibr.append(ibro[i])
       
        ibr = ((np.array(ibr) - np.mean(ibr[:100]))/10).tolist()
        maxibr = max(abs(np.array(ibr)))
        ibra = np.array(ibro) * 0.1
        idx_per_time = (end_idx - 1) / (t_list0[-1] - t_list0[0])
        time400us = int(0.4 * idx_per_time)
        time8ms = int(8 * idx_per_time)
        time15us = int(0.015 * idx_per_time)
        tbfcz = end_idx - np.where(abs(ibra[::-1]) >= maxibr*0.35)[0][0]
        tpre1ka = np.where(abs(ibra[tbfcz:]) <= maxibr*0.01)[0][0] + tbfcz
        ibrlast = max(abs(ibra[tpre1ka - time8ms :tpre1ka])) / 1000 / 1.41421356237
        ibrbflast = max(abs(ibra[tpre1ka - time8ms * 2 :tpre1ka - - time8ms])) / 1000 / 1.41421356237
        idx_per_current = time15us*10 / (ibra[tpre1ka] - ibra[tpre1ka+time15us*10])
        tcz0 = tpre1ka + idx_per_current * maxibr * 0.01
        didt = max(abs(ibra[tcz0-time15us:tcz0]-ibra[tcz0-time15us-10:tcz0-10])) * idx_per_time / 10000
       
        x2 = time1;  y6 = ibr
       
    if 'dfv' in vars():  
        trva = savgol_filter((dfv).tolist(), 10, 8)
        v_list0 = trva;   t_list0 = time0
        time2 = [];   trv = []
        if 'dfe' in vars():
            tcz = np.where(abs(trva[tpre1ka:]) <= 0.1)[0][0] + tpre1ka
            varc = max(trva[tpre1ka:tcz])
            rrrv = max(abs(trva[tcz:tcz+time400us] - trva[tcz-10:tcz+time400us-10])) * idx_per_time / 10000
            vwith = max(abs(trva[tcz:tcz+time400us]))
            pst = tcz / end_idx
            for i in range(end_idx):
                if end_idx * (pst - 0.05) <= i <= end_idx * (pst + 0.05):
                    if i % 2 == 0: time2.append(t_list0[i]);   trv.append(v_list0[i])
                elif i % 1000 == 0:
                    time2.append(t_list0[i]);   trv.append(v_list0[i])
        for i in range(end_idx):
            if i % 2 == 0:
                time2.append(t_list0[i]);   trv.append(v_list0[i])
                
        x3 = time2;   y5 = trv
       
    if 'dfo1' in vars():
        dfo1 = dfo1 - np.mean(dfo1[:100])
        other1 = savgol_filter(dfo1, 100, 8)
        y7 = other1
       
    if 'dfo2' in vars():
        dfo2 = dfo2 - np.mean(dfo2[:100])
        other2 = savgol_filter(dfo2, 100, 8)
        y8 = other2
   
    p = my.plot_bokeh('osc')
    my.base_xaxis(p, min(x1), max(x1), 'time [ms]', 'black')
   
    if 'y1' in vars():
        my.base_yaxis(p, min(y1)*1.2, max(y1)*1.2, '', 'black')
        my.add_line_chart(p, x1, y1, min(y1)*1.2, max(y1)*1.2, 'current', 0.5, 1, 'red', 'A', 'left', False)
    if 'y2' in vars():
        my.add_line_chart(p, x1, y2, min(y2)*1.2, abs(min(y2))*0.2, 'stroke', 0.5, 1, 'green', 'V', 'left', False)
    if 'y3' in vars():
        my.add_line_chart(p, x1, y3, max(y3)*-0.1, max(y3)*10, 'coil', 0.5, 1, 'blue', 'V', 'left', False)
    if 'y4' in vars():
        my.add_line_chart(p, x1, y4, max(y4)*-10, max(y4)*1.2, 'main', 0.5, 1, 'purple', 'V', 'left', False)
    if 'y5' in vars():
        my.add_line_chart(p, x3, y5, min(y5)*1.2, max(y5)*1.2, 'trv', 0.6, 1, 'violet', 'V', 'left', False)
    if 'y6' in vars():
        my.base_yaxis(p, min(y6)*1.2, max(y6)*1.2, '', 'black')
        my.add_line_chart(p, x2, y6, min(y6)*1.2, max(y6)*1.2, 'current', 0.5, 1, 'red', 'A', 'left', False)
    if 'y7' in vars():
        my.add_line_chart(p, x1, y7, min(abs(y7))*-1.2, max(abs(y7))*1.2, 'other1', 0.5, 1, 'blue', 'V', 'left', False)
    if 'y8' in vars():
        my.add_line_chart(p, x1, y8, min(abs(y7))*-1.2, max(abs(y7))*1.2, 'other2', 0.5, 1, 'black', 'V', 'left', False)

    if show == True:
        if 'y1' in vars(): my.show_bokeh_with_dot(p, [x1[idx_cz]], [y1[idx_cz]])
        else: my.show_bokeh_with_dot(p, [], [])
        
        
        
    if 'dfe' in vars():
        st.write('di/dt : ' + str(round(didt, 2)) + ' A/us')
        st.write('ibr_bf_last : ' + str(round(ibrbflast, 2))+ ' kArms')
        st.write('ibr_last : ' + str(round(ibrlast, 2))+ ' kArms')
        st.write('ibr(avg) : ' + str(round(ibrbflast*0.5 + ibrlast*0.5, 2))+ ' kArms')
        if 'dfv' in vars():
            st.write('du/dt : ' + str(round(rrrv, 2))+ ' kV/us')
            st.write('varc : ' + str(round(varc, 2))+ ' kV')
            st.write('vpeak : ' + str(round(vwith, 2))+ ' kV')
            
    if 'dfm' in vars() and 'dfc' in vars():
        topen = x1[idx_bfsep] - x1[idx_sol_start]
        st.write('open time : ' + str(round(topen, 2)) + ' ms')
        if 'dfs' in vars():
            st.write('sliding : ' + str(round(ratio_ctsep * full_stroke, 2)) + ' mm [' + str(round(ratio_ctsep * 100, 2)) + ' %]')
        
    if 'dfs' in vars():
        if 'dfm' not in vars() and 'dfc' in vars():
            topen = x1[idx_sep] - x1[idx_sol_start]
            st.write('open time : ' + str(round(topen, 2)) + ' ms')
        if 'dfi' in vars():
            tarc = x1[idx_cz] - x1[idx_sep]
            st.write('arcing time : ' + str(round(tarc, 2)) + ' ms')
            if 'dfc' in vars():
                tbr = x1[idx_cz] - x1[idx_sol_start]
                st.write('breaking time : ' + str(round(tbr, 2)) + ' ms')
            vr_str_cz = abs(str1[idx_cz] / v_end_str)
            st.write('stroke at current zero : ' + str(round(vr_str_cz * full_stroke, 2)) + ' mm')
        st.write('speed : ' + str(round(drdt * full_stroke, 2))+ ' m/s')
        st.write('undershoot : ' + str(round(v_undershoot * full_stroke, 2))+ ' mm')
        st.write('rebound : ' + str(round(v_rebound * full_stroke, 2))+ ' mm')
    elif 'dfi' in vars() and 'dfc' in vars():
        tbr = x1[idx_cz] - x1[idx_sol_start]
        st.write('breaking time : ' + str(round(tbr, 2)) + ' ms')
        

    return





def czm(data, show):
    df0 = my.upload_large_csv(data, 8, '\t')
    t_array = df0['f0'].to_numpy()
    e_array = df0['f1'].to_numpy()
    v_array = df0['f2'].to_numpy()
    t_list0 = (t_array * 1000).tolist()
    e_list0 = savgol_filter((e_array).tolist(), 80, 8)
    v_list0 = savgol_filter((v_array).tolist(), 10, 8)
   
    time0, time1, ibro, ibr, trv = [], [], [], [], []
    end_idx = len(t_list0)
   
    for i in range(end_idx):
        if i == 0:
            ibro.append(e_list0[i])
        else:
            ibro.append(ibro[i-1] + e_list0[i])
        if i % 100 == 0:
            time1.append(t_list0[i])
            ibr.append(ibro[i])
   
    ibr = ((np.array(ibr) - np.mean(ibr[:100]))/10).tolist()
   
    maxibr = max(abs(np.array(ibr)))
   
    ibra = np.array(ibro) * 0.1
    trva = v_list0
   
    tbfcz = end_idx - np.where(abs(ibra[::-1]) >= maxibr*0.35)[0][0]
    #st.write('time for somewhere with 35% ibr before cz :',t_list0[tbfcz])
   
    tpre1ka = np.where(abs(ibra[tbfcz:]) <= maxibr*0.0125)[0][0] + tbfcz
    #st.write('time for somewhere with 1kAp before cz :', t_list0[tpre1ka])
   
    tcz = np.where(abs(trva[tpre1ka:]) <= 0.1)[0][0] + tpre1ka
    #st.write('time at cz :', t_list0[tcz])
   
    varc = max(trva[tpre1ka:tcz])
   
    idx_per_time = (end_idx - 1) / (t_list0[-1] - t_list0[0])
    time400us = int(0.4 * idx_per_time)
    rrrv = max(abs(trva[tcz:tcz+time400us] - trva[tcz-10:tcz+time400us-10])) * idx_per_time / 10000
    vwith = max(abs(trva[tcz:tcz+time400us]))
   
    time8ms = int(8 * idx_per_time)
    ibrlast = max(abs(ibra[tpre1ka - time8ms :tpre1ka])) / 1000 / 1.41421356237
    ibrbflast = max(abs(ibra[tpre1ka - time8ms * 2 :tpre1ka - - time8ms])) / 1000 / 1.41421356237
   
    time15us = int(0.015 * idx_per_time)
    didt = max(abs(ibra[tcz-time15us:tcz]-ibra[tcz-time15us-10:tcz-10])) * idx_per_time / 10000
   
    pst = tcz / end_idx
   
    for i in range(end_idx):
        if end_idx * (pst - 0.05) <= i <= end_idx * (pst + 0.05):
            if i % 2 == 0:
                time0.append(t_list0[i])
                trv.append(v_list0[i])
        elif i % 1000 == 0:
            time0.append(t_list0[i])
            trv.append(v_list0[i])
           
    x1 = time0
    x2 = time1
    y = ibr
    z = trv
   
    p = my.plot_bokeh('test')
    my.base_xaxis(p, min(x1), max(x1), 'time [ms]', 'black')
    my.base_yaxis(p, min(y)*1.2, max(y)*1.2, '', 'black')
   
    my.add_line_chart(p, x2, y, min(y)*1.2, max(y)*1.2, 'current', 0.5, 1, 'red', 'A', 'left', False)
    my.add_line_chart(p, x1, z, abs(max(z))*-1.2, abs(max(z))*1.2, 'trv', 0.5, 1, 'green', 'V', 'left', False)
    if show == True: my.show_bokeh_with_dot(p, [], [])
   
    return p, varc, rrrv, vwith, ibrbflast, ibrlast, didt


def czm2(czm0, show, x_range):
    dt0 = czm0
    df0 = my.upload_large_csv(dt0, 8, '\t')
    t_array = df0['f0'].to_numpy()
    e_array = df0['f1'].to_numpy()
    v_array = df0['f2'].to_numpy()
    t_list0 = (t_array * 1000).tolist()
    e_list0 = savgol_filter((e_array).tolist(), 80, 8)
    v_list0 = savgol_filter((v_array).tolist(), 10, 8)
   
    time0, time1, ibro, ibr, trv = [], [], [], [], []
    end_idx = len(t_list0)
   
    for i in range(end_idx):
        if i == 0:
            ibro.append(e_list0[i])
        else:
            ibro.append(ibro[i-1] + e_list0[i])
        if i % 100 == 0:
            time1.append(t_list0[i])
            ibr.append(ibro[i])
   
    ibr = ((np.array(ibr) - np.mean(ibr[:100]))/10).tolist()
   
    maxibr = max(abs(np.array(ibr)))
   
    ibra = np.array(ibro) * 0.1
    trva = v_list0
   
    tbfcz = end_idx - np.where(abs(ibra[::-1]) >= maxibr*0.35)[0][0]
    #st.write('time for somewhere with 35% ibr before cz :',t_list0[tbfcz])
   
    tpre1ka = np.where(abs(ibra[tbfcz:]) <= maxibr*0.0125)[0][0] + tbfcz
    #st.write('time for somewhere with 1kAp before cz :', t_list0[tpre1ka])
   
    tcz = np.where(abs(trva[tpre1ka:]) <= 0.1)[0][0] + tpre1ka
    #st.write('time at cz :', t_list0[tcz])
   
    varc = max(v_array[tpre1ka:tcz])
   
    idx_per_time = (end_idx - 1) / (t_list0[-1] - t_list0[0])
    time400us = int(0.4 * idx_per_time)
    rrrv = max(abs(trva[tcz:tcz+time400us] - trva[tcz-10:tcz+time400us-10])) * idx_per_time / 10000
    vwith = max(abs(trva[tcz:tcz+time400us]))
   
   
    time8ms = int(8 * idx_per_time)
    ibrlast = max(abs(ibra[tpre1ka - time8ms :tpre1ka])) / 1000 / 1.41421356237
    ibrbflast = max(abs(ibra[tpre1ka - time8ms * 2 :tpre1ka - - time8ms])) / 1000 / 1.41421356237
   
    time15us = int(0.015 * idx_per_time)
    didt = max(abs(ibra[tcz-time15us:tcz]-ibra[tcz-time15us-10:tcz-10])) * idx_per_time / 10000
   
    pst = tcz / end_idx
   
    for i in range(end_idx):
        if end_idx * (pst - x_range/1000) <= i <= end_idx * (pst + x_range/1000):
            if i % 2 == 0:
                time0.append(t_list0[i])
                trv.append(v_list0[i])
        elif i % 1000 == 0:
            time0.append(t_list0[i])
            trv.append(v_list0[i])
           
    x1 = time0
    x2 = time1
    y = ibr
    z = trv
   
    p = my.plot_bokeh('test')
    my.base_xaxis(p, (pst - x_range/1000) * max(x1), (pst + x_range/1000) * max(x1), 'time [ms]', 'black')
    my.base_yaxis(p, min(y)*1.2, max(y)*1.2, '', 'black')
   
    my.add_line_chart(p, x2, y, min(y)*1.2, max(y)*1.2, 'current', 0.5, 1, 'red', 'A', 'left', False)
    my.add_line_chart(p, x1, z, abs(max(z))*-1.2, abs(max(z))*1.2, 'trv', 0.5, 1, 'green', 'V', 'left', False)
    if show == True:
        my.show_bokeh_with_dot(p, [], [])
   
    return p


def noload(data, show):
    df = my.upload_large_csv(data, 8, ',')
    
    time0 = df['f0'] * 1000
    mct0 = df['f1'] - np.mean(df['f1'][-100:])
    str0 = df['f2'] - np.mean(df['f2'][:100])
    sol0 = df['f3'] - np.mean(df['f3'][:100])
    
    idx_len = len(time0)
    
    mct1 = savgol_filter(mct0, 100, 8)
    for i in range(1, idx_len):
        if abs(str0[i] - str0[i-1]) >= abs(np.mean(str0[-100:])):
            str0[i] = str0[i-1]
    str1 = savgol_filter(str0, 300, 1)
    sol1 = savgol_filter(sol0, 100, 8)
    
    x1 = time0;  y1 = mct1;  y2 = str1;  y3 = sol1
    
    maxmct = max(abs(mct1))
    idx_bfsep = idx_len - np.where(abs(mct1[::-1]) >= maxmct*0.5)[0][0]
    
    p = my.plot_bokeh('osc')
    my.base_xaxis(p, min(x1), max(x1), 'time [ms]', 'black')
    my.base_yaxis(p, max(y1)*-10, max(y1)*1.2, '', 'black')
    
    my.add_line_chart(p, x1, y1, max(y1)*-10, max(y1)*1.2, 'main contact', 0.5, 1, 'red', 'V', 'left', False)
    my.add_line_chart(p, x1, y2, min(y2)*1.2, abs(min(y2))*0.2, 'stroke', 0.5, 1, 'green', 'V', 'left', False)
    my.add_line_chart(p, x1, y3, max(y3)*-0.1, max(y3)*10, 'coil', 0.5, 1, 'blue', 'V', 'left', False)
    
    if show == True: my.show_bokeh_with_dot(p, [x1[idx_bfsep]], [y1[idx_bfsep]])
    
    idx_sol_start = np.where(abs(sol1) >= max(abs(sol1))*0.15)[0][0]
    topen = x1[idx_bfsep] - x1[idx_sol_start]
    v_end_str = np.mean(str1[-100:])
    ratio_ctsep = abs(str1[idx_bfsep] / v_end_str)
    idx_str40 = np.where(abs(str1) >= abs(v_end_str)*0.40)[0][0]
    idx_str75 = np.where(abs(str1) >= abs(v_end_str)*0.75)[0][0]
    drdt = abs(round(   (str1[idx_str75] - str1[idx_str40]) / (x1[idx_str75] - x1[idx_str40]) / v_end_str, 2))
    if min(str1) < v_end_str * 1.005: v_undershoot = abs((min(str1) - v_end_str) / v_end_str)
    else: v_undershoot = 0
    try:
        idx_start_rebound = idx_bfsep + np.where((str1[idx_bfsep + 10 : ] - str1[idx_bfsep : -10]) > 0)[0][0]
        v_rebound_max = max(str1[idx_start_rebound:])
        if v_rebound_max > v_end_str * 0.995: v_rebound = abs((v_end_str - v_rebound_max) / v_end_str)
        else: v_rebound = 0
    except: st.empty()
    
    return p, topen, ratio_ctsep, drdt, v_undershoot, v_rebound


def synthetic(data, ct_sep_per, show):
    df0 = my.upload_large_csv(data, 8, ',')
   
    time0 = df0['f0'] * 1000
    ibr0 = df0['f1'] - np.mean(df0['f1'][:100])
    str0 = df0['f2'] - np.mean(df0['f2'][:100])
    sol0 = df0['f3'] - np.mean(df0['f3'][:100])
   
    idx_len = len(time0)
   
    ibr1 = savgol_filter(ibr0, 100, 8)
    for i in range(1, idx_len):
        if abs(str0[i] - str0[i-1]) >= abs(np.mean(str0[-100:])):
            str0[i] = str0[i-1]
    str1 = savgol_filter(str0, 300, 1)
    sol1 = savgol_filter(sol0, 100, 8)
   
    maxibr = max(abs(ibr1))
    idx_bfcz = idx_len - np.where(abs(ibr1[::-1]) >= maxibr*0.35)[0][0]
    idx_precz = np.where(abs(ibr1[idx_bfcz:]) <= maxibr*0.0125)[0][0] + idx_bfcz
    dididx = abs((ibr1[idx_precz] - ibr1[idx_precz - 5]))/5
    idx_cz = idx_precz + int(maxibr*0.0125 / dididx)
   
    x1 = time0;  y1 = ibr1;  y2 = str1;  y3 = sol1
   
    p = my.plot_bokeh('osc')
    my.base_xaxis(p, min(x1), max(x1), 'time [ms]', 'black')
    my.base_yaxis(p, min(y1)*1.2, max(y1)*1.2, '', 'black')
   
    my.add_line_chart(p, x1, y1, min(y1)*1.2, max(y1)*1.2, 'current', 0.5, 1, 'red', 'A', 'left', False)
    my.add_line_chart(p, x1, y2, min(y2)*1.2, abs(min(y2))*0.2, 'stroke', 0.5, 1, 'green', 'V', 'left', False)
    my.add_line_chart(p, x1, y3, max(y3)*-0.1, max(y3)*10, 'coil', 0.5, 1, 'blue', 'V', 'left', False)
    
    if show == True: my.show_bokeh_with_dot(p, [x1[idx_cz]], [y1[idx_cz]])
    
    idx_sol_start = np.where(abs(sol1) >= max(abs(sol1))*0.15)[0][0]
    v_end_str = np.mean(str1[-100:])
    v_ct_sep = abs(v_end_str * ct_sep_per / 100)
    idx_sep = np.where(abs(str1) > v_ct_sep)[0][0]
    
    topen = x1[idx_sep] - x1[idx_sol_start]
    tarc = x1[idx_cz] - x1[idx_sep]
    tbr = x1[idx_cz] - x1[idx_sol_start]
    vr_str_cz = abs(str1[idx_cz] / v_end_str)
    
    return p, topen, tarc, tbr, vr_str_cz






   
    