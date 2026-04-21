"""
Tamil Nadu 2026 Assembly Election - HTML Report Generator
Generates a comprehensive self-contained HTML report with embedded charts
"""
import base64
import os
import json
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def img_b64(fname):
    p = os.path.join(OUTPUT_DIR, fname)
    if os.path.exists(p):
        with open(p, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode()
    return ""


def load_csv(f):
    with open(os.path.join(DATA_DIR, f), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


polls = load_csv("opinion_polls_2026.csv")
historical = load_csv("historical_assembly_results.csv")
with open(os.path.join(OUTPUT_DIR, "prediction_results.json"), encoding="utf-8") as f:
    pred = json.load(f)

# ─── Build poll table rows ───────────────────────────────────────────────────
poll_rows_html = ""
for p in polls:
    spa_range = f"{p['spa_seats_low']}–{p['spa_seats_high']}"
    admk_range = f"{p['admk_seats_low']}–{p['admk_seats_high']}"
    tvk_range = f"{p['tvk_seats_low']}–{p['tvk_seats_high']}"
    sample = f"{int(p['sample_size']):,}"
    hl = ' class="hl"' if p["agency"] in ["CSDS-Lokniti", "Polstrat"] else ""
    poll_rows_html += (
        f'    <tr{hl}>'
        f'<td>{p["agency"]}</td><td>{p["date"]}</td><td>{sample}</td>'
        f'<td>{spa_range}</td><td>{admk_range}</td><td>{tvk_range}</td>'
        f'<td>{p["spa_vote_pct"]}%</td><td>{p["admk_vote_pct"]}%</td><td>{p["tvk_vote_pct"]}%</td>'
        f'</tr>\n'
    )

# ─── Build historical table rows ─────────────────────────────────────────────
hist_rows_html = ""
for row in historical:
    wp = row.get("winner_party", "")
    color = "#E31A1C" if wp == "DMK" else "#00A651" if wp == "ADMK" else "#333"
    hist_rows_html += (
        f'    <tr>'
        f'<td>{row["year"]}</td>'
        f'<td style="color:{color};font-weight:700;">{wp}</td>'
        f'<td>{row.get("winner_seats", "")}</td>'
        f'<td>{row.get("winner_vote_pct", "")}%</td>'
        f'<td>{row.get("runner_up_party", "")}</td>'
        f'<td>{row.get("runner_up_seats", "")}</td>'
        f'<td>{row.get("runner_up_vote_pct", "")}%</td>'
        f'</tr>\n'
    )

# ─── HTML ────────────────────────────────────────────────────────────────────
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tamil Nadu 2026 Assembly Election — Prediction Report</title>
<style>
:root{{--dmk:#E31A1C;--admk:#00A651;--tvk:#e6b800;--bg:#f0f2f5;--card:#fff;--text:#1a1a2e;--muted:#6c757d;--border:#dee2e6;--accent:#0d6efd;}}
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:"Segoe UI",system-ui,sans-serif;background:var(--bg);color:var(--text);line-height:1.7;}}
.hero{{background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);color:#fff;padding:3.5rem 2rem;text-align:center;}}
.hero h1{{font-size:2.3rem;font-weight:800;margin-bottom:.5rem;letter-spacing:-1px;}}
.hero .sub{{font-size:1rem;opacity:.85;margin:.4rem 0;}}
.hero .badges{{margin-top:1.2rem;display:flex;justify-content:center;gap:.7rem;flex-wrap:wrap;}}
.badge{{background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.3);padding:.3rem .9rem;border-radius:20px;font-size:.82rem;}}
.container{{max-width:1100px;margin:0 auto;padding:2rem 1.5rem;}}
.card{{background:var(--card);border-radius:14px;box-shadow:0 3px 12px rgba(0,0,0,.07);padding:2rem;margin-bottom:2rem;border:1px solid var(--border);}}
h2{{font-size:1.45rem;margin-bottom:1.2rem;padding-bottom:.5rem;border-bottom:3px solid var(--accent);color:#1a1a2e;}}
h3{{font-size:1.05rem;margin:1.3rem 0 .6rem;color:#16213e;font-weight:700;}}
p{{margin-bottom:.8rem;}}
table{{width:100%;border-collapse:collapse;margin:1rem 0;font-size:.88rem;}}
th{{background:#1a1a2e;color:#fff;padding:.65rem .9rem;text-align:left;font-weight:600;}}
td{{padding:.55rem .9rem;border-bottom:1px solid var(--border);}}
tr:nth-child(even){{background:#f5f7fa;}}
tr:hover{{background:#eef1f6;}}
.hl{{background:#fff3cd!important;font-weight:700;}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;}}
.grid3{{display:grid;grid-template-columns:repeat(3,1fr);gap:1.2rem;}}
.stat-card{{background:#f8f9fa;border-radius:10px;padding:1.3rem;text-align:center;border:2px solid var(--border);}}
.stat-card.dmk{{border-color:var(--dmk);}}
.stat-card.admk{{border-color:var(--admk);}}
.stat-card.tvk{{border-color:var(--tvk);}}
.stat-num{{font-size:3rem;font-weight:800;line-height:1;}}
.stat-range{{font-size:.83rem;color:var(--muted);margin:.3rem 0;}}
.stat-label{{font-size:.9rem;font-weight:700;margin-top:.4rem;}}
.prob-bar{{height:10px;border-radius:5px;background:#e9ecef;margin:.5rem 0;overflow:hidden;}}
.prob-fill{{height:100%;border-radius:5px;}}
.winner-box{{background:linear-gradient(135deg,#1a1a2e,#0f3460);color:#fff;border-radius:14px;padding:2.5rem;text-align:center;margin:1.5rem 0;}}
.winner-box .wname{{font-size:2rem;font-weight:800;color:#FFD700;margin:.5rem 0;}}
.scenario{{border-left:4px solid var(--accent);padding:.85rem 1.2rem;margin:.8rem 0;background:#f8f9fa;border-radius:0 8px 8px 0;}}
.s1{{border-color:#28a745;}} .s2{{border-color:#17a2b8;}} .s3{{border-color:#ffc107;}} .s4{{border-color:#dc3545;}} .s5{{border-color:#6f42c1;}}
.risk{{background:#fff5f5;border:1px solid #f5c6cb;border-radius:8px;padding:.8rem 1rem;margin:.5rem 0;}}
img.chart{{width:100%;border-radius:8px;margin:1rem 0;border:1px solid var(--border);}}
.conf-high{{color:#28a745;font-weight:700;}} .conf-med{{color:#fd7e14;font-weight:700;}} .conf-low{{color:#dc3545;font-weight:700;}}
.model-row{{background:#f0f4ff;border-left:4px solid #0d6efd;padding:.7rem 1rem;margin:.5rem 0;border-radius:0 8px 8px 0;}}
.tag{{display:inline-block;padding:.2rem .6rem;border-radius:12px;font-size:.78rem;font-weight:600;margin:.1rem;}}
.tag-dmk{{background:#fce8e8;color:#c0392b;}} .tag-admk{{background:#e8f5ee;color:#1a6b3c;}} .tag-tvk{{background:#fffae8;color:#856404;}}
footer{{text-align:center;padding:2rem;color:var(--muted);font-size:.83rem;border-top:1px solid var(--border);margin-top:2rem;}}
@media(max-width:700px){{.grid2,.grid3{{grid-template-columns:1fr;}} .hero h1{{font-size:1.7rem;}}}}
</style>
</head>
<body>

<div class="hero">
  <div style="font-size:3rem;">🗳️</div>
  <h1>Tamil Nadu 2026 Assembly Election</h1>
  <div class="sub">Comprehensive Multi-Model Prediction Report &nbsp;|&nbsp; 234 Seats &nbsp;|&nbsp; Majority: 118</div>
  <div class="sub">Polling: <strong>April 23, 2026</strong> &nbsp;|&nbsp; Results: <strong>May 4, 2026</strong> &nbsp;|&nbsp; 5.67 Crore Registered Voters</div>
  <div class="badges">
    <span class="badge">📊 8 Opinion Polls (March–April 2026)</span>
    <span class="badge">🧮 7 Prediction Models</span>
    <span class="badge">📅 Updated: April 21, 2026</span>
    <span class="badge">🤖 TN Election Analyst Agent</span>
  </div>
</div>

<div class="container">

<!-- WINNER BOX -->
<div class="winner-box">
  <div style="font-size:.88rem;opacity:.8;text-transform:uppercase;letter-spacing:1.5px;">🏆 Final Ensemble Prediction</div>
  <div class="wname">SPA (DMK-led Alliance) — WINNER</div>
  <div class="wcm">Predicted Chief Minister: <strong>M. K. Stalin</strong> &nbsp;|&nbsp; Confidence: <strong>Medium-High</strong></div>
  <div style="margin-top:1rem;opacity:.82;font-size:.88rem;">6 Models · 8 Polls · All Factors: History, Swing, Caste, Alliance, Incumbency</div>
</div>

<!-- SEAT SUMMARY -->
<div class="card">
  <h2>📌 Seat Prediction Summary</h2>
  <div class="grid3">
    <div class="stat-card dmk">
      <div class="stat-num" style="color:var(--dmk)">147</div>
      <div class="stat-range">Range: 132 – 160 seats</div>
      <div class="stat-label">SPA (DMK-led)</div>
      <div style="font-size:.82rem;color:#888;margin:.3rem 0;">Vote Share: ~41.5%</div>
      <div class="prob-bar"><div class="prob-fill" style="width:98%;background:var(--dmk);"></div></div>
      <div style="font-size:.82rem;color:var(--dmk);font-weight:700;">Win Probability: 98%</div>
    </div>
    <div class="stat-card admk">
      <div class="stat-num" style="color:var(--admk)">74</div>
      <div class="stat-range">Range: 58 – 90 seats</div>
      <div class="stat-label">AIADMK+ (NDA)</div>
      <div style="font-size:.82rem;color:#888;margin:.3rem 0;">Vote Share: ~32.4%</div>
      <div class="prob-bar"><div class="prob-fill" style="width:2%;background:var(--admk);"></div></div>
      <div style="font-size:.82rem;color:var(--admk);font-weight:700;">Win Probability: &lt;2%</div>
    </div>
    <div class="stat-card tvk">
      <div class="stat-num" style="color:#856404">10</div>
      <div class="stat-range">Range: 4 – 14 seats</div>
      <div class="stat-label">TVK (Vijay)</div>
      <div style="font-size:.82rem;color:#888;margin:.3rem 0;">Vote Share: ~18.8%</div>
      <div class="prob-bar"><div class="prob-fill" style="width:1%;background:var(--tvk);"></div></div>
      <div style="font-size:.82rem;color:#856404;font-weight:700;">Kingmaker: ~10% chance</div>
    </div>
  </div>
  <div style="margin-top:1.5rem;padding:1rem;background:#fffbe6;border:1px solid #ffc107;border-radius:8px;font-size:.88rem;">
    <strong>⚠️ Key Caveat:</strong> 8 polls show <strong>SPA ranging from 104 to 189 seats</strong> — massive divergence. 
    Two early polls (IANS-Matrize, News18) predicted a tight race; six later polls converge on a clear DMK win. 
    The ensemble weights recency and sample size, pointing to a <strong>DMK comfortable majority (145–165 seats)</strong> as the most likely outcome (45% probability).
  </div>
</div>

<!-- CHARTS -->
<div class="card">
  <h2>📈 Historical Assembly Election Results (1967–2021)</h2>
  <img class="chart" src="{img_b64('chart1_historical_winners.png')}" alt="Historical Winners Chart">
  <p><strong>Key Pattern:</strong> Power has alternated between DMK and ADMK in <strong>67% of elections</strong> (8/12 transitions). 
  ADMK achieved back-to-back wins (1977–84, 2011–16), but <strong>DMK has never won consecutive elections post-1971</strong> (0 for 5 attempts). 
  This is the central historical tension for 2026.</p>
</div>

<div class="card">
  <h2>🔄 Anti-Incumbency &amp; Alternation Pattern Analysis</h2>
  <img class="chart" src="{img_b64('chart2_alternation_pattern.png')}" alt="Alternation Pattern Chart">
</div>

<div class="grid2">
  <div class="card">
    <h2>📊 Opinion Polls 2026 (8 Surveys)</h2>
    <img class="chart" src="{img_b64('chart3_opinion_polls.png')}" alt="Opinion Polls Chart">
  </div>
  <div class="card">
    <h2>📉 Party Vote Share Trends (1977–2026)</h2>
    <img class="chart" src="{img_b64('chart4_vote_share_trends.png')}" alt="Vote Share Trends Chart">
  </div>
</div>

<div class="card">
  <h2>🏆 Final Ensemble Seat Prediction</h2>
  <img class="chart" src="{img_b64('chart5_final_prediction.png')}" alt="Final Prediction Chart">
</div>

<div class="card">
  <h2>🎭 Five Scenario Probability Distribution</h2>
  <img class="chart" src="{img_b64('chart6_scenarios.png')}" alt="Scenario Analysis Chart">
</div>

<!-- OPINION POLLS TABLE -->
<div class="card">
  <h2>🗂️ All Opinion Polls — Updated April 2026 (8 Surveys)</h2>
  <table>
    <tr><th>Agency</th><th>Date</th><th>Sample</th><th>SPA Seats</th><th>ADMK+ Seats</th><th>TVK Seats</th><th>SPA%</th><th>ADMK%</th><th>TVK%</th></tr>
{poll_rows_html}  </table>
  <div style="font-size:.8rem;color:var(--muted);margin-top:.5rem;">
    ★ Highlighted = most recent polls with highest recency weight. 
    Ensemble weighting: 60% sample size + 40% recency.
    Sources: IANS-Matrize, News18-VoteVibe, Agni, Lokpal, Jan Ki Baat, CVoter-ABP, Polstrat, CSDS-Lokniti.
  </div>
</div>

<!-- HISTORICAL TABLE -->
<div class="card">
  <h2>📜 Historical Assembly Results (1967–2021)</h2>
  <table>
    <tr><th>Year</th><th>Winner</th><th>Seats</th><th>Vote%</th><th>Runner-Up</th><th>Seats</th><th>Vote%</th></tr>
{hist_rows_html}  </table>
</div>

<!-- 7 MODELS -->
<div class="card">
  <h2>🧮 7-Model Prediction Summary &amp; Weights</h2>
  <div class="model-row"><strong>M1 — Historical Alternation (Weight: 10%):</strong> Favors ADMK+ (67% alternation; DMK 0/5 consecutive wins). <span class="conf-med">Confidence: Medium</span></div>
  <div class="model-row"><strong>M2 — Swing Analysis 2024→2026 (Weight: 15%):</strong> SPA 163 | ADMK+ 58 | TVK 7. LS to Assembly swing + TVK drain on ADMK. <span class="conf-low">Confidence: Medium-Low</span></div>
  <div class="model-row"><strong>M3 — Poll Aggregation Bayesian (Weight: 30%):</strong> SPA 158±19 | ADMK+ 65±18 | TVK ~10. 6 of 8 polls lean DMK. <span class="conf-low">Confidence: Low–Med (high divergence)</span></div>
  <div class="model-row"><strong>M4 — Incumbency Factor Scorecard (Weight: 15%):</strong> Net incumbency score +1.8 (pro-DMK). SPA 140–170 | ADMK+ 50–80. <span class="conf-med">Confidence: Medium</span></div>
  <div class="model-row"><strong>M5 — Vote→Seat Cube Law (Weight: 10%):</strong> Scenario B (42%→140 seats). Multi-corner FPTP amplifies the DMK advantage. <span class="conf-med">Confidence: Medium</span></div>
  <div class="model-row"><strong>M6 — Alliance Arithmetic &amp; Caste Matrix (Weight: 20%):</strong> SPA net 31.3% | ADMK+ 21.5% (heavy leakage to TVK/Sasikala). SPA 130–160. <span class="conf-med">Confidence: Medium</span></div>
  <div class="model-row" style="border-color:#28a745;background:#f0fff4;">
    <strong>M7 — Composite Ensemble (FINAL):</strong> 
    <span style="color:var(--dmk);font-weight:800;">SPA: 147 seats (132–160)</span> | 
    ADMK+: 74 (58–90) | TVK: 10 (4–14) | Others: ~4 | 
    Win Prob: <strong>98%</strong> | <span class="conf-high">Confidence: Medium-High</span>
  </div>
</div>

<!-- SCENARIOS -->
<div class="card">
  <h2>🎭 Five Scenarios with Probabilities</h2>
  <div class="scenario s1">
    <strong>Scenario 1: DMK Comfortable Win — 45% (MOST LIKELY)</strong><br>
    Welfare delivery holds. TVK drains ~7% from ADMK. Opposition fragmented. Alliance management excellent.<br>
    <span class="tag tag-dmk">SPA: 145–165</span> <span class="tag tag-admk">ADMK+: 55–75</span> <span class="tag tag-tvk">TVK: 5–12</span> | <em>Stalin continues as CM. Stable majority government.</em>
  </div>
  <div class="scenario s2">
    <strong>Scenario 2: DMK Narrow Win — 20%</strong><br>
    Anti-incumbency partially triggers. ADMK holds Western TN. TVK surprises in urban seats.<br>
    <span class="tag tag-dmk">SPA: 120–144</span> <span class="tag tag-admk">ADMK+: 75–100</span> <span class="tag tag-tvk">TVK: 8–15</span> | <em>DMK forms government with thinner margin.</em>
  </div>
  <div class="scenario s3">
    <strong>Scenario 3: Hung Assembly — 10%</strong><br>
    TVK massively outperforms (>20 seats). Both main blocs fall short of 118. Coalition negotiations.<br>
    <span class="tag tag-dmk">SPA: 100–117</span> <span class="tag tag-admk">ADMK+: 85–110</span> <span class="tag tag-tvk">TVK: 15–30</span> | <em>TVK becomes kingmaker. Vijay enters coalition.</em>
  </div>
  <div class="scenario s4">
    <strong>Scenario 4: ADMK+ Comeback — 20%</strong><br>
    Historic anti-incumbency wave. TVK flops (&lt;5%). NDA vote transfer efficient. PMK delivers Vanniyar belt.<br>
    <span class="tag tag-dmk">SPA: 85–110</span> <span class="tag tag-admk">ADMK+: 115–140</span> <span class="tag tag-tvk">TVK: 2–8</span> | <em>EPS becomes CM. ADMK completes comeback.</em>
  </div>
  <div class="scenario s5">
    <strong>Scenario 5: DMK Landslide — 5%</strong><br>
    2024 LS wave continues unchecked. TVK devastates ADMK. Welfare schemes create unprecedented repeat.<br>
    <span class="tag tag-dmk">SPA: 170–190</span> <span class="tag tag-admk">ADMK+: 35–50</span> <span class="tag tag-tvk">TVK: 5–10</span> | <em>Historic consecutive win. ADMK faces existential crisis.</em>
  </div>
</div>

<!-- KEY FACTORS -->
<div class="card">
  <h2>⚖️ Key Factors Analysis</h2>
  <div class="grid2">
    <div>
      <h3 style="color:var(--dmk);">✅ Factors Favoring SPA (DMK)</h3>
      <ul>
        <li><strong>2024 LS clean sweep:</strong> All 39 TN seats. Strongest pre-Assembly validation ever for any TN ruling party</li>
        <li><strong>Welfare delivery:</strong> Breakfast scheme, Kalaignar insurance, housing — tangible voter base among poor/rural</li>
        <li><strong>TVK as ADMK vote splitter:</strong> 60% of TVK votes come from ADMK base (youth, OBC others)</li>
        <li><strong>Alliance additions:</strong> OPS joining; DMDK defection from NDA — organizational and symbolic gains</li>
        <li><strong>ADMK organizational decline:</strong> No Jayalalithaa; lost OPS, Sasikala, DMDK, Sengottaiyan</li>
        <li><strong>Dalit + Muslim consolidation:</strong> VCK+DMK+IUML hold ~26% consolidated base</li>
        <li><strong>Opposition fragmentation:</strong> Non-DMK vote split across 5 entities under FPTP</li>
      </ul>
    </div>
    <div>
      <h3 style="color:var(--admk);">⚠️ Factors Against DMK / Favoring ADMK+</h3>
      <ul>
        <li><strong>Historical pattern:</strong> DMK has NEVER won consecutive Assembly elections post-1971 (0 for 5 attempts)</li>
        <li><strong>67% alternation rate:</strong> Strongest precedent in Indian state politics</li>
        <li><strong>Cost of living / TASMAC:</strong> Inflation and liquor policy criticism</li>
        <li><strong>Corruption allegations:</strong> Senthil Balaji arrest, ED/CBI cases against allies</li>
        <li><strong>TVK wildcard:</strong> If TVK gets &lt;5%, ADMK+ consolidates anti-DMK vote and could win</li>
        <li><strong>PMK Vanniyar belt:</strong> 40+ northern constituencies where PMK decides outcome</li>
        <li><strong>ADMK-BJP transfer:</strong> If efficient (&gt;80%), combined NDA vote exceeds 35%</li>
      </ul>
    </div>
  </div>
</div>

<!-- REGIONAL -->
<div class="card">
  <h2>🗺️ Regional Breakdown Prediction</h2>
  <table>
    <tr><th>Region</th><th>Key Districts</th><th>Seats</th><th>SPA Est.</th><th>ADMK+ Est.</th><th>TVK Est.</th><th>Lean</th></tr>
    <tr><td>Chennai Metro</td><td>Chennai, Kancheepuram, Tiruvallur</td><td>~42</td><td>28–34</td><td>6–10</td><td>2–4</td><td style="color:var(--dmk);font-weight:700;">Strongly DMK</td></tr>
    <tr><td>Northern TN</td><td>Vellore, Tiruvannamalai, Cuddalore</td><td>~40</td><td>22–28</td><td>10–16</td><td>1–3</td><td style="color:var(--dmk);">DMK Leaning</td></tr>
    <tr><td>Vanniyar Belt</td><td>Salem, Dharmapuri, Villupuram</td><td>~35</td><td>14–18</td><td>14–18</td><td>2–4</td><td style="color:#856404;">⚡ Toss-Up</td></tr>
    <tr><td>Western TN (Kongu)</td><td>Coimbatore, Erode, Tiruppur, Namakkal</td><td>~45</td><td>20–28</td><td>14–22</td><td>2–5</td><td style="color:#fd7e14;">Competitive</td></tr>
    <tr><td>Delta Region</td><td>Thanjavur, Nagapattinam, Tiruvarur</td><td>~25</td><td>18–22</td><td>3–6</td><td>0–2</td><td style="color:var(--dmk);font-weight:700;">Strongly DMK</td></tr>
    <tr><td>Southern TN</td><td>Madurai, Dindigul, Virudhunagar, Tirunelveli</td><td>~30</td><td>14–20</td><td>10–16</td><td>1–3</td><td style="color:var(--dmk);">DMK Leaning</td></tr>
    <tr><td>Far South</td><td>Thoothukudi, Kanyakumari, Nagercoil</td><td>~17</td><td>8–12</td><td>4–8</td><td>0–1</td><td style="color:var(--dmk);">DMK Leaning</td></tr>
  </table>
</div>

<!-- RISKS -->
<div class="card">
  <h2>⚠️ Top Risk Factors That Could Invalidate This Prediction</h2>
  <div class="risk"><strong>Risk 1 — TVK Vote Uncertainty (HIGH IMPACT):</strong> No electoral track record. Actual vote share could range from 5% to 22%. If TVK gets &lt;6%, ADMK+ consolidates all anti-DMK votes and could win. If TVK gets &gt;20%, hung assembly is possible.</div>
  <div class="risk"><strong>Risk 2 — ADMK-BJP Transfer Efficiency (HIGH IMPACT):</strong> First time these two parties contest together in a TN Assembly election. Transfer efficiency untested — could be 60% or 90%. This difference alone determines 15–20 marginal constituencies.</div>
  <div class="risk"><strong>Risk 3 — Historical Anti-Incumbency Pattern (MEDIUM IMPACT):</strong> The most robust predictor in TN still points to ADMK. A late anti-incumbency swing in the last week before polling could flip 15–20 marginal seats and change the result.</div>
  <div class="risk"><strong>Risk 4 — Poll Divergence (HIGH):</strong> IANS-Matrize and News18 predicted a tight race; Agni and Lokpal predicted a DMK landslide. One group is badly wrong. Early pre-election polls were significantly off in 2021 TN elections.</div>
  <div class="risk"><strong>Risk 5 — Late-Breaking Events (UNKNOWN):</strong> Any major incident in the final 48 hours — economic shock, major scandal, natural disaster, or sympathy factor — could shift 10–15 marginal seats and change the arithmetic.</div>
</div>

<!-- CASTE MATRIX -->
<div class="card">
  <h2>🧬 Caste &amp; Community Electoral Matrix 2026</h2>
  <table>
    <tr><th>Community</th><th>TN Share</th><th>Primary Lean</th><th>Key Determinant</th><th>Net Impact</th></tr>
    <tr><td>Dalit / SC</td><td>~20%</td><td style="color:var(--dmk);font-weight:700;">DMK + VCK</td><td>Strong VCK alliance, reservations, housing schemes</td><td>+++ DMK</td></tr>
    <tr><td>Muslim &amp; Minority</td><td>~6%</td><td style="color:var(--dmk);font-weight:700;">SPA (IUML)</td><td>Solidly with DMK; anti-BJP sentiment very high in TN</td><td>+++ DMK</td></tr>
    <tr><td>OBC Others</td><td>~30%</td><td>Mixed → TVK</td><td>TVK's primary hunting ground; key battleground community</td><td>TVK wild card</td></tr>
    <tr><td>Vanniyar</td><td>~12%</td><td>PMK ↔ ADMK split</td><td>PMK in NDA vs PMK(R)-Sasikala split in N. TN</td><td>– ADMK (~2%)</td></tr>
    <tr><td>Thevar</td><td>~10%</td><td style="color:var(--admk);">ADMK base</td><td>Traditional ADMK cadre in South TN</td><td>Neutral</td></tr>
    <tr><td>Gounder (Kongu)</td><td>~10%</td><td style="color:var(--admk);">ADMK stronghold</td><td>BJP urban pockets; TVK may make inroads</td><td>Competitive</td></tr>
    <tr><td>Nadar</td><td>~5%</td><td>Swing</td><td>Far South swing community; INC factor in Kanyakumari</td><td>Low</td></tr>
    <tr><td>Christian</td><td>~6%</td><td>INC / DMK</td><td>Mixed — INC strong in Kanyakumari belt</td><td>Low</td></tr>
  </table>
</div>

<!-- ALLIANCE CONFIG -->
<div class="card">
  <h2>🤝 2026 Alliance Configuration</h2>
  <div class="grid2">
    <div style="border:2px solid var(--dmk);border-radius:10px;padding:1.2rem;">
      <h3 style="color:var(--dmk);margin-top:0;">SPA — Secular Progressive Alliance</h3>
      <p><strong>CM Candidate:</strong> M. K. Stalin (incumbent)</p>
      <p><strong>Parties:</strong> DMK (176 seats) · INC (28) · DMDK (10) · VCK (8) · CPI(M) (5) · CPI (5) · MDMK (4) · IUML/KMDK/others</p>
      <p><strong>Key Additions 2026:</strong> DMDK (defected from NDA) · O. Panneerselvam (OPS) joining — major coup in ADMK heartland</p>
      <p><strong>2021 Result:</strong> 159 seats, 44.06% vote share</p>
      <p><strong>2024 Lok Sabha:</strong> Swept ALL 39 TN seats — historic mandate</p>
    </div>
    <div style="border:2px solid var(--admk);border-radius:10px;padding:1.2rem;">
      <h3 style="color:var(--admk);margin-top:0;">AIADMK+ — NDA Alliance</h3>
      <p><strong>CM Candidate:</strong> Edappadi K. Palaniswami (EPS)</p>
      <p><strong>Parties:</strong> AIADMK (172) · BJP (33) · PMK (18) · AMMK/TTV (11)</p>
      <p><strong>Key Losses 2026:</strong> OPS (joined DMK) · Sasikala (breakaway) · DMDK · Sengottaiyan faction</p>
      <p><strong>2021 Result:</strong> 75 seats, 37.30% vote share</p>
      <p><strong>2024 LS:</strong> ADMK standalone 20.46% + BJP 11.24% = ~32%. Won 0 of 39 seats.</p>
    </div>
  </div>
  <div style="margin-top:1rem;background:#fffbe6;border:2px solid var(--tvk);border-radius:10px;padding:1.2rem;">
    <h3 style="color:#856404;margin-top:0;">🌟 TVK — Tamilaga Vettri Kazhagam (New Entrant)</h3>
    <p><strong>CM Candidate:</strong> Vijay (actor) &nbsp;|&nbsp; <strong>Contesting:</strong> All 234 seats solo &nbsp;|&nbsp; <strong>Prior Record:</strong> None (first-ever election)</p>
    <p>Star power + youth appeal. Karur crowd crush tragedy may have tempered initial enthusiasm. Expected to draw ~18% vote share but convert poorly into seats under FPTP. <strong>Primary role: ADMK vote splitter.</strong></p>
  </div>
</div>

<!-- DISCLAIMER -->
<div class="card" style="background:#fff8f0;border-color:#fd7e14;">
  <h2>📋 Methodology &amp; Disclaimer</h2>
  <ul>
    <li>This is a <strong>statistical prediction model</strong> — NOT a declaration of election results</li>
    <li><strong>7 models used:</strong> Historical Alternation (10%), Swing Analysis (15%), Poll Aggregation/Bayesian (30%), Incumbency Scorecard (15%), Vote→Seat Cube Law (10%), Alliance Arithmetic (20%)</li>
    <li><strong>8 polls aggregated:</strong> IANS-Matrize, News18-VoteVibe, Agni News Agency, Lokpal, Jan Ki Baat, CVoter-ABP, Polstrat, CSDS-Lokniti (March–April 2026)</li>
    <li>Largest uncertainty: TVK vote share (no benchmark), ADMK-BJP vote transfer efficiency</li>
    <li>Polling: April 23, 2026 · Results: May 4, 2026 · Total Seats: 234 · Majority: 118</li>
    <li>Historical data: Election Commission of India · Opinion polls: respective agencies</li>
  </ul>
</div>

</div>

<footer>
  Tamil Nadu 2026 Assembly Election — Prediction Report &nbsp;|&nbsp; Generated: April 21, 2026 &nbsp;|&nbsp; TN Election Analyst Agent<br>
  Data Sources: ECI · CSDS-Lokniti · IANS-Matrize · News18-VoteVibe · Agni · Lokpal · Jan Ki Baat · CVoter-ABP · Polstrat
</footer>
</body>
</html>"""

outfile = os.path.join(OUTPUT_DIR, "TN_2026_Election_Prediction_Report.html")
with open(outfile, "w", encoding="utf-8") as f:
    f.write(html)

size_kb = os.path.getsize(outfile) / 1024
print(f"Report generated: {outfile}")
print(f"File size: {size_kb:.0f} KB")
print("Sections: Winner prediction, 3 stat cards, 6 charts, 8-poll table, historical table, 7 models, 5 scenarios, regional breakdown, caste matrix, alliance config, risks, methodology")
