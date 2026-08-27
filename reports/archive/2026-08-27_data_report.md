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
- snapshot_id: cnsvdata-2026-08-26-759127bad201
- latest_trade_date: 2026-08-26
- generated_at: 2026-08-26 20:05:49
- file_count: 14

## Loaded Data
- daily_rows: 3887
- one_min_rows: 13496
- moneyflow_rows: 3887
- latest_trade_date: 2026-08-26

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-08-26', 'latest_open': 33.84, 'latest_high': 34.43, 'latest_low': 33.77, 'latest_close': 34.11, 'latest_pre_close': 33.84, 'latest_pct_chg': 0.7979, 'latest_volume': 644756.88, 'latest_amount': 2204941.842, 'ma5': 33.684000000000005, 'ma10': 33.589999999999996, 'ma20': 34.146499999999996, 'ma60': 34.695166666666665, 'ret_1d': 0.007978723404255206, 'ret_3d': 0.012767220902612841, 'ret_5d': 0.02926976463488229, 'ret_10d': 0.006491590439657635, 'ret_20d': -0.017852001151741903, 'ret_60d': -0.06419753086419766, 'volume_ma5': 605845.1140000001, 'volume_ma20': 717264.4155, 'volume_ratio_5d': 1.065337010723443, 'volume_ratio_20d': 0.8557829143308937, 'amount_ma5': 2042577.5908, 'amount_ma20': 2455661.4028999996, 'amount_ratio_5d': 1.0880976394127682, 'amount_ratio_20d': 0.8544710462024128, 'price_position_20d': 0.5487364620938622, 'price_position_60d': 0.32629870129870114, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-08-26', 'latest_intraday_open': 33.84, 'latest_intraday_high': 34.43, 'latest_intraday_low': 33.77, 'latest_intraday_close': 34.11, 'intraday_range_pct': 0.01934916446789788, 'close_position_in_day_range': 0.5151515151515123, 'morning_return': 0.01271437019515087, 'afternoon_return': -0.004087591240875876, 'last_30min_return': -0.0005859947260475895, 'last_60min_return': -0.0020479812755997973, 'morning_volume_ratio': 0.6724754453182415, 'afternoon_volume_ratio': 0.3275245546817585, 'last_30min_volume_ratio': 0.11339119018008773, 'last_60min_volume_ratio': 0.1806231831136102, 'intraday_volume_sum': 64475688.0, 'intraday_amount_sum': 2204941852.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': 12764.47, 'net_mf_ratio': 0.005789027972013059, 'small_order_net': 3187.8499999999985, 'medium_order_net': -10760.300000000003, 'large_order_net': 6156.510000000002, 'extra_large_order_net': 1415.9400000000023, 'main_force_net': 7572.450000000004, 'main_force_ratio': 0.003434308268707617, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-08-26', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'positive', 'flow_strength_basic': 'positive', 'flow_strength_score': 9.223336240720677, 'flow_continuity_3d': -1, 'flow_continuity_5d': -1, 'flow_continuity_10d': -4, 'positive_flow_days_5d': 2, 'positive_flow_days_10d': 3, 'flow_reversal_1d': True, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'inflow_confirmed', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
