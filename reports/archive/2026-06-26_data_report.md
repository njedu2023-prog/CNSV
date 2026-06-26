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
- snapshot_id: cnsvdata-2026-06-26-b3d58a5c3acb
- latest_trade_date: 2026-06-26
- generated_at: 2026-06-26 23:11:45
- file_count: 14

## Loaded Data
- daily_rows: 3844
- one_min_rows: 3133
- moneyflow_rows: 3844
- latest_trade_date: 2026-06-26

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-06-26', 'latest_open': 35.2, 'latest_high': 35.29, 'latest_low': 33.21, 'latest_close': 33.4, 'latest_pre_close': 35.33, 'latest_pct_chg': -5.4628, 'latest_volume': 1220541.33, 'latest_amount': 4134975.314, 'ma5': 35.444, 'ma10': 35.73, 'ma20': 35.80149999999999, 'ma60': 36.37533333333333, 'ret_1d': -0.054627795075007035, 'ret_3d': -0.06729963697291275, 'ret_5d': -0.07581627006087444, 'ret_10d': -0.030478955007257058, 'ret_20d': -0.12519643792561552, 'ret_60d': 0.08300907911802846, 'volume_ma5': 1105663.938, 'volume_ma20': 935184.6070000001, 'volume_ratio_5d': 1.1116102911718335, 'volume_ratio_20d': 1.327041635168888, 'amount_ma5': 3943184.3744, 'amount_ma20': 3358300.8142000004, 'amount_ratio_5d': 1.0392298247454588, 'amount_ratio_20d': 1.244021221201048, 'price_position_20d': 0.03619047619047576, 'price_position_60d': 0.24434389140271479, 'new_high_20d': False, 'new_low_20d': True, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-06-26', 'latest_intraday_open': 35.2, 'latest_intraday_high': 35.29, 'latest_intraday_low': 33.21, 'latest_intraday_close': 33.4, 'intraday_range_pct': 0.06227544910179636, 'close_position_in_day_range': 0.09134615384615283, 'morning_return': -0.05198863636363649, 'afternoon_return': 0.0008990110878035473, 'last_30min_return': -0.006543723973825077, 'last_60min_return': -0.009196084247997671, 'morning_volume_ratio': 0.6858281234933683, 'afternoon_volume_ratio': 0.3141718765066317, 'last_30min_volume_ratio': 0.11315602889088565, 'last_60min_volume_ratio': 0.17599588372808317, 'intraday_volume_sum': 122054133.0, 'intraday_amount_sum': 4134975312.0, 'late_session_strength': False, 'late_session_weakness': True, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -57840.16, 'net_mf_ratio': -0.013988030304356977, 'small_order_net': 10873.770000000019, 'medium_order_net': -4325.4100000000035, 'large_order_net': -5421.8399999999965, 'extra_large_order_net': -1126.5199999999968, 'main_force_net': -6548.359999999993, 'main_force_ratio': -0.0015836515342253369, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-06-26', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -15.571681838582315, 'flow_continuity_3d': -3, 'flow_continuity_5d': -3, 'flow_continuity_10d': -2, 'positive_flow_days_5d': 1, 'positive_flow_days_10d': 4, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'outflow_confirmed', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
