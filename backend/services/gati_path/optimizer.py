from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import numpy as np

class GatiOptimizer:
    def __init__(self):
        
        self.model = RandomForestClassifier(
            n_estimators=500,       
            max_depth=15,           
            min_samples_leaf=1, 
            min_samples_split=5,
            random_state=10,       
            class_weight='balanced' 
        )
        
    def train_with_validation(self, train_data, val_data):
        X_train, y_train = train_data
        X_val, y_val = val_data
        
        self.model.fit(X_train, y_train)
        
        val_preds = self.model.predict(X_val)
        val_acc = accuracy_score(y_val, val_preds)
        
        print(f" Gati-Path Intelligence Trained.")
        print(f" Validation Set Accuracy: {val_acc:.2%}")
        return val_acc

    def test_performance(self, test_data):
        X_test, y_test = test_data
        y_pred = self.model.predict(X_test)
        test_acc = accuracy_score(y_test, y_pred)
        
        print(f"🏆 Final Reliable Accuracy: {test_acc:.2%}")
        return test_acc

    def predict_delay_risk(self, data):
        return self.model.predict_proba(data)[:, 1]

    def solve_tsp_with_risk(self, locations, risks):
        
        ordered_indices = np.lexsort((risks, locations)) 
        return ordered_indices.tolist()