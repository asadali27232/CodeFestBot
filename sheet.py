import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1F7tkHoNZGOH7B9KGyaVf33n56_ErB15r1VyAOhXUTx0"
SAMPLE_RANGE_NAME = "Emails!A:C"


def get():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
            .execute()
        )
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return
    except HttpError as err:
        print(err)

    return values


def post(row, value):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """

    if type(row) != int:
        print("Not a valid row number!")
        return
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        UPDATE_RANGE = f"Emails!C{row}:C{row}"

        body = {'values': [[value]]}
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                  range=UPDATE_RANGE, body=body, valueInputOption="RAW")
            .execute()
        )

        print(f"Row {row} updated with {value}!")
    except HttpError as err:
        print(err)


if __name__ == "__main__":
    values = get()

    for row in values:
        if row[0] == "Name" and row[1] == "Email":
            pass
        else:
            # Print columns A and E, which correspond to indices 0 and 4.
            print(f"{row[0]}, {row[1]}")
