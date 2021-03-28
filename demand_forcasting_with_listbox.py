import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import IDEALib as ideaLib
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import  filedialog
from tkinter import messagebox
import win32com.client as win32ComClient
client = win32ComClient.Dispatch(dispatch="Idea.IdeaClient")
from numpy import log
from pandas.plotting import autocorrelation_plot
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima_model import ARIMA, ARMA
from statsmodels.tsa.seasonal import seasonal_decompose
import os
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor 
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from statsmodels.tsa.stattools import acf, pacf
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error

dirname = os.path.dirname(__file__)


# Read from IMD
class UI:
    
    def __init__(self, arıma,ml,help_):  
        
        self.df = None
        self.arıma = arıma
        self.ml = ml
        
        # LABELFRAME 1
        self.labelframe1 = LabelFrame(arıma, 
                                      text = "Upload Data", 
                                      height = 60)
        self.labelframe1.pack(fill="both", 
                              pady=5, 
                              padx=5)
        self.labelframe1.pack_propagate(0)
        self.alt_text = Label(self.labelframe1, 
                              text = "Please Load a dataset:")
        self.alt_text.pack(side=LEFT, padx = 1)
        self.btn1 = Button(self.labelframe1, 
                           text= "Browse", 
                           command = self.load)
        self.btn1.pack(side=LEFT, 
                       padx = 5)
        self.text = tk.StringVar()
        self.text.set("Test")
        self.datalocation=Label(self.labelframe1,
                                text = '')
        self.datalocation.pack(side=LEFT,padx=5)
        
        # LabelFrame 2
        self.labelframe2 = LabelFrame(arıma, 
                                      height = 200)
        
        self.labelframe2.pack(fill = "both", 
                              pady = 5, 
                              padx = 5)
        self.labelframe2.pack_propagate(0)
        
        self.lbdata = Listbox(self.labelframe2, width= 25)
        self.lbdata.place(x=5, y=5)  
        
        self.lbdate = Listbox(self.labelframe2, width= 25, height= 3)
        self.lbdate.place(x=550, y=5) 
        
        self.lbtarget = Listbox(self.labelframe2, width= 25, height= 3)
        self.lbtarget.place(x=550, y=100)
        
        self.btn_date = Button(self.labelframe2, text= "Date >>",
                               width= 10, height= 3,
                               command=self.to_date)
        self.btn_date.place(x= 300, y=5)
        
        self.btn_target = Button(self.labelframe2, text= "Target >>",
                                 width= 10, height= 3,
                                 command= self.to_target)
        self.btn_target.place(x= 300, y=100)
        
        self.btn_reset = Button(self.labelframe2, text= "Clear them all",
                                command= self.clear)
        self.btn_reset.place(x= 550, y= 160)
        
        self.btn_save = Button(self.labelframe2, text= "Save",
                               command= self.save)
        self.btn_save.place(x= 650, y= 160)
        
        self.date = ""
        self.target = ""
        
        #LabelFrame 3
        self.labelframe3 = LabelFrame(arıma, 
                                      text = "Analyze", 
                                      height = 100)
        self.labelframe3.pack(fill = "both", 
                              pady = 5, 
                              padx = 5)
        self.labelframe3.pack_propagate(0)
        
        self.btn2 = Button(self.labelframe3, 
                           text = "Analyze", 
                           command = self.Data_Analyze,
                           width = 25,
                           height = 1)
        
        self.btn2.grid(column = 1, 
                       row = 1,
                       padx = 5)
        
        self.btn_correlation = Button(self.labelframe3, 
                                   text = "Correlation", 
                                   command = self.corr,
                                   width = 25,
                                   height = 1)
        self.btn_correlation.grid(column = 1, 
                               row = 2, 
                               padx = 5,
                               pady = 5)
        self.btnadfuller = Button(self.labelframe3, 
                                   text = "Adfuller Test", 
                                   command = self.adfuller,
                                   width = 25,
                                   height = 1)
        self.btnadfuller.grid(column = 2, 
                               row = 2, 
                               padx = 5,
                               pady = 5)
        
        self.btn_moving_avg = Button(self.labelframe3,
                                     text = 'Moving Average',
                                     command = self.moving_average,
                                     width = 25,
                                     height = 1)
        
        self.btn_moving_avg.grid(column = 4,
                                 row = 2, 
                                 padx = 5,
                                 pady = 5)
        
        self.btn_trend = Button(self.labelframe3, 
                                   text = "Trend", 
                                   command = self.trend,
                                   width = 25,
                                   height = 1)        
        self.btn_trend.grid(column = 2, 
                               row = 1, 
                               padx = 5)
        
        
        self.ismov = 0 # moving average not called
        
        
        
        #LabelFrame 4
        self.labelframe4 = LabelFrame(arıma, 
                                      text = "Result", 
                                      height = 100)
        self.labelframe4.pack(fill = "both", 
                              pady = 5, 
                              padx = 5)
        
        self.labelframe4.pack_propagate(0)
        
        self.lbladfuller = Label(self.labelframe4, 
                                 text="")
        
        self.lbladfuller.grid(column = 1, 
                               row = 1, 
                               padx = 5,
                               pady = 5)
        self.lblinfo = Label(self.labelframe4, 
                                 text="")
        
        self.lblinfo.grid(column = 5, 
                               row = 1, 
                               padx = 5,
                               pady = 5)
        
        #LabelFrame 5
        self.labelframe5 = LabelFrame(arıma, 
                                      text = "ARIMA",
                                      height = 200)
        
        self.labelframe5.pack(fill = "both",
                              pady = 5, 
                              padx = 5)
        self.labelframe5.pack_propagate(0)
        
        self.lbl_model = Label(self.labelframe5,
                               text = "Model: ")
        self.lbl_model.place(x= 5, y= 5)
        
        self.current_model = tk.StringVar()
        self.cmb_arıma = ttk.Combobox(self.labelframe5, width = 27, textvariable = self.current_model)
        
        self.cmb_arıma['values'] = ('AR', 
                          'MA',
                          'ARMA',
                          'ARIMA')
        self.cmb_arıma.place(x= 50, y= 5)
        
        self.lbl_p = Label(self.labelframe5,
                               text = "p: ")
        self.lbl_p.place(x= 5, y= 30)
        
        self.lbl_q = Label(self.labelframe5,
                               text = "q: ")
        self.lbl_q.place(x= 5, y= 50)
        
        self.lbl_predict = Label(self.labelframe5,
                               text = "Predict Dates: ")
        self.lbl_predict.place(x= 5, y= 80)
        
        self.Entry1 = Entry(self.labelframe5, width =5)
        self.Entry1.insert(0,1)
        self.Entry1.place(x=50, y=30)
        self.Entry2 = Entry(self.labelframe5, width =5)
        self.Entry2.insert(0,1)
        self.Entry2.place(x=50, y=50)
        self.Entry3 = Entry(self.labelframe5, width =5)
        self.Entry3.insert(0,20)
        self.Entry3.place(x=90, y=80)
        
        self.ar_tool = Button(self.labelframe5, text ="?", width =1 ,height =1, 
                            font='Helvetica 9 bold')
        
        self.lbl_ar_tooltip = CreateToolTip(self.ar_tool, 
                                            "p for AR order = From the ACF \
graph, x value when the curve \
touches y = 0.0")
        self.ar_tool.place(x=100, y=30)
        self.ma_tool = Button(self.labelframe5, text ="?", width =1 ,height =1, 
                            font='Helvetica 9 bold')
        
        self.lbl_ma_tooltip=CreateToolTip(self.ma_tool, 
                                          "q for AR order = From the ACF \
graph, x value when the curve \
touches y = 0.0")
        self.ma_tool.place(x=100, y=50)
        
        self.btn_run = Button(self.labelframe5, text ="Run", width =12 ,height =1, 
                              command=self.run).place(x=90, y=120)
        
        
        # TAB3 - HELP
        # help data tab
        self.labelframe9 = LabelFrame(help_, 
                                      text = "DATA TAB", 
                                      height = 400)
        self.labelframe9.pack(fill = "both", 
                              pady = 5, 
                              padx = 5)
        
        self.labelframe9.pack_propagate(0)
    
        
        self.upload_text = Label(self.labelframe9, 
                              text = "\nBROWSE BUTTON\nLoads a dataset \
(.IMD or .csv extensions are allowed.)\n----------\nANALYZE BUTTON\nCreates a \
new folder named as \"plots\" and saves the resultant plots into the folder. \
\nCorresponging plots are base_price.png, Center_id Orders.png, \
checkout_price.png, meal_id Orders.png, seasonality.png, Weekly Orders.png.\
\n---------\nCORRELATION BUTTON\nShows the correlation plot. \
\n----------\nADFULLER TEST BUTTON\nDetermines if time series data is \
stationary or not.\n----------\nRESULT SECTION\nAugmented Dickey-Fuller (ADF) \
 test is used.\nADF test is a type of unit root test. A unit root test \
 determines how strongly a time series is defined by a trend.\nThe null \
 hypothesis of the test is that the time series can be represented by a unit \
 root, that it is not stationary (has some time-dependent structure). \nThe \
 alternate hypothesis (rejecting the null hypothesis) is that the time series \
 is stationary.\nFor a time series to be stationary, ADF test must result as \
 follows:\na. If p-value > 0.05: Fail to reject the null hypothesis (H0), the\
 data has a unit root and is non-stationary.\n  If p-value <= 0.05: Reject \
 the null hypothesis (H0), the data does not have a unit root and is \
 stationary.\nb) Critical values at 1%, 5%, 10% confidence intervals should \
    be as close as possible to the Test Statistics.")
        self.upload_text.pack(side="left")
        
        # help arima tab
        self.labelframe10 = LabelFrame(help_, 
                                      text = "ARIMA TAB", 
                                      height = 80)
        self.labelframe10.pack(fill = "both", 
                              pady = 5, 
                              padx = 5)
        
        self.labelframe10.pack_propagate(0)
        self.arima_text = Label(self.labelframe10, 
                              text = "--> Possible methods are AR, MA, ARMA, \
ARIMA for time series analysis. Example: From the ACF graph, we see that curve \
touches y=0.0 line at x=0.\n Thus, from theory, Q = 0 From the PACF graph, \
 we see that curve touches  y=0.0 line at x=1. Thus, from theory, P = 1")
        self.arima_text.pack(side="left")
        
        # ml help tab
        self.labelframe11 = LabelFrame(help_, 
                                      text = "ML TAB", 
                                      height = 80)
        self.labelframe11.pack(fill = "both", 
                              pady = 5, 
                              padx = 5)
        
        self.labelframe11.pack_propagate(0)
        self.ml_text = Label(self.labelframe11, 
                              text = "--> Forecasting with Machine Learning")
        self.ml_text.pack(side="left")
        
        
        self.is_canvas_arıma = 0
        self.is_canvas_ml = 0
        self.indexedDataset = pd.DataFrame()
        self.ts_moving_avg_diff = None
        
        # ML Win
        
        self.var = IntVar()
        
        self.lbl_train = Label(ml, 
                              text = "Please Load a train data:").place(x=5,y=5)
        
        self.btn_train = Button(ml, 
                           text= "Browse", 
                           command = self.load_train).place(x=150, y=5)
        self.lbl_test = Label(ml, 
                              text = "Please Load a test data:").place(x=5,y=40)
        
        self.btn_test = Button(ml, 
                           text= "Browse", 
                           command = self.load_test).place(x=150, y=40)
        
        self.title1 = Label(ml, text ="Model",
                            font='Helvetica 9 bold').place(x=5, y=60)
        
        self.title2 = Label(ml, text ="Order", 
                            font='Helvetica 9 bold').place(x=100, y=80)
        
        self.R1 = Radiobutton(ml, text="LinearRegression", variable= self.var, 
                              value =1).place(x=5, y=60)
        
        self.R2 = Radiobutton(ml, text="KNeighborsRegressor", variable= self.var, 
                              value =2).place(x=5, y=80)
        
        self.R3 = Radiobutton(ml, text="DecisionTreeRegressor", variable= self.var, 
                              value =3).place(x=5, y=100)
        
        self.R3 = Radiobutton(ml, text="RandomForestRegressor", variable= self.var, 
                              value =4).place(x=5, y=120)
        
        self.lbl_knn = Label(ml, text ="n_neighbours:").place(x=170, y=80)
        self.lbl_rf = Label(ml, text ="n_estimators:").place(x=170, y=120)
        
        self.Entry_knn = Entry(ml, width =5)
        self.Entry_knn.insert(0,10)
        self.Entry_knn.place(x=250, y=80)
        self.Entry_rf = Entry(ml, width =5)
        self.Entry_rf.insert(0,10)
        self.Entry_rf.place(x=250, y=120)
        
        self.btn_run_ml = Button(ml, text ="Run", width =12 ,height =1, 
                              command=self.run_ml).place(x=50, y=150)
        
        
        
        pd.set_option('display.max_columns', None)
        pd.set_option("display.float_format",lambda x:"%.4f" % x)
        
    
    def load(self):
        
        self.lbdata.delete(0,'end')
        
        self.filename = filedialog.askopenfilename(initialdir="/",
                        title="Select a File",
                        filetypes=(("Excel files", ".IMD*"), ("all files", 
                                                               "*.*"),
                                   ("Excel files", ".csv*")))
        
        self.datatype = self.filename.split('.')
        if (self.datatype[-1] == 'csv'):
            self.df = pd.read_csv(self.filename)
            # self.indexedDataset= self.df.groupby(['date'])['num_orders'].sum().reset_index()
            # self.indexedDataset.set_index(['date'],inplace=True)
        
        elif self.datatype[-1] == 'IMD':
            self.datalocation['text'] = self.filename  
            
            # Read from .IMD file
            self.filename=self.filename.split('/')
            self.filename=self.filename[-1]                  # Dataset must be in IDEA working directory
            self.df = ideaLib.idea2py(database = self.filename)
            
        if self.df is None:
           messagebox.showinfo("Info",
                               "There was something wrong with the import process of IDEA database to Pandas dataframe")
        elif self.df.empty:
          messagebox.showinfo("Info","You selected an empty IDEA database")
        if self.datatype[-1] == 'IMD':
            
            if 'CENTER_TYPE' in self.df and  \
            'CATEGORY' in self.df and  \
            'CUISINE' in self.df:
                self.df = self.df.astype({"CENTER_TYPE": str,"CATEGORY": str,
                                          "CUISINE": str})
                
            self.df.columns = map(str.lower, self.df.columns)
            
            # self.indexedDataset= self.df.groupby(['date'])['num_orders'].sum().reset_index()
            # self.indexedDataset.set_index(['date'],inplace=True)
            i = 0
            for column in self.df.columns:
                 self.lbdata.insert(i,column)
                 i += 1
        elif self.datatype[-1] == 'csv':
             self.df.columns = map(str.lower, self.df.columns)
             i = 0
             for column in self.df.columns:
                 self.lbdata.insert(i,column)
                 i += 1
        else :
            messagebox.showerror('Error', 'Invalid Data Type')
    def to_date(self):
        selected = self.lbdata.get(ACTIVE)
        self.lbdate.delete(0,'end')
        self.lbdate.insert(0,selected)
    
    def to_target(self):
        selected = self.lbdata.get(ACTIVE)
        self.lbtarget.delete(0,'end')
        self.lbtarget.insert(0,selected)
        
    def clear(self):
        self.lbdate.delete(0,'end')
        self.lbtarget.delete(0,'end')
        
    def save(self):
        self.lbdate.selection_set(0)
        self.date = self.lbdate.get(self.lbdate.curselection())
        self.lbtarget.selection_set(0)
        self.target = self.lbtarget.get(self.lbtarget.curselection())
        
        try:
            self.df[self.date] = pd.to_datetime(self.df[self.date], format='%d.%m.%Y')
        except:
            self.df[self.date] = pd.to_datetime(self.df[self.date])
            
        self.indexedDataset = self.df.groupby([self.date])[self.target].sum().reset_index()
        self.indexedDataset.set_index([self.date], inplace=True)
        
    
    def Data_Analyze(self):
        
        weekly_orders = self.df.groupby(['date'])['num_orders'].sum().reset_index()
        weekly_orders = pd.DataFrame(weekly_orders)
        
        plt.plot(weekly_orders['date'], weekly_orders['num_orders'])
        plt.xlabel('weeks')
        plt.ylabel('orders')
        plt.title('Weekly Orders')
        # plt.show(block = False)
        
        mypath = dirname+"/plots"
        if not os.path.isdir(mypath):
            os.makedirs(mypath)
        #Saving plots:
        plt.savefig(dirname + '/plots/Weekly Orders.png')
        plt.close()
        
        center_id = self.df.groupby(['center_id'])['num_orders'].sum().reset_index()
        center_id = pd.DataFrame(center_id)
        
        plt.bar(center_id['center_id'], center_id['num_orders'])
        plt.xlabel('center_id')
        plt.ylabel('orders')
        plt.title('Center_id Orders')
        plt.savefig(dirname + '/plots/Center_id Orders.png')
        plt.close()
        
        meal_id = self.df.groupby(['meal_id'])['num_orders'].sum().reset_index()
        meal_id = pd.DataFrame(meal_id)
        
        plt.bar(meal_id['meal_id'], meal_id['num_orders'], width=6)
        plt.xlabel('meal_id')
        plt.ylabel('orders')
        plt.title('meal_id Orders')
        plt.savefig(dirname + '/plots/meal_id Orders.png')
        plt.close()
        
        # category = self.df.groupby(['category'])['num_orders'].sum().reset_index()
        # category = pd.DataFrame(category)
        
        # plt.bar(category['category'], category['num_orders'])
        # # plt.xticks(rotation=90)
        # plt.xlabel('category')
        # plt.ylabel('orders')
        # plt.title('category Orders')
        # plt.savefig(dirname + '/plots/category Orders.png')
        # plt.close()
        
        
        # category_cuisine = self.df.groupby(['category','cuisine'])['num_orders'].sum().reset_index()
        # category_cuisine = pd.DataFrame(category_cuisine)
        # category_cuisine['meal'] = category_cuisine['category'] + ', ' + category_cuisine['cuisine']
        
        # plt.bar(category_cuisine['meal'], category_cuisine['num_orders'])
        # # plt.xticks(rotation=90)
        # plt.xlabel('category_cuisine')
        # plt.ylabel('orders')
        # plt.title('category_cuisine Orders')
        # plt.savefig(dirname + '/plots/category_cuisine Orders.png')
        # plt.close()
        
        
        plt.scatter(self.df['checkout_price'],self.df['num_orders'],s=2)
        plt.xlabel('checkout_price')
        plt.ylabel('orders')
        plt.savefig(dirname + '/plots/checkout_price.png')
        plt.ioff()
        
        plt.scatter(self.df['base_price'],self.df['num_orders'],s=2)
        plt.xlabel('base_price')
        plt.ylabel('orders')
        plt.savefig(dirname + '/plots/base_price.png')
        plt.close()
        
        # pd.set_option('display.max_columns', None)
        
        # centertype = self.df.groupby(['center_type'])
        # centertype = pd.DataFrame(centertype)
        
        # lis = centertype[0]
        
        # for i in lis:
            
        #     data = self.df[self.df['center_type'] == i]
        #     center_type = data.groupby(['date','center_type'])['num_orders'].sum().reset_index()
        #     plt.plot(center_type['date'],center_type['num_orders'])
        # plt.legend(lis)
        # plt.savefig(dirname + '/plots/Order Type.png')
        
        
        ts = self.df.groupby(['date'])['num_orders'].sum().reset_index()
        season_df = ts.copy()

        season_df['week_'] = ts['date'] % 52
        seasons = 1
        
        for i in season_df['week_']:
            if (i >0 and i <= 13):
                season_df.loc[season_df['week_'] == i,'season'] = 1
            elif (i > 13 and i <= 26):
                season_df.loc[season_df['week_'] == i,'season'] = 2
            elif (i > 26 and i <= 39):
                season_df.loc[season_df['week_'] == i,'season'] = 3
            elif ((i > 39 and i <= 52) or i ==0):
                season_df.loc[season_df['week_'] == i,'season'] = 4
                
        for i in range (143):
            season_df.loc[season_df.index == i, 'seasons'] = seasons
            if i % 13 == 12:
                seasons += 1    
                
        season_group = season_df.groupby(['seasons'])['num_orders'].sum().reset_index()
            
        plt.plot(season_group['seasons'],season_group['num_orders'])
        plt.title('Seasons')
        plt.xlabel('Seasons')
        plt.ylabel('Orders')
        plt.savefig(dirname + '/plots/seasonality.png')
        plt.close()
        
        messagebox.showinfo('Info', 'Plots are saved')
        
        new_data = self.df.groupby(['date'])['num_orders'].sum().reset_index()
        # new_data['date'] = pd.date_range('2020-01-01', periods=145, freq='W')
        # new_data.drop(columns = 'date', axis = 1, inplace=True)
        # new_data.set_index('date',inplace=True)
        
    
    def corr(self):
        
        if self.ismov == 1:
            df = self.ts_moving_avg_diff
        else:
            df = self.indexedDataset
        
        lag_acf = acf(df, nlags=10)
        lag_pacf = pacf(df, nlags=10, method='ols')
        
        # ACF
        plt.figure(figsize=(22,10))
        
        plt.subplot(121) 
        plt.plot(lag_acf)
        plt.axhline(y=0,linestyle='--',color='gray')
        plt.axhline(y=-1.96/np.sqrt(len(df)),linestyle='--',color='gray')
        plt.axhline(y=1.96/np.sqrt(len(df)),linestyle='--',color='gray')
        plt.title('Autocorrelation Function')
        
        # PACF
        plt.subplot(122)
        plt.plot(lag_pacf)
        plt.axhline(y=0,linestyle='--',color='gray')
        plt.axhline(y=-1.96/np.sqrt(len(df)),linestyle='--',color='gray')
        plt.axhline(y=1.96/np.sqrt(len(df)),linestyle='--',color='gray')
        plt.title('Partial Autocorrelation Function')
        plt.tight_layout()
        plt.show()
        
    def adfuller(self):
        
        #Perform Augmented Dickey–Fuller test:
        # check_adfuller
        def check_adfuller(ts):
            # Dickey-Fuller test
            dftest = adfuller(ts, autolag='AIC')
            dfoutput = pd.Series(dftest[0:4], index=['Test Statistic',
                                                     'p-value','#Lags Used',
                                                     'Number of Observations \
                                                     Used'])
            for key,value in dftest[4].items():
                dfoutput['Critical Value (%s)'%key] = value

            self.lbladfuller['text'] = dfoutput
            self.lblinfo['text'] = "If so there is stability: \n\n - P-value \
is less than 0.05 \n -Test statistics less than critical values"

            
        # check_mean_std
        def check_mean_std(ts):
            #Rolling statistics
            rolmean = ts.rolling(12).mean()
            rolstd = ts.rolling(12).std()
            plt.figure(figsize=(22,10))   
            orig = plt.plot(ts, color='red',label='Original')
            mean = plt.plot(rolmean, color='black', label='Rolling Mean')
            std = plt.plot(rolstd, color='green', label = 'Rolling Std')
            plt.xlabel("Date")
            plt.ylabel("Mean Temperature")
            plt.title('Rolling Mean & Standard Deviation')
            plt.legend()
            plt.show(block = False)
            
        if self.target != "":
            
            # check stationary: mean, variance(std)and adfuller test
            if self.ismov == 0:
                check_mean_std(self.indexedDataset)
                check_adfuller(self.indexedDataset[self.target])
            
            # check stationary: mean, variance(std)and adfuller test
            if self.ismov == 1:
                check_mean_std(self.ts_moving_avg_diff)
                check_adfuller(self.ts_moving_avg_diff[self.target])        
        else:
            messagebox.showerror('Error', 'Please select a Target Column')
        
    
    def moving_average(self):
        self.ismov = 1 #  moving average called
        # Moving average method
        window_size = 12
        moving_avg = self.indexedDataset.rolling(window_size).mean()
        self.ts_moving_avg_diff = self.indexedDataset - moving_avg
        self.ts_moving_avg_diff.dropna(inplace=True) # first 6 is nan value due to window size

    def trend(self):
        
        # x = self.df.groupby(['date'])['num_orders'].sum().reset_index()
        # x.drop(['num_orders'],axis=1,inplace= True)
        # x['date'] = pd.date_range('01-01-2020', periods=145, freq='W')
        # x.drop(columns = 'date', axis = 1, inplace=True)
        # x.set_index('date',inplace=True)
        
        subtraction = self.indexedDataset.index[1] - self.indexedDataset.index[0]
        
        if '7' in str(subtraction):
            freq = 52
        elif '1' in str(subtraction):
            freq = 365
        
        x = self.indexedDataset[self.target]
        
        decomposition = seasonal_decompose(x, freq= 52)
        trend = decomposition.trend
        seasonal = decomposition.seasonal
        residual = decomposition.resid
        
        plt.subplot(411)
        plt.plot(x, label='Original')
        plt.legend(loc='best')
        plt.subplot(412)
        plt.plot(trend, label='Trend')
        plt.legend(loc='best')
        plt.subplot(413)
        plt.plot(seasonal,label='Seasonality')
        plt.legend(loc='best')
        plt.subplot(414)
        plt.plot(residual, label='Residuals')
        plt.legend(loc='best')
        plt.tight_layout()
        plt.show()
    

    
    def run(self):
        
        # if self.var.get() == 0:
        #     messagebox.showinfo('Info','Please select a Model')
        
        # elif self.Entry1.get().isdigit() == False:
        #     messagebox.showerror('Error','Type a number for orders')
        # elif self.Entry2.get().isdigit() == False:
        #     messagebox.showerror('Error','Type a number for orders')
        # else:
        #     radioN = self.var.get()
        #     if radioN == 1:
        #         p = int(self.Entry1.get())
        #         q = 0
        #         if self.ts_moving_avg_diff is not None:
        #             self.arıma_model(p,q,self.ts_moving_avg_diff)
        #         else:
        #             self.arıma_model(p,q,self.indexedDataset)
        #             print(self.indexedDataset)
        #     elif radioN == 2:
        #         p = 0
        #         q = int(self.Entry2.get())
        #         if self.ts_moving_avg_diff is not None:
        #             self.arıma_model(p,q,self.ts_moving_avg_diff)
        #         else:
        #             self.arıma_model(p,q,self.indexedDataset)
        #     elif radioN == 3:
        #         p = int(self.Entry1.get())
        #         q = int(self.Entry2.get())
        #         if self.ts_moving_avg_diff is not None:
        #             self.arma_model(p,q,self.ts_moving_avg_diff)
        #         else:
        #             self.arma_model(p,q,self.indexedDataset)
        #     else:
        #         p = int(self.Entry1.get())
        #         q = int(self.Entry2.get())   
        #         if self.ts_moving_avg_diff is not None:
        #             self.arıma_model(p,q,self.ts_moving_avg_diff)
        #         else:
        #             self.arıma_model(p,q,self.indexedDataset)
        
        if self.cmb_arıma.get() == "":
            messagebox.showerror("Error","Please choose a model")
        
        elif self.Entry1.get().isdigit() == False:
            messagebox.showerror('Error','Type a number for orders')
        elif self.Entry2.get().isdigit() == False:
            messagebox.showerror('Error','Type a number for orders')
        elif self.Entry3.get().isdigit() == False:
            messagebox.showerror('Error','Type a number for Predict Dates')
    
        else:
            current_model = self.cmb_arıma.get()
            pd = int(self.Entry3.get())
        
            if current_model == 'AR':
                p = int(self.Entry1.get())
                q = 0
                if self.ts_moving_avg_diff is not None:
                    self.arıma_model(p,q,pd,self.ts_moving_avg_diff)
                else:
                    self.arıma_model(p,q,pd,self.indexedDataset)
            elif current_model == 'MA':
                p = 0
                q = int(self.Entry2.get())
                if self.ts_moving_avg_diff is not None:
                    self.arıma_model(p,q,pd,self.ts_moving_avg_diff)
                else:
                    self.arıma_model(p,q,pd,self.indexedDataset)
            elif current_model == 'ARMA':
                p = int(self.Entry1.get())
                q = int(self.Entry2.get())
                if self.ts_moving_avg_diff is not None:
                    self.arma_model(p,q,pd,self.ts_moving_avg_diff)
                else:
                    self.arma_model(p,q,pd,self.indexedDataset)
            else:
                p = int(self.Entry1.get())
                q = int(self.Entry2.get())   
                if self.ts_moving_avg_diff is not None:
                    self.arıma_model(p,q,pd,self.ts_moving_avg_diff)
                else:
                    self.arıma_model(p,q,pd,self.indexedDataset)
           
        
    def arıma_model(self,p,q,pd,df):

        if self.is_canvas_arıma == 1:
            self.canvas.get_tk_widget().pack_forget()
        
        ar = ARIMA(df[self.target], order=(p,1,q))
        length = len(df[self.target])
        
        ar_fitted = ar.fit()
        forecast = ar_fitted.predict(length-100, length+pd)
        
        diff_ARIMA = (ar_fitted.fittedvalues - df[self.target])
        diff_ARIMA.dropna(inplace=True)
        
        fig = Figure(figsize=(5, 5), dpi=100)
        fig.add_subplot(111).plot(df)
        fig.add_subplot(111).plot(forecast)
        
        if self.ismov == 1:
            forecast2 = ar_fitted.predict(12, length+11)
        else:
            forecast2 = ar_fitted.predict(1, length)
        error = mean_squared_error(df[self.target], forecast2)
        fig.suptitle('Root mean squared error: %.4F'%error)
        # fig.suptitle('ARIMA Model RSS: %.4F'%sum((diff_ARIMA)**2))
        
        self.canvas = FigureCanvasTkAgg(fig, master =self.labelframe5)  # A tk.DrawingArea.
        self.canvas.get_tk_widget().pack(side=RIGHT)
        self.canvas.draw()        
        self.is_canvas_arıma = 1
        
        
    def arma_model(self,p,q,pd,df):
        
        if self.is_canvas_arıma == 1:
            self.canvas.get_tk_widget().pack_forget()          

        ar = ARMA(df[self.target], order=(p,q))
        length = len(df[self.target])
        
        ar_fitted = ar.fit(disp=0)
        forecast = ar_fitted.predict(length-100, length+pd)
        
        diff_ARIMA = (ar_fitted.fittedvalues - df[self.target])
        diff_ARIMA.dropna(inplace=True)

        fig = Figure(figsize=(5, 5), dpi=100)
        fig.add_subplot(111).plot(df)
        fig.add_subplot(111).plot(forecast)
        
        if self.ismov == 1:
            forecast2 = ar_fitted.predict(12, length+11)
        else:
            forecast2 = ar_fitted.predict(1, length)

        error = mean_squared_error(df[self.target], forecast2)
        fig.suptitle('Root mean squared error: %.4F'%error)
        
        # fig.suptitle('ARMA Model RSS: %.4F'%sum((diff_ARIMA)**2))
        

        self.canvas = FigureCanvasTkAgg(fig, master =self.labelframe5)  # A tk.DrawingArea.
        self.canvas.get_tk_widget().pack(side=RIGHT)
        self.canvas.draw()
        self.is_canvas_arıma = 1
    
    def load_train(self):
        
        self.filename = filedialog.askopenfilename(initialdir="/",
                        title="Select a File",
                        filetypes=(("Excel files", ".IMD*"), ("all files", 
                                                               "*.*"),
                                   ("Excel files", ".csv*")))
        
        self.datatype = self.filename.split('.')
        if (self.datatype[-1] == 'csv'):
            self.train = pd.read_csv(self.filename)
        
        elif self.datatype[-1] == 'IMD':
            
            # Read from .IMD file
            self.filename=self.filename.split('/')
            self.filename=self.filename[-1]                  # Dataset must be in IDEA working directory
            self.train = ideaLib.idea2py(database = self.filename)
            
        if self.train is None:
           messagebox.showinfo("Info",
                               "There was something wrong with the import \
                               process of IDEA database to Pandas dataframe")
        elif self.train.empty:
          messagebox.showinfo("Info","You selected an empty IDEA database")
            # pd.set_option('display.max_columns', None)
            # pd.set_option("display.float_format",lambda x:"%.4f" % x)

        if self.datatype[-1] == 'csv' or 'IMD':
            
            self.train.columns = map(str.lower, self.train.columns)

            if "week" in self.train:                
                self.ts_tot_orders = self.train.groupby(['week'])['num_orders'].sum()
            else:
                self.ts_tot_orders = self.train.groupby(['date'])['sales'].sum().reset_index()
                self.ts_tot_orders['date'] = pd.to_datetime(self.ts_tot_orders['date'])
                # self.ts_tot_orders['date']=self.ts_tot_orders['date'].map(dt.datetime.toordinal)
                self.ts_tot_orders = self.ts_tot_orders.set_index(['date'])
                self.ts_tot_orders = self.ts_tot_orders.iloc[:,-1]
                
            self.y_train = self.train.iloc[:,-1]
            self.x_train = self.train.iloc[:,0:-1]
            
            if 'id' in self.x_train:
                self.x_train = self.x_train.drop(['id'], axis= 1)
            if 'date' in self.x_train:
                self.x_train['date'] = pd.to_datetime(self.x_train['date'])
                # self.x_train['date']=self.x_train['date'].map(dt.datetime.toordinal)
                self.x_train = self.x_train.set_index(['date'])
            
        else :
            messagebox.showerror('Error', 'Invalid Data Type')
        
    def load_test(self):
        
        
        self.filename = filedialog.askopenfilename(initialdir="/",
                        title="Select a File",
                        filetypes=(("Excel files", ".IMD*"), ("all files", 
                                                               "*.*"),
                                   ("Excel files", ".csv*")))
        
        self.datatype = self.filename.split('.')
        if (self.datatype[-1] == 'csv'):
            self.test = pd.read_csv(self.filename)	
        
        elif self.datatype[-1] == 'IMD':
            
            # Read from .IMD file
            self.filename=self.filename.split('/')
            self.filename=self.filename[-1]                  # Dataset must be in IDEA working directory
            self.test = ideaLib.idea2py(database = self.filename)
            
        if self.test is None:
           messagebox.showinfo("Info",
                               "There was something wrong with the import process of IDEA database to Pandas dataframe")
        elif self.test.empty:
          messagebox.showinfo("Info","You selected an empty IDEA database")
        if self.datatype[-1] == 'IMD' or 'csv':
            self.test.columns = map(str.lower, self.test.columns)
            self.test = self.test.drop(['id'], axis= 1)
            if 'date' in self.test:
                self.test['date'] = pd.to_datetime(self.test['date'])
                # self.test['date']=self.test['date'].map(dt.datetime.toordinal)
                self.test = self.test.set_index(['date'])
            
            self.x_test = self.test.copy()

        else :
            messagebox.showerror('Error', 'Invalid Data Type')
            
    def run_ml(self):
        
        if self.var.get() == 0:
            messagebox.showinfo('Info','Please select a Model')
        
        elif self.Entry_knn.get().isdigit() == False:
            messagebox.showerror('Error','Type a number for n_neighbours')
        elif self.Entry_rf.get().isdigit() == False:
            messagebox.showerror('Error','Type a number for n_estimators')
        else:
            # sc = StandardScaler()
            # self.x_test = sc.fit_transform(self.test.values)
            # self.x_test = pd.DataFrame(self.x_test, 
            #                            index=self.test.index, 
            #                            columns=self.test.columns)
            # week = self.test['week']
            # self.x_test = self.x_test.drop(['week'], axis = 1)
            # self.x_test = self.x_test.drop(['id'], axis = 1)
            # self.x_test['week'] = week
            
            # self.x_train = sc.fit_transform(self.train.values)
            # self.x_train = pd.DataFrame(self.x_train, 
            #                            index=self.train.index,
            #                            columns=self.train.columns)
            # week = self.train['week']
            # self.x_train = self.x_train.drop(['week'], axis = 1)
            # self.x_train = self.x_train.drop(['id'], axis = 1)
            # self.x_train['week'] = week
            
            
            radioN = self.var.get()
            if radioN == 1:
                self.Linearregression()
            elif radioN == 2:
                n_neighbours = int(self.Entry_knn.get())
                self.Kneighborsregressor(n_neighbours)
            elif radioN == 3:
                self.Decisiontreeregressor()
            else:
                n_estimators = int(self.Entry_rf.get())
                self.Randomforestregressor(n_estimators)
        
    def Linearregression(self):

        lr = LinearRegression()
        lr.fit(self.x_train, self.y_train)
        
        pred = lr.predict(self.x_test)
        pred = pd.DataFrame(pred)
        # predictions = pd.merge(self.x_test, pred, left_index=True,
        #                        right_index=True, how='inner')
        x_test = self.x_test.reset_index()
        predictions = pd.concat([x_test, pred], axis=1)
        predictions['num_orders'] = predictions[0]
        predictions = predictions.drop([0], axis=1)
        print("predictions\n",predictions)
        if 'week' in predictions:
            ts_tot_pred = predictions.groupby(['week'])['num_orders'].sum()
            ts_tot_pred = pd.DataFrame(ts_tot_pred)
        
        else:
            ts_tot_pred = pd.DataFrame(predictions)
            ts_tot_pred = predictions.groupby(['date'])['num_orders'].sum()
        print("ts_tot_pred\n",ts_tot_pred)
        
        fig = Figure(figsize=(5, 5), dpi=100)
        fig.add_subplot(111).plot(self.ts_tot_orders, color= 'Blue')
        fig.add_subplot(111).plot(ts_tot_pred, color= 'Red')
        
        ideaLib.py2idea(dataframe= ts_tot_pred, 
                        databaseName= 'ts_tot_pred_linear',
                        client= client)
        
        if self.is_canvas_ml == 1:
            self.canvas.get_tk_widget().pack_forget() 
        
        self.canvas = FigureCanvasTkAgg(fig, master =self.ml)  # A tk.DrawingArea.
        self.canvas.get_tk_widget().pack(side=RIGHT)
        self.canvas.draw()        
        self.is_canvas_ml = 1
    
    def Kneighborsregressor(self, n_neighbours):
        
        knn = KNeighborsRegressor(n_neighbours)  
        knn.fit(self.x_train, self.y_train)
        pred = knn.predict(self.x_test)
        pred = pd.DataFrame(pred)
        
        x_test = self.x_test.reset_index()
        predictions = pd.concat([x_test, pred], axis=1)
        predictions['num_orders'] = predictions[0]
        predictions = predictions.drop([0], axis=1)
        print("predictions\n",predictions)
        if 'week' in predictions:
            ts_tot_pred = predictions.groupby(['week'])['num_orders'].sum()
            ts_tot_pred = pd.DataFrame(ts_tot_pred)
        
        else:
            ts_tot_pred = pd.DataFrame(predictions)
            ts_tot_pred = predictions.groupby(['date'])['num_orders'].sum()
        print("ts_tot_pred\n",ts_tot_pred)
        
        
        fig = Figure(figsize=(5, 5), dpi=100)
        fig.add_subplot(111).plot(self.ts_tot_orders, color= 'Blue')
        fig.add_subplot(111).plot(ts_tot_pred, color= 'Red')
        ideaLib.py2idea(dataframe= ts_tot_pred, 
                        databaseName= 'ts_tot_pred_knn',
                        client= client)
        
        if self.is_canvas_ml == 1:
            self.canvas.get_tk_widget().pack_forget() 
        
        self.canvas = FigureCanvasTkAgg(fig, master =self.ml)  # A tk.DrawingArea.
        self.canvas.get_tk_widget().pack(side=RIGHT)
        self.canvas.draw()        
        self.is_canvas_ml = 1
    
    def Decisiontreeregressor(self):
        
        dt = DecisionTreeRegressor()
        dt.fit(self.x_train, self.y_train)
        pred = dt.predict(self.x_test)
        pred = pd.DataFrame(pred)
        
        x_test = self.x_test.reset_index()
        predictions = pd.concat([x_test, pred], axis=1)
        predictions['num_orders'] = predictions[0]
        predictions = predictions.drop([0], axis=1)
        print("predictions\n",predictions)
        if 'week' in predictions:
            ts_tot_pred = predictions.groupby(['week'])['num_orders'].sum()
            ts_tot_pred = pd.DataFrame(ts_tot_pred)
        
        else:
            ts_tot_pred = pd.DataFrame(predictions)
            ts_tot_pred = predictions.groupby(['date'])['num_orders'].sum()
        print("ts_tot_pred\n",ts_tot_pred)
        
        
        if self.is_canvas_ml == 1:
            self.canvas.get_tk_widget().pack_forget() 
        
        fig = Figure(figsize=(5, 5), dpi=100)
        fig.add_subplot(111).plot(self.ts_tot_orders, color= 'Blue')
        fig.add_subplot(111).plot(ts_tot_pred, color= 'Red')
        ideaLib.py2idea(dataframe= ts_tot_pred, 
                        databaseName= 'ts_tot_pred_dt',
                        client= client)
        
        
        self.canvas = FigureCanvasTkAgg(fig, master =self.ml)  # A tk.DrawingArea.
        self.canvas.get_tk_widget().pack(side=RIGHT)
        self.canvas.draw()        
        self.is_canvas_ml = 1
    
    def Randomforestregressor(self, n_estimators):
        
        rf = RandomForestRegressor(n_estimators)
        rf.fit(self.x_train, self.y_train)
        pred = rf.predict(self.x_test)
        pred = pd.DataFrame(pred)
        
        x_test = self.x_test.reset_index()
        predictions = pd.concat([x_test, pred], axis=1)
        predictions['num_orders'] = predictions[0]
        predictions = predictions.drop([0], axis=1)
        print("predictions\n",predictions)
        if 'week' in predictions:
            ts_tot_pred = predictions.groupby(['week'])['num_orders'].sum()
            ts_tot_pred = pd.DataFrame(ts_tot_pred)
        
        else:
            ts_tot_pred = pd.DataFrame(predictions)
            ts_tot_pred = predictions.groupby(['date'])['num_orders'].sum()
        print("ts_tot_pred\n",ts_tot_pred)
              
        
        fig = Figure(figsize=(5, 5), dpi=100)
        fig.add_subplot(111).plot(self.ts_tot_orders, color= 'Blue')
        fig.add_subplot(111).plot(ts_tot_pred, color= 'Red')
        ideaLib.py2idea(dataframe= ts_tot_pred, 
                        databaseName= 'ts_tot_pred_rf',
                        client= client)
        
        if self.is_canvas_ml == 1:
            self.canvas.get_tk_widget().pack_forget() 
        
        self.canvas = FigureCanvasTkAgg(fig, master =self.ml)  # A tk.DrawingArea.
        self.canvas.get_tk_widget().pack(side=RIGHT)
        self.canvas.draw()        
        self.is_canvas_ml = 1
        
    
# Tooltip
class CreateToolTip(object):
    '''
    create a tooltip for a given widget
    '''
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)

    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       relief='solid', borderwidth=1,
                       font=("times", "8", "normal"))
        label.pack(ipadx=1)

    def close(self, event=None):
        if self.tw:
            self.tw.destroy()    
    

root = tk.Tk() 
root.title("Demand Forcasting") 
root.geometry("800x800")
tabControl = ttk.Notebook(root) 
  
tab1 = ttk.Frame(tabControl) 
tab2 = ttk.Frame(tabControl) 
tab3 = ttk.Frame(tabControl) 
tab4 = ttk.Frame(tabControl) 
  
tabControl.add(tab1, text ='ARIMA') 
tabControl.add(tab2, text ='ML')  
tabControl.add(tab3, text ='Help') 
tabControl.pack(expand = 1, fill ="both") 

mywin = UI(tab1,tab2,tab3)

root.mainloop()   