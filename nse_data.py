
import json
from datetime import datetime, time
from time import sleep

import pandas as pd
import pytz
import requests
import streamlit as st

# def get_nse_data():
#     max_retries = 3
#     retry = 0

#     while retry < max_retries:
#         try:
#             nse_url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
#             headers = {'User-Agent': 'Mozilla/5.0'}
#             page = requests.get(nse_url,headers=headers)
#             page_data = json.loads(page.text)
#             return page_data
#         except:
#             st.warning("Retrying, please wait")
#             sleep(5)
#             retry += 1
#     return None

IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(IST).time()
begin_time = time(9, 10)
end_time = time(21, 40)

if current_time >= begin_time and current_time <= end_time:

    nse_url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(nse_url, headers=headers)

    try:
        nse_data = json.loads(page.text)
    except:
        nse_data = None

    if nse_data:

        expiry_date = nse_data['records']['expiryDates'][0]

        pe_values = [data['PE'] for data in nse_data['records']['data']
                     if 'PE' in data and data['PE']['expiryDate'] == expiry_date]
        PE_df = pd.DataFrame(pe_values).sort_values(['strikePrice'])

        timestamp = nse_data['records']['timestamp']

        pe_max_index_oi = PE_df["openInterest"].idxmax()
        PE_MAX_OI = PE_df["strikePrice"][pe_max_index_oi]

        pe_max_index_change_oi = PE_df["changeinOpenInterest"].idxmax()
        PE_MAX_CHANGE_OI = PE_df["strikePrice"][pe_max_index_change_oi]

        PE_CIOI_VOL = PE_df["changeinOpenInterest"][pe_max_index_change_oi]
        PE_VOLUME = PE_df["totalTradedVolume"][pe_max_index_change_oi]

        ce_values = [data['CE'] for data in nse_data['records']['data']
                     if 'CE' in data and data['CE']['expiryDate'] == "10-Jun-2021"]
        CE_df = pd.DataFrame(ce_values).sort_values(['strikePrice'])

        ce_max_index_oi = CE_df["openInterest"].idxmax()
        CE_MAX_OI = CE_df["strikePrice"][ce_max_index_oi]

        ce_max_index_change_oi = CE_df["changeinOpenInterest"].idxmax()
        CE_MAX_CHANGE_OI = CE_df["strikePrice"][ce_max_index_change_oi]

        CE_CIOI_VOL = CE_df["changeinOpenInterest"][ce_max_index_change_oi]
        CE_VOLUME = CE_df["totalTradedVolume"][ce_max_index_change_oi]

        if PE_MAX_OI > CE_MAX_OI:
            MAX_OI_TREND = "BULLISH"
        elif PE_MAX_OI < CE_MAX_OI:
            MAX_OI_TREND = "BEARISH"
        else:
            MAX_OI_TREND = ""

        if PE_MAX_CHANGE_OI > CE_MAX_CHANGE_OI:
            MAX_CHANGE_OI_TREND = "BULLISH"
        elif PE_MAX_CHANGE_OI < CE_MAX_CHANGE_OI:
            MAX_CHANGE_OI_TREND = "BEARISH"
        else:
            MAX_CHANGE_OI_TREND = ""

        if PE_CIOI_VOL > CE_CIOI_VOL:
            CIOI_VOL_TREND = "BULLISH"
        elif PE_CIOI_VOL < CE_CIOI_VOL:
            CIOI_VOL_TREND = "BEARISH"
        else:
            CIOI_VOL_TREND = ""

        if (CIOI_VOL_TREND == "BEARISH" and PE_VOLUME > PE_CIOI_VOL):
            VOL_TREND = "STRONG BEARISH"
        elif (CIOI_VOL_TREND == "BULLISH" and CE_VOLUME > CE_CIOI_VOL):
            VOL_TREND = "STRONG BULLISH"
        else:
            VOL_TREND = ""

        table_data = {'PE': [PE_MAX_OI, PE_MAX_CHANGE_OI, PE_CIOI_VOL, PE_VOLUME],
                      'CE': [CE_MAX_OI, CE_MAX_CHANGE_OI, CE_CIOI_VOL, CE_VOLUME],
                      'TREND': [MAX_OI_TREND, MAX_CHANGE_OI_TREND, CIOI_VOL_TREND, VOL_TREND]}

        table_df = pd.DataFrame(table_data, index=['MAX OI',
                                                   'CHANGE IN OI',
                                                   'CIOI VOLUME',
                                                   'VOLUME'])

        st.subheader("Expiry : {}".format(expiry_date))
        st.subheader("Data Updated at {}".format(timestamp))
        st.table(table_df)

        sleep(60)

    else:
        st.error(
            "Some error occured while fetching the data. Refreshing in 30 seconds...")
        sleep(30)

    st.experimental_rerun()

else:
    st.title("NSE Options Strategy")
    st.subheader("App will display the data only from 9:10 AM to 3:40 PM")

