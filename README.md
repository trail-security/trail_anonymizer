Trail Security Anonymizer
-------------------------------------

TrailSecurityAnonymizer is a Python script designed to anonymize sensitive information within CSV and Excel files.
Using the Presidio library, it identifies and anonymizes specified entities such as email addresses, credit card numbers, social security numbers and more.
The anonymized data is then saved to new files, ensuring privacy and security.

Features
-------------------------------------
- Anonymization: Detects and anonymizes sensitive entities in CSV and Excel files.
- Customizable: Allows specifying which columns and entities to anonymize.
  - Full list of entities can be found [here](https://microsoft.github.io/presidio/supported_entities/)
- Logging: Provides detailed logging of the anonymization process.


Installation
-----
### Option A
Before running the script, ensure that the following Python packages are installed:

- presidio_analyzer
- presidio_anonymizer
- pandas
- openpyxl
- XlsxWriter

```bash
pip install presidio_analyzer presidio_anonymizer pandas openpyxl XlsxWriter
python -m spacy download en_core_web_lg
```

### Option B

Using the `requirements.txt` - [install packages in a virtual environment using pip and venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/):

#### Create a new virtual environment
To create a virtual environment, go to your project’s directory and run the following command. This will create a new virtual environment in a local folder named .venv:
```bash
python3 -m venv .venv
```

#### Active a virtual environment
Before you can start installing or using packages in your virtual environment you’ll need to activate it. Activating a virtual environment will put the virtual environment-specific python and pip executables into your shell’s PATH.
```bash
source .venv/bin/activate
```

#### Prepare pip
pip is the reference Python package manager. It’s used to install and update packages into a virtual environment.
```bash
python3 -m pip install --upgrade pip
```

#### Using a requirements file
```bash
python3 -m pip install -r requirements.txt
```

Usage
-----
To run the anonymizer, create an instance of the TrailAnonymizer class and call the run method with the path to the file you want to anonymize. Optionally, specify the columns and entities to anonymize.


```python
if __name__ == "__main__":
    trail_anonymizer = TrailAnonymizer()
    trail_anonymizer.run("pii_excel_file.xlsx", entities=["CREDIT_CARD", "EMAIL_ADDRESS", "US_SSN"])
```

Parameters
- path: The path to the file to be anonymized. Supported formats are CSV and XLSX.
- columns_to_anonymize (optional): List of columns to anonymize. If not specified, all columns will be processed.
- entities (optional): List of entities to anonymize. Supported entities can be found [here](https://microsoft.github.io/presidio/supported_entities/). If not specified, all entities will be anonymized.