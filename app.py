import streamlit as st
import pandas as pd

st.set_page_config(
    page_title='Multipage App'
)

st.title('Main Page')
st.sidebar.success('Select a page above')


# if 'my_input' not in st.session_state:
#     st.session_state['my_name'] = ''

# xxx = st.text_input('input a test here : ', st.session_state['my_input'])
# submit = st.buttion('Submit')
# if submit:
#     st.session_state['my_input'] = my_input
#     st.write('you have entered : ', my_input)
# with open('list.txt', 'w', encoding='utf8') as f:
#     f.write(my_input)

my_input = st.text_input('input a test here : ')
submit = st.button('save')
if submit:
    name = my_input
    with open('list.csv', 'w', encoding='utf8') as f:
        f.write(name)



submit = st.button('load')
if submit:
    with open('list.csv', 'r', encoding='utf8') as f:
        st.write(f.read())
