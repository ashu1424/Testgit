from fastapi import FastAPI, HTTPException
import pandas as pd
import os

app = FastAPI()

CSV_FILE = "data.csv"


# Helper function to load CSV
def load_data():
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame(columns=["id", "name", "age"])
    return pd.read_csv(CSV_FILE)


# Helper function to save CSV
def save_data(df):
    df.to_csv(CSV_FILE, index=False)


# 1️⃣ Get all data
@app.get("/data")
def get_data():
    df = load_data()
    return df.to_dict(orient="records")


# 2️⃣ Add or update data
@app.post("/data")
def add_or_update_data(id: int, name: str, age: int):
    df = load_data()

    if id in df["id"].values:
        # Update existing record
        df.loc[df["id"] == id, ["name", "age"]] = [name, age]
        message = "Data updated"
    else:
        # Add new record
        new_row = pd.DataFrame([{"id": id, "name": name, "age": age}])
        df = pd.concat([df, new_row], ignore_index=True)
        message = "Data added"

    save_data(df)
    return {"message": message}


# 3️⃣ Delete data
@app.delete("/data/{id}")
def delete_data(id: int):
    df = load_data()

    if id not in df["id"].values:
        raise HTTPException(status_code=404, detail="Record not found")

    df = df[df["id"] != id]
    save_data(df)

    return {"message": "Data deleted"}


# 4️⃣ Get data from CSV (same as fetch but explicit endpoint)
@app.get("/data/{id}")
def get_single_data(id: int):
    df = load_data()

    record = df[df["id"] == id]

    if record.empty:
        raise HTTPException(status_code=404, detail="Record not found")

    return record.to_dict(orient="records")[0]
