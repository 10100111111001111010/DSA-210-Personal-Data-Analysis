import pandas as pd
from datetime import datetime


def engineer_temporal_features(df):
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['hour'] = df['datetime'].dt.hour
    df['day_of_week'] = df['datetime'].dt.day_name()
    df['month'] = df['datetime'].dt.month
    df['year'] = df['datetime'].dt.year
    df['is_weekend'] = df['datetime'].dt.dayofweek.isin([5, 6])
    df['time_of_day'] = pd.cut(df['hour'], bins=[0, 6, 12, 18, 24], labels=['Night', 'Morning', 'Afternoon', 'Evening'])

    return df


def engineer_content_features(df):

    def extract_category(title):
        common_categories = {
            'tutorial': ['tutorial', 'how to', 'guide'],
            'music': ['music', 'official video', 'lyrics'],
            'gaming': ['gameplay', 'gaming', 'playthrough'],
            'tech': ['tech', 'review', 'unboxing'],
            'educational': ['lecture', 'course', 'lesson']
        }

        title_lower = title.lower()
        for category, keywords in common_categories.items():
            if any(keyword in title_lower for keyword in keywords):
                return category
        return 'other'

    df['category'] = df['title'].apply(extract_category)
    return df


def engineer_session_features(df):
    df = df.sort_values('datetime')
    df['time_diff'] = df['datetime'].diff()
    df['new_session'] = df['time_diff'] > pd.Timedelta(minutes=30)
    df['session_id'] = df['new_session'].cumsum()

    return df


def build_features(df):
    df = engineer_temporal_features(df)
    df = engineer_content_features(df)
    df = engineer_session_features(df)

    return df


if __name__ == "__main__":
    # Load the cleaned data
    df = pd.read_csv('../../data/raw/watch-history.csv')

    # Engineer all features
    df_engineered = build_features(df)

    # Save engineered features
    df_engineered.to_csv('../../data/processed/aggregated_stats.csv', index=False)
    print("Engineered features saved to aggregated_stats.csv")