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

## ☁️ Cloud Data Storage with Supabase

This app now supports cloud data storage using Supabase, which provides:

- **Persistent Data**: Your match data persists across deployments and sessions
- **Multi-User Support**: Multiple users can access the same data
- **Real-time Updates**: Changes are reflected immediately across all users
- **Automatic Backups**: Your data is safely stored in the cloud
- **Scalable**: Handles growing datasets efficiently

### Supabase Setup

1. **Create a Supabase Project**:
   - Go to [supabase.com](https://supabase.com)
   - Sign up/Login and create a new project
   - Wait for the project to be ready

2. **Get Your Credentials**:
   - Go to Settings → API in your Supabase dashboard
   - Copy the "Project URL" and "anon public" key

3. **Configure Environment Variables**:
   - Create a `.env` file in your project root:
     ```
     SUPABASE_URL=your_project_url_here
     SUPABASE_KEY=your_anon_key_here
     ```

4. **For Streamlit Cloud Deployment**:
   - Add these secrets in your Streamlit Cloud dashboard:
     ```
     [supabase]
     url = "your_project_url_here"
     key = "your_anon_key_here"
     ```

5. **Create the Database Table**:
   - Run the SQL script in your Supabase SQL editor (see `config.py` for the full script)

### Testing the Connection

Run the test script to verify your Supabase setup:

```bash
python test_supabase.py
```

### Migrating Existing Data

If you have existing data in `data/matches.csv`, you can migrate it to Supabase:

```bash
python migrate_to_supabase.py
```

This will:
- Create a backup of your existing CSV file
- Migrate all your match data to Supabase
- Preserve your original data as a backup

## 🛠️ Installation

1. **Clone the repository**:

   ```bash
   git clone devbm7/deadhot-stats
   cd deadshot-stats
   ```
2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```
3. **Configure API Keys**:

   **For Gemini API (image extraction)**:
   - Go to https://makersuite.google.com/app/apikey
   - Copy `env.example` to `.env` and add your Gemini API key
   
   **For Supabase (cloud storage)**:
   - Go to [supabase.com](https://supabase.com) and create a new project
   - Get your project URL and anon key from Settings → API
   - Add to your `.env` file:
     ```
     SUPABASE_URL=your_project_url_here
     SUPABASE_KEY=your_anon_key_here
     ```
   
4. **Set up Supabase** (for cloud data storage):

   - Run the SQL script in your Supabase SQL editor (see `config.py` for the full script)

4. **Test Supabase connection** (optional):

   ```bash
   python test_supabase.py
   ```

5. **Run the application**:

   ```bash
   streamlit run app.py
   ```
5. **Open your browser** and navigate to `http://localhost:8501`

### 🔑 API Key Setup

The image extraction feature requires a Google Gemini API key:

#### For Local Development:
1. **Get API Key**: Visit https://makersuite.google.com/app/apikey
2. **Create .env file**: Copy `env.example` to `.env` and add your API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

#### For Streamlit Cloud Deployment:
1. **Get API Key**: Visit https://makersuite.google.com/app/apikey
2. **Add to Secrets**: In your Streamlit Cloud dashboard, add:
   ```
   [gemini]
   api_key = "your_gemini_api_key_here"
   ```

> **Note**: The API key is only used for image analysis and is not stored permanently.

## 📁 Project Structure

```
deadshot-stats/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── test_image_extraction.py # Test script for image extraction
├── data/
│   ├── matches.csv       # Match data storage
│   └── Images/           # Example screenshots and assets
│       ├── Example Results/
│       ├── Guns/
│       └── Maps/
└── utils/
    ├── data_processing.py # Data loading and validation
    ├── calculations.py    # Statistical calculations
    ├── visualizations.py  # Chart and plot creation
    └── image_processing.py # AI-powered image data extraction
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
- **map_name**: Name of the map played (Refinery, Factory, Forest, Neo Tokyo, Vineyard, Snowfall)
- **team**: Team assignment (Team1, Team2, or null for FFA)
- **player_name**: Name of the player
- **kills**: Number of kills
- **deaths**: Number of deaths
- **assists**: Number of assists (required for team matches)
- **score**: Total score for the match
- **weapon**: Primary weapon used (AR, SMG, Sniper, Shotgun)
- **ping**: Network ping in milliseconds
- **coins**: Coins earned in the match
- **match_length**: Length of the match in minutes (e.g., 5, 10, 20)

## 🎯 How to Use

### Adding Match Data

#### 👥 Managing Players

The system supports both existing players and custom player names:

**Existing Players**: Choose from a dropdown of players who have played before
**Custom Names**: Type any player name for new players

**Current Players in System**:
- DevilOHeaven
- MaXiMus22  
- Heet63
- Alice, Bob, Charlie, David (sample players)

**Available Maps**:
- Refinery (formerly City)
- Factory (formerly Desert)
- Forest
- Neo Tokyo
- Vineyard
- Snowfall

**Available Weapons**:
- AR (formerly AK47)
- SMG (formerly M4A1)
- Sniper (formerly AWP)
- Shotgun

**To Add New Players**:
1. Run the utility script: `python add_players.py`
2. Edit the `new_players` list in the script
3. Or simply type new player names when adding match data

**To Add All Maps and Weapons**:
1. Run the utility script: `python update_maps_weapons.py`
2. This will add sample matches for all maps and weapons
3. All maps and weapons will then appear in dropdown menus

#### 📷 Image Upload (AI-Powered)
1. Navigate to the **"🎮 Data Input"** page
2. Select the **"📷 Image Upload"** tab
3. **Configure API Key** (if not already done):
   - For local development: Add to `.env` file
   - For cloud deployment: Add to Streamlit secrets
4. Upload a screenshot of the match results
5. Click **"🔍 Extract Data from Image"** to automatically extract data using AI
6. Review and edit the extracted data:
   - **Player Names**: Choose from existing players or type custom names
   - **Stats**: Verify kills, deaths, assists, score, weapon, ping, coins
   - **Match Info**: Confirm date, game mode, map, match length
7. Click **"💾 Save Match"** to save the data

#### ✏️ Manual Input
1. Navigate to the **"🎮 Data Input"** page
2. Select the **"✏️ Manual Input"** tab
3. Fill in match information (date, game mode, map)
4. Click **"➕ Add Player"** to add players
5. Enter each player's statistics
6. Click **"💾 Save Match"** to save the data

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
