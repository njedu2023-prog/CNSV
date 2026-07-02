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
- snapshot_id: cnsvdata-2026-07-02-3828318b81f8
- latest_trade_date: 2026-07-02
- generated_at: 2026-07-02 23:30:04
- file_count: 14

## Loaded Data
- daily_rows: 3848
- one_min_rows: 4097
- moneyflow_rows: 3848
- latest_trade_date: 2026-07-02

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-07-02', 'latest_open': 35.23, 'latest_high': 36.23, 'latest_low': 34.25, 'latest_close': 34.36, 'latest_pre_close': 35.19, 'latest_pct_chg': -2.3586, 'latest_volume': 1124442.92, 'latest_amount': 3938762.649, 'ma5': 34.065999999999995, 'ma10': 35.029, 'ma20': 35.303000000000004, 'ma60': 36.601833333333346, 'ret_1d': -0.02358624609263993, 'ret_3d': 0.022923489133670705, 'ret_5d': -0.027455420322671897, 'ret_10d': -0.07510094212651408, 'ret_20d': -0.054225158271401064, 'ret_60d': 0.11197411003236257, 'volume_ma5': 1101251.902, 'volume_ma20': 1002646.3945, 'volume_ratio_5d': 1.060120290964948, 'volume_ratio_20d': 1.1504834260860948, 'amount_ma5': 3770248.0100000002, 'amount_ma20': 3552107.4493, 'amount_ratio_5d': 1.0838906291800205, 'amount_ratio_20d': 1.1357224363481324, 'price_position_20d': 0.2964426877470354, 'price_position_60d': 0.30414746543778803, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-07-02', 'latest_intraday_open': 35.23, 'latest_intraday_high': 36.23, 'latest_intraday_low': 34.25, 'latest_intraday_close': 34.36, 'intraday_range_pct': 0.057625145518044145, 'close_position_in_day_range': 0.05555555555555536, 'morning_return': -0.012205506670451283, 'afternoon_return': -0.012643678160919491, 'last_30min_return': -0.0008723466123873314, 'last_60min_return': -0.004923255140457661, 'morning_volume_ratio': 0.6238905128238968, 'afternoon_volume_ratio': 0.37610948717610315, 'last_30min_volume_ratio': 0.125675725718474, 'last_60min_volume_ratio': 0.23014165094302874, 'intraday_volume_sum': 112444292.0, 'intraday_amount_sum': 3938762646.0, 'late_session_strength': False, 'late_session_weakness': True, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -50967.91, 'net_mf_ratio': -0.012940081579411768, 'small_order_net': -10863.5, 'medium_order_net': -1591.1699999999983, 'large_order_net': 4144.0199999999895, 'extra_large_order_net': 8310.650000000001, 'main_force_net': 12454.669999999991, 'main_force_ratio': 0.0031620768017494192, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-07-02', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'mixed', 'flow_strength_basic': 'mixed', 'flow_strength_score': -9.778004777662346, 'flow_continuity_3d': -1, 'flow_continuity_5d': -3, 'flow_continuity_10d': -6, 'positive_flow_days_5d': 1, 'positive_flow_days_10d': 2, 'flow_reversal_1d': True, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'outflow_confirmed', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
