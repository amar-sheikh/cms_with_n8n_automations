# cms_with_n8n_automations

## How to run?
### Configure environment
    $ python3 -m venv env
    $ source env/bin/activate
### Install necessary packages
    $ pip install -r requirements.txt
### Start the project
    $ python3 manage.py runserver

## n8n Workflow 1: File Upload and Google Drive Integration

This workflow automates file handling in the application via n8n. It is triggered through a webhook upon file upload and performs the following steps:

- **Trigger**: Activated by an incoming HTTP request containing the uploaded file.
- **Upload to Google Drive**: The file is uploaded to **Google Drive (free tier)** using the Google Drive API.
- **Return Metadata**: After successful upload, the workflow returns:
  - `fileId`: The unique ID of the uploaded file in Google Drive.
  - `thumbnailUrl`: A preview URL for displaying the uploaded file.
- **Database Update**: The `fileId` and `thumbnailUrl` are saved to the database for later retrieval and display.
- **Old File Cleanup**: If an `oldFileId` is provided in the request, the workflow deletes the corresponding file from Google Drive to manage storage and prevent duplication.

### Benefits:
- Simplifies external file storage management.
- Keeps the database in sync with Google Drive.
- Automates cleanup of outdated files.

### Video
