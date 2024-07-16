import streamlit as st


st.title("Employees")

option = st.selectbox('Select one',
    ('Select an option', 'hire', 'status', 'fire')
)

# st.write(f'You selected: {option}')
if option != 'Select an option':
    if option == 'hire':
        st.write('You are hiring this person')
    elif option == 'status':
        st.write('Here is the status')
    elif option == 'fire':
        st.write('Congratulations! You have been fired!')


# TODO: Guts this will be the status page for current employees
# Including hiring and firing as we talked about today
