
# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col,when_matched


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

session = get_active_session()
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()

editable_df = st.data_editor(my_dataframe)
Submitted=st.button('Submit')

if Submitted:
   
    og_dataset = session.table("smoothies.public.orders")
    edited_dataset = session.create_dataframe(editable_df)
    try:
        og_dataset.merge(edited_dataset
                     , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                     , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                    )
        st.success("Someone Clicked the Button")
    except:
        st.success("Something Went Wrong ")
else:
    st.success("There is no Order")
        
