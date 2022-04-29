import google_auth_httplib2
import httplib2
import pandas as pd
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest
from datetime import datetime
import uuid

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
        new_http = google_auth_httplib2.AuthorizedHttp(credentials, http=httplib2.Http())
        return HttpRequest(new_http, *args, **kwargs)

    authorized_http = google_auth_httplib2.AuthorizedHttp(credentials, http=httplib2.Http())
    service = build(
        "sheets",
        "v4",
        requestBuilder=build_request,
        http=authorized_http,
    )
    gsheet_connector = service.spreadsheets()
    return gsheet_connector


def get_data(gsheet_connector, col_range) -> pd.DataFrame:
    values = (
        gsheet_connector.values()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME_DATA}!{col_range}",
        )
        .execute()
    )

    df = pd.DataFrame(values["values"])
    df.columns = df.iloc[0]
    df = df[1:]
    return df


def add_row_to_gsheet(gsheet_connector, row, col_range) -> None:
    gsheet_connector.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME_RESPONSES}!A{col_range}",
        body=dict(values=row),
        valueInputOption="USER_ENTERED",
    ).execute()


st.set_page_config(page_title="User study", page_icon="🗨️", layout="wide")

# create unique session ID per connection
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid1())

if "start" not in st.session_state:
    st.session_state.start = datetime.now(tz=None)

gsheet_connector = connect_to_gsheet()

st.sidebar.write(
    "This is a user study conducted by ACME Corp. If you have any questions "
    "please contact acme@acme.org."
)

st.title("🗨️ Demo User Study")

st.markdown(
    """
#### Hello! 👋

Thank you for taking part in this study and helping us make social media more diverse and equitable.

#### How it works

You are presented with **five** comments from Reddit. These comments will be shown **in context** - that means you also see up to two previous comments that are being replied to.

Here is an example of a single comment in context:

---

> How...how could you think that? Every article for the last 4 months about Trump have been against him. Every move he makes is criticized. One glance from his wife makes him an abuser. His son looking bored makes him a psycho school shooter. It's literally non-stop negative media coverage.
>> This is why Trump won, though. Who cares about all the small shit meaningless memes you just quoted? What about the actually bad shit he has said (and done)?
>>> <mark>A lot of people would disagree on what is bad shit said and done however.</mark>

---

You are asked to rate **only the last comment** (here: _"A lot of people would disagree on what is bad shit said and done however."_)

#### Sliders

Please set the sliders under each comment to a position you think is appropriate. 

It does not matter that much where exactly you place the slider - it is more important that the relation of the slider positions among the five comments makes sense.

##### Civility
How civil/uncivil is the comment?
- **0**: completely civil  (_“I understand your opinion but must disagree.”_)
- **50**: somewhat uncivil  (_“Go annoy someone else with your stupid theories.”_)
- **100**: completely uncivil  (_“Fuck you, you son of a bitch! I hope you die.”_)

##### Politicalness
Is the comment related to politics?
- **0**: Not political at all (_"I like ice cream"_)
- **50**: Somewhat political (_"And I thought free speech was important ... Lol"_)
- **100**: Definitely political (_"Aside from W getting reelected as an incumbent, the GOP hasn't won a majority of the vote since Bush Sr. in 1988."_)

##### Partisanship
Which political partisanship does the author of the comment likely have?
- **-50**: extreme left
- **-25**: left
- **0**: center
- **25**: right
- **50**: extreme right

#### How to decide
What if the author is quoting someone else? What if irony is being used? 

Judging comments on these scales can be challenging, and there are no right answers. 

When in doubt, simply follow your gut instinct.
""",
    unsafe_allow_html=True,
)

with st.form(key="annotation", clear_on_submit=True):
    data = get_data(gsheet_connector, col_range="A:B").sample(n=5)
    st.subheader("Comment 1:")
    st.markdown(data.iloc[0]["comment_markdown"], unsafe_allow_html=True)
    cols = st.columns(3)
    civility_1 = cols[0].slider("Civility:", 0, 100, 50, key="civility_1")
    political_1 = cols[1].slider("Politicalness:", 0, 100, 50, key="political_1")
    partisan_1 = cols[2].slider("Partisanship:", -50, 50, 0, key="partisan_1")
    st.subheader("Comment 2:")
    st.markdown(data.iloc[1]["comment_markdown"], unsafe_allow_html=True)
    cols = st.columns(3)
    civility_2 = cols[0].slider("Civility:", 0, 100, 50, key="civility_2")
    political_2 = cols[1].slider("Politicalness:", 0, 100, 50, key="political_2")
    partisan_2 = cols[2].slider("Partisanship:", -50, 50, 0, key="partisan_2")
    st.subheader("Comment 3:")
    st.markdown(data.iloc[2]["comment_markdown"], unsafe_allow_html=True)
    cols = st.columns(3)
    civility_3 = cols[0].slider("Civility:", 0, 100, 50, key="civility_3")
    political_3 = cols[1].slider("Politicalness:", 0, 100, 50, key="political_3")
    partisan_3 = cols[2].slider("Partisanship:", -50, 50, 0, key="partisan_3")
    st.subheader("Comment 4:")
    st.markdown(data.iloc[3]["comment_markdown"], unsafe_allow_html=True)
    cols = st.columns(3)
    civility_4 = cols[0].slider("Civility:", 0, 100, 50, key="civility_4")
    political_4 = cols[1].slider("Politicalness:", 0, 100, 50, key="political_4")
    partisan_4 = cols[2].slider("Partisanship:", -50, 50, 0, key="partisan_4")
    st.subheader("Comment 5:")
    st.markdown(data.iloc[4]["comment_markdown"], unsafe_allow_html=True)
    cols = st.columns(3)
    civility_5 = cols[0].slider("Civility:", 0, 100, 50, key="civility_5")
    political_5 = cols[1].slider("Politicalness:", 0, 100, 50, key="political_5")
    partisan_5 = cols[2].slider("Partisanship:", -50, 50, 0, key="partisan_5")
    submitted = st.form_submit_button(label="Submit")

if submitted:
    st.session_state.end = datetime.now(tz=None)
    add_row_to_gsheet(
        gsheet_connector,
        [
            [
                st.session_state.session_id,
                str(st.session_state.end),
                str(st.session_state.end - st.session_state.start),
                data.iloc[0]["id"],
                civility_1,
                political_1,
                partisan_1,
                data.iloc[1]["id"],
                civility_2,
                political_2,
                partisan_2,
                data.iloc[2]["id"],
                civility_3,
                political_3,
                partisan_3,
                data.iloc[3]["id"],
                civility_4,
                political_4,
                partisan_4,
                data.iloc[4]["id"],
                civility_5,
                political_5,
                partisan_5,
            ]
        ],
        col_range="A:W",
    )
    st.success("Thanks! Your response was recorded. Want to rate another batch? :)")
    st.balloons()
    st.session_state.start = datetime.now(tz=None)
