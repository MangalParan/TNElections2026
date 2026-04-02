"""
Tamil Nadu 2026 Election - Visualization Charts
Generates charts for the election analysis report using matplotlib
"""

import os
import sys
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_csv(filename):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    print("matplotlib not installed. Installing...")
    os.system(f"{sys.executable} -m pip install matplotlib --quiet")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    HAS_MPL = True

# Color scheme
COLORS = {
    "DMK": "#E31A1C",
    "ADMK": "#00A651",
    "INC": "#19AAED",
    "BJP": "#FF9933",
    "SPA": "#E31A1C",
    "ADMK+": "#00A651",
    "TVK": "#FFD700",
    "NTK": "#800080",
    "Others": "#999999",
    "PMK": "#FFFF00",
    "DMDK": "#FF6600",
}


# ─── Chart 1: Historical Assembly Winners Timeline ────────────────────────

def chart_historical_winners():
    historical = load_csv("historical_assembly_results.csv")
    
    years = [int(r["year"]) for r in historical]
    winner_seats = [int(r["winner_seats"]) for r in historical]
    winner_parties = [r["winner_party"] for r in historical]
    winner_votes = [float(r["winner_vote_pct"]) for r in historical]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
    fig.suptitle("Tamil Nadu Assembly Elections - Historical Results (1967-2021)", 
                 fontsize=16, fontweight="bold", y=0.98)
    
    # Seats chart
    bar_colors = [COLORS.get(p, "#999") for p in winner_parties]
    bars = ax1.bar(years, winner_seats, color=bar_colors, width=3.5, edgecolor="black", linewidth=0.5)
    ax1.axhline(y=118, color="black", linestyle="--", linewidth=1, alpha=0.5, label="Majority (118)")
    ax1.set_ylabel("Seats Won", fontsize=12)
    ax1.set_title("Winning Party Seats", fontsize=13)
    ax1.set_ylim(0, 200)
    
    for bar, party, seats in zip(bars, winner_parties, winner_seats):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
                f"{party}\n{seats}", ha="center", va="bottom", fontsize=8, fontweight="bold")
    
    ax1.legend(loc="upper right")
    
    # Vote % chart
    ax2.plot(years, winner_votes, "o-", color="#333", linewidth=2, markersize=8)
    ax2.fill_between(years, winner_votes, alpha=0.15, color="#E31A1C")
    ax2.set_ylabel("Vote Share (%)", fontsize=12)
    ax2.set_xlabel("Election Year", fontsize=12)
    ax2.set_title("Winning Party Vote Share", fontsize=13)
    ax2.set_ylim(20, 55)
    ax2.grid(axis="y", alpha=0.3)
    
    for x, y, p in zip(years, winner_votes, winner_parties):
        ax2.annotate(f"{y:.1f}%", (x, y), textcoords="offset points",
                    xytext=(0, 10), ha="center", fontsize=8)
    
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "chart1_historical_winners.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {path}")


# ─── Chart 2: Anti-Incumbency Pattern ────────────────────────────────────

def chart_alternation_pattern():
    results = [
        (1967, "DMK"), (1971, "DMK"), (1977, "ADMK"), (1980, "ADMK"),
        (1984, "ADMK"), (1989, "DMK"), (1991, "ADMK"), (1996, "DMK"),
        (2001, "ADMK"), (2006, "DMK"), (2011, "ADMK"), (2016, "ADMK"),
        (2021, "DMK"), (2026, "?")
    ]
    
    fig, ax = plt.subplots(figsize=(14, 6))
    fig.suptitle("Tamil Nadu: Power Alternation Pattern (1967-2026)", 
                 fontsize=16, fontweight="bold")
    
    for i, (year, party) in enumerate(results):
        if party == "DMK":
            color = COLORS["DMK"]
            y_pos = 1
        elif party == "ADMK":
            color = COLORS["ADMK"]
            y_pos = -1
        else:
            color = "#FFD700"
            y_pos = 0
        
        ax.barh(y_pos, 0.8, left=i, color=color, edgecolor="black", linewidth=1, height=0.6)
        ax.text(i + 0.4, y_pos, f"{year}\n{party}", ha="center", va="center",
               fontsize=8, fontweight="bold", color="white" if party != "?" else "black")
    
    ax.set_yticks([-1, 0, 1])
    ax.set_yticklabels(["ADMK Rule", "Unknown", "DMK Rule"], fontsize=12)
    ax.set_xlim(-0.5, len(results) + 0.5)
    ax.set_ylim(-2, 2)
    ax.axhline(y=0, color="gray", linestyle="-", linewidth=0.5)
    ax.set_xticks([])
    
    # Add question mark arrow for 2026
    ax.annotate("2026\n???", xy=(13, 0), fontsize=14, fontweight="bold",
               ha="center", va="center", color="#FF0000",
               bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", edgecolor="red", linewidth=2))
    
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "chart2_alternation_pattern.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {path}")


# ─── Chart 3: Opinion Poll Comparison ────────────────────────────────────

