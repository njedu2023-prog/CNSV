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
- snapshot_id: cnsvdata-2026-07-31-f05451f0431d
- latest_trade_date: 2026-07-31
- generated_at: 2026-07-31 20:07:20
- file_count: 14

## Loaded Data
- daily_rows: 3869
- one_min_rows: 9158
- moneyflow_rows: 3869
- latest_trade_date: 2026-07-31

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-07-31', 'latest_open': 34.33, 'latest_high': 35.26, 'latest_low': 34.2, 'latest_close': 35.18, 'latest_pre_close': 34.63, 'latest_pct_chg': 1.5882, 'latest_volume': 983410.74, 'latest_amount': 3434358.383, 'ma5': 34.312, 'ma10': 33.737, 'ma20': 34.4525, 'ma60': 36.141333333333336, 'ret_1d': 0.01588218307825584, 'ret_3d': 0.05046282472379815, 'ret_5d': 0.06412583182093146, 'ret_10d': 0.08781694495980208, 'ret_20d': -0.05302826379542391, 'ret_60d': -0.13371090864319135, 'volume_ma5': 920640.0140000001, 'volume_ma20': 1164087.3809999998, 'volume_ratio_5d': 1.113889080317999, 'volume_ratio_20d': 0.8134133856532247, 'amount_ma5': 3146280.2308, 'amount_ma20': 4035244.8748500003, 'amount_ratio_5d': 1.1486887810293576, 'amount_ratio_20d': 0.8166673307184592, 'price_position_20d': 0.5, 'price_position_60d': 0.3098591549295774, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-07-31', 'latest_intraday_open': 34.33, 'latest_intraday_high': 35.26, 'latest_intraday_low': 34.2, 'latest_intraday_close': 35.18, 'intraday_range_pct': 0.03013075611142681, 'close_position_in_day_range': 0.9245283018867937, 'morning_return': 0.015147101660355489, 'afternoon_return': 0.00946915351506461, 'last_30min_return': -0.0017026106696935717, 'last_60min_return': 0.0011383039271484208, 'morning_volume_ratio': 0.6100664102976951, 'afternoon_volume_ratio': 0.38993358970230485, 'last_30min_volume_ratio': 0.1100256440152362, 'last_60min_volume_ratio': 0.2139464126657799, 'intraday_volume_sum': 98341074.0, 'intraday_amount_sum': 3434358375.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': 22593.48, 'net_mf_ratio': 0.006578661129786932, 'small_order_net': -2823.8699999999953, 'medium_order_net': -602.0299999999988, 'large_order_net': -915.0099999999948, 'extra_large_order_net': 4340.9000000000015, 'main_force_net': 3425.8900000000067, 'main_force_ratio': 0.0009975342168592797, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-07-31', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'positive', 'flow_strength_basic': 'positive', 'flow_strength_score': 7.576195346646211, 'flow_continuity_3d': 1, 'flow_continuity_5d': 1, 'flow_continuity_10d': 0, 'positive_flow_days_5d': 3, 'positive_flow_days_10d': 5, 'flow_reversal_1d': True, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'inflow_confirmed', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
