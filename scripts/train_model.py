import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score
import os

def train_traffic_model():
    # Load data
    if not os.path.exists('data/traffic.csv'):
        print("Data file not found! Please run generate_data.py first.")
        return

    df = pd.read_csv('data/traffic.csv')
    print("Dataset Loaded. Shape:", df.shape)

    # Features and Target
    X = df[['hour', 'day', 'latitude', 'longitude']]
    y = df['risk']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train XGBoost
    print("Training XGBoost Model...")
    model = XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
        use_label_encoder=False,
        eval_metric='mlogloss'
    )
    
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    print("\nModel Accuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # Save model
    os.makedirs('models', exist_ok=True)
    with open('models/model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    print("\nModel saved to models/model.pkl successfully!")

if __name__ == "__main__":
    train_traffic_model()
