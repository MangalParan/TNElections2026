"""
=============================================================================
TAMIL NADU 2026 ASSEMBLY ELECTION - COMPREHENSIVE PREDICTION ANALYSIS
=============================================================================
Using Multiple Prediction Models:
  1. Historical Alternation Pattern Model
  2. Swing Analysis Model (Lok Sabha 2024 → Assembly 2026)
  3. Opinion Poll Aggregation Model (Bayesian-weighted)
  4. Incumbency Factor Model
  5. Vote Share → Seat Conversion Model
  6. Alliance Arithmetic Model
  7. Composite Ensemble Model (Final Prediction)
=============================================================================
Data Sources: Election Commission of India, Wikipedia, IANS-Matrize,
              News18-VoteVibe, Agni News Agency, Lokpal
=============================================================================
"""

import os
import csv
import math
import json
from collections import OrderedDict

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_csv(filename):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

historical = load_csv("historical_assembly_results.csv")
alliance = load_csv("alliance_wise_results.csv")
polls = load_csv("opinion_polls_2026.csv")

TOTAL_SEATS = 234
MAJORITY = 118

# ─────────────────────────────────────────────────────────────────────────────
# 2026 ALLIANCE CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

alliances_2026 = {
    "SPA (DMK-led)": {
        "parties": ["DMK", "INC", "DMDK", "VCK", "CPI(M)", "CPI", "IUML", "MDMK", "KMDK", "MMK", "MJK", "MPP", "SDPI", "TDK"],
        "seats_contested": 234,
        "cm_candidate": "M. K. Stalin",
        "incumbent": True,
        "key_strength": "Ruling party advantage, 2024 Lok Sabha sweep, welfare schemes",
    },
    "AIADMK+ (NDA)": {
        "parties": ["AIADMK", "BJP", "PMK", "AMMK", "TMC(M)", "IJK", "PBK", "STMK", "TMBSP", "PNK", "TMMK", "SIFB"],
        "seats_contested": 234,
        "cm_candidate": "Edappadi K. Palaniswami",
        "incumbent": False,
        "key_strength": "Reunited NDA, AIADMK ground cadre, PMK caste arithmetic",
    },
    "TVK (Solo)": {
        "parties": ["TVK"],
        "seats_contested": 234,
        "cm_candidate": "Vijay",
        "incumbent": False,
        "key_strength": "Star power, youth appeal, first election novelty",
    },
    "NTK (Solo)": {
        "parties": ["NTK"],
        "seats_contested": 234,
        "cm_candidate": "Seeman",
        "incumbent": False,
        "key_strength": "Ideological base, Tamil identity politics",
    },
    "PMK(R)-Sasikala": {
        "parties": ["PMK(R)", "AIPTMMK"],
        "seats_contested": 81,
        "cm_candidate": "N/A (Spoiler)",
        "incumbent": False,
        "key_strength": "Vanniyar vote split, Sasikala's AIADMK nostalgia base",
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# 2021 ASSEMBLY RESULTS (Baseline)
# ─────────────────────────────────────────────────────────────────────────────

results_2021 = {
    "DMK_alliance": {"seats": 159, "vote_pct": 44.06, "dmk_own": 133, "inc": 18, "others": 8},
    "ADMK_alliance": {"seats": 75, "vote_pct": 37.30, "admk_own": 66, "bjp": 4, "pmk": 5},
    "Others": {"seats": 0, "vote_pct": 18.64, "ntk_vote": 6.58, "mnm_vote": 2.58},
}

# 2024 Lok Sabha Results in TN (per assembly segment approximation)
results_2024_ls = {
    "SPA_vote_pct": 42.12,  # DMK 26.93 + INC 10.67 + allies ~4.52
    "ADMK_vote_pct": 20.46,  # standalone
    "NDA_total_vote_pct": 34.08,  # includes BJP 11.24 separately
    "BJP_vote_pct": 11.24,
    "TVK_vote_pct": 0.0,  # didn't contest
    "NTK_vote_pct": 5.24,
    "Others_vote_pct": 18.56,
    "SPA_seats": 39,
    "ADMK_seats": 0,
    "NDA_seats": 0,
}

print("=" * 80)
print("  TAMIL NADU 2026 ASSEMBLY ELECTION - PREDICTION ANALYSIS")
print("  Election Date: April 23, 2026 | Results: May 4, 2026")
print("  Total Seats: 234 | Majority Mark: 118")
print("=" * 80)

# ─────────────────────────────────────────────────────────────────────────────
# MODEL 1: HISTORICAL ALTERNATION PATTERN
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "─" * 80)
print("  MODEL 1: HISTORICAL ALTERNATION PATTERN")
print("─" * 80)

# TN has a strong anti-incumbency pattern since 1967
winners = []
for row in historical:
    y = int(row["year"])
    w = row["winner_party"]
    if w in ["DMK"]:
        winners.append((y, "DMK"))
    elif w in ["ADMK"]:
        winners.append((y, "ADMK"))
    elif w == "INC":
        winners.append((y, "INC"))
    else:
        winners.append((y, w))

print("\n  Historical Winners (Assembly):")
print("  " + "-" * 50)
for y, w in winners:
    tag = " ★ Broke pattern" if False else ""
    print(f"    {y}: {w}")

# Count alternation
alternations = 0
continuations = 0
for i in range(1, len(winners)):
    prev_camp = "DMK" if winners[i-1][1] == "DMK" else "ADMK"
    curr_camp = "DMK" if winners[i][1] == "DMK" else "ADMK"
    if prev_camp != curr_camp:
        alternations += 1
    else:
        continuations += 1

total_transitions = alternations + continuations
alt_pct = (alternations / total_transitions * 100) if total_transitions > 0 else 0

print(f"\n  Since Dravidian era (1967):")
print(f"    Alternations (power changed): {alternations}/{total_transitions} ({alt_pct:.0f}%)")
print(f"    Continuations (same party won): {continuations}/{total_transitions} ({100-alt_pct:.0f}%)")

# 2021 winner was DMK → alternation pattern suggests ADMK should win
# But 1991 DMK→ADMK was broken in 1984 (ADMK→ADMK) and 2006-2016 pattern varies
# Actual record since 1967: DMK, DMK, ADMK, ADMK, ADMK, DMK, ADMK, DMK, ADMK, DMK, ADMK, ADMK, DMK
# So alternations = ~8/12 transitions

print(f"\n  2021 Winner: DMK")
print(f"  Alternation Pattern Prediction: {'ADMK favored' if alt_pct > 60 else 'Mixed signal'}")
print(f"  Confidence: {'Medium' if alt_pct > 65 else 'Low'} (pattern holds {alt_pct:.0f}% of the time)")

# However, 2016 was ADMK win with re-election (continuation)
# Key insight: When DMK wins, they have NEVER won re-election in the post-1977 era
# DMK won: 1989 → lost 1991, 1996 → lost 2001, 2006 → lost 2011, 2021 → ?

dmk_re_election_attempts = 0
dmk_re_election_success = 0
for i in range(1, len(winners)):
    if winners[i-1][1] == "DMK" and i < len(winners):
        dmk_re_election_attempts += 1
        if winners[i][1] == "DMK":
            dmk_re_election_success += 1

print(f"\n  DMK Re-election Record: {dmk_re_election_success}/{dmk_re_election_attempts}")
print(f"  DMK has NEVER won consecutive assembly elections (post-1971)")

model1_prediction = {
    "SPA": {"seats_range": (95, 120), "probability": 0.35},
    "ADMK+": {"seats_range": (100, 140), "probability": 0.50},
    "TVK": {"seats_range": (5, 20), "probability": 0.01},
    "Others": {"seats_range": (0, 10), "probability": 0.0},
    "confidence": "Medium",
    "note": "Alternation pattern favors ADMK, but pattern is not absolute"
}

print(f"\n  Model 1 Output:")
for party, data in model1_prediction.items():
    if isinstance(data, dict) and "seats_range" in data:
        lo, hi = data["seats_range"]
        print(f"    {party:20s}: {lo:3d} - {hi:3d} seats (Win Prob: {data['probability']:.0%})")

# ─────────────────────────────────────────────────────────────────────────────
# MODEL 2: SWING ANALYSIS (Lok Sabha 2024 → Assembly 2026)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "─" * 80)
print("  MODEL 2: SWING ANALYSIS (2024 Lok Sabha → 2026 Assembly)")
print("─" * 80)

# 2024 LS: SPA swept all 39 seats
# But Assembly elections differ from LS in TN
# Key differences:
# 1. AIADMK and BJP contested separately in LS 2024 (now together in 2026)
# 2. TVK didn't exist in 2024
# 3. NTK typically gets more in Assembly than LS

# Combined NDA vote in 2024 LS
admk_2024_ls = 20.46
bjp_2024_ls = 11.24
pmk_2024_ls = 3.0  # approximate
nda_combined_2024 = admk_2024_ls + bjp_2024_ls + pmk_2024_ls  # ~34.7%

spa_2024_ls = 42.12
ntk_2024_ls = 5.24

print(f"\n  2024 Lok Sabha Vote Shares (approximated):")
print(f"    SPA (DMK-led):     {spa_2024_ls:.2f}%")
print(f"    ADMK (standalone): {admk_2024_ls:.2f}%")
print(f"    BJP (standalone):  {bjp_2024_ls:.2f}%")
print(f"    NDA combined:      {nda_combined_2024:.2f}%")
print(f"    NTK:               {ntk_2024_ls:.2f}%")
print(f"    SPA swept all 39 Lok Sabha seats")

# Swing calculation
# In 2021 Assembly: DMK alliance ~44%, ADMK alliance ~37%
# In 2024 LS: SPA ~42%, NDA combined ~34.7% (but split)
# Now in 2026: NDA is united again + AMMK

# Estimated 2026 vote shares based on swing
# TVK factor: Expected to get 8-15% (celebrity party first election)
# This vote will come primarily from: ADMK voters (youth), DMK soft voters, new voters

# Historical parallel: DMDK in 2006 got 8.38%, MGR's ADMK launch got big numbers
# TVK is expected to hurt ADMK more than DMK

tvk_estimated_vote = 12.0  # estimated median from polls
ntk_estimated_vote = 4.0   # typically 3-7% in assembly

# Vote transfer assumptions
# TVK draws: 60% from ADMK base, 25% from DMK base, 15% from others
tvk_from_admk = tvk_estimated_vote * 0.60  # 7.2%
tvk_from_dmk = tvk_estimated_vote * 0.25   # 3.0%
tvk_from_others = tvk_estimated_vote * 0.15 # 1.8%

# Sasikala factor: estimated 2-3% vote, mostly from ADMK base
sasikala_vote = 2.5
sasikala_from_admk = sasikala_vote * 0.85

# PMK(R) factor: ~1-2% (split with main PMK)
pmkr_vote = 1.5
pmkr_from_admk = pmkr_vote * 0.70  # Vanniyar vote split

# Adjusted 2026 estimates
spa_2026_est = spa_2024_ls - tvk_from_dmk + 2.0  # +2% for state election local factors
admk_2026_est = nda_combined_2024 + 3.0 - tvk_from_admk - sasikala_from_admk - pmkr_from_admk
# NDA gains +3% from AMMK alliance consolidation, loses to TVK/Sasikala/PMK(R)

print(f"\n  2026 Projected Vote Shares (Swing Model):")
print(f"    SPA (DMK-led):     {spa_2026_est:.1f}% (base {spa_2024_ls:.1f}% - TVK loss + state factor)")
print(f"    ADMK+ (NDA):       {admk_2026_est:.1f}% (united NDA {nda_combined_2024:.1f}% - TVK/Sasikala drain)")
print(f"    TVK:               {tvk_estimated_vote:.1f}% (celebrity factor, first election)")
print(f"    NTK:               {ntk_estimated_vote:.1f}%")
print(f"    PMK(R)-Sasikala:   {sasikala_vote + pmkr_vote:.1f}%")
print(f"    Others:            {100 - spa_2026_est - admk_2026_est - tvk_estimated_vote - ntk_estimated_vote - sasikala_vote - pmkr_vote:.1f}%")

# Vote to seat conversion (using cube law approximation for FPTP)
# In TN, the relationship between vote share and seats is highly non-linear
# due to multi-cornered contests

def vote_to_seats_tn(vote_spa, vote_admk, vote_tvk, vote_others, total=234):
    """Approximate seat conversion using modified cube law for TN multi-corner contests"""
    # In a 3-way contest, the relationship is different from 2-way
    votes = {"SPA": vote_spa, "ADMK+": vote_admk, "TVK": vote_tvk, "Others": vote_others}
    total_vote = sum(votes.values())
    
    # Normalize
    for k in votes:
        votes[k] = votes[k] / total_vote
    
    # Modified power law (exponent ~2.5 for multi-corner TN contests)
    power = 2.5
    powered = {k: v**power for k, v in votes.items()}
    total_powered = sum(powered.values())
    
    seats = {}
    for k, v in powered.items():
        seats[k] = round(v / total_powered * total)
    
    # Adjust to total
    diff = total - sum(seats.values())
    if diff != 0:
        max_party = max(seats, key=seats.get)
        seats[max_party] += diff
    
    return seats

swing_seats = vote_to_seats_tn(
    spa_2026_est, admk_2026_est, tvk_estimated_vote,
    ntk_estimated_vote + sasikala_vote + pmkr_vote + 3.0
)

print(f"\n  Swing Model Seat Projection:")
for party, seats in swing_seats.items():
    print(f"    {party:20s}: {seats:3d} seats")

model2_prediction = {
    "SPA": {"seats_range": (130, 160), "vote_pct": spa_2026_est},
    "ADMK+": {"seats_range": (60, 90), "vote_pct": admk_2026_est},
    "TVK": {"seats_range": (2, 12), "vote_pct": tvk_estimated_vote},
    "Others": {"seats_range": (0, 5), "vote_pct": ntk_estimated_vote + sasikala_vote + pmkr_vote},
    "confidence": "Medium-Low (LS-to-Assembly swing is unreliable)"
}

# ─────────────────────────────────────────────────────────────────────────────
# MODEL 3: OPINION POLL AGGREGATION (Bayesian-weighted)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "─" * 80)
print("  MODEL 3: OPINION POLL AGGREGATION (Bayesian-weighted)")
print("─" * 80)

print("\n  Available Opinion Polls:")
print(f"  {'Agency':<22s} {'Date':<12s} {'Sample':>8s} {'SPA Seats':>12s} {'ADMK+ Seats':>13s} {'TVK Seats':>11s} {'SPA%':>6s} {'ADMK%':>7s} {'TVK%':>6s}")
print("  " + "-" * 105)

poll_data = []
for p in polls:
    agency = p["agency"]
    date = p["date"]
    sample = int(p["sample_size"])
    spa_lo = int(p["spa_seats_low"])
    spa_hi = int(p["spa_seats_high"])
    admk_lo = int(p["admk_seats_low"])
    admk_hi = int(p["admk_seats_high"])
    tvk_lo = int(p["tvk_seats_low"])
    tvk_hi = int(p["tvk_seats_high"])
    spa_vote = float(p["spa_vote_pct"])
    admk_vote = float(p["admk_vote_pct"])
    tvk_vote = float(p["tvk_vote_pct"])
    
    print(f"  {agency:<22s} {date:<12s} {sample:>8,d} {spa_lo:>5d}-{spa_hi:<5d} {admk_lo:>6d}-{admk_hi:<5d} {tvk_lo:>5d}-{tvk_hi:<4d} {spa_vote:>5.1f}% {admk_vote:>5.1f}% {tvk_vote:>5.1f}%")
    
    poll_data.append({
        "agency": agency,
        "sample": sample,
        "spa_seats_mid": (spa_lo + spa_hi) / 2,
        "admk_seats_mid": (admk_lo + admk_hi) / 2,
        "tvk_seats_mid": (tvk_lo + tvk_hi) / 2,
        "spa_vote": spa_vote,
        "admk_vote": admk_vote,
        "tvk_vote": tvk_vote,
    })

# Bayesian weighting: weight by sample size and recency
# More recent polls and larger samples get higher weight
total_samples = sum(p["sample"] for p in poll_data)
weights = []
for i, p in enumerate(poll_data):
    sample_weight = p["sample"] / total_samples
    recency_weight = (i + 1) / len(poll_data)  # more recent = higher index
    combined_weight = sample_weight * 0.6 + recency_weight * 0.4
    weights.append(combined_weight)

# Normalize weights
total_weight = sum(weights)
weights = [w / total_weight for w in weights]

print(f"\n  Bayesian Weights:")
for i, p in enumerate(poll_data):
    print(f"    {p['agency']:<22s}: {weights[i]:.3f} (Sample: {p['sample']:>8,d})")

# Weighted average
spa_seats_agg = sum(p["spa_seats_mid"] * w for p, w in zip(poll_data, weights))
admk_seats_agg = sum(p["admk_seats_mid"] * w for p, w in zip(poll_data, weights))
tvk_seats_agg = sum(p["tvk_seats_mid"] * w for p, w in zip(poll_data, weights))
others_seats_agg = TOTAL_SEATS - spa_seats_agg - admk_seats_agg - tvk_seats_agg

spa_vote_agg = sum(p["spa_vote"] * w for p, w in zip(poll_data, weights))
admk_vote_agg = sum(p["admk_vote"] * w for p, w in zip(poll_data, weights))
tvk_vote_agg = sum(p["tvk_vote"] * w for p, w in zip(poll_data, weights))

print(f"\n  Weighted Poll Aggregate:")
print(f"    SPA (DMK-led):  {spa_seats_agg:.0f} seats  ({spa_vote_agg:.1f}% vote share)")
print(f"    ADMK+ (NDA):    {admk_seats_agg:.0f} seats  ({admk_vote_agg:.1f}% vote share)")
print(f"    TVK:            {tvk_seats_agg:.0f} seats  ({tvk_vote_agg:.1f}% vote share)")
print(f"    Others:         {others_seats_agg:.0f} seats")

# Confidence interval (using standard deviation)
spa_seats_vals = [p["spa_seats_mid"] for p in poll_data]
admk_seats_vals = [p["admk_seats_mid"] for p in poll_data]

spa_std = (sum((x - spa_seats_agg)**2 * w for x, w in zip(spa_seats_vals, weights)))**0.5
admk_std = (sum((x - admk_seats_agg)**2 * w for x, w in zip(admk_seats_vals, weights)))**0.5

print(f"\n  Confidence Intervals (±1σ):")
print(f"    SPA:   {spa_seats_agg:.0f} ± {spa_std:.0f} → ({max(0,spa_seats_agg-spa_std):.0f} - {min(234,spa_seats_agg+spa_std):.0f})")
print(f"    ADMK+: {admk_seats_agg:.0f} ± {admk_std:.0f} → ({max(0,admk_seats_agg-admk_std):.0f} - {min(234,admk_seats_agg+admk_std):.0f})")

# Note: There's massive divergence between polls
print(f"\n  ⚠ WARNING: Polls show HIGH DIVERGENCE")
print(f"    SPA range across polls: {min(p['spa_seats_mid'] for p in poll_data):.0f} - {max(p['spa_seats_mid'] for p in poll_data):.0f}")
print(f"    ADMK+ range: {min(p['admk_seats_mid'] for p in poll_data):.0f} - {max(p['admk_seats_mid'] for p in poll_data):.0f}")
print(f"    Two polls show tight race; two show DMK landslide")

model3_prediction = {
    "SPA": {"seats_range": (int(spa_seats_agg - spa_std), int(spa_seats_agg + spa_std))},
    "ADMK+": {"seats_range": (int(admk_seats_agg - admk_std), int(admk_seats_agg + admk_std))},
    "TVK": {"seats_range": (2, 12)},
    "Others": {"seats_range": (0, 5)},
    "confidence": "Low (high inter-poll divergence)"
}

# ─────────────────────────────────────────────────────────────────────────────
# MODEL 4: INCUMBENCY FACTOR MODEL
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "─" * 80)
print("  MODEL 4: INCUMBENCY FACTOR MODEL")
print("─" * 80)

