import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load Datasets[cite: 1]
matches = pd.read_csv("matches.csv")
deliveries = pd.read_csv("deliveries.csv")

# 1. Total number of matches conducted in 2008[cite: 1]
matches_2008 = len(matches[matches["season"] == 2008])
print(f"1. Total matches in 2008: {matches_2008}\n")

# 2. Cities with maximum and minimum number of matches[cite: 1]
city_counts = matches["city"].value_counts()
max_city = city_counts[city_counts == city_counts.max()].index.tolist()
min_city = city_counts[city_counts == city_counts.min()].index.tolist()
print(f"2. City/Cities with MAX matches: {max_city}")
print(f"   City/Cities with MIN matches: {min_city}\n")

# 3. Total count of matches city-wise[cite: 1]
matches_citywise = matches["city"].value_counts()
print("3. Match count city-wise:\n", matches_citywise, "\n")

# 4. Tally the toss decisions each team has taken[cite: 1]
toss_tally = (
    matches.groupby(["toss_winner", "toss_decision"])
    .size()
    .unstack(fill_value=0)
)
print("4. Toss decisions per team:\n", toss_tally, "\n")

# 5. Total number of normal and tied matches[cite: 1]
result_counts = matches["result"].value_counts()
print("5. Match Result Counts:\n", result_counts, "\n")

# 6. Teams where the result was a tie[cite: 1]
tied_matches = matches[matches["result"] == "tie"]
tied_teams = set(tied_matches["team1"]).union(set(tied_matches["team2"]))
print("6. Teams involved in tied matches:\n", tied_teams, "\n")

# 7. Team winning by highest and lowest number of runs[cite: 1]
max_run_win_idx = matches["win_by_runs"].idxmax()
max_runs_team = matches.loc[max_run_win_idx, "winner"]
max_runs_val = matches.loc[max_run_win_idx, "win_by_runs"]

min_runs_df = matches[matches["win_by_runs"] > 0]
min_runs_val = min_runs_df["win_by_runs"].min()
min_runs_teams = min_runs_df[min_runs_df["win_by_runs"] == min_runs_val][
    "winner"
].unique()

print(
    f"7. Highest Win by Runs: {max_runs_team} ({max_runs_val} runs)"
)
print(
    f"   Lowest Win by Runs (>0): {list(min_runs_teams)} ({min_runs_val} run)\n"
)

# 8. Mean, Median, and Std Dev of 'win_by_runs'[cite: 1]
mean_wbr = matches["win_by_runs"].mean()
median_wbr = matches["win_by_runs"].median()
std_wbr = matches["win_by_runs"].std()
print(
    f"8. Win By Runs Statistics:\n   Mean: {mean_wbr:.2f}\n   Median: {median_wbr}\n   Std Dev: {std_wbr:.2f}\n"
)

# 9. Venue where team won by highest and lowest runs[cite: 1]
max_runs_venue = matches.loc[max_run_win_idx, "venue"]
min_runs_venues = min_runs_df[min_runs_df["win_by_runs"] == min_runs_val][
    "venue"
].unique()
print(f"9. Venue with Highest Run Win: {max_runs_venue}")
print(f"   Venues with Lowest Run Win: {list(min_runs_venues)}\n")

# 10. Players winning 'Player of the Match' > 3 times[cite: 1]
pom_counts = matches["player_of_match"].value_counts()
top_pom = pom_counts[pom_counts > 3]
print("10. Players with >3 Player of the Match awards:\n", top_pom, "\n")

# 11. All deliveries where batsman scored a six[cite: 1]
sixes_df = deliveries[deliveries["batsman_runs"] == 6]
print(f"11. Total sixes hit in dataset: {len(sixes_df)}\n")

# 12. Average runs scored in matches across all venues[cite: 1]
match_runs = (
    deliveries.groupby("match_id")["total_runs"].sum().reset_index()
)
match_venue_df = matches[["id", "venue"]].merge(
    match_runs, left_on="id", right_on="match_id"
)
avg_runs_venue = match_venue_df.groupby("venue")["total_runs"].mean()
print("12. Average runs scored per match by venue:\n", avg_runs_venue, "\n")

# 13. Umpires who umpired maximum number of times[cite: 1]
all_umpires = pd.concat(
    [matches["umpire1"], matches["umpire2"], matches["umpire3"]]
).value_counts()
top_umpires = all_umpires[all_umpires == all_umpires.max()]
print("13. Most frequent umpires:\n", top_umpires, "\n")

