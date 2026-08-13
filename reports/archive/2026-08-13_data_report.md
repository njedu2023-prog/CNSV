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
- snapshot_id: cnsvdata-2026-08-13-a75cf0a66be6
- latest_trade_date: 2026-08-13
- generated_at: 2026-08-13 20:05:45
- file_count: 14

## Loaded Data
- daily_rows: 3878
- one_min_rows: 11327
- moneyflow_rows: 3878
- latest_trade_date: 2026-08-13

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-08-13', 'latest_open': 33.88, 'latest_high': 34.3, 'latest_low': 33.74, 'latest_close': 33.78, 'latest_pre_close': 33.89, 'latest_pct_chg': -0.3246, 'latest_volume': 654358.55, 'latest_amount': 2223201.627, 'ma5': 34.264, 'ma10': 34.617999999999995, 'ma20': 34.0355, 'ma60': 35.329166666666666, 'ret_1d': -0.0032457952198288176, 'ret_3d': -0.030146425495262585, 'ret_5d': -0.03209169054441252, 'ret_10d': -0.024545192030031804, 'ret_20d': 0.023636363636363678, 'ret_60d': -0.12713178294573646, 'volume_ma5': 809492.1959999999, 'volume_ma20': 877024.449, 'volume_ratio_5d': 0.8036615227294382, 'volume_ratio_20d': 0.7227435817592647, 'amount_ma5': 2790291.6798, 'amount_ma20': 2979501.0660499996, 'amount_ratio_5d': 0.7890620652477767, 'amount_ratio_20d': 0.72372707923637, 'price_position_20d': 0.5153374233128837, 'price_position_60d': 0.20143884892086336, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-08-13', 'latest_intraday_open': 33.88, 'latest_intraday_high': 34.3, 'latest_intraday_low': 33.74, 'latest_intraday_close': 33.78, 'intraday_range_pct': 0.016577856719952492, 'close_position_in_day_range': 0.07142857142857052, 'morning_return': 0.005312868949232552, 'afternoon_return': -0.008220786846741102, 'last_30min_return': -0.005300353356890497, 'last_60min_return': -0.007346459006758788, 'morning_volume_ratio': 0.521962431758552, 'afternoon_volume_ratio': 0.47803756824144805, 'last_30min_volume_ratio': 0.16560937424902603, 'last_60min_volume_ratio': 0.24115372222155576, 'intraday_volume_sum': 65435855.0, 'intraday_amount_sum': 2223201634.0, 'late_session_strength': False, 'late_session_weakness': True, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -2552.59, 'net_mf_ratio': -0.001148159469208593, 'small_order_net': 5861.489999999998, 'medium_order_net': -1365.489999999998, 'large_order_net': -7227.669999999998, 'extra_large_order_net': 2731.6600000000035, 'main_force_net': -4496.009999999995, 'main_force_ratio': -0.002022313201554703, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-08-13', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -3.1704726707632958, 'flow_continuity_3d': -3, 'flow_continuity_5d': -5, 'flow_continuity_10d': -6, 'positive_flow_days_5d': 0, 'positive_flow_days_10d': 2, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
