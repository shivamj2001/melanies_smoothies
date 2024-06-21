# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas as pd



# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
    """Choose the custom fruits you want in your smoothie.
    """
)


name_on_order = st.text_input("Name on the Smoothie", "")
st.write("The name on your Smoothie will be:", name_on_order)


cnx = st.connection("snowflake")
session = cnx.session()

#session = get_active_session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()


ingredients_list = st.multiselect(
    'choose upto 5 ingredient: ', my_dataframe,max_selections = 5)


if ingredients_list:

      ingredients_string = ''

      for fruits_chosen in ingredients_list:
             ingredients_string += fruits_chosen + ' '
             st.subheader(fruits_chosen + 'Nutrition Information')
             fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruits_chosen)
             fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

      st.write(ingredients_string)

      my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)  
              values ('""" + ingredients_string + """','""" + name_on_order + """')"""

  #st.write(my_insert_stmt)
  #st.stop

      time_to_insert = st.button('Submit Order')  

      if time_to_insert:
          session.sql(my_insert_stmt).collect()
    
          st.success(f'Your Smoothie is ordered,{name_on_order}!', icon="✅")


#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)




























