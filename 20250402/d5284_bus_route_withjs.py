import requests
import html
import pandas as pd
import re
from playwright.sync_api import sync_playwright


def get_bus_route(rid):
    url = f'https://pda5284.gov.taipei/MQS/route.jsp?rid={rid}'
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        # Optionally wait for specific elements to load or use a timeout
        page.wait_for_timeout(1000)  # wait for 1 second
        content = page.content()
        browser.close()
    
    # Write the rendered HTML to a file route_{rid}.html
    with open(f"bus_route_{rid}.html", "w", encoding="utf-8") as file:
        file.write(content)

    # 定義以單一 <tr></tr> 為單位的 regex pattern，使用非貪婪模式匹配
    pattern = r'<tr class="ttego[12]">.*?<td><a href="stop\.jsp\?sid=(\d+)">(.*?)</a></td><td[^>]*>(.*?)</td>.*?</tr>'
    matches = re.findall(pattern, content, re.DOTALL)
    
    if not matches:
        raise ValueError(f"No go data found for route ID {rid}")
    # Extract the bus route information from the matches
    bus_routes = []
    for m in matches:
        # m is a tuple: (sid, stop name, arrival info)
        bus_routes.append(m)

    # Create a DataFrame from the bus route information with the new columns
    df_go = pd.DataFrame(bus_routes, columns=["Stop ID", "Stop Name", "Arrival Info"])

    pattern = r'<tr class="tteback[12]">.*?<td><a href="stop\.jsp\?sid=(\d+)">(.*?)</a></td><td[^>]*>(.*?)</td>.*?</tr>'
    matches = re.findall(pattern, content, re.DOTALL)
    if not matches:
        raise ValueError(f"No back data found for route ID {rid}")
    # Extract the bus route information from the matches
    bus_routes = []
    for m in matches:
        # m is a tuple: (sid, stop name, arrival info)
        bus_routes.append(m)
    # Create a DataFrame from the bus route information with the new columns
    df_back = pd.DataFrame(bus_routes, columns=["Stop ID", "Stop Name", "Arrival Info"])

    return df_go, df_back

# Test function
if __name__ == "__main__":
    rid = "10417"  # Test route ID
    try:
        go_df, back_df = get_bus_route(rid)

        print("Go DataFrame:")
        print(go_df)
        print("\nBack DataFrame:")
        print(back_df)
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    except IOError as e:
        print(f"File operation failed: {e}")
    except ValueError as e:
        print(f"Error: {e}")

