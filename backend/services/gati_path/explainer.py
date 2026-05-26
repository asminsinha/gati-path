import shap
import pandas as pd
import numpy as np

class GatiExplainer:
    def __init__(self, model, X_train):
        # We use the TreeExplainer which is optimized for Random Forest
        self.explainer = shap.TreeExplainer(model)
        self.X_train = X_train

    def explain_decision(self, sample_data):
        # Calculate SHAP values
        shap_values = self.explainer.shap_values(sample_data)
        
        # 1. Handle Class Selection
        # For Classifiers, SHAP usually returns a list: [values_for_0, values_for_1]
        # We want index 1 (Delayed)
        if isinstance(shap_values, list):
            impact_data = shap_values[1]
        elif isinstance(shap_values, np.ndarray) and len(shap_values.shape) == 3:
            # Some newer versions return (samples, features, classes)
            impact_data = shap_values[:, :, 1]
        else:
            impact_data = shap_values

        # 2. FORCE 1-DIMENSIONAL (The Fix)
        # We use .flatten() to ensure it's a simple list of numbers
        impact_1d = np.array(impact_data).flatten()

        # 3. Create the Report
        # We make sure the number of columns matches the number of impact values
        feature_importance = pd.DataFrame({
            'Feature': self.X_train.columns,
            'Impact': impact_1d
        }).sort_values(by='Impact', ascending=False)
        
        # Print the insight for the Vitarai Dashboard
        top_reason = feature_importance.iloc[0]['Feature']
        print(f"\n[Vitarai Insight]: High risk of delay detected.")
        print(f"Primary Factor: {top_reason.replace('_', ' ')}")
        
        return feature_importance