# 14. Total number of matches played in each season[cite: 1]
season_matches = matches["season"].value_counts().sort_index()
print("14. Matches played per season:\n", season_matches, "\n")

# 15. Total runs scored in each season[cite: 1]
merged_matches = matches[["id", "season"]].merge(
    deliveries, left_on="id", right_on="match_id"
)
season_runs = merged_matches.groupby("season")["total_runs"].sum()
print("15. Total runs per season:\n", season_runs, "\n")

# 16. Total runs scored by each batsman (Top 10)[cite: 1]
top_batsmen = (
    deliveries.groupby("batsman")["batsman_runs"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print("16. Top 10 Batsmen by total runs:\n", top_batsmen, "\n")

# 17. Total number of wickets taken by each bowler[cite: 1]
bowler_dismissals = [
    "caught",
    "bowled",
    "lbw",
    "stumped",
    "caught and bowled",
    "hit wicket",
]
bowler_wickets = (
    deliveries[deliveries["dismissal_kind"].isin(bowler_dismissals)]
    .groupby("bowler")["player_dismissed"]
    .count()
    .sort_values(ascending=False)
)
print(
    "17. Top 10 Bowlers by Wickets:\n", bowler_wickets.head(10), "\n"
)

# 18. Batting averages and top 10[cite: 1]
batsman_runs = deliveries.groupby("batsman")["batsman_runs"].sum()
dismissals = deliveries[deliveries["player_dismissed"].notna()][
    "player_dismissed"
].value_counts()
batting_avg = (batsman_runs / dismissals).dropna().sort_values(ascending=False)
print("18. Top 10 Batting Averages:\n", batting_avg.head(10), "\n")

# 19. Visualize toss decisions across all seasons[cite: 1]
toss_season = (
    matches.groupby(["season", "toss_decision"])
    .size()
    .unstack(fill_value=0)
)
plt.figure(figsize=(10, 5))
toss_season.plot(kind="bar", stacked=False, figsize=(10, 5))
plt.title("19. Toss Decisions Across All Seasons")
plt.xlabel("Season")
plt.ylabel("Count")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# 20. Visualize Total Matches vs Winning Matches vs Win Rate for all teams[cite: 1]
t1 = matches["team1"].value_counts()
t2 = matches["team2"].value_counts()
total_played = (t1.add(t2, fill_value=0)).sort_index()
wins = matches["winner"].value_counts().sort_index()

team_stats = pd.DataFrame({"Total": total_played, "Wins": wins}).fillna(0)
team_stats["Win Rate (%)"] = (team_stats["Wins"] / team_stats["Total"]) * 100

fig, ax1 = plt.subplots(figsize=(12, 6))
team_stats[["Total", "Wins"]].plot(kind="bar", ax=ax1, width=0.8)
ax1.set_ylabel("Matches Count")
ax1.set_title(
    "20. Total Matches vs Winning Matches vs Win Rate for All Teams"
)
ax1.grid(axis="y", linestyle="--", alpha=0.5)

ax2 = ax1.twinx()
ax2.plot(
    team_stats.index,
    team_stats["Win Rate (%)"],
    color="red",
    marker="o",
    linewidth=2,
    label="Win Rate (%)",
)
ax2.set_ylabel("Win Rate (%)")
fig.tight_layout()
plt.show()

# 21. Distribution of teams who won the matches[cite: 1]
plt.figure(figsize=(10, 6))
matches["winner"].value_counts().plot(kind="pie", autopct="%1.1f%%")
plt.title("21. Distribution of Match Winners")
plt.ylabel("")
plt.tight_layout()
plt.show()

# 22. Visualize toss outcomes of all teams[cite: 1]
toss_team = (
    matches.groupby(["toss_winner", "toss_decision"])
    .size()
    .unstack(fill_value=0)
)
plt.figure(figsize=(12, 6))
toss_team.plot(kind="bar", figsize=(12, 6))
plt.title("22. Toss Decisions Chosen by Each Team")
plt.xlabel("Count")
plt.ylabel("Team")
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# 23. Top 5 teams with most wins across all seasons[cite: 1]
top5_wins = matches["winner"].value_counts().head(5).sort_values(ascending=True)
plt.figure(figsize=(8, 4))
plt.bar(top5_wins.index, top5_wins.values, color="skyblue", edgecolor="black")
plt.title("23. Top 5 Teams with Most Wins")
plt.xlabel("Total Wins")
plt.ylabel("Team")
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()