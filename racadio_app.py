import streamlit as st
import pandas as pd
import numpy as np
import gspread 
import openpyxl
import datetime 
    

#Configure the page
st.set_page_config(page_title='Racadio Dashboard', layout='wide')
st.title('Racadio Dashboard')
tab1, tab2 = st.tabs(['Main Spreadsheet', 'Manual Entries'])
today = datetime.date.today()


#Congifure the first tab which will display the main spreadsheet and allow for reloading the data.
with tab1:
    st.header('Query Expenses')
    if st.button('Reload Data'):
        st.cache_data.clear()
        st.rerun()
    st.session_state.df = pd.read_excel('C:\\Users\\Racadio\\Documents\\Python_dashboard_1\\racadio_sheet.xlsx')
    #Format the date input.
    st.session_state.df['Date'] = pd.to_datetime(st.session_state.df['Date'], errors='coerce').dt.strftime('%m-%d-%Y')
    selection = st.multiselect('Select the Expense Type:', ['Babysitting', 'Bills', 'Food', 'Fuel', 'House', 'prosper', 'tinker', 'Will Oil Change'], default=[])
    search_term = st.text_input('Search Date (mm-dd-yyyy) or Description:')
    if selection:
        filtered_df = st.session_state.df[st.session_state.df['Type'].isin(selection)]
        st.dataframe(filtered_df)
    elif search_term:
        if search_term in st.session_state.df['Date'].values:
            filtered_df = st.session_state.df[st.session_state.df['Date'] == search_term]
            st.dataframe(filtered_df)
        elif search_term in st.session_state.df['Description'].values:
            filtered_df = st.session_state.df[st.session_state.df['Description'].str.contains(search_term, case=False, na=False)]
            st.dataframe(filtered_df)
    else:
        st.dataframe(st.session_state.df)

#Configure the second tab which will allow for manual entry of new expenses and saving them to the Excel file. It will also display the updated DataFrame after adding a new entry.
with tab2:
    with st.form('Add New Entry', clear_on_submit=True):
        type = st.selectbox('Select Expense Type:', ['Babysitting', 'Bills', 'Food', 'Fuel', 'House', 'prosper', 'tinker', 'Will Oil Change'])
        date = st.date_input('Enter Date:', value=today, format='MM-DD-YYYY')
        amount = st.number_input('Enter Amount:', min_value=None, step=0.01)
        description = st.text_area('Enter Description:')

        submitted = st.form_submit_button('Add Entry')

     #Process the new entry and add it to the DataFrame, then save it to the Excel file.
    if submitted:
        try:
            new_row = pd.DataFrame({'Type': [type], 'Date': [date], 'Amounts': [amount], 'Description': [description]})
            st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
            st.session_state.df.to_excel('C:\\Users\\Racadio\\Documents\\Python_dashboard_1\\racadio_sheet.xlsx', index=False)
        except Exception as e:
            st.error(f"An error occurred while adding the entry: {e}")

    #Display the updated DataFrame after adding the new entry.
    if st.checkbox('Show current sheet'):
        st.dataframe(pd.read_excel('C:\\Users\\Racadio\\Documents\\Python_dashboard_1\\racadio_sheet.xlsx'))



    
    



    
