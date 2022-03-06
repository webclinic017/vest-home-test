# vest-test-home

This repository was created to evaluate the level of programming

### Dependencies
  - python 3.10
  - pipenv
  - docker-componse


### Installation

Install the dependencies:
```
pipenv install
docker-compose up -d
```

### Run

```
pipenv run server
```

### Example usage

Make a POST /nasdaq/trade

Example:
```
{
  "action": "buy" || "sell",
  "symbol": "AAPL",
  "shares": 5
}
```

Make a POST /nasdaq/list-stock

Example:
```
{
  "symbol": "AAPL"
}
```

Make a POST /nasdaq/list-stock

Example:
```
{
  "symbol": "AAPL"
  "dateFrom": "YYYY-MM-DD", | optional
  "dateTo": "YYYY-MM-DD", | optional
}
```