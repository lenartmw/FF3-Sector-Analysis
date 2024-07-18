import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv('sectorsdata.csv')

periods = []
currentperiod =[]
cycledates = []

regression_results = {
    'Expansion': {'Technology': [], 'Healthcare': [], 'Financials': []},
    'Contraction': {'Technology': [], 'Healthcare': [], 'Financials': []},
}

def preparedata(currentperiod):
    dates = []
    Mkt_RF = []
    SMB = []
    HML = []
    Technology = []
    Healthcare = []
    Financials = []

    for data in currentperiod:
        if isinstance(data, (tuple, list)) and len(data) >= 7:
            dates.append(data[0])
            Mkt_RF.append(data[1])
            SMB.append(data[2])
            HML.append(data[3])
            Technology.append(data[4])
            Healthcare.append(data[5])
            Financials.append(data[6])

    X = np.column_stack((Mkt_RF, SMB, HML))
    y_tech = np.array(Technology)
    y_health = np.array(Healthcare)
    y_fin = np.array(Financials)

    return (X, y_tech, y_health, y_fin, dates)

def calcregression(X, y, sector, cycle_type, start_date, end_date):

    model = LinearRegression()
    model.fit(X, y)
    intercept = np.round(model.intercept_, 4)
    coefficients = np.round(model.coef_, 4)

    regression_results[cycle_type][sector].append((start_date, end_date, intercept, coefficients))

    print(f"Regression results for {sector} sector during {cycle_type} ({start_date} to {end_date}):")
    print("Coefficients:", coefficients)
    print("Intercept:", intercept)

def getresults(currentperiod, cycle_type):
    X, y_tech, y_health, y_fin, dates = preparedata(currentperiod)

    start_date = dates[0]
    end_date = dates[-1]
    cycledates.append((start_date, end_date, cycle_type))

    calcregression(X, y_tech, "Technology", cycle_type, start_date, end_date)
    calcregression(X, y_health, "Healthcare", cycle_type, start_date, end_date)
    calcregression(X, y_fin, "Financials", cycle_type, start_date, end_date)

prevcycletype = None
for i, row in df.iterrows():
    date = row['Date']
    mkt_value = row['Mkt-RF']
    smb_value = row['SMB']
    hml_value = row['HML']
    recessions = row['Recession']
    technology_value = row['XLK']
    healthcare_value = row['XLV']
    financials_value = row['XLF']
    cycle_type = None

    if recessions == 0:
        cycle_type = "Expansion"
    elif recessions == 1:
        cycle_type = "Contraction"

    if prevcycletype is not None and cycle_type != prevcycletype:
        getresults(currentperiod, prevcycletype)
        if currentperiod:
            periods.append((currentperiod, prevcycletype))
            currentperiod = []

    currentperiod.append((date, mkt_value, smb_value, hml_value, technology_value, healthcare_value, financials_value))
    prevcycletype = cycle_type

if currentperiod:
    getresults(currentperiod, prevcycletype)
    periods.append((currentperiod, prevcycletype))

#######################################################################################################################################
plt.style.use('seaborn-v0_8')
fig, axes = plt.subplots(3, sharex=True)
fig.set_size_inches(18.5, 10.5)

# ------------------------------------------------------------------------
tech_results = []
for cycle_type, results in regression_results.items():
    for result in results['Technology']:
        start_date, end_date, intercept, coefficients = result
        tech_results.append([cycle_type, start_date, end_date, intercept, coefficients[0], coefficients[1], coefficients[2]])

dftech = pd.DataFrame(tech_results, columns=['Cycle Type', 'Start Date', 'End Date', 'Intercept', 'Mkt-RF', 'SMB', 'HML'])
dftech['Start Date'] = pd.to_datetime(dftech['Start Date'], format='%d/%m/%y')
dftech = dftech.sort_values(by='Start Date').reset_index(drop=True)

axes[0].plot(dftech['Start Date'], dftech['Mkt-RF'], label='Mkt-RF')
axes[0].plot(dftech['Start Date'], dftech['SMB'], label='SMB')
axes[0].plot(dftech['Start Date'], dftech['HML'], label='HML')
axes[0].set_title('Technology Sector Regression Results')
axes[0].set_xlabel('Date')
axes[0].set_ylabel('Value')
axes[0].legend(loc='upper left')
axes[0].grid(True)

axes[0].set_xticks(dftech['Start Date'])
axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
plt.xticks(rotation=45, ha='right')

# ------------------------------------------------------------------------
health_results = []
for cycle_type, results in regression_results.items():
    for result in results['Healthcare']:
        start_date, end_date, intercept, coefficients = result
        health_results.append([cycle_type, start_date, end_date, intercept, coefficients[0], coefficients[1], coefficients[2]])

dfhealth = pd.DataFrame(health_results, columns=['Cycle Type', 'Start Date', 'End Date', 'Intercept', 'Mkt-RF', 'SMB', 'HML'])
dfhealth['Start Date'] = pd.to_datetime(dfhealth['Start Date'], format='%d/%m/%y')
dfhealth = dfhealth.sort_values(by='Start Date').reset_index(drop=True)

axes[1].plot(dfhealth['Start Date'], dfhealth['Mkt-RF'], label='Mkt-RF')
axes[1].plot(dfhealth['Start Date'], dfhealth['SMB'], label='SMB')
axes[1].plot(dfhealth['Start Date'], dfhealth['HML'], label='HML')
axes[1].set_title('Healthcare Sector Regression Results')
axes[1].set_xlabel('Date')
axes[1].set_ylabel('Value')
axes[1].legend(loc='upper left')
axes[1].grid(True)

# ------------------------------------------------------------------------
fin_results = []
for cycle_type, results in regression_results.items():
    for result in results['Financials']:
        start_date, end_date, intercept, coefficients = result
        fin_results.append([cycle_type, start_date, end_date, intercept, coefficients[0], coefficients[1], coefficients[2]])

dffin = pd.DataFrame(fin_results, columns=['Cycle Type', 'Start Date', 'End Date', 'Intercept', 'Mkt-RF', 'SMB', 'HML'])
dffin['Start Date'] = pd.to_datetime(dffin['Start Date'], format='%d/%m/%y')
dffin = dffin.sort_values(by='Start Date').reset_index(drop=True)

axes[2].plot(dffin['Start Date'], dffin['Mkt-RF'], label='Mkt-RF')
axes[2].plot(dffin['Start Date'], dffin['SMB'], label='SMB')
axes[2].plot(dffin['Start Date'], dffin['HML'], label='HML')
axes[2].set_title('Financials Sector Regression Results')
axes[2].set_xlabel('Date')
axes[2].set_ylabel('Value')
axes[2].legend(loc='upper left')
axes[2].grid(True)

# ------------------------------------------------------------------------
plt.tight_layout()
plt.show()

