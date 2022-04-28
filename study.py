import google_auth_httplib2
import httplib2
import pandas as pd
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest
import json

SCOPE = "https://www.googleapis.com/auth/spreadsheets"
SPREADSHEET_ID = "1S7YBK5AqAE9GPHdZEto9WTPGOyLHSBP5EgDTejlG8dU"
SHEET_NAME_DATA = "Database"
SHEET_NAME_RESPONSES = "Responses"
GSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"


@st.experimental_singleton()
def connect_to_gsheet():
    # Create a connection object.
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[SCOPE],
    )

    # Create a new Http() object for every request
    def build_request(http, *args, **kwargs):
        new_http = google_auth_httplib2.AuthorizedHttp(
            credentials, http=httplib2.Http()
        )
        return HttpRequest(new_http, *args, **kwargs)

    authorized_http = google_auth_httplib2.AuthorizedHttp(
        credentials, http=httplib2.Http()
    )
    service = build(
        "sheets",
        "v4",
        requestBuilder=build_request,
        http=authorized_http,
    )
    gsheet_connector = service.spreadsheets()
    return gsheet_connector


def get_data(gsheet_connector) -> pd.DataFrame:
    values = (
        gsheet_connector.values()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME_DATA}!A:B",
        )
        .execute()
    )

    df = pd.DataFrame(values["values"])
    df.columns = df.iloc[0]
    df = df[1:]
    return df


def add_row_to_gsheet(gsheet_connector, row) -> None:
    gsheet_connector.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME_RESPONSES}!A:O",
        body=dict(values=row),
        valueInputOption="USER_ENTERED",
    ).execute()


st.set_page_config(page_title="User study", page_icon="🗨️", layout="centered")

st.title("🗨️ Demo User Study")

gsheet_connector = connect_to_gsheet()

st.sidebar.write(
    "This is a user study conducted by ACME Corp. If you have any questions "
    "please contact acme@acme.org."
)


with st.form(key="annotation", clear_on_submit=True):
    data = get_data(gsheet_connector).sample(n=5)
    st.subheader("Comment 1:")
    st.write(data.iloc[0]['comment'])
    cols = st.columns(2)
    value_a_1 = cols[0].slider("Partisanship:", -50, 50, 0, key="value_a_1")
    value_b_1 = cols[1].slider("How political:", 0, 100, 50, key="value_b_1")
    st.subheader("Comment 2:")
    st.write(data.iloc[1]['comment'])
    cols = st.columns(2)
    value_a_2 = cols[0].slider("Partisanship:", -50, 50, 0, key="value_a_2")
    value_b_2 = cols[1].slider("How political:", 0, 100, 50, key="value_b_2")
    st.subheader("Comment 3:")
    st.write(data.iloc[2]['comment'])
    cols = st.columns(2)
    value_a_3 = cols[0].slider("Partisanship:", -50, 50, 0, key="value_a_3")
    value_b_3 = cols[1].slider("How political:", 0, 100, 50, key="value_b_3")
    st.subheader("Comment 4:")
    st.write(data.iloc[3]['comment'])
    cols = st.columns(2)
    value_a_4 = cols[0].slider("Partisanship:", -50, 50, 0, key="value_a_4")
    value_b_4 = cols[1].slider("How political:", 0, 100, 50, key="value_b_4")
    st.subheader("Comment 5:")
    st.write(data.iloc[4]['comment'])
    cols = st.columns(2)
    value_a_5 = cols[0].slider("Partisanship:", -50, 50, 0, key="value_a_5")
    value_b_5 = cols[1].slider("How political:", 0, 100, 50, key="value_b_5")
    submitted = st.form_submit_button(label="Submit")


if submitted:
    add_row_to_gsheet(
        gsheet_connector,
        [[data.iloc[0]['id'], value_a_1, value_b_1,
          data.iloc[1]['id'], value_a_2, value_b_2,
          data.iloc[2]['id'], value_a_3, value_b_3,
          data.iloc[3]['id'], value_a_4, value_b_4,
          data.iloc[4]['id'], value_a_5, value_b_5]],
    )
    st.success("Thanks! Your response was recorded. Want to rate another batch? :)")
    st.balloons()

expander = st.expander("See all records")
with expander:
    st.write(f"Open original [Google Sheet]({GSHEET_URL})")
    st.dataframe(get_data(gsheet_connector))
