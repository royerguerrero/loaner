# MO Backend Technical Test

## Introduction
MO Loans is a API for handle and supervise customer's loans and payments.

### Entity-relationship model
```mermaid
erDiagram
    loans {
        integer id
        timestamp created_at
        timestamp updated_at
        varchar external_id
        numeric amount
        smallint status
        varchar contract_version
        timestamp maximum_payment_date
        timestamp taken_at
        integer customer_id
        numeric outstanding
    }
    customers {
        integer id
        timestamp created_at
        timestamp updated_at
        varchar external_id
        smallint status
        numeric score
        timestamp preapproved_at
    }
    payments {
        integer id
        timestamp created_at
        timestamp updated_at
        varchar external_id
        numeric total_amount
        smallint status
        timestamp paid_at
        integer customer_id
    }
    payment_details {
        integer id
        timestamp created_at
        timestamp updated_at
        numeric amount
        integer loan_id
        integer payment_id
    }

    loans ||--o{ customers: "customer_id"
    loans ||--|{ payment_details: "loan_id"
    customers ||--o{ payments: "customer_id"
    payments ||--|{ payment_details: "payment_id"
```

## How run the project in development
You have 2 options to run the project:
- Using Docker
- Using your local machine

### Using Docker

### Using your local machine

## How aport to the project
- Use conventional commits. [Learn it. here](https://www.conventionalcommits.org/en/v1.0.0/#summary)
- Use Ship / Show / Ask [Learn it. here](https://martinfowler.com/articles/ship-show-ask.html)
- Use PEP8 for Python code.

### Endpoints
- GET: /api/customers/
- POST: /api/customers/
- POST: /api/customers/bulk
- GET: /api/customers/balance
- GET: /api/customers/{customer_id}/loans
- GET: /api/customers/{customer_id}/payments
- POST: /api/loans
- GET: /api/loans
- POST: /api/payments
- GET: /api/payments
