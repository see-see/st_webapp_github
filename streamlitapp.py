from random import random
import streamlit as st

# from streamlit import (
#     session_state as ss,
#     title as tt
# )
import functions as fn
fn.checks('start')

st.title("My To-do App")
st.subheader("To-do list to increase _productivity_.")
st.caption(f"{st.session_state['EDIT_TEXT_CAPTION']}", unsafe_allow_html=True)

# Upon 'on_change' event add_tod() is run and
# then immediately whole program from start is run
text = st.text_input(label='label', label_visibility='hidden',
                     placeholder=st.session_state['TEXT_PLACEHOLDER'], key='to-do',
                     on_change=fn.add_todo)

st.caption(f":red{st.session_state['CAPTION_TEXT']}")

cont = st.container()
with cont:
    col1, col2 = st.columns([0.1, 1])  # [0.1, 1] specifies sizes of columns
    with col1:
        st.button('Edit', key='edit', on_click=fn.edit, args=['edit_button'],
                  disabled=st.session_state['EDIT_DISABLE'])
    with col2:
        st.button('Mark Complete', key='mc', on_click=fn.mc,
                  disabled=st.session_state['MC_DISABLE'])

radio = st.radio(
    label='List of todos: ',
    key="radio",
    options=[i.strip() for i in fn.read_file()],
    disabled=st.session_state['RAD_DISABLE'],
    index=st.session_state['radioindex']
)

fn.checks('end')
