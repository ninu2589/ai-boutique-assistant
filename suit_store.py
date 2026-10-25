import groq
import streamlit as st
from suit_helper import MissingAPIKeyError, show_suit_and_saree_types


# Successful results are cached per location; errors are not cached, so a retry calls Groq again
@st.cache_data(show_spinner=False, ttl=24 * 60 * 60)
def get_stores(location):
    return show_suit_and_saree_types(location)


st.title('Suit and Saree Store')
location = st.sidebar.selectbox(
    'Choose a Suit and Saree store', ('Ahmedabad', 'Vadodra', 'Jaipur', 'Delhi', 'Gurugram', 'Bengaluru','Chennai','Jodhpur','Gwalior', 'Lucknow','Surat','Indore','Pune','Kolkata','Mumbai','Hyderabad','Nagpur','Bhopal','Chandigarh','Mysore'))
search = st.sidebar.button('Search', type='primary')

if not search:
    st.info('Choose a location and click **Search** to find stores.')
    st.stop()

try:
    with st.spinner(f'Finding stores in {location}…'):
        response = get_stores(location)
except MissingAPIKeyError:
    st.error('Groq API key is missing. Set GROQ_API_KEY or add API_KEY to secret_file.py.')
except groq.AuthenticationError:
    st.error('Groq rejected the API key. Check that it is correct and still active.')
except groq.RateLimitError:
    st.warning('Groq free-tier limit reached. Please wait a minute and try again.')
except (groq.APIConnectionError, groq.APITimeoutError):
    st.error('Could not reach Groq. Check your internet connection and try again.')
except groq.APIError as e:
    st.error(f'Groq returned an error: {getattr(e, "message", e)}')
else:
    st.header("Store Names")
    st.write(response["store_names"].strip())

    st.header("Types of Suits and Sarees")
    st.write(response["suit_types"].strip())
