import requests
import logging

logger = logging.getLogger('external_requests')

def requests_wrapper(url, params=None, function_name="", headers=None, method="GET"):
    logger.info(f"Calling {method} URL: {url} | In: {function_name} | Params: {params} | Headers | {headers}")
    try:
        if method == "GET":
            response = requests.get(url=url, params=params, headers=headers)
        elif method == "POST":
            response = requests.post(url=url, params=params, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url=url, params=params, headers=headers)
        else:
            raise Exception(f"invalid method {method}")
        logger.info(f"Response from {url}: {response.status_code} | Body: {response.text[:500]}")
        return response.json()
    except Exception as e:
        logger.error(f"Failed to fetch from {url}: {e}")
        raise
