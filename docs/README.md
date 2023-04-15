# Demo
> Using 3 diffrent payloads to create predictions. Used payloads can be found under `data` directory.


## Request 1

**Request:**
```sh
curl --location 'http://127.0.0.1:8080/api/v1/predict' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--data '{
    "age": 23,
    "gender": "MALE",
    "country_code": "EG",
    "city": "CAIRO",
    "seniority": 12,
    "segment": "INDIVIDUAL",
    "relationship_type": "FORMER CUSTOMER",
    "activity_level": "INACTIVE",
    "income": 12000
}'
```
**Response:**
```json
{
    "_links": {
        "details": "http://127.0.0.1:8080/api/v1/predict/01GY3B3WHMF7YZKBMTQ3N847MG"
    },
    "created_on": "2023-04-15 20:53:41.582035",
    "invocation_id": "01GY3B3WHMF7YZKBMTQ3N847MG",
    "invocation_status": "COMPLETED",
    "predictions": [
        "Current Accounts",
        "Pensions",
        "Direct Debit",
        "Payroll Account",
        "Payroll",
        "E-Account",
        "Credit Card"
    ],
    "updated_on": "2023-04-15 20:53:41.632030"
}
```

## Request 2

**Request:**
```sh
curl --location 'http://127.0.0.1:8080/api/v1/predict' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--data '{
    "age": 33,
    "gender": "FEMALE",
    "country_code": "ES",
    "city": "MADRID",
    "seniority": 36,
    "segment": "UNIVERSITY",
    "relationship_type": "ACTIVE",
    "activity_level": "ACTIVE",
    "income": 55000
}'
        }'
```
**Response:**
```json
{
    "_links": {
        "details": "http://127.0.0.1:8080/api/v1/predict/01GY3BW9XHYF5MNXN3EESD6WDJ"
    },
    "created_on": "2023-04-15 21:07:01.683809",
    "invocation_id": "01GY3BW9XHYF5MNXN3EESD6WDJ",
    "invocation_status": "COMPLETED",
    "predictions": [
        "Current Accounts",
        "Direct Debit",
        "Pensions",
        "Payroll",
        "Payroll Account",
        "Credit Card",
        "E-Account"
    ],
    "updated_on": "2023-04-15 21:07:01.731815"
}
```

## Request 3

**Request:**
```sh
curl --location 'http://127.0.0.1:8080/api/v1/predict' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--data '{
    "age": 58,
    "gender": "MALE",
    "country_code": "ES",
    "city": "MADRID",
    "seniority": 240,
    "segment": "VIP",
    "relationship_type": "ACTIVE",
    "activity_level": "ACTIVE",
    "income": 120000
}'
```
**Response:**
```json
{
    "_links": {
        "details": "http://127.0.0.1:8080/api/v1/predict/01GY3C1NY8Y00PX1H461DR596B"
    },
    "created_on": "2023-04-15 21:09:57.838365",
    "invocation_id": "01GY3C1NY8Y00PX1H461DR596B",
    "invocation_status": "COMPLETED",
    "predictions": [
        "Current Accounts",
        "Credit Card",
        "Long-term deposits",
        "Direct Debit",
        "Pensions",
        "E-Account",
        "Payroll"
    ],
    "updated_on": "2023-04-15 21:09:57.885364"
}
```