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
- snapshot_id: cnsvdata-2026-08-20-bcc99b2d6f98
- latest_trade_date: 2026-08-20
- generated_at: 2026-08-20 20:05:47
- file_count: 14

## Loaded Data
- daily_rows: 3883
- one_min_rows: 12532
- moneyflow_rows: 3883
- latest_trade_date: 2026-08-20

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-08-20', 'latest_open': 33.13, 'latest_high': 33.8, 'latest_low': 32.93, 'latest_close': 32.99, 'latest_pre_close': 33.14, 'latest_pct_chg': -0.4526, 'latest_volume': 576017.65, 'latest_amount': 1914841.167, 'ma5': 33.338, 'ma10': 33.801, 'ma20': 34.1155, 'ma60': 34.91716666666666, 'ret_1d': -0.004526252263126085, 'ret_3d': -0.0196136701337295, 'ret_5d': -0.023386619301361766, 'ret_10d': -0.05472779369627501, 'ret_20d': -0.022808056872037796, 'ret_60d': -0.1322987901104682, 'volume_ma5': 601564.23, 'volume_ma20': 776315.8295, 'volume_ratio_5d': 0.9332265134943256, 'volume_ratio_20d': 0.7192467280130781, 'amount_ma5': 2008515.1664, 'amount_ma20': 2653634.1113500004, 'amount_ratio_5d': 0.9249603673437429, 'amount_ratio_20d': 0.6998977200058571, 'price_position_20d': 0.032653061224491964, 'price_position_60d': 0.1399371069182391, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-08-20', 'latest_intraday_open': 33.13, 'latest_intraday_high': 33.8, 'latest_intraday_low': 32.93, 'latest_intraday_close': 32.99, 'intraday_range_pct': 0.026371627765989614, 'close_position_in_day_range': 0.06896551724138213, 'morning_return': -0.001509206157561227, 'afternoon_return': -0.002720677146311856, 'last_30min_return': -0.000605877006967459, 'last_60min_return': 0.00030321406913302873, 'morning_volume_ratio': 0.6490962907126197, 'afternoon_volume_ratio': 0.35090370928738035, 'last_30min_volume_ratio': 0.09373825611072856, 'last_60min_volume_ratio': 0.18893016559475218, 'intraday_volume_sum': 57601765.0, 'intraday_amount_sum': 1914841175.0, 'late_session_strength': False, 'late_session_weakness': True, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -8909.34, 'net_mf_ratio': -0.0046527827756901365, 'small_order_net': -2486.8799999999974, 'medium_order_net': 602.7599999999948, 'large_order_net': 4505.360000000001, 'extra_large_order_net': -2621.2299999999996, 'main_force_net': 1884.130000000001, 'main_force_ratio': 0.000983961506818806, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-08-20', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'mixed', 'flow_strength_basic': 'mixed', 'flow_strength_score': -3.6688212688713304, 'flow_continuity_3d': -3, 'flow_continuity_5d': -3, 'flow_continuity_10d': -8, 'positive_flow_days_5d': 1, 'positive_flow_days_10d': 1, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
