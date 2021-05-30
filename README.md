
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt.

```bash
pip install -r requirements.txt
```

## How to start flask server

```bash
cd app
python main.py
```

## Working with APIs

### Insert Data to Pools API

Receives a JSON in the form of a document with two fields: a pool-id (numeric) and a pool-values (array of values) and is meant to append (if pool already exists) or insert (new pool) the values to the appropriate pool (as per the id)

- **Method:** POST
- URL Params

```
http://<host>/pools
```
- **Required**
  - poolId
  - poolValues

Ex:
```
        {
            "poolId": 123546,
            "poolValues": [
                1,
                7,
                2,
                6
            ]
        }
```

- **Schemas**
  - poolId: Int
  - poolValues: Array(Number)
- Success Response:
  - Code: 200
  - Content:
    - appended: appended exsited pool(key = poolId)
    - inserted: when add new pool

Ex:
```
{
    "status": "appended"
}
```

### Get quantile API

query a pool, the two fields are pool-id (numeric) identifying the queried pool, and a quantile (in percentile form), return a quantile of pool and total number of elements in the pool.

- **Method:** POST
- URL Params

```
http://<host>/get_quantile
```
- **Required**
  - poolId
  - percentile

Ex:
```
        {
            "poolId": 123546,
            "percentile": 80
        }
```

- **Schemas**
  - poolId: Int
  - percentile: Number(0~100)
- Success Response:
  - Code: 200
  - Content:
    - total_number_elements: total elements on the pool
    - quantile: 6
    - quantile is lower value between two data points i < j(which is same as numpy.quantile as param interpolation='lower')

Ex:
```
{
    "total_number_elements": 3,
    "quantile": 6
}
```
