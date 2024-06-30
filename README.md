Trail Security Anonymizer
-------------------------------------

TrailSecurityAnonymizer is a package designed to anonymize sensitive information within CSV and Excel files.
Using the Presidio library, it identifies and anonymizes specified entities such as email addresses, credit card numbers, social security numbers and more.
The anonymized data is then saved to new files, ensuring privacy and security.

Features
-------------------------------------
- Anonymization: Detects and anonymizes sensitive entities in CSV and Excel files.
- Customizable: Allows specifying which columns and entities to anonymize.
  - Full list of entities can be found [here](https://microsoft.github.io/presidio/supported_entities/)
- Logging: Provides detailed logging of the anonymization process.


```python
if __name__ == "__main__":
    trail_anonymizer = TrailAnonymizer()
    trail_anonymizer.run("pii_excel_file.xlsx", entities=["CREDIT_CARD", "EMAIL_ADDRESS", "US_SSN"])
```

Parameters
- path: The path to the file to be anonymized. Supported formats are CSV and XLSX.
- columns_to_anonymize (optional): List of columns to anonymize. If not specified, all columns will be processed.
- entities (optional): List of entities to anonymize. Supported entities can be found [here](https://microsoft.github.io/presidio/supported_entities/). If not specified, all entities will be anonymized.
