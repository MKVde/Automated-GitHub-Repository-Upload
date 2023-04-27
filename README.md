# Automated-GitHub-Repository-Upload

The GitHub Uploader is a Python script that allows users to upload files to a GitHub repository using a graphical user interface. This script was built using PyQt5, a Python library for creating desktop applications, and the GitHub API.


## Requirements

The GitHub Uploader requires the following:

* Python 3.x
* PyQt5
* requests


## Usage/Examples

To use the GitHub Uploader, follow these steps:

1. Clone or download the GitHub Uploader repository to your local machine.

2. Install the required Python libraries using pip. To install PyQt5 and requests, run the following command:

```
pip install PyQt5 requests
```
3. Open the **Automated-GitHub-Repository-Upload.py** file using a Python IDE or text editor.

4. Run the script to launch the GitHub Uploader GUI.

5. Fill out the following fields:

* GitHub Repository Name: The name of the GitHub repository you want to upload your files to.
* GitHub Username: Your GitHub username.
* Token: Your personal access token for GitHub. You can create a new token by following these [instructions](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

6. Click the Select Folder button to choose the folder that contains the files you want to upload.

7. Click the Upload button to upload your files to GitHub.



## Documentation

The GitHub Uploader GUI has the following components:

* **GitHub Repository Name:** A label and text input field for the name of the GitHub repository you want to upload your files to.
* **GitHub Username:** A label and text input field for your GitHub username.
* **Token:** A label and text input field for your personal access token for GitHub.
* **Select Folder:** A button that allows you to select the folder that contains the files you want to upload.
* **Selected Folder:** A label and text input field that displays the path to the selected folder.
* **Progress Bar:** A progress bar that shows the progress of the upload.
* **Repository Status:** A label that displays the status of the repository, such as whether it was created or updated.
* **Upload:** A button that uploads your files to GitHub.
* **Exit:** A button that closes the GitHub Uploader GUI.


## Contributions

Contributions are welcome! If you find any bugs or issues with the script, please feel free to create an issue or pull request.


## License

This script is licensed under the [**MIT**](https://choosealicense.com/licenses/mit/) License. See the LICENSE file for more information.




