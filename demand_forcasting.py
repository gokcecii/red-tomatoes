import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
from statsmodels.tsa.arima_model import ARIMA

# Read from CSV
# center_info = pd.read_csv('D://MED IDEA//project//red_project//fulfilment_center_info.csv')
# meal_info = pd.read_csv('D://MED IDEA//project//red_project//meal_info.csv')
# test_data = pd.read_csv('D://MED IDEA//project//red_project//test.csv')
# train_data = pd.read_csv('D://MED IDEA//project//red_project//train.csv')

# Read from IMD
class UI:
    
    def __init__(self, win,arıma,ml,help_):  
        
        self.df = None
        
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
                       row = 1)
        
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
        self.btnadfuller.grid(column = 3, 
                               row = 2, 
                               padx = 5,
                               pady = 5)
        
        
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
        
        self.lbladfuller.grid(column = 4, 
                               row = 2, 
                               padx = 5,
                               pady = 5)
        
        
        # Arıma win
        
        self.title1 = Label(arıma, text ="Model", font='Helvetica 9 bold')
        self.title1.grid(column =1, row =1, pady =10)
        self.title2 = Label(arıma, text ="Order", font='Helvetica 9 bold')
        self.title2.grid(column =2, row =1, pady =10)
        
        self.var = IntVar()
        self.R1 = Radiobutton(arıma, text="AR", variable= self.var, 
                              value =1,
                              command=self.sel)
        self.R1.grid(column =1,
                     row =2)
        self.R2 = Radiobutton(arıma, text="MA", variable= self.var, 
                              value =2,
                              command=self.sel)
        self.R2.grid(column =1,
                     row =3)
        self.R3 = Radiobutton(arıma, text="ARMA", variable= self.var, 
                              value =3,
                              command=self.sel)
        self.R3.grid(column =1,
                     row =4)
        self.R3 = Radiobutton(arıma, text="ARIMA", variable= self.var, 
                              value =4,
                              command=self.sel)
        self.R3.grid(column =1,
                     row =5)
        
        
        self.Entry1 = Entry(arıma, width =5)
        self.Entry1.grid(column =2, row =2)
        self.Entry2 = Entry(arıma, width =5)
        self.Entry2.grid(column =2, row =3)
        self.Entry3 = Entry(arıma, width =5)
        self.Entry3.grid(column =2, row =5)
        
        self.btn_run = Button(arıma, text ="Run", width =12 ,height =1, command=self.run)
        self.btn_run.grid(column =3, row =3, padx =25)
    
    def load(self):
        
        self.filename = filedialog.askopenfilename(initialdir="/",
                        title="Select a File",
                        filetypes=(("Excel files", "*.IMD*"), ("all files", 
                                                               "*.*")))
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
        else:
            pd.set_option('display.max_columns', None)
            pd.set_option("display.float_format",lambda x:"%.2f" % x)
            self.df = self.df.astype({"CENTER_TYPE": str,"CATEGORY": str,
                                          "CUISINE": str})
            self.df.columns = map(str.lower, self.df.columns)
                 
    
    def Data_Analyze(self):
        
        weekly_orders = self.df.groupby(['week'])['num_orders'].sum().reset_index()
        weekly_orders = pd.DataFrame(weekly_orders)
        
        plt.plot(weekly_orders['week'], weekly_orders['num_orders'])
        plt.xlabel('weeks')
        plt.ylabel('orders')
        plt.title('Weekly Orders')
        # plt.show(block = False)
        plt.savefig('plots/Weekly Orders.png')
        plt.close()
        
        center_id = self.df.groupby(['center_id'])['num_orders'].sum().reset_index()
        center_id = pd.DataFrame(center_id)
        
        plt.bar(center_id['center_id'], center_id['num_orders'])
        plt.xlabel('center_id')
        plt.ylabel('orders')
        plt.title('Center_id Orders')
        plt.savefig('plots/Center_id Orders.png')
        plt.close()
        
        meal_id = self.df.groupby(['meal_id'])['num_orders'].sum().reset_index()
        meal_id = pd.DataFrame(meal_id)
        
        plt.bar(meal_id['meal_id'], meal_id['num_orders'], width=6)
        plt.xlabel('meal_id')
        plt.ylabel('orders')
        plt.title('meal_id Orders')
        plt.savefig('plots/meal_id Orders.png')
        plt.close()
        
        # category = self.df.groupby(['category'])['num_orders'].sum().reset_index()
        # category = pd.DataFrame(category)
        
        # plt.bar(category['category'], category['num_orders'])
        # # plt.xticks(rotation=90)
        # plt.xlabel('category')
        # plt.ylabel('orders')
        # plt.title('category Orders')
        # plt.savefig('plots/category Orders.png')
        # plt.close()
        
        
        # category_cuisine = self.df.groupby(['category','cuisine'])['num_orders'].sum().reset_index()
        # category_cuisine = pd.DataFrame(category_cuisine)
        # category_cuisine['meal'] = category_cuisine['category'] + ', ' + category_cuisine['cuisine']
        
        # plt.bar(category_cuisine['meal'], category_cuisine['num_orders'])
        # # plt.xticks(rotation=90)
        # plt.xlabel('category_cuisine')
        # plt.ylabel('orders')
        # plt.title('category_cuisine Orders')
        # plt.savefig('plots/category_cuisine Orders.png')
        # plt.close()
        
        
        plt.scatter(self.df['checkout_price'],self.df['num_orders'],s=2)
        plt.xlabel('checkout_price')
        plt.ylabel('orders')
        plt.savefig('plots/checkout_price.png')
        plt.ioff()
        
        plt.scatter(self.df['base_price'],self.df['num_orders'],s=2)
        plt.xlabel('base_price')
        plt.ylabel('orders')
        plt.savefig('plots/base_price.png')
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
        # plt.savefig('plots/Order Type.png')
        
        
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
        plt.savefig('plots/seasonality.png')
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

        
    
    def sel(self):
       self.selection = "You selected the option " + str(self.var.get())
       label.config(text = selection)
        
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
            dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
            for key,value in dftest[4].items():
                dfoutput['Critical Value (%s)'%key] = value

            self.lbladfuller['text'] = dfoutput

            
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
            plt.show()
            
        # check stationary: mean, variance(std)and adfuller test
        check_mean_std()
        check_adfuller(self.indexedDataset.num_orders)
        
        # Moving average method
        window_size = 6
        moving_avg = self.indexedDataset.rolling(window_size).mean()
        plt.figure(figsize=(22,10))
        plt.plot(self.indexedDataset, color = "red",label = "Original")
        plt.plot(moving_avg, color='black', label = "moving_avg_mean")
        plt.title("Mean Temperature of Bindukuri Area")
        plt.xlabel("Date")
        plt.ylabel("Mean Temperature")
        plt.legend()
        plt.show()
        
        self.ts_moving_avg_diff = self.indexedDataset - moving_avg
        self.ts_moving_avg_diff.dropna(inplace=True) # first 6 is nan value due to window size
        
        # check stationary: mean, variance(std)and adfuller test
        check_mean_std()
        check_adfuller(self.ts_moving_avg_diff.num_orders)
        
    def run(self):
        
        ar = ARIMA(self.ts_moving_avg_diff['num_orders'], order=(1,1,0))
        # diff_ARIMA = (ar_fit.fittedvalues - self.ts_moving_avg_diff['num_orders'])
        # diff_ARIMA.dropna(inplace=True)
        ar_fitted = ar.fit(disp=0)
        forecast = ar_fitted.predict(1, 250)
        
        # plt.plot(self.ts_moving_avg_diff)
        plt.plot(self.ts_moving_avg_diff)
        plt.plot(forecast)
        # plt.plot(ar_fit.fittedvalues, color='red')
        # plt.title('AR Model RSS: %.4F'%sum((diff_ARIMA)**2))
        plt.show()


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

