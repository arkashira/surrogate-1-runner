import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load analytics data with caching for efficiency
@st.cache
def load_data(file_path):
    """
    Loads data from a specified CSV file path.
    
    Args:
        file_path (str): The path to the CSV file containing the analytics data.
        
    Returns:
        pd.DataFrame: A DataFrame containing the loaded analytics data.
    """
    data = pd.read_csv(file_path)
    return data

file_path = 'analytics.csv'
data = load_data(file_path)

# Display data with enhanced visualizations and actionable insights
st.title('AI Model Access Analytics Dashboard')
st.write('### Access Frequency Analysis')
plt.figure(figsize=(10, 6))
data['access_frequency'].plot(kind='hist', bins=30, color='skyblue', edgecolor='black')
plt.xlabel('Access Frequency')
plt.ylabel('Number of Occurrences')
plt.title('Distribution of Access Frequencies')
st.pyplot(plt)

st.write('### Access Duration Analysis')
plt.figure(figsize=(10, 6))
data['access_duration'].plot(kind='box', color='green', patch_artist=True)
plt.ylabel('Duration')
plt.title('Box Plot of Access Durations')
st.pyplot(plt)

# Additional Insights and Actions
st.write('#### Key Insights:')
insights = [
    "The histogram shows that most users have moderate access frequencies.",
    "The box plot indicates that there are some outliers in access durations."
]
for insight in insights:
    st.write(f"- {insight}")

st.write('#### Recommended Actions:')
actions = [
    "Investigate the reasons behind the moderate access frequencies to optimize user engagement.",
    "Analyze the outliers in access durations to identify potential issues or heavy users."
]
for action in actions:
    st.write(f"- {action}")