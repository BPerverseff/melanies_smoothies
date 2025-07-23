# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f"Customize Your Smoothie :cup_with_straw: ")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

#Add Name to order
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

from snowflake.snowpark.functions import col

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
# comment out this line to not display the DF 
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

#Add a multiselect
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)


#Comment this out as it displays empty brackets when the list is empty
    #Display the list variable
    #st.write(ingredients_list)
    #st.text(ingredients_list)

#Replace with this as it is cleaner
if ingredients_list:

    #create an empty string variable
    ingredients_string = ''

    #Convert the list into the new string variable
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutritional Information')
        smoothiefroot_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)

        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    #Output the string
    st.write(ingredients_string)

    #Create a sql statement for insert
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
        values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    #comment this out as it is no longer required
    #st.write(my_insert_stmt)

    #Add a submit button
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothie is ordered!', icon="✅")
      



