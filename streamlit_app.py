# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import panda as py
Name_of_order=st.text_input('Name On the Smoothie ')
st.write('The Name Of your Smooothie will be :', Name_of_order)
# Write directly to the app
st.title("Example Streamlit App :balloon:")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)


# option = st.selectbox(
#     "What is your faviourate Food",
#     ("Banan", "Stovery", "Peachace"),
# )

# st.write("Your Faviorate food is:", option)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIt_NAME'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredients_list=st.multiselect(
    'Chose upto 5 ingredient :',
    my_dataframe,
    max_selections = 5
)

if ingredients_list:
    ingredients_string=''
    for fruit_chose in ingredients_list:
        ingredients_string += fruit_chose + ''
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chose + 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_chose)
        fv_df =st.dataframe(data=fruityvice_response.json() ,use_container_width=True)
    st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,Name_on_order)
            values ('""" + ingredients_string + " " "','"""+ Name_of_order + """')"""
    st.write(my_insert_stmt)
    # st.stop();
    time_to_insert=st.button("Submit Order ")
    if ingredients_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
    if time_to_insert :
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

