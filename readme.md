# Platts Streaming Examples

## eWindow Market Data

This example shows how to connect to the Platts eWindow Market Data Streaming API for a set of `--markets` and save the results to a local database.

| Parameter      | Description                                                                                     |
| :------------- | :---------------------------------------------------------------------------------------------- |
| -a, --apikey   | Your eWindow API Key. **Required**                                                              |
| -u, --username | Your Platts Username. **Required**                                                              |
| -p, --password | Your Platts Password. **Required**                                                              |
| -m, --markets  | The markets you wish to subscribe to. Comma-delimited string: `"EU BFOE, EU MTBE"` **Required** |

### Getting Started

```python
pip install asyncio requests websockets
python main.py -a {APIKEY} -u {USERNAME} -p {PASSWORD} -m "EU BFOE, EU MTBE"
```

You will see logs in the log.log file. Any Bids, Order, or Trades that come in will be saved to the `ewmd` table in `database.db`.

```sql
sqlite3 database.db
SELECT * FROM ewmd
LIMIT 20;
```
