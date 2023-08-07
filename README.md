# DMARC Record Checker

This application is built using the Dash framework and allows users to verify the DMARC records of a domain. If a domain doesn't have a DMARC record, it will be added to a list of domains without DMARC.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Python Installation**: Ensure you have Python installed on your machine.
2. **Clone the Repository**: git clone https://github.com/CorentinBzi/DMARC-Record-Checker.git
3. **Install Required Packages**:
Navigate to the project directory and install the necessary packages: pip install dash dash-bootstrap-components pandas dnspython

## Usage

1. **Run the Application**: python DMARC_records_checker.py
2. **Access the Application**:
Open a web browser and navigate to: http://127.0.0.1:8050/

## Features

- **Domain Input**: Users can input the domain they wish to check.
- **DMARC Verification**: By clicking the "Vérifier" button, the application will check the DMARC record of the provided domain.
- **List of Domains without DMARC**: Domains without a DMARC record will be displayed in a table.

## Contributing

Pull requests are welcome. For significant changes, please open an issue first to discuss the desired changes.

## License

This project is licensed under the MIT License. Please refer to the `LICENSE` file for more details.
