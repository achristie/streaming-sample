import requests

def get_token(username, password, apikey):
  """Get an Access Token to make API calls with."""
  body = {
    "username": username,
    "password": password
  }
  headers = {
    "appkey": apikey
  }
  try:
    r = requests.post("https://api.platts.com/auth/api", data=body, headers=headers)
    r.raise_for_status()
    return r.json()["access_token"]
  except Exception as err:
    if r.status_code >= 500:
      print(err)
    else:
      print(r.status_code, r.json())