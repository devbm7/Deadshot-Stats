# Deadshot Stats Dashboard

A very nice good comprehensive gaming analytics dashboard for tracking player performance, team dynamics, and match statistics.

## 🎮 Game Modes Supported

### Standard Modes
- **Team**: Team-based matches with assists and team assignments
- **FFA (Free-for-All)**: Individual performance tracking

### Tag Collection Modes
- **Confirm**: Tag collection mode where players drop tags when killed. The player with the most collected tags wins.
- **Team Confirm**: Team-based tag collection where teams compete for the most total tags. The team with the most tags wins.

## 🚀 Features

### 📊 Analytics
- **Player Performance**: K/D ratios, win rates, per-minute statistics
- **Team Analysis**: Team chemistry, role analysis, formation performance
- **Match History**: Timeline analysis, map performance, weapon usage
- **Advanced Analytics**: Player evolution, performance clusters, streak analysis

### 🎯 Tag Collection Features
- **Tag Tracking**: Complete tag collection statistics for Confirm/Team Confirm modes
- **Tag Leaderboards**: Track total tags and average tags per match
- **Tag Performance**: Best match tags, tags per minute metrics
- **Team Tag Analysis**: Team tag collection performance and win rates

### 📈 Visualizations
- Interactive charts and graphs
- Performance trends over time
- Team chemistry heatmaps
- Player comparison radar charts

### 🎮 Data Input
- **AI-Powered Image Extraction**: Upload screenshots for automatic data extraction
- **Manual Entry**: Direct data input with validation
- **Bulk Import**: Support for CSV/Excel data import

## 🛠️ Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables (see Configuration section)
4. Run the app: `streamlit run app.py`

## ⚙️ Configuration

### Required Environment Variables
- `GEMINI_API_KEY`: For AI-powered image extraction
- `SUPABASE_URL` and `SUPABASE_KEY`: For cloud data storage

### Local Development
Create a `.streamlit/secrets.toml` file:
```toml
[gemini]
api_key = "your_gemini_api_key_here"

[supabase]
url = "your_supabase_url_here"
key = "your_supabase_key_here"
```

## 📊 Data Structure

The dashboard tracks the following metrics:
- **Basic Stats**: Kills, deaths, assists, score, coins
- **Tag Stats**: Tags collected (for Confirm/Team Confirm modes)
- **Performance**: K/D ratios, win rates, per-minute metrics
- **Technical**: Ping, weapon usage, map performance
- **Team**: Team assignments, team performance, chemistry

## 🎯 Tag Collection Mechanics

### Confirm Mode
- Players drop tags when killed
- Other players can collect these tags
- Winner is determined by total tags collected
- Individual performance tracking

### Team Confirm Mode
- Same tag collection mechanics as Confirm
- Teams compete for total team tags
- Team with most combined tags wins
- Includes team assists and coordination

## 📈 Analytics Features

### Player Analysis
- Individual performance tracking
- Tag collection efficiency
- Performance evolution over time
- Achievement tracking

### Team Analysis
- Team chemistry and synergy
- Role-based analysis
- Formation performance
- Tag collection strategies

### Advanced Features
- Performance clustering
- Streak analysis
- Gaming session analysis
- Predictive analytics

## 🏆 Leaderboards

Multiple leaderboard types including:
- K/D Ratio
- Total Kills
- Win Rate
- **Total Tags** (new)
- **Average Tags per Match** (new)
- And more...

## 🔧 Technical Details

- **Backend**: Python with Streamlit
- **Data Storage**: CSV files with Supabase cloud backup
- **AI Integration**: Google Gemini for image processing
- **Visualizations**: Plotly for interactive charts
- **Data Processing**: Pandas for analytics

## 📝 Usage

1. **Add Match Data**: Use the Data Input page to add new matches
2. **View Analytics**: Explore player and team performance
3. **Track Progress**: Monitor improvements over time
4. **Compare Players**: Use comparison tools to analyze differences
5. **Export Data**: Download statistics for external analysis

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

This project is licensed under the MIT License.