def chart_opinion_polls():
    polls = load_csv("opinion_polls_2026.csv")
    
    agencies = [p["agency"] for p in polls]
    spa_lo = [int(p["spa_seats_low"]) for p in polls]
    spa_hi = [int(p["spa_seats_high"]) for p in polls]
    admk_lo = [int(p["admk_seats_low"]) for p in polls]
    admk_hi = [int(p["admk_seats_high"]) for p in polls]
    tvk_lo = [int(p["tvk_seats_low"]) for p in polls]
    tvk_hi = [int(p["tvk_seats_high"]) for p in polls]
    
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.suptitle("TN 2026 Opinion Polls - Seat Projections Comparison",
                 fontsize=16, fontweight="bold")
    
    x = range(len(agencies))
    width = 0.25
    
    # SPA bars with range
    spa_mid = [(lo + hi) / 2 for lo, hi in zip(spa_lo, spa_hi)]
    spa_err = [(hi - lo) / 2 for lo, hi in zip(spa_lo, spa_hi)]
    admk_mid = [(lo + hi) / 2 for lo, hi in zip(admk_lo, admk_hi)]
    admk_err = [(hi - lo) / 2 for lo, hi in zip(admk_lo, admk_hi)]
    tvk_mid = [(lo + hi) / 2 for lo, hi in zip(tvk_lo, tvk_hi)]
    tvk_err = [(hi - lo) / 2 for lo, hi in zip(tvk_lo, tvk_hi)]
    
    bars1 = ax.bar([i - width for i in x], spa_mid, width, yerr=spa_err,
                   color=COLORS["SPA"], label="SPA (DMK-led)", edgecolor="black",
                   linewidth=0.5, capsize=5, alpha=0.85)
    bars2 = ax.bar([i for i in x], admk_mid, width, yerr=admk_err,
                   color=COLORS["ADMK+"], label="ADMK+ (NDA)", edgecolor="black",
                   linewidth=0.5, capsize=5, alpha=0.85)
    bars3 = ax.bar([i + width for i in x], tvk_mid, width, yerr=tvk_err,
                   color=COLORS["TVK"], label="TVK", edgecolor="black",
                   linewidth=0.5, capsize=5, alpha=0.85)
    
    ax.axhline(y=118, color="black", linestyle="--", linewidth=2, label="Majority (118)")
    ax.set_xlabel("Polling Agency", fontsize=12)
    ax.set_ylabel("Projected Seats", fontsize=12)
    ax.set_xticks(list(x))
    ax.set_xticklabels(agencies, fontsize=10, rotation=15, ha="right")
    ax.set_ylim(0, 210)
    ax.legend(fontsize=11, loc="upper right")
    ax.grid(axis="y", alpha=0.3)
    
    # Add value labels
    for bars, mids in [(bars1, spa_mid), (bars2, admk_mid), (bars3, tvk_mid)]:
        for bar, mid in zip(bars, mids):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                   f"{mid:.0f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
    
    # Add sample sizes
    for i, p in enumerate(polls):
        sample = int(p["sample_size"])
        ax.text(i, -12, f"n={sample:,}", ha="center", fontsize=8, color="gray")
    
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "chart3_opinion_polls.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {path}")


# ─── Chart 4: Vote Share Trends ──────────────────────────────────────────

def chart_vote_share_trends():
    data = [
        (2006, 26.46, 32.64, 0, 0, 40.90),
        (2011, 22.39, 38.40, 0, 0, 39.21),
        (2016, 31.86, 41.06, 0, 0, 27.08),
        (2021, 37.70, 33.29, 0, 6.58, 22.43),
        (2026, 40.0, 34.0, 13.0, 4.0, 9.0),  # Projected
    ]
    
    years = [d[0] for d in data]
    dmk_v = [d[1] for d in data]
    admk_v = [d[2] for d in data]
    tvk_v = [d[3] for d in data]
    ntk_v = [d[4] for d in data]
    others_v = [d[5] for d in data]
    
    fig, ax = plt.subplots(figsize=(12, 7))
    fig.suptitle("TN Assembly Elections - Vote Share Trends (2006-2026P)",
                 fontsize=16, fontweight="bold")
    
    ax.stackplot(years, dmk_v, admk_v, tvk_v, ntk_v, others_v,
                labels=["DMK Alliance", "ADMK Alliance", "TVK", "NTK", "Others"],
                colors=[COLORS["DMK"], COLORS["ADMK"], COLORS["TVK"], COLORS["NTK"], COLORS["Others"]],
                alpha=0.8)
    
    ax.set_xlabel("Election Year", fontsize=12)
    ax.set_ylabel("Vote Share (%)", fontsize=12)
    ax.set_xlim(2006, 2026)
    ax.set_ylim(0, 100)
    ax.legend(loc="upper right", fontsize=10)
    ax.grid(axis="y", alpha=0.3)
    
    # Mark 2026 as projected
    ax.axvline(x=2025, color="gray", linestyle=":", linewidth=1)
    ax.text(2025.5, 95, "← Projected →", fontsize=10, color="gray", style="italic")
    
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "chart4_vote_share_trends.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {path}")


