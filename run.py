from trail_anonymizer import TrailAnonymizer

if __name__ == "__main__":
    trail_anonymizer = TrailAnonymizer()

    # Entities can be taken from: https://microsoft.github.io/presidio/supported_entities/

    trail_anonymizer.run(
        "mock_data/fake_pii_excel.xlsx",
        # columns_to_anonymize=["Email", "Phone Number", "Social Security Number", "Credit Card Number"],
        entities=["CREDIT_CARD", "EMAIL_ADDRESS", "US_SSN"],
    )
