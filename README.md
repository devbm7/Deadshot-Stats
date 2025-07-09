# 🎯 Deadshot Stats Dashboard

A comprehensive gaming statistics dashboard built with Streamlit to track and analyze player performance in FPS games.

## 🚀 Features

### 📊 Dashboard Overview
- **Quick Stats Cards**: Total matches, kills, players, and average K/D ratio
- **Recent Activity**: Last 7 days of gaming activity
- **Interactive Charts**: K/D leaderboards and weapon usage statistics
- **Match Timeline**: Visual representation of all matches over time

### 🎮 Data Input
- **Manual Match Entry**: Add new matches with detailed player statistics
- **Flexible Game Modes**: Support for both Team and FFA (Free-for-All) matches
- **Comprehensive Data**: Track kills, deaths, assists, score, weapons, ping, and coins
- **Data Validation**: Automatic validation to ensure data integrity

### 📈 Player Analysis
- **Individual Performance**: Detailed stats for each player
- **Performance Trends**: Track player improvement over time
- **Player Details**: Favorite weapons, best matches, assists, wins/losses, and averages

### 👥 Team Analysis
- **Team Performance**: Win/loss ratios and team statistics
- **Team Synergy**: Analyze how teams perform together including assists
- **Team Comparisons**: Head-to-head team performance analysis

### 📋 Leaderboards
- **Multiple Metrics**: K/D ratio, total kills, assists, average kills, total score, coins, win rate
- **Interactive Rankings**: Sortable leaderboards with visual charts
- **Player Rankings**: See who's performing best in different categories

### 🔧 Advanced Analytics
- **Player Comparison**: Radar charts comparing multiple players
- **Ping Impact**: Analyze how ping affects performance
- **Weapon Meta**: Most popular and effective weapons
- **Map Performance**: Track performance across different maps

### 📈 Match History
- **Filtered Views**: Filter by date range, players, and game modes
- **Match Timeline**: Visual timeline of all matches
- **Map Analysis**: Performance statistics for different maps

## **Advanced Analytics**

The Advanced Analytics page provides deep insights into player performance patterns:

### **Player Evolution Timeline**
- **Trend Analysis**: Track how players improve over time with moving averages
- **Performance Metrics**: K/D ratio, kills per minute, and score per minute evolution
- **Improvement Insights**: Compare first and latest match performance

### **Performance Clusters**
- **Player Grouping**: Machine learning clustering based on playing styles
- **Cluster Characteristics**: Groups players by K/D ratio, kills per minute, assists, and win rate
- **Cluster Analysis**: Identifies high performers, balanced players, and struggling players

### **Streak Analysis**
- **Win/Loss Streaks**: Track current and maximum streaks for each player
- **Recent Performance**: Win rate in last 10 matches
- **Streak Insights**: Visual indicators for ongoing streaks

### **Game Mode Analysis**
- **Mode Comparison**: Team vs FFA performance metrics
- **Normalized Metrics**: Per-minute statistics to avoid bias from match length
- **Player Distribution**: Matches per player across different modes

### **Map Performance Analysis**
- **Map Heatmaps**: Visual representation of performance across maps
- **Per-Minute Metrics**: Normalized statistics for fair comparison
- **Map Preferences**: Which maps favor different play styles

### **Weapon-Map Combinations**
- **Effectiveness Matrix**: Which weapons perform best on which maps
- **Usage Patterns**: Most popular weapon choices per map
- **Performance Correlation**: Weapon effectiveness vs map characteristics

## **Team Analysis**

The Team Analysis page provides comprehensive insights into team performance and dynamics:

### **Team Performance**
- **Team Statistics**: Win rates, total kills, average scores per team
- **Team Comparison**: Visual comparison of team performance metrics
- **Team Details**: Expandable sections with detailed team statistics

### **Team Dynamics**
- **Team Chemistry Matrix**: Heatmap showing win rates when players team up together
- **Player Role Analysis**: Radar chart showing each player's strengths and primary role
- **Team Formation Performance**: Bubble chart showing how different team combinations perform

### **Player Roles**
- **Killer**: High K/D ratio and kill rate - primary damage dealer
- **Support**: High assist rate with low deaths - team support player
- **Aggressive**: High death rate - aggressive but risky playstyle
- **Leader**: High win rate with good K/D - team leader
- **Balanced**: Well-rounded player with balanced stats

### **Team Formation Analysis**
- **Formation Performance**: Win rates and statistics for different player combinations
- **Formation Size**: Analysis of 2-player, 3-player, and larger team formations
- **Elite Formations**: Identification of the most successful team combinations

## **Fun & Engaging Features**

The Fun Features page provides gamified elements to make stats tracking more engaging:

### **Battle Royale Rankings**
- **Tournament-Style Rankings**: Tier-based ranking system with Champion, Elite, Veteran, Rookie, and Novice tiers
- **Ranking Score**: Weighted combination of K/D ratio, win rate, kills per minute, matches played, and assists
- **Tier Visualization**: Diamond-shaped markers with color-coded tiers
- **Player Positioning**: Visual representation of player rankings within each tier

### **Achievement Badges**
- **Unlockable Achievements**: 10 different badges based on performance milestones
- **Progress Tracking**: Visual progress bars for each achievement
- **Badge Categories**:
  - **Sharpshooter**: K/D ratio above 2.0
  - **Kill Master**: 100+ total kills
  - **Survivor**: Less than 0.3 deaths per minute
  - **Support Hero**: 0.5+ assists per minute
  - **Winner**: 70%+ win rate
  - **Veteran**: 20+ matches played
  - **Speed Demon**: 1.0+ kills per minute
  - **Consistent**: 10+ matches played
  - **Elite**: Elite tier ranking
  - **Champion**: Champion tier ranking

