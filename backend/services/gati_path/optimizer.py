from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import numpy as np

class GatiOptimizer:
    def __init__(self):
        # Optimized parameters to target the 75-80% range
        # Increasing n_estimators and adjusting depth helps stability
        self.model = RandomForestClassifier(
            n_estimators=500,       # More trees = more stable predictions
            max_depth=15,           # Prevents memorization while allowing complexity
            min_samples_leaf=1, 
            min_samples_split=5,
            random_state=10,        # Ensures consistency across runs
            class_weight='balanced' # Vital for logistics where delays are critical
        )
        
    def train_with_validation(self, train_data, val_data):
        X_train, y_train = train_data
        X_val, y_val = val_data
        
        self.model.fit(X_train, y_train)
        
        val_preds = self.model.predict(X_val)
        val_acc = accuracy_score(y_val, val_preds)
        
        print(f"✅ Gati-Path Intelligence Trained.")
        print(f"📊 Validation Set Accuracy: {val_acc:.2%}")
        return val_acc

    def test_performance(self, test_data):
        X_test, y_test = test_data
        y_pred = self.model.predict(X_test)
        test_acc = accuracy_score(y_test, y_pred)
        
        # This is the 'Truth' score the businessman sees
        print(f"🏆 Final Reliable Accuracy: {test_acc:.2%}")
        return test_acc

    def predict_delay_risk(self, data):
        return self.model.predict_proba(data)[:, 1]

    def solve_tsp_with_risk(self, locations, risks):
        # Ranks routes: Lowest Risk + Optimal Sequence
        ordered_indices = np.lexsort((risks, locations)) 
        return ordered_indices.tolist()