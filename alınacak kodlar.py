# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 15:51:13 2021

@author: kenan
"""


#%%

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler
from sklearn import metrics

result = train_data.iloc[:,1:8].values
y = train_data['num_orders'].values


x_train, x_test, y_train, y_test = train_test_split(result, y,
                                                    test_size=0.2, 
                                                    shuffle=True,
                                                    random_state=0)

# scaler=StandardScaler()

# X_train = scaler.fit_transform(x_train)
# X_test = scaler.fit_transform(x_test)

X_train = x_train
X_test = x_test

lr = LinearRegression()
lr.fit(X_train, y_train)

pred = lr.predict(X_test)

plt.plot(y_test)
plt.plot(pred)
plt.title('LinearRegression')
plt.show()

print('Root Mean Squared Error for LinearRegression:',
      np.sqrt(metrics.mean_squared_error(y_test, pred)))



#%%

from sklearn.neighbors import KNeighborsRegressor

knn = KNeighborsRegressor(n_neighbors=10)  
knn.fit(X_train, y_train)
pred = knn.predict(X_test)

plt.plot(y_test)
plt.plot(pred)
plt.title('KNeighbour')
plt.show()

print('Root Mean Squared Error for knn:', 
      np.sqrt(metrics.mean_squared_error(y_test, pred)))


#%%

from sklearn.tree import DecisionTreeRegressor

dt = DecisionTreeRegressor()
dt.fit(X_train, y_train)
pred = dt.predict(X_test)

plt.plot(y_test)
plt.plot(pred)
plt.title('DecisionTree')
plt.show()

print('Root Mean Squared Error for Dt:', np.sqrt(metrics.mean_squared_error(y_test, pred)))

#%%

from sklearn.ensemble import RandomForestRegressor 

rf = RandomForestRegressor(n_estimators=10)
rf.fit(X_train, y_train)
pred = rf.predict(X_test)

plt.plot(y_test)
plt.plot(pred)
plt.title('RandomForest')
plt.show()

print('Root Mean Squared Error for RF:', np.sqrt(metrics.mean_squared_error(y_test, pred)))



#%%

x_train = train_data.iloc[:,1:8].values
y = train_data['num_orders'].values
x_test = test_data.iloc[:,1:].values


# scaler=StandardScaler()

# X_train = scaler.fit_transform(x_train)
# X_test = scaler.fit_transform(x_test)


lr = LinearRegression()
lr.fit(x_train, y)
pred = lr.predict(x_test)

pred = pd.DataFrame(pred)

predictions = pd.merge(test_data, pred, left_index=True, right_index=True, 
                       how='inner')

predictions['pred'] = predictions[0]

predictions_group = predictions.groupby(['week'])['pred'].sum().reset_index()

plt.plot(weekly_orders['week'],weekly_orders['num_orders'])
plt.plot(predictions_group['week'],predictions_group['pred'])
plt.title('Linear Forecast')
plt.xlabel('Week')
plt.show()

#%%

knn = KNeighborsRegressor(n_neighbors=10)
knn.fit(x_train, y)
pred = knn.predict(x_test)

pred = pd.DataFrame(pred)

predictions = pd.merge(test_data, pred, left_index=True, right_index=True, 
                       how='inner')

predictions['pred'] = predictions[0]

predictions_group = predictions.groupby(['week'])['pred'].sum().reset_index()

plt.plot(weekly_orders['week'],weekly_orders['num_orders'])
plt.plot(predictions_group['week'],predictions_group['pred'])
plt.title('Kneighbour Forecast')
plt.xlabel('Week')
plt.show()

#%%

dt = DecisionTreeRegressor()
dt.fit(x_train, y)
pred = dt.predict(x_test)

pred = pd.DataFrame(pred)

predictions = pd.merge(test_data, pred, left_index=True, right_index=True, 
                       how='inner')

predictions['pred'] = predictions[0]

predictions_group = predictions.groupby(['week'])['pred'].sum().reset_index()

plt.plot(weekly_orders['week'],weekly_orders['num_orders'])
plt.plot(predictions_group['week'],predictions_group['pred'])
plt.title('DecisionTree Forecast')
plt.xlabel('Week')
plt.show()

#%%

rf = RandomForestRegressor(n_estimators=10)
rf.fit(x_train, y)
pred = rf.predict(x_test)

pred = pd.DataFrame(pred)

predictions = pd.merge(test_data, pred, left_index=True, right_index=True, 
                       how='inner')

predictions['pred'] = predictions[0]

predictions_group = predictions.groupby(['week'])['pred'].sum().reset_index()

plt.plot(weekly_orders['week'],weekly_orders['num_orders'])
plt.plot(predictions_group['week'],predictions_group['pred'])
plt.title('RandomForest Forecast')
plt.xlabel('Week')
plt.show()

#%%

num_orders = new_data['num_orders']
order_resamp_yr = num_orders.resample('A').mean()
num_order_yr = num_orders.rolling(12).mean()

ax = num_orders.plot(alpha=0.5, style='-') # store axis (ax) for latter plots
order_resamp_yr.plot(style=':', label='Resample at year frequency', ax=ax)
num_order_yr.plot(style='--', label='Rolling average (smooth), window size=12', ax=ax)
ax.legend()

from statsmodels.tsa.seasonal import seasonal_decompose
x = new_data['num_orders']

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

#%%

from pandas.plotting import autocorrelation_plot


autocorrelation_plot(new_data['num_orders'])
plt.show()

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import statsmodels.api as sm

fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(new_data['num_orders'].dropna(),lags=40,ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(new_data['num_orders'].dropna(),lags=40,ax=ax2)
plt.show()


#%%
# Ar MA ARIMA

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

plt.rcParams.update({'figure.figsize':(9,7), 'figure.dpi':120})

# Import data

# Original Series
fig, axes = plt.subplots(3, 2, sharex=True)
axes[0, 0].plot(new_data.num_orders); axes[0, 0].set_title('Original Series')
plot_acf(new_data.num_orders, ax=axes[0, 1])

# 1st Differencing
axes[1, 0].plot(new_data.num_orders.diff()); axes[1, 0].set_title('1st Order Differencing')
plot_acf(new_data.num_orders.diff().dropna(), ax=axes[1, 1])

# 2nd Differencing
axes[2, 0].plot(new_data.num_orders.diff().diff()); axes[2, 0].set_title('2nd Order Differencing')
plot_acf(new_data.num_orders.diff().diff().dropna(), ax=axes[2, 1])

plt.show()

# PACF plot of 1st differenced series
plt.rcParams.update({'figure.figsize':(9,3), 'figure.dpi':120})

fig, axes = plt.subplots(1, 2, sharex=True)
axes[0].plot(new_data.num_orders.diff()); axes[0].set_title('1st Differencing')
axes[1].set(ylim=(0,5))
plot_pacf(new_data.num_orders.diff().dropna(), ax=axes[1])

plt.show()

fig, axes = plt.subplots(1, 2, sharex=True)
axes[0].plot(new_data.num_orders.diff()); axes[0].set_title('1st Differencing')
axes[1].set(ylim=(0,1.2))
plot_acf(new_data.num_orders.diff().dropna(), ax=axes[1])

plt.show()

#%%


new_data['SMA_20'] = new_data.num_orders.rolling(4, min_periods=1).mean()

plt.plot(new_data['SMA_20'])
plt.plot(new_data['num_orders'])

result = adfuller(new_data.SMA_20.dropna())
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])


#%%

ts_log = np.log(new_data)
plt.plot(ts_log)


#%%

# print(train_data.corr())

from statsmodels.tsa.arima_model import ARIMA

# new_data['num_orders'] = np.log1p(new_data['num_orders'])

ar = ARIMA(new_data['num_orders'], order=(1,1,0))
ar_fit = ar.fit()
print(ar_fit.summary())
diff_ARIMA = (ar_fit.fittedvalues - new_data['num_orders'])
diff_ARIMA.dropna(inplace=True)


plt.plot(new_data['num_orders'])
plt.plot(ar_fit.fittedvalues, color='red')
plt.title('AR Model RSS: %.4F'%sum((diff_ARIMA)**2))
plt.show()

#%%
ma = ARIMA(new_data['num_orders'], order=(0,1,2))
ma_fit = ma.fit()
print(ma_fit.summary())

plt.plot(new_data['num_orders'])
plt.plot(ma_fit.fittedvalues, color='red')
plt.title('MA Model RSS: %.4f'% sum((ma_fit.fittedvalues-new_data['num_orders'])**2))
plt.show()

#%%
arıma = ARIMA(new_data['num_orders'], order=(1,1,1))
arıma_fit = arıma.fit()
print(arıma_fit.summary())

plt.plot(new_data['num_orders'])
plt.plot(arıma_fit.predict(), color='red')
plt.title('ARIMA Model RSS: %.4f'% sum((arıma_fit.fittedvalues-new_data['num_orders'])**2))
plt.show()


#%%

residuals = pd.DataFrame(arıma_fit.resid)
fig, ax = plt.subplots(1,2)
residuals.plot(title="Residuals", ax=ax[0])
residuals.plot(kind='kde', title='Density', ax=ax[1])
plt.show()


# predict = arıma_fit.predict(dynamic=False)
# plt.plot(new_data['num_orders'])
# plt.plot(predict)
# plt.show()

#%%

x_test = pd.DataFrame()
x_test['date'] = pd.date_range('2022-10-16', periods=10, freq='W')
print("Data: ", x_test)

# new_data = new_data.reset_index()
# new_data['forecast']=ar.predict(start=90,end=103,dynamic=True)
# plt.plot(new_data.index, new_data['forecast'])7

predict = ar_fit.forecast(steps=15)

plt.plot(new_data['num_orders'])
plt.plot(predict)
plt.show()