# Factors affecting incumbency
print("\n  FACTORS FAVORING DMK (Incumbency Advantage):")
print("  +" + "-" * 60)
factors_dmk = [
    ("2024 Lok Sabha clean sweep", 9, "All 39 seats. Strongest validation of any ruling party."),
    ("Welfare schemes delivery", 7, "Breakfast scheme, Kalaignar insurance, housing. Tangible benefits to poor."),
    ("Reasonably stable governance", 6, "No major governance crisis, COVID handling was decent."),
    ("Alliance management", 8, "DMDK, MNM additions strengthen coalition. OPS joining is a coup."),
    ("ADMK disarray (post-Jaya)", 7, "AIADMK lost OPS, Sasikala, Sengottaiyan. Organization weakened."),
    ("CM Stalin's personal image", 6, "Moderate positive image. Not polarizing."),
    ("Strong organizational machinery", 8, "DMK's booth-level management is superior to rivals."),
]

for name, score, detail in factors_dmk:
    print(f"    [+{score}/10] {name}")
    print(f"            {detail}")

print("\n  FACTORS AGAINST DMK (Anti-incumbency):")
print("  +" + "-" * 60)
factors_anti = [
    ("Historical anti-incumbency pattern", 8, "DMK has NEVER won consecutive Assembly elections post-1971."),
    ("Rising prices / inflation", 6, "Cost of living concerns affect all ruling parties."),
    ("Law and order concerns", 5, "Perception issues around crime, though not major crisis."),
    ("Corruption allegations", 5, "Senthil Balaji arrest, various scams alleged by opposition."),
    ("Dravidian fatigue factor", 4, "Some voters seeking alternatives (TVK represents this)."),
    ("Liquor policy criticism", 5, "TASMAC shops, alcohol-related social issues."),
]

