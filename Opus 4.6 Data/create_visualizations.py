import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (15, 10)

# Load data
df = pd.read_excel('sample_application_logs.xlsx')
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['Hour'] = df['timestamp'].dt.hour
df['Date'] = df['timestamp'].dt.date

# Create a figure with multiple subplots
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('Application Logs Analysis Dashboard - Feb 1-3, 2026', fontsize=16, fontweight='bold')

# 1. Status Code Distribution (Pie Chart)
ax1 = axes[0, 0]
status_counts = df['status_code'].value_counts()
colors = ['#2ecc71' if x == 200 else '#e74c3c' for x in status_counts.index]
ax1.pie(status_counts.values, labels=[f'{x}\n({status_counts[x]} req)' for x in status_counts.index], 
        autopct='%1.1f%%', colors=colors, startangle=90)
ax1.set_title('Status Code Distribution\n50% Error Rate!', fontweight='bold', color='red')

# 2. Error Rate by Request Type (Bar Chart)
ax2 = axes[0, 1]
error_rates = df.groupby('request_type').apply(
    lambda x: (x['status_code'] != 200).sum() / len(x) * 100
).sort_values(ascending=False)
bars = ax2.barh(range(len(error_rates)), error_rates.values)
ax2.set_yticks(range(len(error_rates)))
ax2.set_yticklabels(error_rates.index)
ax2.set_xlabel('Error Rate (%)')
ax2.set_title('Error Rate by Request Type', fontweight='bold')
ax2.axvline(x=50, color='orange', linestyle='--', label='50% threshold')
# Color bars based on severity
for i, (bar, val) in enumerate(zip(bars, error_rates.values)):
    if val >= 60:
        bar.set_color('#e74c3c')  # Red for critical
    elif val >= 40:
        bar.set_color('#f39c12')  # Orange for high
    else:
        bar.set_color('#f1c40f')  # Yellow for moderate
ax2.legend()

# 3. Response Time by Request Type (Box Plot)
ax3 = axes[0, 2]
df_sorted = df.sort_values('request_type')
request_types = df['request_type'].unique()
data_to_plot = [df[df['request_type'] == rt]['response_time_ms'].values for rt in sorted(request_types)]
bp = ax3.boxplot(data_to_plot, labels=sorted(request_types), patch_artist=True)
for patch in bp['boxes']:
    patch.set_facecolor('#3498db')
ax3.set_ylabel('Response Time (ms)')
ax3.set_title('Response Time Distribution by Request Type', fontweight='bold')
ax3.tick_params(axis='x', rotation=45)
plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')

# 4. Requests Over Time (Line Chart)
ax4 = axes[1, 0]
hourly_counts = df.groupby('Hour').size()
ax4.plot(hourly_counts.index, hourly_counts.values, marker='o', linewidth=2, markersize=8, color='#9b59b6')
ax4.fill_between(hourly_counts.index, hourly_counts.values, alpha=0.3, color='#9b59b6')
ax4.set_xlabel('Hour of Day')
ax4.set_ylabel('Number of Requests')
ax4.set_title('Request Volume by Hour', fontweight='bold')
ax4.grid(True, alpha=0.3)
ax4.set_xticks(range(0, 24, 2))

# 5. Average Response Time by Request Type (Bar Chart)
ax5 = axes[1, 1]
avg_response = df.groupby('request_type')['response_time_ms'].mean().sort_values(ascending=False)
bars = ax5.bar(range(len(avg_response)), avg_response.values, color='#16a085')
ax5.set_xticks(range(len(avg_response)))
ax5.set_xticklabels(avg_response.index, rotation=45, ha='right')
ax5.set_ylabel('Average Response Time (ms)')
ax5.set_title('Average Response Time by Request Type', fontweight='bold')
ax5.axhline(y=1000, color='red', linestyle='--', label='1000ms threshold')
ax5.legend()

# 6. Daily Request Volume (Bar Chart)
ax6 = axes[1, 2]
daily_counts = df.groupby('Date').size()
dates_str = [str(d) for d in daily_counts.index]
bars = ax6.bar(dates_str, daily_counts.values, color=['#e67e22', '#3498db', '#2ecc71'])
ax6.set_xlabel('Date')
ax6.set_ylabel('Number of Requests')
ax6.set_title('Daily Request Volume', fontweight='bold')
ax6.tick_params(axis='x', rotation=45)
# Add value labels on bars
for i, (bar, val) in enumerate(zip(bars, daily_counts.values)):
    ax6.text(i, val + 0.5, str(val), ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('application_logs_analysis.png', dpi=300, bbox_inches='tight')
print("✅ Visualization saved as 'application_logs_analysis.png'")

# Create a second figure for detailed error analysis
fig2, axes2 = plt.subplots(1, 2, figsize=(16, 6))
fig2.suptitle('Detailed Error Analysis', fontsize=16, fontweight='bold')

# Error types by request type (Stacked bar)
ax_err1 = axes2[0]
error_df = df[df['status_code'] != 200]
error_pivot = pd.crosstab(error_df['request_type'], error_df['status_code'])
error_pivot.plot(kind='bar', stacked=True, ax=ax_err1, 
                 color=['#e74c3c', '#e67e22', '#f39c12', '#f1c40f'])
ax_err1.set_xlabel('Request Type')
ax_err1.set_ylabel('Number of Errors')
ax_err1.set_title('Error Types by Request Type', fontweight='bold')
ax_err1.legend(title='Status Code', bbox_to_anchor=(1.05, 1), loc='upper left')
ax_err1.tick_params(axis='x', rotation=45)
plt.setp(ax_err1.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Success vs Error comparison
ax_err2 = axes2[1]
success_count = (df['status_code'] == 200).sum()
error_count = (df['status_code'] != 200).sum()
ax_err2.bar(['Success (200)', 'Errors (4xx/5xx)'], [success_count, error_count], 
            color=['#2ecc71', '#e74c3c'], width=0.6)
ax_err2.set_ylabel('Number of Requests')
ax_err2.set_title('Success vs Error Requests', fontweight='bold')
ax_err2.set_ylim(0, max(success_count, error_count) * 1.2)
# Add value labels
for i, val in enumerate([success_count, error_count]):
    ax_err2.text(i, val + 1, f'{val}\n({val/len(df)*100:.1f}%)', 
                ha='center', va='bottom', fontweight='bold', fontsize=12)

plt.tight_layout()
plt.savefig('error_analysis_detailed.png', dpi=300, bbox_inches='tight')
print("✅ Detailed error analysis saved as 'error_analysis_detailed.png'")

print("\n" + "="*60)
print("All visualizations created successfully!")
print("="*60)

