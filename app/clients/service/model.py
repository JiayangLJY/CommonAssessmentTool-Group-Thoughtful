import os
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from app.clients.util import util_get_cols, get_model
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration from .env
MODEL_TYPE = os.getenv("MODEL_TYPE", "RandomForestRegressor")  # Default: RandomForestRegressor
MODEL_OUTPUT_NAME = os.getenv("MODEL_OUTPUT_NAME", "different.pkl")  # Default: different.pkl

def prepare_models():
    """
    Prepare and train a machine learning model based on the configuration.
    """
    # Load dataset and define the features and labels
    backendCode = pd.read_csv('data_commontool.csv')

    # Load categorical columns dynamically
    categorical_cols = util_get_cols()

    # Define interventions
    interventions = [
        'employment_assistance',
        'life_stabilization',
        'retention_services',
        'specialized_services',
        'employment_related_financial_supports',
        'employer_financial_supports',
        'enhanced_referrals'
    ]
    categorical_cols.extend(interventions)

    # Prepare training data
    X_categorical_baseline = backendCode[categorical_cols]
    y_baseline = backendCode['success_rate']  # Assuming 'success_rate' is the target variable
    X_categorical_baseline = np.array(X_categorical_baseline)
    y_baseline = np.array(y_baseline)

    # Split data into training and testing sets
    X_train_baseline, X_test_baseline, y_train_baseline, y_test_baseline = train_test_split(
        X_categorical_baseline, y_baseline, test_size=0.2, random_state=42
    )

    # Dynamically load the model based on configuration
    model = get_model(MODEL_TYPE)

    # Train the model
    print(f"Training {MODEL_TYPE} model...")
    model.fit(X_train_baseline, y_train_baseline)

    # Example: Predicting on the test set (optional, for evaluation)
    baseline_predictions = model.predict(X_test_baseline)
    print(f"Sample predictions: {baseline_predictions[:5]}")

    return model


# def test_column_order():
#     """
#     Test if the column order matches the expected original order.
#     """
#     print("\n#################### test_column_order() ####################")
#     test_original_cols = [
#         'age', 'gender', 'work_experience', 'canada_workex', 'dep_num', 'canada_born', 'citizen_status',
#         'level_of_schooling', 'fluent_english', 'reading_english_scale', 'speaking_english_scale',
#         'writing_english_scale', 'numeracy_scale', 'computer_scale', 'transportation_bool',
#         'caregiver_bool', 'housing', 'income_source', 'felony_bool', 'attending_school',
#         'currently_employed', 'substance_use', 'time_unemployed', 'need_mental_health_support_bool'
#     ]
#     cols = util_get_cols()
#     if cols == test_original_cols:
#         print("PASS")
#     else:
#         print("FAIL")


def main():
    """
    Main function to prepare and save the trained model.
    """
    print("Starting model")
    model = prepare_models()

    # Save the model to a file (configurable via .env)
    pickle.dump(model, open(MODEL_OUTPUT_NAME, "wb"))
    print(f"Model saved as {MODEL_OUTPUT_NAME}")

    # Optional: Reload the model to verify save/load functionality
    model = pickle.load(open(MODEL_OUTPUT_NAME, "rb"))
    print(f"Model reloaded successfully from {MODEL_OUTPUT_NAME}")

if __name__ == "__main__":
    main()
