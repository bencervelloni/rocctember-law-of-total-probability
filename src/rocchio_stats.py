"""Brayan Rocchio at-bats and walk-off rates, September vs. other months, 2024-2026 regular season
(Baseball Savant export).

Usage: python src/rocchio_stats.py data/savant_data.csv
"""
import sys
import pandas as pd

csv = sys.argv[1] if len(sys.argv) > 1 else "data/savant_data.csv"
df = pd.read_csv(csv, low_memory=False)

pa = df[df["events"].notna() & (df["events"] != "truncated_pa")].copy()
ab_exclude = {"walk", "hit_by_pitch", "sac_fly", "sac_bunt", "intent_walk", "catcher_interf"}
pa["is_ab"] = ~pa["events"].isin(ab_exclude)
pa["month"] = pd.to_datetime(pa["game_date"]).dt.month
pa["is_sept"] = pa["month"] == 9
ab = pa[pa["is_ab"]]

n_sept, n_other = int(ab["is_sept"].sum()), int((~ab["is_sept"]).sum())
print("== At-bats ==")
print(f"Total: {len(ab):,}  |  September: {n_sept} (P = {n_sept/len(ab):.3f})  |  "
      f"Other months: {n_other:,} (P = {n_other/len(ab):.3f})")

# Walk-offs: counts confirmed by hand (Statcast has no walk-off flag)
n_s, n_o, wo_s, wo_o = 190, 1043, 4, 3
n = n_s + n_o
r_s, r_o = wo_s / n_s, wo_o / n_o
print("\n== Walk-offs ==")
print(f"September: {wo_s}/{n_s} = {r_s:.4f} | Other: {wo_o}/{n_o} = {r_o:.4f} | {r_s/r_o:.1f}x")
print(f"Recomposed: {r_s*n_s/n + r_o*n_o/n:.4f}  actual: {(wo_s+wo_o)/n:.4f}")
