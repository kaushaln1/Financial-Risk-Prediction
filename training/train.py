import os
import argparse
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from feast import FeatureStore

def train_model(feature_repo_path):
    print(f"Loading feature store from {feature_repo_path}...")
    # 1. Initialize Feast
    fs = FeatureStore(repo_path=feature_repo_path)
    
    # 2. Get training data
    # For demonstration, we load the parquet file directly to use as the entity dataframe
    # In production, this would be a query to get the population of users we want to train on.
    data_path = os.path.join(feature_repo_path, "data/user_stats.parquet")
    if not os.path.exists(data_path):
        print(f"Error: Data file not found at {data_path}. Run features/generate_data.py first.")
        return

    entity_df = pd.read_parquet(data_path)
    
    print("Retrieving historical features...")
    # We want to retrieve features for these entities
    feature_vector = fs.get_historical_features(
        entity_df=entity_df,
        features=[
            "user_risk_features:credit_score",
            "user_risk_features:income",
            "user_risk_features:total_debt",
            "user_risk_features:num_late_payments"
        ]
    ).to_df()
    
    # Simple target generation (mocking ground truth for the example)
    # Logic: if num_late_payments > 2 or credit_score < 550 -> high risk (1)
    print("Generating synthetic targets...")
    feature_vector['target'] = feature_vector.apply(
        lambda row: 1 if row['num_late_payments'] > 2 or row['credit_score'] < 550 else 0, axis=1
    )
    
    features = ["credit_score", "income", "total_debt", "num_late_payments"]
    X = feature_vector[features]
    y = feature_vector['target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    # 3. MLflow Tracking
    # Default to Minikube service URL if env var not set
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://192.168.49.2:31591")
    print(f"Logging to MLflow at {tracking_uri}...")
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment("financial_risk_prediction")
    
    with mlflow.start_run():
        n_estimators = 100
        clf = RandomForestClassifier(n_estimators=n_estimators)
        clf.fit(X_train, y_train)
        
        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_metric("accuracy", accuracy)
        
        # Log the model and register it
        mlflow.sklearn.log_model(clf, "model", registered_model_name="financial_risk_model")
        print(f"Model trained with accuracy: {accuracy}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--feature_repo", default="../features", help="Path to Feast feature repo")
    args = parser.parse_args()
    
    train_model(args.feature_repo)

