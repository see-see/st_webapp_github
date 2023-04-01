from streamlit import session_state as ss
from random import random
import streamlit.components.v1 as components
# EDIT_FLAG is used as plan is: When 'Edit' button is clicked the value
# held in radio(to-do selected to edit) is displayed in the text box and
# User can make changes and press enter.
# Now when enter is pressed after entering the new to do in input box, the
# 'onchange' event takes over and calls 'add_todo().
# If EDIT_FLAG is false in 'add_todo()' means new to-do is entered.
# When 'Edit' button is clicked EDIT_FLAG is set to True, which means existing
# to-do is being edited so call goes as:
#
# **** EDIT pressed -->
# **** edit(call_from) : selected to-do shown in input box and EDITFLAG set to true -->
# **** to-do is edited and ENTER pressed -->
# **** 'onchange' event happens and add-to.do() called -->
# **** in add-to.do() as EDITFLAG is true now, else part is executed and edit(call_from)
# **** is called and to-do is edited in storage file.
FILEPATH = "storage.txt"


def checks(val):
    if val == 'start':
        todos = read_file()
        inst_st_var()
        if len(todos) == 0:
            disable_buttons()
    elif val == 'end':
        edit_check()


def inst_st_var():
    variables = {
        'EDIT_FLAG': False,
        'TEMP': '',
        'CAPTION_TEXT': '',
        'MC_DISABLE': False,
        'EDIT_TEXT_CAPTION': '',
        'EDIT_DISABLE': False,
        'RAD_DISABLE': False,
        'TEXT_PLACEHOLDER': 'Add todo',
        'to-do': '',
        'radioindex': 0
    }

    for var, val in variables.items():
        if var not in ss:
            ss[var] = val

    # The below code inserts random value at every run of program, so that html code is injected everytime.
    # If html code doesnt change, the script will not be injected.
    # The code below doesn't allow addition of text from text-box if its lose focus, like user types in
    # a value but instead of enter, user clicks somewhere else outside the text box.
    ss['rand'] = random()
    components.html(
        f"""
                 <p></p>
                <script>
                const d = {ss['rand']};
                const doc = window.parent.document;
                const input = doc.querySelector('input[aria-label="label"');

                input.addEventListener('focusout', function() {{ 
                    input.focus();                
                    event.stopPropagation();
                    event.preventDefault();                    
                    console.log('Lost focus');
                    
                    
                }});
                </script>
                """,
        height=0,
        width=0,
    )


def reset_var():
    variables = {
        'EDIT_FLAG': False,
        'TEMP': '',
        'CAPTION_TEXT': '',
        'MC_DISABLE': False,
        'EDIT_TEXT_CAPTION': '',
        'EDIT_DISABLE': False,
        'RAD_DISABLE': False,
        'TEXT_PLACEHOLDER': 'Add todo',
        'radioindex': 0
    }
    for var, val in variables.items():
        ss[var] = val


def disable_buttons():
    ss['MC_DISABLE'] = True
    ss['EDIT_DISABLE'] = True


def read_file():
    with open(FILEPATH, 'r') as file:
        todo_local = file.readlines()
        return todo_local


def write_to_file(todo_local):
    with open(FILEPATH, 'w') as file:
        file.writelines(todo_local)


def add_todo():
    # print('add todo')

    # ss["to-do"].strip() to remove spaces in beginning of to-do entered like: '  Hi'
    to_do = ss["to-do"].strip() + '\n'
    # print('to-do: ', to_do)
    todos = read_file()

    if ss["to-do"].strip() != '' and to_do not in todos and not ss['EDIT_FLAG']:  # to check if to-do entered is not a space
        todos.append(to_do)
        write_to_file(todos)
        ss['MC_DISABLE'] = False

    elif to_do in todos:
        ss['CAPTION_TEXT'] = f"':green[{to_do.strip()}]' already exists!"
    elif ss['EDIT_FLAG'] and to_do.strip() == '' or to_do.strip() == '':
        ss['CAPTION_TEXT'] = 'Please enter text!'
    else:
        edit('add_todo')

    # noticed that if 'to-do' in session_state is deleted, it means only that from
    # session the key value pair is deleted. But nothing happens to widget. only way is callback
    # function like 'add-to*do' be executed and write  ss['to-do'] = ""
    ss['to-do'] = ""


def edit(call_from):
    # print('in edit')
    if call_from == 'edit_button':
        # print('in callfrom edit')
        ss['EDIT_FLAG'] = True
        ss['TEMP'] = ss['radio']
        ss['MC_DISABLE'] = True
        ss['EDIT_DISABLE'] = True
        ss['RAD_DISABLE'] = True
        ss['EDIT_TEXT_CAPTION'] = f":green[Editing to-do:<br> {ss['TEMP'].strip()}]"
        ss['TEXT_PLACEHOLDER'] = ss['radio']

    elif call_from == 'add_todo':
        if ss['to-do'].strip() != '':
            # print('in callfrom addtodo')
            to_do = ss['to-do'].strip()
            todos = read_file()
            index = todos.index(ss['TEMP'] + '\n')
            todos[index] = to_do + '\n'
            write_to_file(todos)
            # print('about to change')
            ss['to-do'] = ''
            ss['EDIT_FLAG'] = False
            ss['MC_DISABLE'] = False
            ss['EDIT_DISABLE'] = False
            ss['RAD_DISABLE'] = False
            ss['EDIT_TEXT_CAPTION'] = ""
            ss['TEXT_PLACEHOLDER'] = "Add todo"
            ss['CAPTION_TEXT'] = ""
            ss['radioindex'] = index

        else:
            ss['CAPTION_TEXT'] = 'Please press Edit again and enter some text!'


def mc():
    # print('in MC')
    todos = read_file()
    todos.remove(ss['radio'] + '\n')
    write_to_file(todos)


def edit_check():
    if not ss['EDIT_FLAG']:
        reset_var()
