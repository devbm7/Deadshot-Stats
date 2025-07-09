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
- **Player Details**: Favorite weapons, best matches, and averages
- **Accuracy Metrics**: Calculate and display player accuracy percentages

### 👥 Team Analysis
- **Team Performance**: Win/loss ratios and team statistics
- **Team Synergy**: Analyze how teams perform together
- **Team Comparisons**: Head-to-head team performance analysis

### 📋 Leaderboards
- **Multiple Metrics**: K/D ratio, total kills, accuracy, average kills, total score, coins
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
match_id,datetime,game_mode,map_name,team,player_name,kills,deaths,assists,score,weapon,ping,coins
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
- **Accuracy**: Percentage of kills vs total engagements
- **Average Kills per Match**: Consistency metric
- **Best Performance**: Highest kills and score in a single match
- **Weapon Preferences**: Most used weapons and performance with each

### Team Performance
- **Win Rate**: Percentage of matches won
- **Team Synergy**: Combined team performance
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