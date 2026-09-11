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
- snapshot_id: cnsvdata-2026-09-11-4c522d2d4f75
- latest_trade_date: 2026-09-11
- generated_at: 2026-09-11 22:16:27
- file_count: 14

## Loaded Data
- daily_rows: 3899
- one_min_rows: 16388
- moneyflow_rows: 3899
- latest_trade_date: 2026-09-11

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-09-11', 'latest_open': 39.5, 'latest_high': 40.0, 'latest_low': 38.9, 'latest_close': 39.75, 'latest_pre_close': 40.82, 'latest_pct_chg': -2.6213, 'latest_volume': 1832757.63, 'latest_amount': 7247794.175, 'ma5': 39.512, 'ma10': 37.178999999999995, 'ma20': 35.48950000000001, 'ma60': 34.90933333333333, 'ret_1d': -0.026212640862322445, 'ret_3d': 0.017144319344933434, 'ret_5d': 0.0608486789431546, 'ret_10d': 0.14289821736630248, 'ret_20d': 0.1894075403949731, 'ret_60d': 0.09988931931377976, 'volume_ma5': 1719966.448, 'volume_ma20': 1069635.4085, 'volume_ratio_5d': 0.9033238415368849, 'volume_ratio_20d': 1.8075662043244536, 'amount_ma5': 6755171.4662, 'amount_ma20': 3907111.8461999996, 'amount_ratio_5d': 0.9310907467444376, 'amount_ratio_20d': 1.9772331811435473, 'price_position_20d': 0.8335273573923166, 'price_position_60d': 0.8425110132158591, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-09-11', 'latest_intraday_open': 39.5, 'latest_intraday_high': 40.0, 'latest_intraday_low': 38.9, 'latest_intraday_close': 39.75, 'intraday_range_pct': 0.027672955974842803, 'close_position_in_day_range': 0.772727272727273, 'morning_return': 0.007594936708860578, 'afternoon_return': -0.0012562814070351536, 'last_30min_return': -0.0005028916268544625, 'last_60min_return': -0.004009020295665189, 'morning_volume_ratio': 0.7474211688318002, 'afternoon_volume_ratio': 0.2525788311681998, 'last_30min_volume_ratio': 0.0901955868545477, 'last_60min_volume_ratio': 0.13455396172597028, 'intraday_volume_sum': 183275763.0, 'intraday_amount_sum': 7247794162.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': -22464.78, 'net_mf_ratio': -0.003099533383203449, 'small_order_net': 17618.059999999998, 'medium_order_net': 30486.389999999985, 'large_order_net': 1030.8299999999872, 'extra_large_order_net': -49135.28999999998, 'main_force_net': -48104.45999999999, 'main_force_ratio': -0.006637117285411874, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-09-11', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -9.736650668615322, 'flow_continuity_3d': 1, 'flow_continuity_5d': 1, 'flow_continuity_10d': 2, 'positive_flow_days_5d': 3, 'positive_flow_days_10d': 6, 'flow_reversal_1d': True, 'flow_reversal_3d': True, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
