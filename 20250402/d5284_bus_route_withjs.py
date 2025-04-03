import requests
import html
import pandas as pd
import re
from playwright.sync_api import sync_playwright

class BusRoute:
    def __init__(self, rid):
        self.rid = rid
        self.content = None
        self.url = f'https://pda5284.gov.taipei/MQS/route.jsp?rid={rid}'
        self._fetch_content()

    def _fetch_content(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.url)
            page.wait_for_timeout(1000)  # wait for 1 second
            self.content = page.content()
            browser.close()

        # Write the rendered HTML to a file route_{rid}.html
        with open(f"data/bus_route_{self.rid}.html", "w", encoding="utf-8") as file:
            file.write(self.content)

    def timetable(self, direction):
        if direction not in ["ttego", "tteback"]:
            raise ValueError("Direction must be 'ttego' or 'tteback'")

        pattern = (
            rf'<tr class="{direction}[12]">.*?'
            rf'<td><a href="stop\.jsp\?sid=(\d+)">(.*?)</a></td>'
            rf'<td[^>]*>(.*?)</td>.*?</tr>'
        )

        matches = re.findall(pattern, self.content, re.DOTALL)

        if not matches:
            raise ValueError(f"No data found for direction {direction} and route ID {self.rid}")

        bus_routes = []
        for m in matches:
            bus_routes.append(m)

        #write the bus route data to a CSV file
        with open(f"data/bus_route_{self.rid}_{direction}.csv", "w", encoding="utf-8") as file:
            for route in bus_routes:
                file.write(",".join(route) + "\n")

        dataframe = pd.DataFrame(bus_routes, columns=["stop_id", "stop_name", "arrival_info"])
        setattr(self, f"timetable_{direction}", dataframe)  
        
        for _, row in dataframe.iterrows():
            arrival_info = row['arrival_info']
            # Check for valid arrival info format
            info_list = str(self.check_arrival_info(arrival_info))
            dataframe.at[_, 'arrival_info'] = info_list

        return dataframe        

    def check_arrival_info(self, arrival_info):
        # arrival_info has the following format pattern:
            # 未發車<br><img border="0" src="bus1.gif"><font style="color:darkblue;">679-U5</font>
            # 6分<br><img border="0" src="bus1.gif"><font style="color:darkblue;">648-U5</font>
            # bus_stop_status = ['進站中','未發車','交管不停','末班已過','今日未營運']
        #status_map = {'進站中': int(0), '未發車': int(-1), '交管不停': int(-2), '末班已過': int(-3), '今日未營運': int(-4)}
 
        #split the arrival_info string into parts by '<br>'
        arrival_info_parts = arrival_info.split('<br>')

        # Updated regex pattern to match all specified arrival_info types
        pattern_elem1 = r'^[(?:將到站)|(?:未發車)|(?:進站中)|(?:交管不停)|(?:末班已過)|(?:今日未營運)|(?:\d+分)]'
        pattern_elem2 = r'^<img border="0" src="bus1\.gif"><font style="color:darkblue;">(.*?)</font>$'

        info_list = []
        for info in arrival_info_parts:
            # Check if the info matches one of the specified arrival_info types
            match1 = re.search(pattern_elem1, info)
            match2 = re.search(pattern_elem2, info)
            if match1 and not match2:
                info_p = info
            elif not match1 and match2:
                info_p = match2.group(1)
            else:
                info_p = None
            info_list.append(info_p)
        
        return info_list
    

# Test class
if __name__ == "__main__":
    rid = "10417"  # Test route ID
    try:
        bus_route = BusRoute(rid)
        go_df = bus_route.timetable("ttego")
        back_df = bus_route.timetable("tteback")

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

