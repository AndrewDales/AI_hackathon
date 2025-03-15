from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import json
import os

# Google Sheet details
#You can get the google sheet ID from the url of your google sheet.  It looks something like this:1Hg1fvyvqoSDgN1T8AAt89o28_q-LlsuyjiNKXOborHw
#Provide this as SHEET_ID in the function call.

# Path to save service account JSON key file
SERVICE_ACCOUNT_FILE = "serviceAccountCreds.json"

# save credentials file if does not exist already
if not os.path.exists(SERVICE_ACCOUNT_FILE):
    credentials = {
        "type": "service_account",
        "project_id": "hackathon-452517",
        "private_key_id": "8ba0ac85f25819f648624824f21c529e2f462617",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQClS/uAoVJWsBCc\nR4oGf0ezT7m7VfiZV12zM16w6529CesZiA/0MWk+s0fhbBpGkioTFeInQzbcB0Y7\nhZmunkQSgNu1ESmZSA3gui3Qe1MU2kAxn936Ug2gKRSqso5n8cveK1OOmd/DTOCa\nVTLhyPEukq9i/Ucc0xWSzhnWQ+y4bu4m+0hRwuUM4Cnt1aATFQGnPvqxbY0t1iSC\n0V79fl3kmKGWLm/yrf5avAlE0hpoQfcmjc9vOIq7ALSxEhJL/t5WvhMlrYPlA8FU\nJU2DpPD1NWWtRqxEioNej/RyzFVtR6x3jx4AWO7jdPpLD9VjsrkFh+8PgHWyvwMs\nzh6sYpP1AgMBAAECggEAJhnQx8pHmqw8M+2ogs1hV1Nb7jLHmf7hnf4MCE9THWEV\nJB4xATpHdlioS61ZlCU6VgpgBelQEqEJnwwxS6b27WXu3rptQoPxkPiROWJH2QFi\ntR2SstGpit6VQTBls09wjM4jVTYiNhf5GJHlZ9Zjw3azvyc+9kWwjhV8Lp+bB7rI\n4U/8QngxgWkPdMTZFvboQ35nONqoYvpr5eT2F1tHrPGcLZTNrIr5oygL9sPEkOOI\nxjHKHgpilOzjPARQRfKQ4FKbjYSNF2b/Af1mM/ak1zcBtaD7a5dzGrwC8bEWHYW6\nA0gkrAaviNsT+dlXvm0xJqoJWrrPfnu3+BD2CEf7CQKBgQDh+c6ahfiUElkhm93c\nN8JoeGZfXO9OcF2TWlWK8G+HshF3qftF50HW4cw0pVGoVO1bKfSctp74n8NKpLUv\n1eVWOBNqHE/WG+pOeknqFZqm8we5MiUf/BPXB/w+XwljapWyx5GSUCulDtTB1kCX\nFEXMZqMW0fso0UYtKaf7tSWGXQKBgQC7QkeTgiQbw7MkgVzGCrJukocQfHfRd0kX\n2DbSZ/HlQ2xUuOyFqjj5/4YaTWQyzXh3Mz75JdZ6pIzrvyc2xlyXrtPgaWwBYCW/\nyfeEO3ycMY4oC4aZknwCEFb4tCKpxhAXkpxcnKCMw8qtzfBtdJhCfvRvbev1jdUi\n+Hg0BLk6eQKBgC2R0rgWjCpQCOleJT9jfzDSFtLkSt3mivhMHzQFiHg00JDxFlri\nZ8SNhECZlf38ImFf9JQlv6kjjp5e2Krs13KrnD6ptu/WcUmiH4W1FZrVJ5mRIytw\nChAy7Asn3xzNQaLr289Fm4eNlhoAusW8sNanW/weHCf/C8fPvrBjt02BAoGAKGHZ\nt6jICqjAWC4BiL/DzO6Sa+67lBNqUtcQs30xACTzFq4ua4DS+q6tB70Kz53ZzbLi\ncK5FO3uC3FADr99FFnzgOjPh08YdPefbFcwSSkixhFc/9pxNW9CUQNvv4bbRv5Oh\nXqN0SAbtDWAs6h3LvANOyTzmNrUYcossuOMP4tkCgYEAwO3H9DbqSYBrl+Fd2g21\nRhtOLua7q6bn1A2KIYKAcU87wj9Ui0b1p77d28Sewa4wNB5PFqmtG0v1Te5hkK6Y\ntFbu+TcNJn5khTIhSL3GiXoiocx7u7vK9Nb32ZJvyvxfEdQ2vusJMW9QXLzxCXsQ\nFlUgliR4p6dxBbqJV5wxIB4=\n-----END PRIVATE KEY-----\n",
        "client_email": "hackathon1@hackathon-452517.iam.gserviceaccount.com",
        "client_id": "108263797441224198143",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/hackathon1%40hackathon-452517.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }

    with open(SERVICE_ACCOUNT_FILE, 'w') as f:
        json.dump(credentials, f)

# Authenticate and build service
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE,
                                              scopes=["https://www.googleapis.com/auth/spreadsheets"])
service = build("sheets", "v4", credentials=creds)


def googleSheetRead(RANGE="Sheet1!A2:A10", SHEET_ID = "get_sheet_ID_from_web_URL"):
    # Read a cell / range
    request = service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=RANGE)
    response = request.execute()
    data = response.get("values", [])
    for row in data:
        print(row)  # Each row is a list of values
    return (data)


def googleSheetWrite(CELL="Sheet1!A2", VALUE="hello world", SHEET_ID = "get_sheet_ID_from_web_URL"):
    # Update a cell
    request = service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID,
        range=CELL,
        valueInputOption="RAW",
        body={"values": [[VALUE]]}
    )
    response = request.execute()
    print("Updated Cell:", response)
    return (response)


def googleSheetClear(RANGE="Sheet1!A1:B10", SHEET_ID = "get_sheet_ID_from_web_URL"):
    # Clear a range
    service.spreadsheets().values().clear(
        spreadsheetId=SHEET_ID,
        range=RANGE,
        body={}
    ).execute()


if __name__ == "__main__":
    data = googleSheetWrite(CELL="Sheet1!A3", VALUE="I am cell A3")
    more_data = googleSheetWrite(CELL="Sheet1!A5", VALUE="Test, testing, testing!")
    response = googleSheetRead(RANGE="Sheet1!A1:A10")


