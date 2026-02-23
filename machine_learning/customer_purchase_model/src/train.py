"""
Customer Purchase Classification
Pipeline de ML para predecir si un cliente es comprador frecuente.

Uso:
    python src/train.py
"""

from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

DATA_PATH = Path(__file__).parent.parent / "data" / "Customer Purchasing Behaviors.csv"
NUMERIC_COLS = ["age", "annual_income", "purchase_amount", "loyalty_score"]
RANDOM_STATE = 42


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")
    return df


def create_target(df: pd.DataFrame) -> pd.DataFrame:
    threshold = df["purchase_frequency"].mean()
    df["purchased"] = (df["purchase_frequency"] > threshold).astype(int)
    counts = df["purchased"].value_counts()
    print(f"Distribucion de clases - frecuentes: {counts[1]}, ocasionales: {counts[0]}")
    return df


def preprocess(df: pd.DataFrame):
    X = df.drop(columns=["purchased", "purchase_frequency", "user_id"])
    y = df["purchased"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )

    X_train = pd.get_dummies(X_train, columns=["region"], drop_first=True)
    X_test = pd.get_dummies(X_test, columns=["region"], drop_first=True)

    scaler = StandardScaler()
    X_train[NUMERIC_COLS] = scaler.fit_transform(X_train[NUMERIC_COLS])
    X_test[NUMERIC_COLS] = scaler.transform(X_test[NUMERIC_COLS])

    return X_train, X_test, y_train, y_test


def train(X_train, y_train) -> LogisticRegression:
    model = LogisticRegression(random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    return model


def evaluate(model, X_test, y_test) -> None:
    y_pred = model.predict(X_test)
    print("\nResultados:")
    print(classification_report(y_test, y_pred, target_names=["Ocasional", "Frecuente"]))


def main():
    df = load_data(DATA_PATH)
    df = create_target(df)
    X_train, X_test, y_train, y_test = preprocess(df)
    model = train(X_train, y_train)
    evaluate(model, X_test, y_test)


if __name__ == "__main__":
    main()
