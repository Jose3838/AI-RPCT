# AI-RPCT Bloomberg Execution Roadmap

Total Steps: 50
Done: 41
In Progress: 7
Not Started: 2
Completion: 82.0%

## data_moat

- [in_progress] 1. Collect source-labeled public GPU price snapshots daily. (data/manual_market_snapshots.csv)
- [done] 2. Expand priority coverage to 20+ GPU types. (data/gpu_universe.csv)
- [done] 3. Expand priority coverage to 15+ providers. (data/provider_universe.csv)
- [done] 4. Track priority regions for region-level pressure. (data/region_universe.csv)
- [in_progress] 5. Reach 30 clean daily core signal records. (data/core_signal_history.csv)
- [not_started] 6. Reach 90 clean daily core signal records. (data/core_signal_history.csv)
- [not_started] 7. Reach 180 clean daily core signal records. (data/core_signal_history.csv)
- [done] 8. Track manual snapshot quality and rejection reasons. (data/manual_snapshot_quality.csv)
- [done] 9. Track collection cadence and missing history days. (data/collection_cadence_audit.csv)
- [done] 10. Build source provenance for every paid-facing data point. (analytics/paid_data_point_provenance.py)

## trust

- [done] 11. Document each core signal methodology. (data/signal_methodology_registry.csv)
- [done] 12. Gate every claim as research-preview or paid-safe. (analytics/claim_gate_matrix.py)
- [done] 13. Expose signal trust status in terminal summary. (api/terminal_core.py)
- [done] 14. Separate fallback data from live provider data. (data/provider_preflight.csv)
- [done] 15. Create customer-facing trust center copy. (docs/TRUST_CENTER.md)
- [done] 16. Add forecast accuracy backtesting to paid-readiness gates. (analytics/forecast_accuracy.py)
- [done] 17. Add source URL coverage metrics by provider/GPU/region. (analytics/source_url_coverage_metrics.py)
- [done] 18. Add confidence score for each morning brief recommendation. (analytics/morning_brief.py)
- [done] 19. Publish safe-claims and unsafe-claims in research preview. (reports/research_preview_brief_*.md)
- [done] 20. Create methodology changelog for signal formula changes. (docs/SIGNAL_METHODOLOGY_CHANGELOG.md)

## core_intelligence

- [done] 21. Strengthen GPU Scarcity Index with source-backed observations. (analytics/source_backed_scarcity.py)
- [done] 22. Strengthen Capacity Shock Forecast with validation history. (analytics/forecast_validation_history.py)
- [done] 23. Strengthen Provider Reliability Score with live ingestion. (analytics/provider_reliability_live_overlay.py)
- [done] 24. Add Price Dislocation Signal. (analytics/price_dislocation_signal.py)
- [done] 25. Add AI Infrastructure Stress Index composite. (analytics/ai_infrastructure_stress_index.py)
- [done] 26. Add region-level scarcity heatmap data. (analytics/region_scarcity_heatmap.py)
- [done] 27. Add provider recovery and credential readiness plan. (scripts/provider_recovery_plan.py)
- [done] 28. Add collection target planner for manual snapshots. (data/snapshot_collection_plan.csv)
- [done] 29. Add daily provider reliability gap analysis. (data/provider_reliability_gaps.csv)
- [done] 30. Add signal performance score over time. (analytics/signal_performance_score.py)

## terminal_product

- [done] 31. Generate daily AI Infrastructure Morning Brief. (reports/morning_brief_*.md)
- [done] 32. Expose structured morning brief in terminal summary. (data/morning_brief_summary.csv)
- [done] 33. Create customer-ready executive brief. (analytics/customer_ready_executive_brief.py)
- [done] 34. Add actionable alerts for scarcity, shock and reliability drops. (analytics/core_intelligence_alerts.py)
- [done] 35. Add latest reports registry for customer consumption. (api/terminal_core.py)
- [done] 36. Add daily founder close for next-session continuity. (scripts/founder_daily_close.py)
- [in_progress] 37. Create terminal UI focused on morning decisions. (web)
- [done] 38. Add explain-this-score drilldowns. (analytics/signal_explainability_drilldowns.py)
- [done] 39. Add source evidence viewer for manual snapshots. (analytics/source_evidence_view.py)
- [done] 40. Add customer watchlists for GPUs/providers/regions. (analytics/customer_watchlists.py)

## commercial

- [done] 41. Define ICP and buying trigger. (docs/ICP.md)
- [in_progress] 42. Package research preview for first design partners. (docs/BETA_OFFER.md)
- [in_progress] 43. Create weekly public AI infrastructure stress report. (reports/weekly_infrastructure_report_*.txt)
- [done] 44. Build customer report export. (intelligence/reports/customer_report_pdf_export_v1.py)
- [done] 45. Create first paid-beta readiness checklist. (docs/BETA_CHECKLIST.md)
- [in_progress] 46. Add billing and entitlement hardening for paid beta. (api/access.py)
- [done] 47. Create outreach sequence and demo script. (docs/OUTREACH_SCRIPT.md)
- [done] 48. Secure first design partner feedback loop. (docs/DESIGN_PARTNER_FEEDBACK_LOOP.md)
- [in_progress] 49. Set first paid price and offer terms. (docs/PRICING.md)
- [done] 50. Ship public credibility page with methodology and sample brief. (docs/PUBLIC_CREDIBILITY_PAGE.md)
