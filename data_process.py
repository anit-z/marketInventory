import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'SimHei'


# The API endpoint for the POST request
url = "https://v1.cn-abs.com/ajax/ChartMarketHandler.ashx"

# Headers
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "v1.cn-abs.com",
    "Origin": "https://v1.cn-abs.com",
    "Referer": "https://v1.cn-abs.com/",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
}

# Payload for the POST request
payload = {    
    'type': 'marketInventory', # 市场产品累计存量金额统计
}


def fetch_data(url, headers, data):
    """
    Fetches data from the URL using a POST request.
    
    Args:
        url (str): The URL to which the POST request is made.
        headers (dict): Headers to include in the request.
        data (dict): Data to send in the body of the POST request.
        
    Returns:
        The response from the server.
    """
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        # Assuming the response's content is JSON, parse and return it.
        # If the response is in another format, this line will need to change.
        res = response.json()
        return res
    else:
        print("Failed to retrieve content, status code:", response.status_code)
        return None


def main(data):
    # Fetch and process data from the API
    response = fetch_data(url, headers, data)
    
    if response is not None:
        print("Response from server:", response)
        # Further processing can be done here depending on the structure of response
    return response


def data_parse(data):
    """
    Parses the given data and returns a dictionary containing the parsed information.
    
    Parameters:
        data (list): A list of dictionaries containing the data to be parsed.
        
    Returns:
        dict: A dictionary containing the parsed information. 
    """
    res = {}
    for item in data:
        # print(item)
        type = item['SeriesName']
        # print('type: ', type)
        type_data = []
        points = item['Points']
        # print('points: ', points)
        for point in points:
            year = point['X']
            value = point['Y']
            # print('year: ', year)
            # print('value: ', value)
            type_data.append({'year': year, 'value': value})
        res[type] = type_data
        
    return res


def data2df(data):
    """
    Convert data to a DataFrame.

    Args:
        data (dict): A dictionary containing the data.

    Returns:
        pandas.DataFrame: The DataFrame containing the converted data.
    """
    # Converting data to DataFrame
    # First, create a list of dictionaries, which will be rows for the DataFrame
    rows_list = []

    # Iterate over each category in the data dictionary
    for category, values in data.items():
        # Iterate over each data point in the values list
        for entry in values:
            # Create a dictionary for each year with the category as an additional key
            row = {'Year': entry['year'], category: entry['value']}
            rows_list.append(row)

    # Create a DataFrame from the list of dictionaries
    df_financial = pd.DataFrame(rows_list)

    # Since each row is treated as a separate entity, we need to group by Year and aggregate the results
    df_financial = df_financial.groupby('Year').aggregate('sum').reset_index()
    
    return df_financial


def save_to_csv(df, fileName):
    """
    Save DataFrame to CSV file.

    Parameters:
    - df (DataFrame): The DataFrame to be saved.

    Returns:
    - None
    """
    # Save DataFrame to CSV file
    df.to_csv('./data/{}.csv'.format(fileName))


def visualization(df):
    """
    Visualizes the data in a line plot.

    Parameters:
    - df: The data to be visualized.

    Returns:
    None
    """
    # Visualizing the data
    # Convert data to DataFrame and visualize
    plt.figure(figsize=(15, 8))

    # Plot each category
    for category in data.keys():
        plt.plot(df['Year'], df[category], label=category, marker='o')

    plt.title('Statistics of accumulated stock amount of market products')
    plt.xlabel('Year')
    plt.ylabel('Value (in billions)')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    payload = {    
        'type': 'marketInventory', # 市场产品累计存量金额统计
    }
    data = main(data=payload)
    print(data)

    data = data_parse(data)
    print(data)

    df = data2df(data)
    print(df)

    visualization(df)

    file_name = 'market_inventory'
    save_to_csv(df, file_name)