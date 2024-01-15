# Church Billionaire Sacco Management

## Introduction

This CBS application is designed for managing the members, beneficiaries, monthly savings, loan applications, and loan payments of the Church Billionaire Sacco. 
The application aims to streamline the Sacco's operations and enhance efficiency in managing member details, savings, and loan-related transactions.

## Features

### Members

1. First Name
2. Last Name
3. Middle Name
4. Phone Number
5. Address [Country, City, Region]
6. Email
7. CBS Number
8. Date of Birth
9. Gender
10. NIN (National Identification Number)
11. Membership status {Submitted, Registered, Active}

### Beneficiaries

1. Member
2. First Name
3. Middle Name
4. Last Name
5. Phone Number
6. Relationship
7. Percentage

### Monthly Savings

1. Member
2. Paid for
3. Amount
4. Amount in Words
5. Year
6. Date of Payment

### Loans Applications

1. Member
2. Amount
3. Total Interest
4. Payment Period
5. Payment Start Date
6. Referees (List of fellow Members) (Condition: Referee should not have a loan)

### Loan Payments

1. Member
2. Loan Amount
3. Amount Paid against the loan
4. Auto Compute the Interest
5. Loan Balance

## Installation

To install and configure the Church Billionaire Sacco Management application, follow the steps below:

1. Clone this repository to your folder.

    ```bash
    git clone https://github.com/your_username/sacco-management.git
    ```

2. Install the required dependencies.

    ```bash
    pip install -r requirements.txt
    ```

3. Start your CBS application

    ```bash
    odoo-bin -c odoo.conf
    ```

4. Access the CBS application through your web browser and install the module.

## Usage

1. Log in to your CBS application instance.

2. Navigate to the Sacco Management module.

3. Add Members, Beneficiaries, Record Monthly Savings, Submit Loan Applications, and Manage Loan Payments.

4. Enjoy the streamlined Sacco management process!

## License

This Church Billionaire Sacco Management application is open-source software licensed under the [MIT License](LICENSE).