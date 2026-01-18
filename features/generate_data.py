import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_user_data():
    num_users = 1000
    user_ids = [str(i) for i in range(1000, 1000 + num_users)]
    
    # Generate timestamps for the last 60 days
    timestamps = [datetime.now() - timedelta(days=np.random.randint(0, 60)) for _ in range(num_users)]
    
    data = pd.DataFrame({
        "user_id": user_ids,
        "event_timestamp": timestamps,
        "created_timestamp": datetime.now(),
        "credit_score": np.random.randint(300, 850, num_users),
        "income": np.random.uniform(20000, 150000, num_users),
        "total_debt": np.random.uniform(1000, 50000, num_users),
        "num_late_payments": np.random.randint(0, 10, num_users)
    })
    
    return data

if __name__ == "__main__":
    df = generate_user_data()
    df.to_parquet("data/user_stats.parquet")
    print("Generated data/user_stats.parquet")