### **Gaming Session Analysis**
- **Daily Performance**: Track K/D ratio trends over time
- **Hourly Performance**: Identify best gaming hours
- **Session Duration**: Analyze gaming session patterns
- **Session Performance**: Compare performance across different sessions
- **Peak Performance**: Identify optimal gaming periods

## **Interactive Dashboards**

The Interactive Dashboards page provides advanced tools for player comparison and scenario simulation:

### **Player Comparison Tool**
- **Side-by-Side Comparison**: Visual comparison of two players across all metrics
- **Interactive Sliders**: Adjust player stats to simulate different scenarios
- **Detailed Metrics**: K/D ratio, win rate, kills per minute, assists, total matches, total kills
- **Winner Analysis**: Shows which player wins in each category
- **Custom Scenarios**: Use sliders to boost or reduce player stats and see the impact

### **Scenario Simulator**
- **Team Composition Testing**: Simulate different team combinations
- **Performance Prediction**: Predict win rates and team performance
- **Synergy Analysis**: Calculate team synergy based on player roles
- **Head-to-Head Simulation**: Compare your team against opponents
- **Radar Chart Visualization**: Visual representation of team strengths

### **Optimal Team Finder**
- **Best Team Discovery**: Find the optimal team composition from available players
- **Comprehensive Analysis**: Test all possible combinations
- **Scoring System**: Rank teams by predicted win rate, synergy, and K/D ratio
- **Top Combinations**: View the best team combinations with detailed stats
- **Bubble Chart Visualization**: Visual representation of team performance

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd deadshot-stats
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and navigate to `http://localhost:8501`

## 📁 Project Structure

```
deadshot-stats/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── data/
│   └── matches.csv       # Match data storage
└── utils/
    ├── data_processing.py # Data loading and validation
    ├── calculations.py    # Statistical calculations
    └── visualizations.py  # Chart and plot creation
```

## 📊 Data Schema

The application uses a CSV file to store match data with the following structure:

```csv
match_id,datetime,game_mode,map_name,team,player_name,kills,deaths,assists,score,weapon,ping,coins,match_length
```

### Fields Explained:
- **match_id**: Unique identifier for each match
- **datetime**: Date and time of the match
- **game_mode**: "Team" or "FFA" (Free-for-All)
- **map_name**: Name of the map played
- **team**: Team assignment (Team1, Team2, or null for FFA)
- **player_name**: Name of the player
- **kills**: Number of kills
- **deaths**: Number of deaths
- **assists**: Number of assists (required for team matches)
- **score**: Total score for the match
- **weapon**: Primary weapon used
- **ping**: Network ping in milliseconds
- **coins**: Coins earned in the match
- **match_length**: Length of the match in minutes (e.g., 5, 10, 20)

## 🎯 How to Use

### Adding Match Data
1. Navigate to the **"🎮 Data Input"** page
2. Fill in match information (date, game mode, map)
3. Click **"➕ Add Player"** to add players
4. Enter each player's statistics
5. Click **"💾 Save Match"** to save the data

### Viewing Analytics
- **Dashboard**: Get an overview of all statistics
- **Player Analysis**: Select a player to see detailed performance
- **Team Analysis**: View team performance and win rates
- **Leaderboards**: Compare players across different metrics
- **Advanced Analytics**: Deep dive into performance patterns

### Filtering Data
- Use date range selectors to filter by time period
- Select specific players to focus on their data
- Filter by game mode (Team vs FFA)
- Use the sidebar navigation to switch between different views

## 📈 Key Metrics Tracked

### Individual Performance
- **K/D Ratio**: Kills divided by deaths
- **Win Rate**: Percentage of matches won
- **Total Assists**: Total assists across all matches
- **Average Kills per Match**: Consistency metric
- **Average Assists per Match**: Team support metric
- **Best Performance**: Highest kills, assists, and score in a single match
- **Weapon Preferences**: Most used weapons and performance with each

### Team Performance
- **Win Rate**: Percentage of matches won
- **Team Synergy**: Combined team performance including assists
- **Average Team Score**: Team scoring consistency

### Overall Statistics
- **Most Active Player**: Player with most matches
- **Weapon Meta**: Most popular and effective weapons
- **Map Performance**: Best and worst maps for each player
- **Ping Impact**: Performance correlation with network latency

## 🔧 Customization

### Adding New Metrics
1. Update the data schema in `utils/data_processing.py`
2. Add calculation functions in `utils/calculations.py`
3. Create visualization functions in `utils/visualizations.py`
4. Update the main app to display new metrics

### Styling
- Modify the CSS in the main app for custom styling
- Update chart colors and layouts in visualization functions
- Customize the sidebar and navigation

### Data Sources
- Currently uses CSV file storage
- Can be extended to support databases (SQLite, PostgreSQL)
- API integration possible for real-time data

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Cloud Deployment
The application can be deployed to:
- **Streamlit Cloud**: Direct deployment from GitHub
- **Heroku**: Using the requirements.txt
- **AWS/GCP**: Using container deployment

### Data Persistence
- Data is stored in `data/matches.csv`
- Backup the CSV file for data safety
- Consider database migration for larger datasets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🎮 Gaming Tips

- **Track Your Progress**: Use the dashboard to identify improvement areas
- **Analyze Weapon Performance**: Find your most effective weapons
- **Monitor Ping Impact**: Understand how network affects your gameplay
- **Team Synergy**: Use team analysis to improve coordination
- **Set Goals**: Use leaderboards to set performance targets

---

**Happy Gaming! 🎯** 