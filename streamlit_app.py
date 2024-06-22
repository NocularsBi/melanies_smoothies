# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!.
    """
)

# Don't add apostrophes just yet, not handled yet in the prototype
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)


# option = st.selectbox(
#    'What is your favorite fruit?',
#    ('Banana', 'Strawberries', 'Peaches'))
# st.write('Your favorite fruit is : ', option)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Dataframe (we don't really wanna show it in our page so we can comment it out for now)
#st.dataframe(data=my_dataframe, use_container_width=True)

# Multiselect option (Won't enforce the 5 ingredients limit)
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections = 5
)

# ingredients_list ends up being a list of values that you select
# st.write(ingredients_list)
# st.text(ingredients_list)

# "if !ingredients_list" is the same thing as "if ingredients_list is null"
# "if ingredients_list" is the same thing as "if ingredients_list is not null"

if ingredients_list:
    # Convert the list to a string to store the ingredients into the orders table
    ingredients_string = ''
    for fruit in ingredients_list:
        ingredients_string += fruit + ' '
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
        values ('""" + ingredients_string + """', '"""+name_on_order+"""')"""
    
    # st.write(my_insert_stmt)
    # Very good troubleshooting piece of code: st.stop()

    # Let's make a submit order button so the orders table only populates when the button is pressed
    time_to_insert = st.button('Submit Order')
    
    # If the button is clicked by the customer
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon = "✅")


