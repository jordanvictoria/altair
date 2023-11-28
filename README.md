# Altair Python Developer – Code Exam 1

### Objective
The objective of this technical assessment was to create a Python script that asynchronously pulls data for three different countries from the RESTCountries API, returning the currency, capital, and alternate spellings for each country. In addition to meeting the core requirements, I also implemented unit and integration testing to ensure reliability of the script.

### Approach

1. **Virtual Environment Setup:**
   - The project is set up within a virtual environment using Python 3.9 to ensure a clean and isolated development environment.

2. **Dependency Management:**
   - The `requirements.txt` file is provided, listing the necessary packages installed via pip, including `aiohttp` and `asyncio` for asynchronous interaction.

3. **Asynchronous Interaction:**
   - Asynchronous interaction with the RESTCountries API is achieved using the `aiohttp` and `asyncio` Python libraries.

4. **Error Handling:**
   - Errors, such as network errors or API request errors, are handled gracefully to ensure robustness.

5. **Logging:**
   - Logging is implemented using the `logging` library to capture and log relevant information during script execution.

6. **Code Organization:**
   - The code is organized into functions for better readability and maintainability, following best practices.

7. **Data Extraction and Output:**
   - Information for each country, including Country Name, Currency, Capital, and Alternate Spellings, is extracted and printed.
   - The extracted data is then written to a CSV file named `country_info.csv`.

8. **Testing:**
   - Both unit tests and integration tests have been added to ensure the correctness and reliability of the script.
   - To run unit tests: `python -m unittest tests.unit_tests`
   - To run integration tests: `python -m unittest tests.integration_tests`

9. **Additional Considerations:**
   - Proper asynchronous handling using `asyncio` and `aiohttp` libraries is implemented.
   - The script is designed to be modular, with functions like `fetch_and_process_country`, `print_country_info`, and `write_to_csv` for clarity and reusability.

### Usage
To run the script, execute the `main` function by running the script directly. Ensure the virtual environment is activated, and dependencies are installed as per the `requirements.txt`. To run unit tests: `python -m unittest tests.unit_tests`. To run integration tests: `python -m unittest tests.integration_tests`.
