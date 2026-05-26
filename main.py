import os
import numpy as np
import json
from backend.services.gati_path.data_loader import GatiDataLoader
from backend.services.gati_path.optimizer import GatiOptimizer
from backend.services.gati_path.explainer import GatiExplainer

def run_gati_path_production():
    print("🚀 Initializing Vitarai Gati-Path (Production Pipeline)...")
    
    # 1. Initialize Loader
    dataset_path = os.path.join("data", "raw", "smart_logistics_dataset.csv")
    loader = GatiDataLoader(dataset_path)
    loader.load_and_preprocess()
    
    # 2. Unpack the 70/15/15 Stratified Split
    # This is the line that fixes your 'unpack' error
    train_set, val_set, test_set = loader.get_stratified_split()
    
    # 3. Train and Validate
    optimizer = GatiOptimizer()
    optimizer.train_with_validation(train_set, val_set)
    
    # 4. Final Evaluation on UNSEEN Test Data
    final_accuracy = optimizer.test_performance(test_set)
    
    # 5. Simulate a Business Request using the Test Set
    X_test, y_test = test_set
    sample_batch = X_test.head(5)
    risks = optimizer.predict_delay_risk(sample_batch)
    
    # Optimize Route
    locations = np.array(range(len(sample_batch)))
    best_sequence = optimizer.solve_tsp_with_risk(locations, risks)
    
    # 6. Explain the logic (XAI)
    explainer = GatiExplainer(optimizer.model, train_set[0])
    explanation = explainer.explain_decision(sample_batch.iloc[[0]])

    # 7. Professional JSON Output
    output = {
        "module": "Gati-Path",
        "engine_version": "2.0.0-stratified",
        "performance_metrics": {
            "test_accuracy": f"{final_accuracy:.2%}",
            "status": "Reliable" if final_accuracy > 0.70 else "Needs Tuning"
        },
        "business_intelligence": {
            "recommended_sequence": best_sequence,
            "batch_risk_avg": f"{np.mean(risks):.2%}",
            "primary_delay_factor": str(explanation.iloc[0]['Feature'])
        }
    }
    
    print("\n--- OUTBOUND DATA FOR VITARAI DASHBOARD ---")
    print(json.dumps(output, indent=4))

if __name__ == "__main__":
    try:
        run_gati_path_production()
    except Exception as e:
        print(f"❌ Error during pipeline execution: {e}")