import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("Test streamlit app")

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_seleced = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_seleced]
streamlit.dataframe(my_fruit_list)


def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
# streamlit.text(fruityvice_response.json())

  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  streamlit.dataframe(fruityvice_normalized)


streamlit.header('Fruityvice Fruit Advice!')
try:  
  fruit_choice = streamlit.text_input('What fruit would you like information about ?', 'Kiwi')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function=get_fruityivce_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error
#streamlit.write('The user entered', fruit_choice)




streamlit.stop()
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.text("The Fruit load list contains:")
streamlit.dataframe(my_data_row)

fruit_add = streamlit.text_input('what fruit would you like to add ?', 'Kiwi')

my_cur.execute(f"insert into fruit_load_list values ('{fruit_add}')")
#my_cur.executemany(stmt, fruit_add)
streamlit.write('Thanks for adding', fruit_add)