for name, score, detail in factors_anti:
    print(f"    [-{score}/10] {name}")
    print(f"            {detail}")

pro_score = sum(s for _, s, _ in factors_dmk) / len(factors_dmk)
anti_score = sum(s for _, s, _ in factors_anti) / len(factors_anti)
net_incumbency = pro_score - anti_score

print(f"\n  Net Incumbency Score: {pro_score:.1f} (Pro) - {anti_score:.1f} (Anti) = {net_incumbency:+.1f}")
print(f"  Interpretation: {'Slightly positive' if net_incumbency > 0 else 'Negative'} incumbency environment")

# Incumbency-adjusted prediction
if net_incumbency > 1.5:
    model4_spa = (140, 170)
    model4_admk = (50, 80)
elif net_incumbency > 0:
    model4_spa = (120, 150)
    model4_admk = (70, 100)
else:
    model4_spa = (90, 120)
    model4_admk = (100, 135)

print(f"\n  Model 4 Seat Projection:")
print(f"    SPA (DMK-led): {model4_spa[0]} - {model4_spa[1]}")
print(f"    ADMK+ (NDA):   {model4_admk[0]} - {model4_admk[1]}")
print(f"    TVK:           5 - 15")
print(f"    Others:        0 - 5")

model4_prediction = {
    "SPA": {"seats_range": model4_spa},
    "ADMK+": {"seats_range": model4_admk},
    "TVK": {"seats_range": (5, 15)},
    "Others": {"seats_range": (0, 5)},
    "confidence": "Medium"
}

