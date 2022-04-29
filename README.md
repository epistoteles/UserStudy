<h1 align="center">User Study Template Repository</h1>
<h4 align="center">Streamlit ♥️ Google Sheets</h4>

## About

This repository demonstrates how you can create a free & simple publicly hosted user study with streamlit that writes the results to a Google Sheets document. It is inspired by [this](https://github.com/streamlit/example-app-bug-report) streamlit bug tracker example. :)

Try out submitting answers here: https://share.streamlit.io/epistoteles/userstudy/main/study.py

And watch the results show up in this document (_Responses_): https://docs.google.com/spreadsheets/d/1S7YBK5AqAE9GPHdZEto9WTPGOyLHSBP5EgDTejlG8dU/edit#gid=1622526439

Besides the answers themselves the app currently logs a unique session ID per connection, a timestamp, and how long it took the user to respond.

## How to use

1. Fork this repository (the fork has to be public).
2. Create a copy of the Google Sheets document used in this repository of which you are the owner (File > Make a copy).
3. Create a csv file containing your samples and upload it to the _Database_ Google Sheet (File > Import > Upload > Replace current sheet). The `create_study_sample.py` file is only useful if you worked with me at Vector. :)
4. Copy the ID from the url of your Google Sheets document and replace `SPREADSHEET_ID` inside `study.py` with it.
5. Create a GCP profile if you don't have one (it doesn't matter who owns the GCP account).
6. Create a new service account (this is a virtual GCP entity that sends requests on your behalf).
7. Write down the unique email address of that service account (something like yourserviceaccount@random-words-123456.iam.gserviceaccount.com) and share your Google Sheets document with that email (via the regular share button).
8. Generate a key for your service account ("Manage keys") and download it as a JSON file.
9. Convert that JSON into TOML (e.g. via the supplied convert.py script `python convert.py input.json secrets.toml`).
10. Insert `[gcp_service_account]` as first line in the toml file.
11. For local debugging, create a folder `.streamlit` and move `secrets.toml` in there. The `.gitignore` automatically ignores all \*.json and \*.toml files as well as the contents of that folder.
12. Go to https://share.streamlit.io/ and create a new app.
13. Connect streamlit with the GitHub account that owns the fork.
14. Enter the details of your forked repository.
15. Under 'Advanced Settings...', paste the contents of your `secrets.toml` file as secret.
16. Done! Your streamlit app will be deployed and you can simply share the link.

## How to adapt

All assumptions about how the study works are included in the `study.py` file. This includes
- which fields/sliders there are
- how to pull and present the samples from the Google Sheet
- where to write the answers to

The code is sensitive to what columns are named in _Database_ and what names individual sheets have (_Database_, _Responses_).

Feel free to play around with the code in study.py and change it as you desire! :)
