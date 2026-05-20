import matplotlib.pyplot as plt
import pandas as pd

class DiskGeometryVisualization:
    def __init__(self, data):
        self.data = data

    def display_histogram(self):
        plt.figure(figsize=(10, 6))
        plt.hist(self.data['disk_size'], bins=20, color='blue', edgecolor='black')
        plt.title('Disk Size Distribution')
        plt.xlabel('Disk Size (GB)')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.show()

    def display_pie_chart(self):
        labels = ['Used', 'Free']
        sizes = [self.data['used_space'].sum(), self.data['free_space'].sum()]
        colors = ['red', 'green']

        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title('Disk Space Usage')
        plt.show()

    def display_line_chart(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.data['timestamp'], self.data['disk_usage'], marker='o', linestyle='-', color='orange')
        plt.title('Disk Usage Over Time')
        plt.xlabel('Timestamp')
        plt.ylabel('Disk Usage (%)')
        plt.grid(True)
        plt.show()

def main():
    # Example data loading
    data = {
        'disk_size': [500, 1000, 2000, 3000],
        'used_space': [200, 400, 800, 1200],
        'free_space': [300, 600, 1200, 1800],
        'disk_usage': [40, 40, 40, 40],
        'timestamp': pd.date_range(start='2023-01-01', periods=4, freq='M')
    }
    df = pd.DataFrame(data)

    viz = DiskGeometryVisualization(df)
    viz.display_histogram()
    viz.display_pie_chart()
    viz.display_line_chart()

if __name__ == "__main__":
    main()