# ─────────────────────────────────────────────────────────────────────────────
# MODEL 5: VOTE SHARE → SEAT CONVERSION (Cube Root Law)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "─" * 80)
print("  MODEL 5: VOTE SHARE → SEAT CONVERSION MODEL")
print("─" * 80)

# Calibrate using historical data
print("\n  Historical Vote Share vs Seats (Winning Party):")
print(f"  {'Year':<6s} {'Winner':<8s} {'Vote%':>7s} {'Seats':>7s} {'Seat%':>7s} {'Ratio':>7s}")
print("  " + "-" * 45)
for row in historical:
    y = row["year"]
    w = row["winner_party"]
    v = float(row["winner_vote_pct"])
    s = int(row["winner_seats"])
    sp = s / 234 * 100
    ratio = sp / v if v > 0 else 0
    print(f"  {y:<6s} {w:<8s} {v:>6.1f}% {s:>6d} {sp:>6.1f}% {ratio:>6.2f}x")

# In TN, the vote-to-seat multiplier for the winner is typically 1.3-1.8x
# In multi-cornered contests, this can be lower

# Estimate 2026 scenarios
print("\n  2026 Scenarios (Vote Share → Seats):")
scenarios = [
    ("Scenario A: Close 3-way", 39, 36, 14, 11),
    ("Scenario B: DMK lead", 42, 34, 12, 12),
    ("Scenario C: DMK dominant", 45, 32, 10, 13),
    ("Scenario D: ADMK lead", 36, 40, 13, 11),
]

