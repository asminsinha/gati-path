import pandas as pd
from sklearn.model_selection import train_test_split

class GatiDataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        
    def load_and_preprocess(self):
        self.df = pd.read_csv(self.file_path)
        
        
        cols_to_drop = ['Timestamp', 'Asset_ID', 'Logistics_Delay_Reason', 'Shipment_Status']
        self.df = self.df.drop(columns=[c for c in cols_to_drop if c in self.df.columns], errors='ignore')
        self.df = self.df.fillna(0)
        
        
        traffic_map = {'Clear': 0, 'Detour': 1, 'Heavy': 2}
        self.df['Traffic_Status'] = self.df['Traffic_Status'].map(traffic_map)
        
        
        self.df['Route_Pressure'] = self.df['Demand_Forecast'] / (self.df['Asset_Utilization'] + 1)
        
        
        self.df['Traffic_Impact'] = self.df['Traffic_Status'] * self.df['Waiting_Time']
        
        self.df['Value_Priority'] = self.df['User_Transaction_Amount'] * self.df['User_Purchase_Frequency']
        
        return self.df

    def get_stratified_split(self):
        X = self.df.drop(columns=['Logistics_Delay'])
        y = self.df['Logistics_Delay']

        
        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y, test_size=0.30, random_state=42, stratify=y, shuffle=True
        )
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp
        )
        
        return (X_train, y_train), (X_val, y_val), (X_test, y_test)