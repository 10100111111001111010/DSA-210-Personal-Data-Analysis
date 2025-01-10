# YouTube Viewing Habits Analysis: Understanding Digital Content Consumption

- [Presentation File](presentation/DSA210-Presentation.pptx)

## Motivation
This project aims to analyze personal YouTube viewing patterns using data collected through Google Takeout. By examining viewing habits and temporal patterns, the goal is to gain insights into digital content consumption behaviors and understand how they reflect daily routines and interests. This analysis can help optimize content consumption and provide valuable insights into time management.

## Data Source
The data is sourced from personal YouTube watch history through Google Takeout, containing detailed information about:
- Video titles and links
- Precise timestamps of views
- Watch duration and session information
- Complete viewing history from 2024 onwards

## Data Analysis Techniques

### 1. Temporal Pattern Analysis
The project implements a comprehensive TemporalAnalyzer class that processes and analyzes viewing patterns across different time scales:

- **Hourly Analysis**: Examines the distribution of video consumption throughout the day
- **Daily Patterns**: Investigates viewing habits across different days of the week
- **Monthly Trends**: Tracks changes in viewing patterns over months
- **Session Analysis**: Identifies and analyzes viewing sessions with specific focus on binge-watching behavior

### 2. Key Features Analyzed
- Time-based patterns (hour of day, day of week, monthly trends)
- Session identification and analysis
- Binge-watching patterns (defined as sessions with more than 5 videos)
- Average video consumption rates

### 3. Visualization Techniques
The project utilizes various visualization methods to present the findings:
- Bar charts for hourly and daily patterns
- Line plots for monthly trends
- Custom-colored visualizations for AM/PM viewing patterns
- Specialized plots for binge-watching analysis

## Key Findings

1. **Temporal Patterns**
   - Detailed hourly distribution of video consumption
   - Weekly viewing patterns and weekend vs. weekday differences
   - Monthly trends showing long-term viewing habits

2. **Binge-Watching Insights**
   - Overall binge-watching percentage across all sessions
   - Hour-by-hour breakdown of binge-watching tendencies
   - Peak binge-watching hours identified

## Technical Implementation

### Tools and Libraries Used
- Python 3.13
- pandas: Data manipulation and analysis
- matplotlib: Data visualization
- seaborn: Enhanced visualizations
- numpy: Numerical computations
- Other utilities: os, calendar, collections

### Code Structure
1. **Data Loading and Preprocessing**
   - CSV file reading and datetime conversion
   - Feature engineering for temporal analysis
   - Session identification logic

2. **Analysis Components**
   - Temporal pattern analysis
   - Session-based analysis
   - Binge-watching pattern detection
   - Visualization generation

3. **Visualization Pipeline**
   - Consistent styling with custom color schemes
   - Automated figure generation and saving
   - Clean and minimal plot designs

## Limitations and Future Work

### Current Limitations
- Analysis limited to 2024 data
- Focus primarily on temporal patterns
- Basic session identification based on time gaps

### Future Enhancements
1. **Extended Analysis**
   - Content category analysis
   - Channel preference analysis
   - Correlation with external factors

2. **Technical Improvements**
   - Real-time data updating
   - Interactive visualizations
   - Machine learning for pattern prediction

3. **Additional Features**
   - Content recommendation system
   - Automated reporting system
   - Personal insights dashboard