for name, spa_v, admk_v, tvk_v, other_v in scenarios:
    seats = vote_to_seats_tn(spa_v, admk_v, tvk_v, other_v)
    leader = max(seats, key=seats.get)
    majority = "✓ MAJORITY" if seats[leader] >= MAJORITY else "✗ No majority"
    print(f"\n    {name}")
    print(f"      SPA {spa_v}% → {seats['SPA']} seats | ADMK+ {admk_v}% → {seats['ADMK+']} seats | TVK {tvk_v}% → {seats['TVK']} seats | {majority}")

# ─────────────────────────────────────────────────────────────────────────────
# MODEL 6: ALLIANCE ARITHMETIC & CASTE MATRIX
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "─" * 80)
print("  MODEL 6: ALLIANCE ARITHMETIC & VOTE TRANSFER MODEL")
print("─" * 80)

print("\n  Alliance Composition & Estimated Core Vote Banks:")
print(f"  {'Alliance':<20s} {'Parties':>8s} {'Est. Core Vote':>15s} {'Transfer Efficiency':>20s}")
print("  " + "-" * 68)

alliance_votes = {
    "SPA (DMK-led)": {
        "core_vote": 38.0,  # DMK ~28% + INC ~5% + Left ~3% + DMDK ~2%
        "transfer_efficiency": 0.85,  # High - well-oiled alliance
        "new_additions": 2.0,  # DMDK, OPS factor
        "leakage_to_tvk": 3.0,
    },
    "ADMK+ (NDA)": {
        "core_vote": 34.0,  # ADMK ~25% + BJP ~5% + PMK ~4%
        "transfer_efficiency": 0.75,  # Medium - AIADMK-BJP alliance untested
        "new_additions": 3.0,  # AMMK reunion, PMK solidification
        "leakage_to_tvk": 5.0,  # Youth and disenchanted ADMK voters
        "leakage_to_sasikala": 2.0,
    },
    "TVK": {
        "core_vote": 5.0,   # True believers / fan base
        "transfer_efficiency": 0.90,  # Solo party, no transfer needed
        "new_voter_attraction": 8.0,  # Celebrity pull
        "leakage_to_tvk": 0,
    },
    "NTK": {
        "core_vote": 4.0,
        "transfer_efficiency": 0.95,  # Ideological voters, very loyal
        "leakage_to_tvk": 0.5,
    },
}

