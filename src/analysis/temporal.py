from secrets import randbits

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os
import calendar


class TemporalAnalyzer:
    def __init__(self, df):
        """Initialize with a DataFrame containing 'title' and 'datetime' columns"""
        self.df = self._preprocess_data(df)
        # Set default style parameters
        plt.style.use('default')  # Using default style instead of seaborn
        plt.rcParams.update({
            'figure.figsize': (12, 6),
            'axes.grid': True,
            'grid.alpha': 0.3,
            'font.size': 10,
            'axes.labelsize': 12,
            'axes.titlesize': 14,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10
        })

    def _preprocess_data(self, df):
        """Preprocess the data and create temporal features"""
        df = df.copy()
        df['datetime'] = pd.to_datetime(df['datetime'])
        df['date'] = df['datetime'].dt.date
        df['month'] = df['datetime'].dt.month
        df['month_name'] = df['datetime'].dt.month_name()
        df['year_month'] = df['datetime'].dt.to_period('M')
        df['hour'] = df['datetime'].dt.hour
        df['day_of_week'] = df['datetime'].dt.day_name()

        # Calculate time differences for session analysis
        df = df.sort_values('datetime')
        df['time_diff'] = df['datetime'].diff()
        df['minutes_diff'] = df['time_diff'].dt.total_seconds() / 60

        # Define sessions (videos watched within 30 minutes of each other)
        df['new_session'] = df['minutes_diff'] > 30
        df['session_id'] = df['new_session'].cumsum()

        return df

    def analyze_monthly_trends(self, output_dir=None):
        """Analyze and visualize monthly viewing trends"""
        if output_dir is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            output_dir = os.path.join(project_root, 'reports', 'figures')

        os.makedirs(output_dir, exist_ok=True)

        # Calculate average daily views per month
        monthly_counts = self.df.groupby('year_month').size()
        days_in_month = self.df.groupby('year_month')['date'].nunique()
        avg_daily_views = monthly_counts / days_in_month

        plt.figure()
        ax = avg_daily_views.plot(kind='bar', color='#3b82f6')
        plt.title('Average Daily Videos Watched per Month', pad=20)
        plt.xlabel('')
        plt.ylabel('Average Videos per Day')
        plt.xticks(rotation=45)
        plt.grid(True, axis='y', alpha=0.3)

        # Add value labels on top of bars
        for i, v in enumerate(avg_daily_views):
            ax.text(i, v, f'{v:.1f}', ha='center', va='bottom')

        plt.tight_layout()
        plt.savefig(f'{output_dir}/monthly_daily_avg.png', dpi=300, bbox_inches='tight')
        plt.close()

        return {'avg_daily_views': avg_daily_views}

    def analyze_daily_patterns(self, output_dir=None):
        """Analyze and visualize daily viewing patterns"""
        if output_dir is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            output_dir = os.path.join(project_root, 'reports', 'figures')

        os.makedirs(output_dir, exist_ok=True)

        # Calculate average videos by day of week
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_counts = self.df.groupby('day_of_week').size()
        daily_avg = (daily_counts / self.df['date'].nunique() * 7).reindex(day_order)

        plt.figure()
        ax = daily_avg.plot(kind='bar', color='#3b82f6')
        plt.title('Average Videos Watched by Day of Week', pad=20)
        plt.xlabel('')
        plt.ylabel('')
        plt.xticks(rotation=45)
        plt.grid(True, color= 'white' ,axis='y', alpha=1)

        plt.tight_layout()
        plt.savefig(f'{output_dir}/daily_patterns.png', dpi=300, bbox_inches='tight')
        plt.close()

        return {'daily_averages': daily_avg}

    def analyze_hourly_patterns(self, output_dir=None):
        """Analyze and visualize hourly viewing patterns"""
        if output_dir is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            output_dir = os.path.join(project_root, 'reports', 'figures')

        os.makedirs(output_dir, exist_ok=True)

        # Calculate average videos by hour
        hourly_counts = self.df.groupby('hour').size()
        hourly_avg = hourly_counts / self.df['date'].nunique()

        plt.figure()
        ax = hourly_avg.plot(kind='bar', color='#3b82f6')
        plt.title('Average Videos Watched by Hour', pad=20)
        plt.xlabel('Hour of Day (24-hour format)')
        plt.xticks(rotation = 360)
        plt.ylabel('Average Number of Videos')
        plt.grid(True, color= '#FFFFFF' ,axis='y', alpha= 1)

        # Add value labels
        for i, v in enumerate(hourly_avg):
            ax.text(i, v, f'{v:.1f}', ha='center', va='bottom')

        plt.tight_layout()
        plt.savefig(f'{output_dir}/hourly_patterns.png', dpi=300, bbox_inches='tight')
        plt.close()

        return {'hourly_averages': hourly_avg}

    def analyze_sessions(self, output_dir=None):
        """Analyze viewing session patterns"""
        if output_dir is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            output_dir = os.path.join(project_root, 'reports', 'figures')

        os.makedirs(output_dir, exist_ok=True)

        # Calculate session statistics
        session_stats = self.df.groupby('session_id').agg({
            'datetime': ['count', 'min', 'max']
        })
        session_stats.columns = ['video_count', 'start_time', 'end_time']
        session_stats['duration_minutes'] = (
                                                    session_stats['end_time'] - session_stats['start_time']
                                            ).dt.total_seconds() / 60

        # Create duration categories
        duration_bins = [0, 30, 60, 90, 120, float('inf')]
        duration_labels = ['0-30min', '30-60min', '60-90min', '90-120min', '120+min']
        session_stats['duration_category'] = pd.cut(
            session_stats['duration_minutes'],
            bins=duration_bins,
            labels=duration_labels
        )

        # Plot session duration distribution
        duration_dist = session_stats['duration_category'].value_counts().sort_index()

        plt.figure()
        ax = duration_dist.plot(kind='bar', color='#3b82f6')
        plt.title('Distribution of Session Durations', pad=20)
        plt.xlabel('Session Duration')
        plt.ylabel('Number of Sessions')
        plt.grid(True, axis='y', alpha=0.3)
        plt.xticks(rotation=45)

        # Add value labels
        for i, v in enumerate(duration_dist):
            ax.text(i, v, str(v), ha='center', va='bottom')

        plt.tight_layout()
        plt.savefig(f'{output_dir}/session_durations.png', dpi=300, bbox_inches='tight')
        plt.close()

        return {'session_stats': session_stats}

    def generate_report(self, output_file=None):
        """Generate a comprehensive analysis report"""
        if output_file is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            output_file = os.path.join(project_root, 'reports', 'temporal_analysis.txt')

        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Run all analyses
        monthly_stats = self.analyze_monthly_trends()
        daily_stats = self.analyze_daily_patterns()
        hourly_stats = self.analyze_hourly_patterns()
        session_stats = self.analyze_sessions()

        # Generate report
        with open(output_file, 'w') as f:
            f.write("YouTube Viewing Habits Analysis Report\n")
            f.write("====================================\n\n")

            # Overall Statistics
            total_videos = len(self.df)
            total_days = self.df['date'].nunique()
            total_sessions = len(session_stats['session_stats'])

            f.write("Overall Statistics\n")
            f.write("-----------------\n")
            f.write(f"Total videos watched: {total_videos:,}\n")
            f.write(f"Total days with activity: {total_days:,}\n")
            f.write(f"Total viewing sessions: {total_sessions:,}\n")
            f.write(f"Average videos per active day: {total_videos / total_days:.1f}\n\n")

            # Peak Activity Times
            daily_avg = daily_stats['daily_averages']
            hourly_avg = hourly_stats['hourly_averages']

            f.write("Peak Activity Times\n")
            f.write("-----------------\n")
            f.write(f"Most active day: {daily_avg.idxmax()} ({daily_avg.max():.1f} videos)\n")
            f.write(f"Peak viewing hour: {hourly_avg.idxmax():02d}:00 ({hourly_avg.max():.1f} videos)\n\n")

            # Session Analysis
            session_data = session_stats['session_stats']
            avg_duration = session_data['duration_minutes'].mean()
            median_duration = session_data['duration_minutes'].median()

            f.write("Session Analysis\n")
            f.write("----------------\n")
            f.write(f"Average session duration: {avg_duration:.1f} minutes\n")
            f.write(f"Median session duration: {median_duration:.1f} minutes\n")
            f.write(f"Average videos per session: {session_data['video_count'].mean():.1f}\n")


def main():
    try:
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        data_path = os.path.join(project_root, 'data', 'raw', 'watch-history.csv')

        print(f"Loading data from: {data_path}")
        df = pd.read_csv(data_path)

        print("Creating analyzer instance...")
        analyzer = TemporalAnalyzer(df)

        print("Generating visualizations and report...")
        analyzer.analyze_monthly_trends()
        analyzer.analyze_daily_patterns()
        analyzer.analyze_hourly_patterns()
        analyzer.analyze_sessions()
        analyzer.generate_report()

        print("Analysis complete! Check the reports directory for results.")

    except Exception as e:
        print(f"Error during analysis: {e}")


if __name__ == "__main__":
    main()