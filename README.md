<h1 align="center">User Study Template Repository</h1>
<h4 align="center">Streamlit ♥️ Google Sheets</h4>

## About

This repository demonstrates how you can create a free & simple publicly hosted user study with streamlit that writes the results to a Google Sheets document :)

Try out submitting answers here: https://share.streamlit.io/epistoteles/userstudy/main/study.py

And watch the results show up in this document: https://docs.google.com/spreadsheets/d/1S7YBK5AqAE9GPHdZEto9WTPGOyLHSBP5EgDTejlG8dU/edit?usp=sharing

## How-to

1. Fork this repository (the fork has to be public).
2. Create a copy of the Google Sheets template used in this repository of which you are the owner.
3. Copy the ID from the url of your Google Sheets document and replace `SPREADSHEET_ID` inside `study.py` with it.
4. Create a GCP profile if you don't have one (it doesn't matter who owns the GCP account).
5. Create a new service account (this is a virtual GCP entity that sends requests on your behalf).
6. Write down the unique email address of that service account (something like yourserviceaccount@random-words-123456.iam.gserviceaccount.com) and share your Google Sheets document with that email (via the regular share button).
7. Generate a key for your service account ("Manage keys") and download it as a JSON file.
8. Convert that JSON into TOML (e.g. via the supplied convert.py script `python convert.py input.json secrets.toml`).
9. Insert `[gcp_service_account]` as first line in the toml file.
10. For local debugging, create a folder `.streamlit` and move `secrets.toml` in there. The `.gitignore` automatically ignores all .json and .toml files as well as the contents of that folder.
11. Go to https://share.streamlit.io/ and create a new app.
12. Connect streamlit with the GitHub account that owns the fork.
13. Enter the details of your forked repository.
14. Under 'Advanced Settings...', paste the contents of your `secrets.toml` file as secret.
15. Done! Your streamlit app will be deployed and you can simply share the link.