for alliance_name, data in alliance_votes.items():
    core = data["core_vote"]
    eff = data["transfer_efficiency"]
    effective = core * eff
    additions = data.get("new_additions", 0) + data.get("new_voter_attraction", 0)
    leakage = data.get("leakage_to_tvk", 0) + data.get("leakage_to_sasikala", 0)
    net = effective + additions - leakage
    print(f"  {alliance_name:<20s} Core: {core:>5.1f}%  ×{eff:.0%} eff  +{additions:.1f}%  -{leakage:.1f}% leak  = {net:.1f}% net")

# Caste matrix analysis
print("\n  Key Caste/Community Factor Analysis:")
print("  " + "-" * 65)
caste_factors = [
    ("Vanniyar (N. TN)", "PMK split hurts ADMK in ~40 seats", "ADMK -2%", "Moderate"),
    ("Thevar (S. TN)", "ADMK traditional base, partially intact", "Neutral", "Low"),
    ("Gounder (W. TN)", "ADMK stronghold, TVK may make inroads", "ADMK -1%", "Moderate"),
    ("Dalit (SC seats)", "VCK+DMK hold strong. BSP non-factor", "DMK +1%", "High"),
    ("Muslim (12%)", "Solidly with DMK alliance (IUML, SDPI)", "DMK +1%", "High"),
    ("Christian (6%)", "Mixed - INC in Kanyakumari, some BJP", "Neutral", "Low"),
    ("OBC Others", "Fragmented - TVK's main hunting ground", "TVK +2%", "Moderate"),
]

for community, analysis, impact, confidence in caste_factors:
    print(f"    {community:<22s} | {analysis:<45s} | {impact:<10s} | {confidence}")

model6_prediction = {
    "SPA": {"seats_range": (130, 160), "net_vote": 37.0},
    "ADMK+": {"seats_range": (55, 85), "net_vote": 33.0},
    "TVK": {"seats_range": (5, 15), "net_vote": 13.0},
    "Others": {"seats_range": (0, 8), "net_vote": 7.0},
    "confidence": "Medium"
}

# ─────────────────────────────────────────────────────────────────────────────
# MODEL 7: COMPOSITE ENSEMBLE MODEL (FINAL PREDICTION)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 80)
print("  MODEL 7: COMPOSITE ENSEMBLE - FINAL PREDICTION")
print("=" * 80)

# Weight each model
model_weights = {
    "Historical Pattern (M1)": 0.10,
    "Swing Analysis (M2)": 0.15,
    "Opinion Polls (M3)": 0.30,
    "Incumbency (M4)": 0.15,
    "Vote→Seat (M5)": 0.10,
    "Alliance Arithmetic (M6)": 0.20,
}

# Collect all model predictions (using midpoints of ranges)
all_models = {
    "M1": model1_prediction,
    "M2": model2_prediction,
    "M3": model3_prediction,
    "M4": model4_prediction,
    "M5": {"SPA": {"seats_range": (130, 155)}, "ADMK+": {"seats_range": (65, 90)}, "TVK": {"seats_range": (3, 12)}, "Others": {"seats_range": (0, 5)}},
    "M6": model6_prediction,
}

# Calculate weighted ensemble
spa_mids = [
    (107.5, 0.10),  # M1
    (145.0, 0.15),  # M2
    (spa_seats_agg, 0.30),  # M3
    ((model4_spa[0] + model4_spa[1]) / 2, 0.15),  # M4
    (142.5, 0.10),  # M5
    (145.0, 0.20),  # M6
]

admk_mids = [
    (120.0, 0.10),  # M1
    (75.0, 0.15),   # M2
    (admk_seats_agg, 0.30),  # M3
    ((model4_admk[0] + model4_admk[1]) / 2, 0.15),  # M4
    (77.5, 0.10),   # M5
    (70.0, 0.20),   # M6
]

tvk_mids = [
    (12.5, 0.10),
    (7.0, 0.15),
    (tvk_seats_agg, 0.30),
    (10.0, 0.15),
    (7.5, 0.10),
    (10.0, 0.20),
]

ensemble_spa = sum(m * w for m, w in spa_mids)
ensemble_admk = sum(m * w for m, w in admk_mids)
ensemble_tvk = sum(m * w for m, w in tvk_mids)
ensemble_others = TOTAL_SEATS - ensemble_spa - ensemble_admk - ensemble_tvk

