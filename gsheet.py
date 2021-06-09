from datetime import datetime, time
from time import sleep

import gspread
import pandas as pd
import pytz
from df2gspread import df2gspread as d2g
from nsepython import nsefetch
from oauth2client.service_account import ServiceAccountCredentials

# define the scope
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'nse-data-316020-8ac9539cefcf.json', scope)
# authorize the clientsheet
client = gspread.authorize(creds)
spreadsheet_key = '1Q2405Pk6GjDzMIwjkRT4uSHLyPnpFuKXocvnJhslMWY'
wks_name = 'NIFTY'


IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(IST).time()
begin_time = time(9, 10)
end_time = time(15, 40)

while True:
    if current_time >= begin_time and current_time <= end_time:

        try:
            nifty_data = nsefetch(
                'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY')
            banknifty_data = nsefetch(
                'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY')
        except:
            nifty_data = None
            nifty_data = None

        if nifty_data and nifty_data:

            expiry_date = nifty_data['records']['expiryDates'][0]

            pe_values = [data['PE'] for data in nifty_data['records']['data']
                         if 'PE' in data and data['PE']['expiryDate'] == expiry_date]
            PE_df = pd.DataFrame(pe_values).sort_values(['strikePrice'])

            timestamp = nifty_data['records']['timestamp']

            pe_max_index_oi = PE_df["openInterest"].idxmax()
            PE_MAX_OI = PE_df["strikePrice"][pe_max_index_oi]

            pe_max_index_change_oi = PE_df["changeinOpenInterest"].idxmax()
            PE_MAX_CHANGE_OI = PE_df["strikePrice"][pe_max_index_change_oi]

            PE_CIOI_VOL = PE_df["changeinOpenInterest"][pe_max_index_change_oi]
            PE_VOLUME = PE_df["totalTradedVolume"][pe_max_index_change_oi]

            ce_values = [data['CE'] for data in nifty_data['records']['data']
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
                          'TREND': [MAX_OI_TREND, MAX_CHANGE_OI_TREND, CIOI_VOL_TREND, VOL_TREND],
                          'Timestamp': timestamp}

            nifty_table_df = pd.DataFrame(table_data, index=['MAX OI',
                                                             'CHANGE IN OI',
                                                             'CIOI VOLUME',
                                                             'VOLUME'])

            # Bank Nifty

            pe_values = [data['PE'] for data in nifty_data['records']['data']
                         if 'PE' in data and data['PE']['expiryDate'] == expiry_date]
            PE_df = pd.DataFrame(pe_values).sort_values(['strikePrice'])

            timestamp = nifty_data['records']['timestamp']

            pe_max_index_oi = PE_df["openInterest"].idxmax()
            PE_MAX_OI = PE_df["strikePrice"][pe_max_index_oi]

            pe_max_index_change_oi = PE_df["changeinOpenInterest"].idxmax()
            PE_MAX_CHANGE_OI = PE_df["strikePrice"][pe_max_index_change_oi]

            PE_CIOI_VOL = PE_df["changeinOpenInterest"][pe_max_index_change_oi]
            PE_VOLUME = PE_df["totalTradedVolume"][pe_max_index_change_oi]

            ce_values = [data['CE'] for data in nifty_data['records']['data']
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
                          'TREND': [MAX_OI_TREND, MAX_CHANGE_OI_TREND, CIOI_VOL_TREND, VOL_TREND],
                          'Timestamp': timestamp}

            banknifty_table_df = pd.DataFrame(table_data, index=['MAX OI',
                                                                 'CHANGE IN OI',
                                                                 'CIOI VOLUME',
                                                                 'VOLUME'])

            d2g.upload(nifty_table_df, spreadsheet_key, wks_name,
                       credentials=creds, row_names=True, clean=False, start_cell='A2')

            d2g.upload(banknifty_table_df, spreadsheet_key, wks_name,
                       credentials=creds, row_names=True, clean=False, start_cell='A10')

            print("Data Uploaded for {}".format(timestamp))
            sleep(50)

        else:
            print(
                "Some error occured while fetching the data. Refreshing in 30 seconds...")
            sleep(30)

    else:
        print("App will display the data only from 9:10 AM to 3:40 PM")
        sleep(100)