# ─── Chart 5: Final Prediction Summary ───────────────────────────────────

def chart_final_prediction():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle("TN 2026 Election - Final Prediction (Ensemble Model)",
                 fontsize=16, fontweight="bold", y=1.02)
    
    # Seat prediction (donut chart)
    labels = ["SPA\n(DMK-led)", "ADMK+\n(NDA)", "TVK", "Others"]
    seats = [148, 75, 8, 3]
    colors = [COLORS["SPA"], COLORS["ADMK+"], COLORS["TVK"], COLORS["Others"]]
    explode = (0.05, 0.02, 0.02, 0.02)
    
    wedges, texts, autotexts = ax1.pie(seats, labels=labels, colors=colors,
                                        explode=explode, autopct=lambda p: f"{p*234/100:.0f}\n({p:.1f}%)",
                                        startangle=90, pctdistance=0.72,
                                        textprops={"fontsize": 11, "fontweight": "bold"})
    
    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_fontweight("bold")
    
    centre_circle = plt.Circle((0, 0), 0.45, fc="white")
    ax1.add_artist(centre_circle)
    ax1.text(0, 0.05, "234", fontsize=24, fontweight="bold", ha="center", va="center")
    ax1.text(0, -0.15, "seats", fontsize=12, ha="center", va="center", color="gray")
    ax1.set_title("Predicted Seat Distribution", fontsize=13, fontweight="bold")
    
    # Win probability
    probs = [65, 30, 1, 4]  # percentages
    prob_labels = ["SPA\n(DMK-led)", "ADMK+\n(NDA)", "TVK", "Hung\nAssembly"]
    prob_colors = [COLORS["SPA"], COLORS["ADMK+"], COLORS["TVK"], "#FFA500"]
    
    bars = ax2.barh(prob_labels, probs, color=prob_colors, edgecolor="black", linewidth=0.5, height=0.6)
    ax2.set_xlabel("Win Probability (%)", fontsize=12)
    ax2.set_title("Government Formation Probability", fontsize=13, fontweight="bold")
    ax2.set_xlim(0, 80)
    ax2.grid(axis="x", alpha=0.3)
    
    for bar, prob in zip(bars, probs):
        ax2.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f"{prob}%", ha="left", va="center", fontsize=14, fontweight="bold")
    
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "chart5_final_prediction.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {path}")


# ─── Chart 6: Scenario Analysis ──────────────────────────────────────────

def chart_scenarios():
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.suptitle("TN 2026 Election - Scenario Analysis",
                 fontsize=16, fontweight="bold")
    
    scenarios = [
        ("DMK Landslide\n(5% prob)", 180, 45, 6, 3),
        ("DMK Comfortable\n(45% prob)", 155, 65, 10, 4),
        ("DMK Narrow\n(20% prob)", 130, 90, 12, 2),
        ("Hung Assembly\n(10% prob)", 108, 100, 22, 4),
        ("ADMK+ Win\n(20% prob)", 95, 130, 6, 3),
    ]
    
    y_positions = range(len(scenarios))
    
    for i, (name, spa, admk, tvk, others) in enumerate(scenarios):
        left = 0
        for val, color, label in [(spa, COLORS["SPA"], "SPA"), 
                                   (admk, COLORS["ADMK+"], "ADMK+"),
                                   (tvk, COLORS["TVK"], "TVK"),
                                   (others, COLORS["Others"], "Others")]:
            ax.barh(i, val, left=left, color=color, edgecolor="white", linewidth=1, height=0.6)
            if val > 15:
                ax.text(left + val/2, i, f"{val}", ha="center", va="center",
                       fontsize=10, fontweight="bold", color="white")
            left += val
    
    ax.axvline(x=118, color="black", linestyle="--", linewidth=2, label="Majority (118)")
    ax.set_yticks(list(y_positions))
    ax.set_yticklabels([s[0] for s in scenarios], fontsize=11)
    ax.set_xlabel("Seats", fontsize=12)
    ax.set_xlim(0, 240)
    
    # Legend
    patches = [mpatches.Patch(color=COLORS["SPA"], label="SPA (DMK-led)"),
               mpatches.Patch(color=COLORS["ADMK+"], label="ADMK+ (NDA)"),
               mpatches.Patch(color=COLORS["TVK"], label="TVK"),
               mpatches.Patch(color=COLORS["Others"], label="Others")]
    ax.legend(handles=patches, loc="lower right", fontsize=10)
    ax.grid(axis="x", alpha=0.3)
    
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "chart6_scenarios.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {path}")


# ─── Generate all charts ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n  Generating Visualization Charts...")
    print("  " + "=" * 50)
    chart_historical_winners()
    chart_alternation_pattern()
    chart_opinion_polls()
    chart_vote_share_trends()
    chart_final_prediction()
    chart_scenarios()
    print("  " + "=" * 50)
    print("  All charts generated successfully!")
    print(f"  Output directory: {OUTPUT_DIR}")