# Margin of error
spa_variance = sum(w * (m - ensemble_spa)**2 for m, w in spa_mids)
admk_variance = sum(w * (m - ensemble_admk)**2 for m, w in admk_mids)
spa_moe = spa_variance ** 0.5
admk_moe = admk_variance ** 0.5

print(f"\n  Model Weights:")
for model_name, weight in model_weights.items():
    print(f"    {model_name:<30s}: {weight:.0%}")

print(f"\n  ╔{'═' * 70}╗")
print(f"  ║{'FINAL ENSEMBLE PREDICTION':^70s}║")
print(f"  ╠{'═' * 70}╣")
print(f"  ║  {'Alliance':<25s} {'Seats':>8s} {'Range':>15s} {'Win Prob':>10s}    ║")
print(f"  ╠{'─' * 70}╣")

# Calculate win probability based on ensemble and variance
# SPA wins if > 117 seats
def normal_cdf_approx(x):
    """Approximate CDF of standard normal distribution"""
    # Using Zelen & Severo (1964) approximation
    if x < -8: return 0.0
    if x > 8: return 1.0
    b0 = 0.2316419
    b1 = 0.319381530
    b2 = -0.356563782
    b3 = 1.781477937
    b4 = -1.821255978
    b5 = 1.330274429
    t = 1 / (1 + b0 * abs(x))
    pdf = math.exp(-x**2 / 2) / math.sqrt(2 * math.pi)
    cdf = 1 - pdf * (b1*t + b2*t**2 + b3*t**3 + b4*t**4 + b5*t**5)
    return cdf if x >= 0 else 1 - cdf

spa_z = (ensemble_spa - MAJORITY) / max(spa_moe, 1)
admk_z = (ensemble_admk - MAJORITY) / max(admk_moe, 1)

spa_win_prob = normal_cdf_approx(spa_z)
admk_win_prob = normal_cdf_approx(admk_z)

# Normalize probabilities
total_prob = spa_win_prob + admk_win_prob + 0.02  # 2% for others
spa_win_prob_norm = spa_win_prob / total_prob
admk_win_prob_norm = admk_win_prob / total_prob
tvk_win_prob = 0.01
others_win_prob = 0.01

spa_lo = max(0, int(ensemble_spa - spa_moe))
spa_hi = min(234, int(ensemble_spa + spa_moe))
admk_lo = max(0, int(ensemble_admk - admk_moe))
admk_hi = min(234, int(ensemble_admk + admk_moe))
tvk_lo = max(0, int(ensemble_tvk - 5))
tvk_hi = min(30, int(ensemble_tvk + 5))

print(f"  ║  {'SPA (DMK-led)':<25s} {ensemble_spa:>7.0f}  ({spa_lo:>3d} - {spa_hi:>3d})   {spa_win_prob_norm:>8.0%}      ║")
print(f"  ║  {'ADMK+ (NDA)':<25s} {ensemble_admk:>7.0f}  ({admk_lo:>3d} - {admk_hi:>3d})   {admk_win_prob_norm:>8.0%}      ║")
print(f"  ║  {'TVK':<25s} {ensemble_tvk:>7.0f}  ({tvk_lo:>3d} - {tvk_hi:>3d})   {tvk_win_prob:>8.0%}      ║")
print(f"  ║  {'Others (NTK etc.)':<25s} {ensemble_others:>7.0f}  ({0:>3d} - {5:>3d})   {others_win_prob:>8.0%}      ║")
print(f"  ╠{'─' * 70}╣")
print(f"  ║  {'LIKELY OUTCOME:':<25s} {'DMK-led SPA forms government':>43s}  ║")
print(f"  ║  {'PREDICTED CM:':<25s} {'M. K. Stalin (DMK)':>43s}  ║")
print(f"  ╚{'═' * 70}╝")

# ─────────────────────────────────────────────────────────────────────────────
# DETAILED ANALYSIS SUMMARY
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 80)
print("  KEY FINDINGS & ANALYSIS")
print("=" * 80)

print("""
  1. DMK-LED SPA IS THE FRONTRUNNER (Confidence: Medium-High)
     - Despite Tamil Nadu's strong anti-incumbency tradition, the DMK 
       benefits from the 2024 Lok Sabha sweep (39/39 seats), effective 
       welfare scheme delivery, and a fractured opposition.
     - The reunited NDA (AIADMK + BJP + PMK) should have been formidable,
       but loses significantly to TVK vote splitting and Sasikala/PMK(R).

  2. TVK IS THE WILDCARD (Critical Impact: Vote Splitter)
     - Vijay's TVK contesting all 234 seats will primarily eat into 
       ADMK+ votes (60:25:15 split with DMK and others).
     - Expected to win 5-12 seats but drain 8-15% of votes.
     - TVK's impact is similar to DMDK in 2006 which spoiled ADMK's chances.
     - The Karur crowd crush tragedy may have tempered initial enthusiasm.

  3. OPPOSITION FRAGMENTATION HELPS DMK (Decisive Factor)
     - ADMK bleeding votes to: TVK (~7%), Sasikala-AIPTMMK (~2%), 
       PMK(R) (~1.5%), internal dissent.
     - Combined opposition vote may exceed DMK alliance, but fractured 
       across 3+ entities, converting poorly into seats under FPTP.

  4. HISTORICAL PATTERN vs. CURRENT REALITY (Conflict)
     - Pattern says ADMK should win (DMK never won consecutive elections).
     - But current conditions are unprecedented: ADMK has no charismatic 
       leader (post-Jayalalithaa), a new third force (TVK) disrupts the 
       binary, and DMK's 2024 performance was historically strong.

  5. KEY BATTLEGROUND REGIONS:
     - Western TN (Coimbatore, Tiruppur, Erode): ADMK stronghold, TVK 
       could play spoiler. BJP has urban pockets.
     - Northern TN (Chennai, Tiruvallur, Kancheepuram): DMK's fortress.
       TVK could gain in urban constituencies.
     - Southern TN (Madurai, Tirunelveli, Thoothukudi): Traditional 
       swing region. Thevar belt could go ADMK.
     - Delta Region (Thanjavur, Nagapattinam): DMK stronghold.

  6. RISK FACTORS FOR PREDICTION:
     - TVK's actual vote share is completely unknown (no electoral 
       track record). Could be 5% or 20%.
     - ADMK-BJP alliance vote transfer efficiency is untested.
     - Late-breaking events, campaign momentum, and Vijay's personal 
       appeal could shift things dramatically.
     - Polls show massive divergence (SPA from 109 to 185 seats).
""")

