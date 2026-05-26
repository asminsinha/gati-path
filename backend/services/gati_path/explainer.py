import shap
import pandas as pd
import numpy as np

class GatiExplainer:
    def __init__(self, model, X_train):
      
        self.explainer = shap.TreeExplainer(model)
        self.X_train = X_train

    def explain_decision(self, sample_data):
      
        shap_values = self.explainer.shap_values(sample_data)
        
    
        if isinstance(shap_values, list):
            impact_data = shap_values[1]
        elif isinstance(shap_values, np.ndarray) and len(shap_values.shape) == 3:
          
            impact_data = shap_values[:, :, 1]
        else:
            impact_data = shap_values

        
        impact_1d = np.array(impact_data).flatten()

       
        feature_importance = pd.DataFrame({
            'Feature': self.X_train.columns,
            'Impact': impact_1d
        }).sort_values(by='Impact', ascending=False)
        
       
        top_reason = feature_importance.iloc[0]['Feature']
        print(f"\n[Vitarai Insight]: High risk of delay detected.")
        print(f"Primary Factor: {top_reason.replace('_', ' ')}")
        
        return feature_importance