# CNSV Data Status Report

## CNSVdata Gate
- ready: True
- status: PASS
- can_continue: True
- can_run_backtest: True
- can_use_moneyflow_as_strong_factor: True
- can_generate_formal_signal: False
- blocking_reason: None

## Data Manifest
- snapshot_id: cnsvdata-2026-10-20-5ee6f35d3d06
- latest_trade_date: 2026-10-20
- generated_at: 2026-10-20 22:55:18
- file_count: 14

## Loaded Data
- daily_rows: 3920
- one_min_rows: 21449
- moneyflow_rows: 3920
- latest_trade_date: 2026-10-20

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-10-20', 'latest_open': 35.86, 'latest_high': 36.04, 'latest_low': 34.79, 'latest_close': 35.22, 'latest_pre_close': 36.06, 'latest_pct_chg': -2.3295, 'latest_volume': 732651.62, 'latest_amount': 2578900.496, 'ma5': 36.122, 'ma10': 37.520999999999994, 'ma20': 38.222, 'ma60': 36.033166666666666, 'ret_1d': -0.0232945091514144, 'ret_3d': -0.006488011283497963, 'ret_5d': -0.10038314176245211, 'ret_10d': -0.09576379974326066, 'ret_20d': -0.09645972293483829, 'ret_60d': 0.06694940926991833, 'volume_ma5': 1020739.75, 'volume_ma20': 1014480.0365, 'volume_ratio_5d': 0.6565307786360931, 'volume_ratio_20d': 0.6970722722462854, 'amount_ma5': 3693010.0435999995, 'amount_ma20': 3883611.9203000003, 'amount_ratio_5d': 0.6273856099990682, 'amount_ratio_20d': 0.6375711115147957, 'price_position_20d': 0.11538461538461565, 'price_position_60d': 0.30146231721034866, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-10-20', 'latest_intraday_open': 35.86, 'latest_intraday_high': 36.04, 'latest_intraday_low': 34.79, 'latest_intraday_close': 35.22, 'intraday_range_pct': 0.03549119818285065, 'close_position_in_day_range': 0.34399999999999975, 'morning_return': -0.016452872281093045, 'afternoon_return': -0.0014176353841792722, 'last_30min_return': 0.006861063464837169, 'last_60min_return': 0.009458297506448776, 'morning_volume_ratio': 0.5631541905278254, 'afternoon_volume_ratio': 0.4368458094721745, 'last_30min_volume_ratio': 0.13460787816179265, 'last_60min_volume_ratio': 0.2180492687643276, 'intraday_volume_sum': 73265162.0, 'intraday_amount_sum': 2578900504.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -20857.44, 'net_mf_ratio': -0.008087725770091132, 'small_order_net': 13262.290000000008, 'medium_order_net': 13187.940000000002, 'large_order_net': 2542.8600000000006, 'extra_large_order_net': -28993.089999999997, 'main_force_net': -26450.229999999996, 'main_force_ratio': -0.010256398042896804, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-10-20', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -18.344123812987934, 'flow_continuity_3d': -1, 'flow_continuity_5d': -3, 'flow_continuity_10d': -4, 'positive_flow_days_5d': 1, 'positive_flow_days_10d': 3, 'flow_reversal_1d': True, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