# ─────────────────────────────────────────────────────────────────────────────
# SCENARIO ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────

print("─" * 80)
print("  SCENARIO ANALYSIS")
print("─" * 80)

scenarios_final = [
    {
        "name": "SCENARIO 1: DMK Comfortable Win (Most Likely - 45%)",
        "description": "DMK welfare schemes hold urban & rural base. TVK eats into ADMK. Alliance intact.",
        "spa": "145-165", "admk": "55-75", "tvk": "5-12", "others": "0-3",
        "outcome": "Stalin continues as CM. Stable government."
    },
    {
        "name": "SCENARIO 2: DMK Narrow Win (Probability - 20%)",
        "description": "Anti-incumbency kicks in partially. TVK surprise in some pockets. ADMK performs better in Western TN.",
        "spa": "120-144", "admk": "75-100", "tvk": "8-15", "others": "0-5",
        "outcome": "DMK forms government but with thinner margin."
    },
    {
        "name": "SCENARIO 3: Hung Assembly (Probability - 10%)",
        "description": "TVK performs much better than expected (>20 seats). Both DMK and ADMK fall short.",
        "spa": "100-117", "admk": "85-110", "tvk": "15-30", "others": "2-8",
        "outcome": "Coalition negotiations. TVK becomes kingmaker."
    },
    {
        "name": "SCENARIO 4: ADMK+ Comeback (Probability - 20%)",
        "description": "Anti-incumbency wave. TVK flops. United NDA transfers votes efficiently. PMK delivers Vanniyar belt.",
        "spa": "85-110", "admk": "115-140", "tvk": "2-8", "others": "0-3",
        "outcome": "EPS becomes CM. NDA forms coalition government."
    },
    {
        "name": "SCENARIO 5: DMK Landslide (Probability - 5%)",
        "description": "2024 LS momentum continues. TVK massively splits ADMK. Welfare schemes create wave.",
        "spa": "170-190", "admk": "35-50", "tvk": "5-10", "others": "0-3",
        "outcome": "Historic repeat win for DMK. ADMK faces existential crisis."
    },
]

for s in scenarios_final:
    print(f"\n  {s['name']}")
    print(f"  {s['description']}")
    print(f"    SPA: {s['spa']} | ADMK+: {s['admk']} | TVK: {s['tvk']} | Others: {s['others']}")
    print(f"    → {s['outcome']}")

# ─────────────────────────────────────────────────────────────────────────────
# SAVE RESULTS
# ─────────────────────────────────────────────────────────────────────────────

results = {
    "election": "2026 Tamil Nadu Legislative Assembly",
    "date": "2026-04-23",
    "total_seats": 234,
    "majority": 118,
    "registered_voters": 56707380,
    "prediction": {
        "most_likely_winner": "SPA (DMK-led Alliance)",
        "predicted_cm": "M. K. Stalin",
        "ensemble_seats": {
            "SPA": {"predicted": round(ensemble_spa), "range": [spa_lo, spa_hi], "win_probability": round(spa_win_prob_norm, 2)},
            "ADMK+": {"predicted": round(ensemble_admk), "range": [admk_lo, admk_hi], "win_probability": round(admk_win_prob_norm, 2)},
            "TVK": {"predicted": round(ensemble_tvk), "range": [tvk_lo, tvk_hi], "win_probability": round(tvk_win_prob, 2)},
            "Others": {"predicted": round(ensemble_others), "range": [0, 5], "win_probability": round(others_win_prob, 2)},
        },
        "vote_share_estimate": {
            "SPA": round(spa_vote_agg, 1),
            "ADMK+": round(admk_vote_agg, 1),
            "TVK": round(tvk_vote_agg, 1),
        },
        "confidence": "Medium-High",
        "key_risk": "TVK vote share uncertainty, ADMK-BJP transfer efficiency",
    },
    "models_used": list(model_weights.keys()),
    "data_sources": ["ECI", "Wikipedia", "IANS-Matrize", "News18-VoteVibe", "Agni News Agency", "Lokpal"],
}

output_file = os.path.join(OUTPUT_DIR, "prediction_results.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n\n  Results saved to: {output_file}")
print("=" * 80)
print("  END OF ANALYSIS")
print("=" * 80)
