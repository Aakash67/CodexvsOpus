import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Load the Excel file
print("=" * 80)
print("APPLICATION LOGS ANALYSIS")
print("=" * 80)
print("\n1. LOADING DATASET...")

df = pd.read_excel('sample_application_logs.xlsx')

# Display basic information
print(f"\nDataset Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"\nColumns: {list(df.columns)}")
print(f"\nData Types:\n{df.dtypes}")
print(f"\nFirst few rows:")
print(df.head(10))

print("\n" + "=" * 80)
print("2. DATA OVERVIEW")
print("=" * 80)
print(f"\nDate Range: {df['timestamp'].min()} to {df['timestamp'].max()}")
print(f"Total Records: {len(df):,}")
print(f"Unique Users: {df['user_id'].nunique()}")
print(f"Request Types: {df['request_type'].unique()}")
print(f"Status Codes: {sorted(df['status_code'].unique())}")

print("\n" + "=" * 80)
print("3. KEY METRICS")
print("=" * 80)

# Average response time
avg_response_time = df['response_time_ms'].mean()
median_response_time = df['response_time_ms'].median()
print(f"\nResponse Time Statistics:")
print(f"  Average: {avg_response_time:.2f} ms")
print(f"  Median: {median_response_time:.2f} ms")
print(f"  Min: {df['response_time_ms'].min():.2f} ms")
print(f"  Max: {df['response_time_ms'].max():.2f} ms")
print(f"  Std Dev: {df['response_time_ms'].std():.2f} ms")

# Error rates by status code
print(f"\nStatus Code Distribution:")
status_counts = df['status_code'].value_counts().sort_index()
total_requests = len(df)
for status, count in status_counts.items():
    percentage = (count / total_requests) * 100
    status_type = "SUCCESS" if status == 200 else "ERROR"
    print(f"  {status} ({status_type}): {count:,} requests ({percentage:.2f}%)")

# Overall error rate
error_rate = (df['status_code'] != 200).sum() / total_requests * 100
print(f"\nOverall Error Rate: {error_rate:.2f}%")

print("\n" + "=" * 80)
print("4. PEAK USAGE ANALYSIS")
print("=" * 80)

# Convert timestamp to datetime if not already
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['Hour'] = df['timestamp'].dt.hour
df['Date'] = df['timestamp'].dt.date
df['DayOfWeek'] = df['timestamp'].dt.day_name()

# Requests by hour
hourly_requests = df.groupby('Hour').size().sort_values(ascending=False)
print(f"\nTop 5 Peak Hours (by request count):")
for hour, count in hourly_requests.head(5).items():
    print(f"  Hour {hour:02d}:00 - {count:,} requests")

# Requests by day
daily_requests = df.groupby('Date').size().sort_values(ascending=False)
print(f"\nTop 3 Busiest Days:")
for date, count in daily_requests.head(3).items():
    print(f"  {date}: {count:,} requests")

# Requests by day of week
dow_requests = df.groupby('DayOfWeek').size()
print(f"\nRequests by Day of Week:")
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
for day in day_order:
    if day in dow_requests.index:
        print(f"  {day}: {dow_requests[day]:,} requests")

print("\n" + "=" * 80)
print("5. PERFORMANCE BY REQUEST TYPE")
print("=" * 80)

# Group by request type
request_type_stats = df.groupby('request_type').agg({
    'response_time_ms': ['count', 'mean', 'median', 'min', 'max'],
    'status_code': lambda x: (x != 200).sum()
}).round(2)

request_type_stats.columns = ['Total_Requests', 'Avg_Response_ms', 'Median_Response_ms', 
                               'Min_Response_ms', 'Max_Response_ms', 'Error_Count']
request_type_stats['Error_Rate_%'] = (request_type_stats['Error_Count'] / 
                                       request_type_stats['Total_Requests'] * 100).round(2)

print("\n" + request_type_stats.to_string())

print("\n" + "=" * 80)
print("6. ANOMALY DETECTION")
print("=" * 80)

# Response time anomalies (using IQR method)
Q1 = df['response_time_ms'].quantile(0.25)
Q3 = df['response_time_ms'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df['response_time_ms'] < lower_bound) | (df['response_time_ms'] > upper_bound)]
print(f"\nResponse Time Outliers (IQR method):")
print(f"  Normal range: {max(0, lower_bound):.2f} - {upper_bound:.2f} ms")
print(f"  Outliers detected: {len(outliers)} ({len(outliers)/len(df)*100:.2f}%)")

if len(outliers) > 0:
    print(f"\nSample of extreme outliers:")
    extreme_outliers = outliers.nlargest(5, 'response_time_ms')[['timestamp', 'user_id',
                                                                   'request_type', 'response_time_ms',
                                                                   'status_code']]
    print(extreme_outliers.to_string(index=False))

# Error clustering
errors = df[df['status_code'] != 200]
if len(errors) > 0:
    print(f"\nError Analysis:")
    print(f"  Total errors: {len(errors)}")
    error_by_type = errors.groupby('request_type')['status_code'].value_counts()
    print(f"\n  Errors by Request Type and Status Code:")
    for (req_type, status), count in error_by_type.items():
        print(f"    {req_type} - {status}: {count} errors")

print("\n" + "=" * 80)
print("7. USER BEHAVIOR PATTERNS")
print("=" * 80)

# Top users by request count
top_users = df['user_id'].value_counts().head(5)
print(f"\nTop 5 Most Active Users:")
for user, count in top_users.items():
    print(f"  User {user}: {count:,} requests")

# Average requests per user
avg_requests_per_user = df.groupby('user_id').size().mean()
print(f"\nAverage requests per user: {avg_requests_per_user:.2f}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)

