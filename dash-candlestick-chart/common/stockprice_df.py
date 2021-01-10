# return stock price pandas
import pandas as pd

DAILY_FREQUENCY_TAIL = 260
WEEKLY_FREQUENCY_TAIL = 52
MONTHLY_FREQUENCY_TAIL = 60
YEARLY_FREQUENCY_TAIL = 100


def get_stock_df(stock_code, frequency):
    if frequency == 'W':
        return weekly_df(stock_code, WEEKLY_FREQUENCY_TAIL)
    elif frequency == 'M':
        return monthly_df(stock_code, MONTHLY_FREQUENCY_TAIL)
    elif frequency == 'Y':
        return yearly_df(stock_code, YEARLY_FREQUENCY_TAIL)
    else:
        return daily_df(stock_code, DAILY_FREQUENCY_TAIL)


def daily_df(stock_code, tail_num):
    path_file = "./data/%s.AX.csv" % stock_code
    return pd.read_csv(path_file).tail(tail_num)


def weekly_df(stock_code, tail_num):
    path_file = "./data/%s.AX.csv" % stock_code

    df = pd.read_csv(path_file, parse_dates=['Date'], index_col=['Date'])

    df_weekly = df.resample('W').agg({'Open': 'first',
                                      'High': 'max',
                                      'Low': 'min',
                                      'Close': 'last',
                                      'Volume': 'sum'})
    min_tail = min(tail_num, len(df_weekly.index))
    return df_weekly.reset_index().tail(min_tail)


def monthly_df(stock_code, tail_num):
    path_file = "./data/%s.AX.csv" % stock_code

    df = pd.read_csv(path_file, parse_dates=['Date'], index_col=['Date'])

    df_monthly = df.resample('MS').agg({'Open': 'first',
                                        'High': 'max',
                                        'Low': 'min',
                                        'Close': 'last',
                                        'Volume': 'sum'})
    min_tail = min(tail_num, len(df_monthly.index))
    return df_monthly.reset_index().tail(min_tail)


def yearly_df(stock_code, tail_num):
    path_file = "./data/%s.AX.csv" % stock_code

    df = pd.read_csv(path_file, parse_dates=['Date'], index_col=['Date'])

    df_yearly = df.resample('YS').agg({'Open': 'first',
                                       'High': 'max',
                                       'Low': 'min',
                                       'Close': 'last',
                                       'Volume': 'sum'})
    min_tail = min(tail_num, len(df_yearly.index))
    return df_yearly.reset_index().tail(min_tail)


def get_dash_table_header(frequency):
    if frequency == 'W':
        return 'Datatable: Available from last ' + str(WEEKLY_FREQUENCY_TAIL) + ' weeks'
    elif frequency == 'M':
        return 'Datatable: Available from last ' + str(MONTHLY_FREQUENCY_TAIL) + ' months'
    elif frequency == 'Y':
        return 'Datatable: Available from last ' + str(YEARLY_FREQUENCY_TAIL) + ' years'
    else:
        return 'Datatable: Last ' + str(DAILY_FREQUENCY_TAIL) + ' days'
