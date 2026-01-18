from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource, ValueType
from feast.types import Float32, Int64, String

# 1. Define the Entity
user = Entity(
    name="user",
    join_keys=["user_id"],
    description="User entity for financial risk analysis",
)

# 2. Define the Data Source
# In a real scenario, this would be a Parquet file on S3 or a SQL query.
# For local dev, we point to a local parquet file.
user_stats_source = FileSource(
    name="user_stats_source",
    path="data/user_stats.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",
)

# 3. Define the Feature View
user_risk_features = FeatureView(
    name="user_risk_features",
    entities=[user],
    ttl=timedelta(days=30),
    schema=[
        Field(name="credit_score", dtype=Int64),
        Field(name="income", dtype=Float32),
        Field(name="total_debt", dtype=Float32),
        Field(name="num_late_payments", dtype=Int64),
    ],
    online=True,
    source=user_stats_source,
    tags={"team": "risk_assessment"},
)

