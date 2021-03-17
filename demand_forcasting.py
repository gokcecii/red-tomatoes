# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 09:54:00 2021

@author: kenan
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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

dirname = os.path.dirname(__file__)

# Read from CSV
# center_info = pd.read_csv('D://MED IDEA//project//red_project//fulfilment_center_info.csv')
# meal_info = pd.read_csv('D://MED IDEA//project//red_project//meal_info.csv')
# test_data = pd.read_csv('D://MED IDEA//project//red_project//test.csv')
# train_data = pd.read_csv('D://MED IDEA//project//red_project//train.csv')

# Read from IMD
class UI:
    
    def __init__(self, win,arıma,ml,help_):  
        
        self.df = None
        self.arıma = arıma
        self.ml = ml
        
        # LABELFRAME 1
        self.labelframe1 = LabelFrame(win, 
                                      text = "Upload Data", 
                                      height = 100)
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
        
        
        #LabelFrame 2
        self.labelframe2 = LabelFrame(win, 
                                      text = "Analyze", 
                                      height = 100)
        self.labelframe2.pack(fill = "both", 
                              pady = 5, 
                              padx = 5)
        self.labelframe2.pack_propagate(0)
        
        self.btn2 = Button(self.labelframe2, 
                           text = "Analyze", 
                           command = self.Data_Analyze)
        self.btn2.grid(column = 1, 
                       row = 1,
                       padx = 5)
        
        self.btn_correlation = Button(self.labelframe2, 
                                   text = "Correlation", 
                                   command = self.corr,
                                   width = 25,
                                   height = 1)
        self.btn_correlation.grid(column = 1, 
                               row = 2, 
                               padx = 5,
                               pady = 5)
        self.btnadfuller = Button(self.labelframe2, 
                                   text = "Adfuller Test", 
                                   command = self.adfuller,
                                   width = 25,
                                   height = 1)
        self.btnadfuller.grid(column = 2, 
                               row = 2, 
                               padx = 5,
                               pady = 5)
        
        self.btn_moving_avg = Button(self.labelframe2,
                                     text = 'Moving Average',
                                     command = self.moving_average,
                                     width = 25,
                                     height = 1)
        
        self.btn_moving_avg.grid(column = 4,
                                 row = 2, 
                                 padx = 5,
                                 pady = 5)
        
        self.btn_trend = Button(self.labelframe2, 
                                   text = "Trend", 
                                   command = self.trend,
                                   width = 25,
                                   height = 1)        
        self.btn_trend.grid(column = 2, 
                               row = 1, 
                               padx = 5)
        
        
        
        self.ismov = 0 # did not call moving average
        
               #LabelFrame 3
        self.labelframe3 = LabelFrame(win, 
                                      text = "Result", 
                                      height = 100)
        self.labelframe3.pack(fill = "both", 
                              pady = 5, 
                              padx = 5)
        
        self.labelframe2.pack_propagate(0)
        
        self.lbladfuller = Label(self.labelframe3, 
                                 text="")
        
        self.lbladfuller.grid(column = 1, 
                               row = 1, 
                               padx = 5,
                               pady = 5)
        self.lblinfo = Label(self.labelframe3, 
                                 text="")
        
        self.lblinfo.grid(column = 5, 
                               row = 1, 
                               padx = 5,
                               pady = 5)
        
        
        # TAB4 - HELP
        # help data tab
        self.labelframe4 = LabelFrame(help_, 
                                      text = "DATA TAB", 
                                      height = 400)
        self.labelframe4.pack(fill = "both", 
                              pady = 5, 
                              padx = 5)
        
        self.labelframe4.pack_propagate(0)
    
        
        self.upload_text = Label(self.labelframe4, 
                              text = "\nBROWSE BUTTON\nLoads a dataset (.IMD or .csv extensions are allowed.)\n----------\nANALYZE BUTTON\nCreates a new folder named as \"plots\" and saves the resultant plots into the folder.\nCorresponging plots are base_price.png, Center_id Orders.png, checkout_price.png, meal_id Orders.png, seasonality.png, Weekly Orders.png.\n---------\nCORRELATION BUTTON\nShows the correlation plot.\n----------\nADFULLER TEST BUTTON\nDetermines if time series data is stationary or not.\n----------\nRESULT SECTION\nAugmented Dickey-Fuller (ADF) test is used.\nADF test is a type of unit root test. A unit root test determines how strongly a time series is defined by a trend.\nThe null hypothesis of the test is that the time series can be represented by a unit root, that it is not stationary (has some time-dependent structure). \nThe alternate hypothesis (rejecting the null hypothesis) is that the time series is stationary.\nFor a time series to be stationary, ADF test must result as follows:\na. If p-value > 0.05: Fail to reject the null hypothesis (H0), the data has a unit root and is non-stationary.\n  If p-value <= 0.05: Reject the null hypothesis (H0), the data does not have a unit root and is stationary.\nb) Critical values at 1%, 5%, 10% confidence intervals should be as close as possible to the Test Statistics.")
        self.upload_text.pack(side="left")
        
        # help arima tab
        self.labelframe5 = LabelFrame(help_, 
                                      text = "ARIMA TAB", 
                                      height = 80)
        self.labelframe5.pack(fill = "both", 
                              pady = 5, 
                              padx = 5)
        
        self.labelframe5.pack_propagate(0)
        self.arima_text = Label(self.labelframe5, 
                              text = "--> Possible methods are AR, MA, ARMA, ARIMA for time series analysis. Example: From the ACF graph, we see that curve touches y=0.0 line at x=0.\n Thus, from theory, Q = 0 From the PACF graph, we see that curve touches  y=0.0 line at x=1. Thus, from theory, P = 1")
        self.arima_text.pack(side="left")
        
        # ml help tab
        self.labelframe6 = LabelFrame(help_, 
                                      text = "ML TAB", 
                                      height = 80)
        self.labelframe6.pack(fill = "both", 
                              pady = 5, 
                              padx = 5)
        
        self.labelframe6.pack_propagate(0)
        self.ml_text = Label(self.labelframe6, 
                              text = "--> Forecasting with Machine Learning")
        self.ml_text.pack(side="left")
        


        
        # Arıma win
        
        self.title1 = Label(arıma, text ="Model",
                            font='Helvetica 9 bold').place(x=5, y=0)
        
        self.title2 = Label(arıma, text ="Order", 
                            font='Helvetica 9 bold').place(x=100, y=0)
        
        self.var = IntVar()
        self.R1 = Radiobutton(arıma, text="AR", variable= self.var, 
                              value =1).place(x=5, y=20)
        
        self.R2 = Radiobutton(arıma, text="MA", variable= self.var, 
                              value =2).place(x=5, y=40)
        
        self.R3 = Radiobutton(arıma, text="ARMA", variable= self.var, 
                              value =3).place(x=5, y=60)
        
        self.R3 = Radiobutton(arıma, text="ARIMA", variable= self.var, 
                              value =4).place(x=5, y=80)
        
        
        self.Entry1 = Entry(arıma, width =5)
        self.Entry1.insert(0,1)
        self.Entry1.place(x=100, y=20)
        self.Entry2 = Entry(arıma, width =5)
        self.Entry2.insert(0,1)
        self.Entry2.place(x=100, y=40)
        
        self.ar_tool = Button(arıma, text ="?", width =1 ,height =1, 
                            font='Helvetica 9 bold')
        
        self.lbl_ar_tooltip = CreateToolTip(self.ar_tool, "p for AR order")
        self.ar_tool.place(x=140, y=20)
        self.ma_tool = Button(arıma, text ="?", width =1 ,height =1, 
                            font='Helvetica 9 bold')
        
        self.lbl_ma_tooltip=CreateToolTip(self.ma_tool, "q for MA order")
        self.ma_tool.place(x=140, y=40)
        self.btn_run = Button(arıma, text ="Run", width =12 ,height =1, 
                              command=self.run).place(x=100, y=80)
        
        self.is_canvas_arıma = 0
        self.is_canvas_ml = 0
        
        # ML Win
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
        
        self.var = IntVar()
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
        
        # self.ar_tool = Button(ml, text ="?", width =1 ,height =1, 
        #                     font='Helvetica 9 bold')
        
        # self.lbl_ar_tooltip = CreateToolTip(self.ar_tool, "p for AR order")
        # self.ar_tool.place(x=140, y=20)
        # self.ma_tool = Button(arıma, text ="?", width =1 ,height =1, 
        #                     font='Helvetica 9 bold')
        
        # self.lbl_ma_tooltip=CreateToolTip(self.ma_tool, "q for MA order")
        # self.ma_tool.place(x=140, y=40)
        
        self.btn_run_ml = Button(ml, text ="Run", width =12 ,height =1, 
                              command=self.run_ml).place(x=50, y=150)
        
        
        
        pd.set_option('display.max_columns', None)
        pd.set_option("display.float_format",lambda x:"%.4f" % x)
        
    
    def load(self):
        
        self.filename = filedialog.askopenfilename(initialdir="/",
                        title="Select a File",
                        filetypes=(("Excel files", ".IMD*"), ("all files", 
                                                               "*.*"),
                                   ("Excel files", ".csv*")))
        
        self.datatype = self.filename.split('.')
        if (self.datatype[-1] == 'csv'):
            messagebox.showinfo('Info','Please try again later')
            # self.df = pd.read_csv(self.filename)
            # self.df = client.OpenDatabase(self.df)	
        
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
            # pd.set_option('display.max_columns', None)
            # pd.set_option("display.float_format",lambda x:"%.4f" % x)
            self.df = self.df.astype({"CENTER_TYPE": str,"CATEGORY": str,
                                          "CUISINE": str})
            self.df.columns = map(str.lower, self.df.columns)
        elif self.datatype[-1] == 'csv':
             self.df.columns = map(str.lower, self.df.columns)
        else :
            messagebox.showerror('Error', 'Invalid Data Type')
                 
    
    def Data_Analyze(self):
        
        weekly_orders = self.df.groupby(['week'])['num_orders'].sum().reset_index()
        weekly_orders = pd.DataFrame(weekly_orders)
        
        plt.plot(weekly_orders['week'], weekly_orders['num_orders'])
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
        #     center_type = data.groupby(['week','center_type'])['num_orders'].sum().reset_index()
        #     plt.plot(center_type['week'],center_type['num_orders'])
        # plt.legend(lis)
        # plt.savefig(dirname + '/plots/Order Type.png')
        
        
        ts = self.df.groupby(['week'])['num_orders'].sum().reset_index()
        season_df = ts.copy()

        season_df['week_'] = ts['week'] % 52
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
        
        new_data = self.df.groupby(['week'])['num_orders'].sum().reset_index()
        # new_data['date'] = pd.date_range('2020-01-01', periods=145, freq='W')
        # new_data.drop(columns = 'week', axis = 1, inplace=True)
        # new_data.set_index('date',inplace=True)
        
        
        # result = adfuller(new_data.num_orders.dropna())
        # print('ADF Statistic: %f' % result[0])
        # print('p-value: %f' % result[1])
        
    
    def corr(self):
        new_data = self.df.groupby(['week'])['num_orders'].sum().reset_index()
        autocorrelation_plot(new_data['num_orders'])
        plt.show(block = False)

    
    # def sel(self):
       # self.selection = "You selected the option " + str(self.var.get())
       # label.config(text = selection)
        
    def adfuller(self):
        
        self.indexedDataset= self.df.groupby(['week'])['num_orders'].sum().reset_index()
        self.indexedDataset.set_index(['week'],inplace=True)

        #Perform Augmented Dickey–Fuller test:
        # check_adfuller
        def check_adfuller(ts):
            # Dickey-Fuller test
            print('Results of Dickey Fuller Test:')
            dftest = adfuller(ts, autolag='AIC')
            print(dftest)
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
        def check_mean_std():
            #Rolling statistics
            ts = self.indexedDataset
            rolmean = ts.rolling(6).mean()
            rolstd = ts.rolling(6).std()
            plt.figure(figsize=(22,10))   
            orig = plt.plot(ts, color='red',label='Original')
            mean = plt.plot(rolmean, color='black', label='Rolling Mean')
            std = plt.plot(rolstd, color='green', label = 'Rolling Std')
            plt.xlabel("Date")
            plt.ylabel("Mean Temperature")
            plt.title('Rolling Mean & Standard Deviation')
            plt.legend()
            plt.show(block = False)
            
        # check stationary: mean, variance(std)and adfuller test
        if self.ismov == 0:
            check_mean_std()
            check_adfuller(self.indexedDataset.num_orders)
        
        # plt.figure(figsize=(22,10))
        # plt.plot(self.indexedDataset, color = "red",label = "Original")
        # plt.plot(moving_avg, color='black', label = "moving_avg_mean")
        # plt.title("Mean Temperature of Bindukuri Area")
        # plt.xlabel("Date")
        # plt.ylabel("Mean Temperature")
        # plt.legend()
        # plt.show()
        
        # check stationary: mean, variance(std)and adfuller test
        if self.ismov == 1:
            check_mean_std()
            check_adfuller(self.ts_moving_avg_diff.num_orders)
        
    
    def moving_average(self):
        self.ismov = 1 #  moving average called
        # Moving average method
        window_size = 6
        moving_avg = self.indexedDataset.rolling(window_size).mean()
        self.ts_moving_avg_diff = self.indexedDataset - moving_avg
        self.ts_moving_avg_diff.dropna(inplace=True) # first 6 is nan value due to window size

    def trend(self):
        x = self.df.groupby(['week'])['num_orders'].sum().reset_index()
        x['date'] = pd.date_range('2020-01-01', periods=145, freq='W')
        x.drop(columns = 'week', axis = 1, inplace=True)
        x.set_index('date',inplace=True)
        x = x.astype(float) # force float
        decomposition = seasonal_decompose(x)
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
        
        if self.var.get() == 0:
            messagebox.showinfo('Info','Please select a Model')
        
        elif self.Entry1.get().isdigit() == False:
            messagebox.showerror('Error','Type a number for orders')
        elif self.Entry2.get().isdigit() == False:
            messagebox.showerror('Error','Type a number for orders')
        else:
            radioN = self.var.get()
            if radioN == 1:
                p = int(self.Entry1.get())
                q = 0
                self.arıma_model(p,q)
            elif radioN == 2:
                p = 0
                q = int(self.Entry2.get())
                self.arıma_model(p,q)
            elif radioN == 3:
                p = int(self.Entry1.get())
                q = int(self.Entry2.get())
                self.arma_model(p,q)
            else:
                p = int(self.Entry1.get())
                q = int(self.Entry2.get())   
                self.arıma_model(p,q)
    
           
        
    def arıma_model(self,p,q):

        if self.is_canvas_arıma == 1:
            self.canvas.get_tk_widget().pack_forget()
        
        ar = ARIMA(self.ts_moving_avg_diff['num_orders'], order=(p,1,q))
        # diff_ARIMA = (ar_fit.fittedvalues - self.ts_moving_avg_diff['num_orders'])
        # diff_ARIMA.dropna(inplace=True)
        ar_fitted = ar.fit(disp=0)
        forecast = ar_fitted.predict(100, 180)
        
        # plt.plot(ar_fit.fittedvalues, color='red')
        # plt.title('AR Model RSS: %.4F'%sum((diff_ARIMA)**2))

        
        fig = Figure(figsize=(6, 6), dpi=100)
        fig.add_subplot(111).plot(self.ts_moving_avg_diff)
        fig.add_subplot(111).plot(forecast)
        

        self.canvas = FigureCanvasTkAgg(fig, master =self.arıma)  # A tk.DrawingArea.
        self.canvas.get_tk_widget().pack(side=RIGHT)
        self.canvas.draw()        
        self.is_canvas_arıma = 1
        
        
    def arma_model(self,p,q):
        
        if self.is_canvas_arıma == 1:
            self.canvas.get_tk_widget().pack_forget()          
        
        ar = ARMA(self.ts_moving_avg_diff['num_orders'], order=(p,q))
        # diff_ARIMA = (ar_fit.fittedvalues - self.ts_moving_avg_diff['num_orders'])
        # diff_ARIMA.dropna(inplace=True)
        ar_fitted = ar.fit(disp=0)
        forecast = ar_fitted.predict(100, 180)
        
        # plt.plot(ar_fit.fittedvalues, color='red')
        # plt.title('AR Model RSS: %.4F'%sum((diff_ARIMA)**2))

        fig = Figure(figsize=(6, 6), dpi=100)
        fig.add_subplot(111).plot(self.ts_moving_avg_diff)
        fig.add_subplot(111).plot(forecast)
        

        self.canvas = FigureCanvasTkAgg(fig, master =self.arıma)  # A tk.DrawingArea.
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
                               "There was something wrong with the import process of IDEA database to Pandas dataframe")
        elif self.train.empty:
          messagebox.showinfo("Info","You selected an empty IDEA database")
            # pd.set_option('display.max_columns', None)
            # pd.set_option("display.float_format",lambda x:"%.4f" % x)

        if self.datatype[-1] == 'csv' or 'IMD':
            
            self.train.columns = map(str.lower, self.train.columns)
            self.ts_tot_orders = self.train.groupby(['week'])['num_orders'].sum()
            
            self.x_train = self.train.drop(['num_orders'], axis=1).values
            self.y_train = self.train['num_orders'].values
            
            
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
            
            self.x_test = self.test
            

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
        
        predictions = pd.merge(self.x_test, pred, left_index=True, right_index=True, how='inner')
        predictions['num_orders'] = predictions[0]
        predictions = predictions.drop([0], axis=1)
        ts_tot_pred = predictions.groupby(['week'])['num_orders'].sum()
        ts_tot_pred = pd.DataFrame(ts_tot_pred)
        
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
        
        predictions = pd.merge(self.x_test, pred, left_index=True, right_index=True, how='inner')
        predictions['num_orders'] = predictions[0]
        predictions = predictions.drop([0], axis=1)
        ts_tot_pred = predictions.groupby(['week'])['num_orders'].sum()
        ts_tot_pred = pd.DataFrame(ts_tot_pred)
        
        
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
        
        predictions = pd.merge(self.x_test, pred, left_index=True, right_index=True, how='inner')
        predictions['num_orders'] = predictions[0]
        predictions = predictions.drop([0], axis=1)
        ts_tot_pred = predictions.groupby(['week'])['num_orders'].sum()
        ts_tot_pred = pd.DataFrame(ts_tot_pred)
        
        
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
        
        predictions = pd.merge(self.x_test, pred, left_index=True, right_index=True, how='inner')
        predictions['num_orders'] = predictions[0]
        predictions = predictions.drop([0], axis=1)
        ts_tot_pred = predictions.groupby(['week'])['num_orders'].sum()
        ts_tot_pred = pd.DataFrame(ts_tot_pred)
              
        
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
root.title("Tab Widget") 
root.geometry("800x400")
tabControl = ttk.Notebook(root) 
  
tab1 = ttk.Frame(tabControl) 
tab2 = ttk.Frame(tabControl) 
tab3 = ttk.Frame(tabControl) 
tab4 = ttk.Frame(tabControl) 
  
tabControl.add(tab1, text ='Data') 
tabControl.add(tab2, text ='Arıma')
tabControl.add(tab3, text ='ML')  
tabControl.add(tab4, text ='Help') 
tabControl.pack(expand = 1, fill ="both") 

mywin = UI(tab1,tab2,tab3,tab4)


# ttk.Label(tab1,  
#           text ="Welcome to GeeksForGeeks").grid(column = 0,  
#                                                 row = 0, 
#                                                 padx = 30, 
#                                                 pady = 30)   
# ttk.Label(tab2, 
#           text ="Lets dive into theworld of computers").grid(column = 0, 
#                                                         row = 0,  
#                                                         padx = 30, 
#                                                         pady = 30) 
  
root.mainloop()   