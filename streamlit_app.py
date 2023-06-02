import pandas
import requests
import streamlit
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner.')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        streamlit.dataframe(fruityvice_normalized)
except URLError as e:
    streamlit.error()
streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("the fruit load list cotains:")
streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input("What fruit would you like to add?")
streamlit.write('Thanks for adding ', add_my_fruit)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")

# import streamlit
# import requests
# import pandas as pd
# import snowflake.connector
# from urllib.error import URLError

# streamlit.title('My Parents New Healthy Diner')
# streamlit.header('Breakfast menu')
# streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
# streamlit.text('🥗 Kale, Spinake & Rocket Smoothie')
# streamlit.text('🐔 Hard-Boiled Free-Range Egg')
# streamlit.text('🥑🍞 Avocado Toast')

# streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# my_fruit_list = my_fruit_list.set_index('Fruit')

# # let's put a pick list here so they can pick the fruit they want to incluide
# fruits_selected = streamlit.multiselect(
#     'Pick some fruits:',
#     list(my_fruit_list.index),
#     ['Avocado', 'Strawberries']
# )
# fruits_to_show = my_fruit_list.loc[fruits_selected]

# # display the table on the page
# streamlit.dataframe(fruits_to_show)

# def get_fruityvice_data(this_fruit_choice):
#     fruitvyce_response = requests.get('https://fruityvice.com/api/fruit/'+
#                                     this_fruit_choice)
#     fruitvyce_normalized = pd.json_normalize(fruitvyce_response.json())
#     return fruitvyce_normalized

# # New section to display fruityvice api response
# streamlit.header('Frutyvice Fruit Advice!')
# try:
#     fruit_choice = streamlit.text_input('What fruit would you like information about?',
#                                         placeholder='fruit name')
#     if not fruit_choice:
#         streamlit.error('Please select a fruit to get information')
#     else:
#         back_from_function = get_fruityvice_data(fruit_choice)
#         streamlit.dataframe(back_from_function)
# except URLError as e:
#     streamlit.error()
# streamlit.stop()
    
# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("select * from fruit_load_list")
# my_data_rows = my_cur.fetchall()
# streamlit.header("the fruit load list contains:")
# streamlit.dataframe(my_data_rows)

# add_my_fruit = streamlit.text_input("What fruit would you like to add?")
# streamlit.write('Thanks for adding', add_my_fruit)

# my_cur.execute("insert into fruit_load_list values ('from streamlit')")

# streamlit.header("View Our Fruit List- Add Your Favorites!")
# #Snowflake-related functions
# def get_fruit_load_list():
#     with my_cnx.cursor() as my_cur:
#         my_cur.execute("select * from fruit_load_list")
#         return my_cur.fetchall()

# # Add a button to load the fruit
# if streamlit.button('Get Fruit Load List'):
#     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#     my_data_rows = get_fruit_load_list()
#     my_cnx.close()
#     streamlit.dataframe(my_data_rows)

# # Allow the end user to add a fruit to the list
# def insert_row_snowflake(new_fruit):
#     with my_cnx.cursor() as my_cur:
#         my_cur.execute("insert into fruit_load_list values ('" + new_fruit +"')")
#         return streamlit.write('Thanks for adding', new_fruit)

# add_my_fruit = streamlit.text_input("What fruit would you like to add?")
# if streamlit.button('Add a fruit to the list'):
#     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#     back_from_function = insert_row_snowflake(add_my_fruit)
#     streamlit.text(back_from_function)
