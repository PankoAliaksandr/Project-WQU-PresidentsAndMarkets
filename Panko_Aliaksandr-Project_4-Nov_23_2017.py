# Libraries
import pandas as pd
import re
import quandl
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
# $ pip install quandl


# Class to execute the assingment tasks
class Resp_VS_Dem:

    # Constructor
    def __init__(self):

        self.__df_presidents_info = pd.DataFrame()
        self.__df_sp500_value_m = pd.DataFrame()
        self.__df_dji_value_d = pd.DataFrame()
        self.__df_annual_returns_dji = pd.DataFrame()
        self.__df_annual_returns_sp500 = pd.DataFrame()
        self.__df_rep_returns_sp500 = pd.DataFrame()
        self.__df_rep_returns_dji = pd.DataFrame()
        self.__df_dem_returns_sp500 = pd.DataFrame()
        self.__df_dem_returns_dji = pd.DataFrame()

        # Statistics
        self.__rep_dji_mean = 0
        self.__rep_dji_median = 0
        self.__rep_sp500_mean = 0
        self.__rep_sp500_median = 0
        self.__dem_dji_mean = 0
        self.__dem_dji_median = 0
        self.__dem_sp500_mean = 0
        self.__dem_sp500_median = 0
        self.__rep_dji_sd = 0
        self.__rep_sp500_sd = 0
        self.__dem_dji_sd = 0
        self.__dem_sp500_sd = 0

    def Get_Presidents_Info(self):
        return self.__df_presidents_info

    def Get_SP500_Value(self):
        return self.__df_sp500_value_m

    def Get_DJI_Value(self):
        return self.__df_dji_value_d

    def Get_Annual_Returns_DJI(self):
        return self.__df_annual_returns_dji

    def Get_Annual_Returns_SP500(self):
        return self.__df_annual_returns_sp500

    def Get_Rep_Returns_SP500(self):
        return self.__df_rep_returns_sp500

    def Get_Rep_Returns_DJI(self):
        return self.__df_rep_returns_dji

    def Get_Dem_Returns_SP500(self):
        return self.__df_dem_returns_sp500

    def Get_Dem_Returns_DJI(self):
        return self.__df_dem_returns_dji

    def Download_President_Data(self, link):

        # Step 1: Parse Wikipedia and find the table of presidents:
        self.__df_presidents_info = pd.read_html(link)[1]  # required table #1

        # Prepare data
        # Set column names
        self.__df_presidents_info.columns = ['Term2', 'Years', 'Vise1',
                                             'President', 'Prior Office',
                                             'Vise2', 'Party', 'Term1', 'Vise3'
                                             ]
        # Remain only relevant ones
        self.__df_presidents_info = self.__df_presidents_info[[
                'Years', 'President', 'Party']]

        # Drop NA and empty lines
        self.__df_presidents_info.dropna(inplace=True)
        self.__df_presidents_info.reset_index(drop=True, inplace=True)

        # Get years of the presidence
        def __Find_Year(year):
            return re.findall('(\d\d\d\d)', year)

        # Retrive Years
        self.__df_presidents_info.Years = self.__df_presidents_info.Years.\
            apply(__Find_Year)

        # Get Presidents' names
        def __Find_Name(name):
            patterns = [r"[A-Z]{1}[a-z]+ [A-Z]{1}[a-z]+",
                        r"[A-Z]{1}[a-z]+ [A-Z]{1}\. [A-Z]{1}[a-z]+"]

            pattern = "|".join(patterns)
            return re.findall(pattern, name)

        # Unlist function
        def __Unlist(one_el_list):
            return one_el_list[0]

        # Retrieve Names
        self.__df_presidents_info.President = self.__df_presidents_info.\
            President.apply(__Find_Name)

        # Unlist Names
        self.__df_presidents_info.President = self.__df_presidents_info.\
            President.apply(__Unlist)

        # Define Party name
        def __Def_Party(party):
            patterns = [r"Democratic", r"Republican", r"Federalist",
                        r"Unaffiliated", r"Whig", r"National Union"]

            pattern = "|".join(patterns)
            return re.findall(pattern, party)

        # Define Party name
        self.__df_presidents_info.Party = self.__df_presidents_info.\
            Party.apply(__Def_Party)

        # Cut before 1920
        def __Cut(self):
            for i in range(len(self.__df_presidents_info)):
                if int(self.__df_presidents_info.Years[i][0]) < int(1920):
                    self.__df_presidents_info =\
                        self.__df_presidents_info.drop(i)

            # Reset Index
            self.__df_presidents_info =\
                self.__df_presidents_info.reset_index(drop=True)

        # Cut before 1920
        __Cut(self)

        # Create .csv file
        def __Create_csv(self):
            self.__df_presidents_info.to_csv('Presidents')

        # Create .csv file
        __Create_csv(self)

    def Download_Indices_Data(self):

        # Download S&P500 monthly value till 2017-10-01
        def __Download_SP500(self):
            self.__df_sp500_value_m = quandl.get(
                        "MULTPL/SP500_REAL_PRICE_MONTH",
                        start_date="1920-01-01",
                        end_date='2017-10-01')

        # Download S&P500 monthly value till 2017-10-01
        __Download_SP500(self)

        # Download DJI daily value till 2017-10-01
        def __Download_DJI(self):
            # Daily DJI [till 2016-04-15 ]
            df_dji_d1 = quandl.get("BCB/UDJIAD1", start_date="1920-01-01")
            df_dji_d1.columns = ['Value']

            # Next trading day is 2016-04-18
            # Yahoo Finance is used to get latest data
            df_dji_d2 = pdr.get_data_yahoo('^DJI', start='2016-04-18',
                                           end='2017-10-01')

            # Prepare for union
            df_dji_d2 = df_dji_d2['Adj Close']
            df_dji_d2 = df_dji_d2.to_frame()
            df_dji_d2.columns = ['Value']

            # Unite 2 parts of DJI
            frames = [df_dji_d1, df_dji_d2]
            self.__df_dji_value_d = pd.concat(frames)

        # Download DJI daily value till 2017-10-01
        __Download_DJI(self)

    def Calculate_Annual_Returns(self):

        # Monthly sp500 returns
        df_sp500_m_r = self.__df_sp500_value_m.pct_change(1)

        # Daily dji returns
        df_dji_d_r = self.__df_dji_value_d.pct_change(1)

        # Fuction gives the return for the whole period
        # returns here a not in percentage
        def __Total_Return_From_Returns(returns):
            return (1 + returns).prod() - 1

        # Calculate annual returns DJI
        self.__df_annual_returns_dji = df_dji_d_r.groupby(
                df_dji_d_r.index.year).apply(__Total_Return_From_Returns)

        # Calculate annual returns SP500
        self.__df_annual_returns_sp500 = df_sp500_m_r.groupby(
                df_sp500_m_r.index.year).apply(__Total_Return_From_Returns)

    def Segregate_Returns(self):

        # For each president determine the start and the end of his term
        for i in range(len(self.__df_presidents_info)):
            begin = int(self.__df_presidents_info.Years[i][0])
            if i == (len(self.__df_presidents_info) - 1):
                # last president
                end = int(self.__df_presidents_info.Years[i][0])
            else:
                end = int(self.__df_presidents_info.Years[i][1]) - 1

            # Retrieve term returns DJI
            ts_part_r_dji = self.__df_annual_returns_dji.Value[
                    (begin <= self.__df_annual_returns_dji.index) &
                    (self.__df_annual_returns_dji.index <= end)]

            # Retrieve term returns SP500
            ts_part_r_sp500 = self.__df_annual_returns_sp500.Value[
                    (begin <= self.__df_annual_returns_sp500.index) &
                    (self.__df_annual_returns_sp500.index <= end)]

            # Segment returns
            if str(self.__df_presidents_info.Party[i][0]) == 'Republican':
                # add to respublicans returns
                frames_dji = [self.__df_rep_returns_dji, ts_part_r_dji]
                frames_sp500 = [self.__df_rep_returns_sp500, ts_part_r_sp500]
                self.__df_rep_returns_dji = pd.concat(frames_dji)
                self.__df_rep_returns_sp500 = pd.concat(frames_sp500)
            else:
                # add to democrats returns
                frames_dji = [self.__df_dem_returns_dji, ts_part_r_dji]
                frames_sp500 = [self.__df_dem_returns_sp500, ts_part_r_sp500]
                self.__df_dem_returns_dji = pd.concat(frames_dji)
                self.__df_dem_returns_sp500 = pd.concat(frames_sp500)

        # Rename column
        self.__df_rep_returns_dji.columns = ['Return']
        self.__df_rep_returns_sp500.columns = ['Return']
        self.__df_dem_returns_dji.columns = ['Return']
        self.__df_dem_returns_sp500.columns = ['Return']

    def Calculate_Statistics(self):

        # Republican Mean
        self.__rep_dji_mean = self.__df_rep_returns_dji.Return.mean()
        print("\nself.__rep_dji_mean", self.__rep_dji_mean)
        self.__rep_sp500_mean = self.__df_rep_returns_sp500.Return.mean()
        print("\nself.__rep_sp500_mean", self.__rep_sp500_mean)
        # Republican Median
        self.__rep_dji_median = self.__df_rep_returns_dji.Return.median()
        print("\nself.__rep_dji_median", self.__rep_dji_median)
        self.__rep_sp500_median = self.__df_rep_returns_sp500.Return.\
            median()
        print("\nself.__rep_sp500_median", self.__rep_sp500_median)

        # Democratic Mean
        self.__dem_dji_mean = self.__df_dem_returns_dji.Return.mean()
        print("\nself.__dem_dji_mean", self.__dem_dji_mean)
        self.__dem_sp500_mean = self.__df_dem_returns_sp500.Return.mean()
        print("\nself.__dem_sp500_mean", self.__dem_sp500_mean)
        # Democratic Median
        self.__dem_dji_median = self.__df_dem_returns_dji.Return.median()
        print("\nself.__dem_dji_median", self.__dem_dji_median)
        self.__dem_sp500_median = self.__df_dem_returns_sp500.Return.\
            median()
        print("\nself.__dem_sp500_median", self.__dem_sp500_median)

        # Republican Standard deviation
        self.__rep_dji_sd = self.__df_rep_returns_dji.Return.std()
        print("\nself.__rep_dji_sd", self.__rep_dji_sd)
        self.__rep_sp500_sd = self.__df_rep_returns_sp500.Return.std()
        print("\nself.__rep_sp500_sd", self.__rep_sp500_sd)
        # Democratic Standard deviation
        self.__dem_dji_sd = self.__df_dem_returns_dji.Return.std()
        print("\nself.__dem_dji_sd", self.__dem_dji_sd)
        self.__dem_sp500_sd = self.__df_dem_returns_sp500.Return.std()
        print("\nself.__dem_sp500_sd", self.__dem_sp500_sd)

    def Visualize_Results(self):

        # DJI Republican Returns
        plt.hist(self.__df_rep_returns_dji.Return, bins=20, color='c',
                 label="Returns")
        plt.title("DJI Republican Returns")
        plt.axvline(self.__df_rep_returns_dji.Return.mean(), color='b',
                    linestyle='dashed', linewidth=2)
        plt.axvline(self.__df_rep_returns_dji.Return.mean(), color='g',
                    linestyle='dashed', linewidth=2)
        plt.show()

        # SP500 Republican Returns
        plt.hist(self.__df_rep_returns_sp500.Return, bins=20, color='c',
                 label="Returns")
        plt.title("SP500 Republican Returns")
        plt.axvline(self.__df_rep_returns_sp500.Return.mean(), color='b',
                    linestyle='dashed', linewidth=2)
        plt.axvline(self.__df_rep_returns_sp500.Return.mean(), color='g',
                    linestyle='dashed', linewidth=2)
        plt.show()

        # DJI Democratic Returns
        plt.hist(self.__df_dem_returns_dji.Return, bins=20, color='c',
                 label="Returns")
        plt.title("DJI Democratic Returns")
        plt.axvline(self.__df_dem_returns_dji.Return.mean(), color='b',
                    linestyle='dashed', linewidth=2)
        plt.axvline(self.__df_dem_returns_dji.Return.median(), color='g',
                    linestyle='dashed', linewidth=2)
        plt.show()

        # SP500 Democratic Returns
        plt.hist(self.__df_dem_returns_sp500.Return, bins=20, color='c',
                 label="Returns")
        plt.title("SP500 Democratic Returns")
        plt.axvline(self.__df_dem_returns_sp500.Return.mean(), color='b',
                    linestyle='dashed', linewidth=2)
        plt.axvline(self.__df_dem_returns_sp500.Return.median(), color='g',
                    linestyle='dashed', linewidth=2)
        plt.show()

    def Main(self, link):
        self.Download_President_Data(link)
        self.Download_Indices_Data()
        self.Calculate_Annual_Returns()
        self.Segregate_Returns()
        self.Calculate_Statistics()
        self.Visualize_Results()


research = Resp_VS_Dem()
research.Main(
    'https://en.wikipedia.org/wiki/List_of_Presidents_of_the_United_States')
