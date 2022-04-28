## UserStudy running as streamlit demo

If you want to host your own instance of this study, you need:
- a GCP profile (it doesn't matter who owns the GCP account)
- a service account crated with that profile
- a Google Sheets document that you have shared with the unique email address of that service account (something like yourserviceaccount@random-words-123456.iam.gserviceaccount.com), just like you would share it with a friend
- the json key of that service account that you have saved as `key.json` inside the main directory (you can download if from the keys section of the service account management in GCP)
