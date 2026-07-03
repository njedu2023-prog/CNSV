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
- snapshot_id: cnsvdata-2026-07-03-3fd3a1502203
- latest_trade_date: 2026-07-03
- generated_at: 2026-07-03 23:24:30
- file_count: 14

## Loaded Data
- daily_rows: 3849
- one_min_rows: 4338
- moneyflow_rows: 3849
- latest_trade_date: 2026-07-03

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-07-03', 'latest_open': 34.8, 'latest_high': 37.66, 'latest_low': 34.8, 'latest_close': 37.15, 'latest_pre_close': 34.36, 'latest_pct_chg': 8.1199, 'latest_volume': 1881514.53, 'latest_amount': 6836128.407, 'ma5': 34.816, 'ma10': 35.129999999999995, 'ma20': 35.315999999999995, 'ma60': 36.712500000000006, 'ret_1d': 0.08119906868451676, 'ret_3d': 0.09943770346256287, 'ret_5d': 0.11227544910179632, 'ret_10d': 0.027946873270614292, 'ret_20d': 0.007047980482515426, 'ret_60d': 0.21763356276630597, 'volume_ma5': 1233446.542, 'volume_ma20': 1053796.696, 'volume_ratio_5d': 1.70852329660721, 'volume_ratio_20d': 1.8765484425227241, 'amount_ma5': 4310478.6285999995, 'amount_ma20': 3735184.43425, 'amount_ratio_5d': 1.8131773795432622, 'amount_ratio_20d': 1.9245274825082133, 'price_position_20d': 0.8478260869565212, 'price_position_60d': 0.5128205128205127, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-07-03', 'latest_intraday_open': 34.8, 'latest_intraday_high': 37.66, 'latest_intraday_low': 34.8, 'latest_intraday_close': 37.15, 'intraday_range_pct': 0.07698519515477792, 'close_position_in_day_range': 0.8216783216783223, 'morning_return': 0.031321839080459934, 'afternoon_return': 0.035107272220674224, 'last_30min_return': -0.006950013365410235, 'last_60min_return': 0.004325493376588163, 'morning_volume_ratio': 0.4550071053663349, 'afternoon_volume_ratio': 0.5449928946336652, 'last_30min_volume_ratio': 0.08941228851418968, 'last_60min_volume_ratio': 0.2446602099851974, 'intraday_volume_sum': 188151453.0, 'intraday_amount_sum': 6836128420.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': 90239.48, 'net_mf_ratio': 0.013200378142048554, 'small_order_net': -10192.179999999993, 'medium_order_net': -4735.529999999999, 'large_order_net': -19.54000000000815, 'extra_large_order_net': 14947.240000000005, 'main_force_net': 14927.699999999997, 'main_force_ratio': 0.002183648274469868, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-07-03', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'positive', 'flow_strength_basic': 'positive', 'flow_strength_score': 15.38402641651842, 'flow_continuity_3d': 1, 'flow_continuity_5d': -1, 'flow_continuity_10d': -4, 'positive_flow_days_5d': 2, 'positive_flow_days_10d': 3, 'flow_reversal_1d': True, 'flow_reversal_3d': True, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'inflow_confirmed', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
