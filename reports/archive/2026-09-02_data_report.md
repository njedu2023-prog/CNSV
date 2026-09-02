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
- snapshot_id: cnsvdata-2026-09-02-9103eafbefc0
- latest_trade_date: 2026-09-02
- generated_at: 2026-09-02 22:19:27
- file_count: 14

## Loaded Data
- daily_rows: 3892
- one_min_rows: 14701
- moneyflow_rows: 3892
- latest_trade_date: 2026-09-02

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-09-02', 'latest_open': 34.2, 'latest_high': 34.47, 'latest_low': 33.73, 'latest_close': 33.93, 'latest_pre_close': 34.43, 'latest_pct_chg': -1.4522, 'latest_volume': 710156.61, 'latest_amount': 2417258.71, 'ma5': 34.348, 'ma10': 34.016000000000005, 'ma20': 34.004, 'ma60': 34.580000000000005, 'ret_1d': -0.014522218995062453, 'ret_3d': -0.02443933294997125, 'ret_5d': -0.00527704485488123, 'ret_10d': 0.023838261919130854, 'ret_20d': -0.0360795454545455, 'ret_60d': -0.020779220779220786, 'volume_ma5': 733056.57, 'volume_ma20': 692588.917, 'volume_ratio_5d': 0.9863606488423989, 'volume_ratio_20d': 1.0048140189441497, 'amount_ma5': 2513374.7561999997, 'amount_ma20': 2360916.00295, 'amount_ratio_5d': 0.9782862821476243, 'amount_ratio_20d': 1.0015697385703708, 'price_position_20d': 0.4855072463768106, 'price_position_60d': 0.29707792207792194, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-09-02', 'latest_intraday_open': 34.2, 'latest_intraday_high': 34.47, 'latest_intraday_low': 33.73, 'latest_intraday_close': 33.93, 'intraday_range_pct': 0.02180960801650463, 'close_position_in_day_range': 0.2702702702702734, 'morning_return': -0.0008771929824561431, 'afternoon_return': -0.0070237050043898686, 'last_30min_return': -0.0020588235294117796, 'last_60min_return': -0.008764241893076119, 'morning_volume_ratio': 0.6588202988070476, 'afternoon_volume_ratio': 0.3411797011929524, 'last_30min_volume_ratio': 0.11208607915372357, 'last_60min_volume_ratio': 0.18474361591874783, 'intraday_volume_sum': 71015661.0, 'intraday_amount_sum': 2417258710.0, 'late_session_strength': False, 'late_session_weakness': True, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -42260.51, 'net_mf_ratio': -0.017482824583554817, 'small_order_net': 9479.5, 'medium_order_net': 17701.489999999998, 'large_order_net': 9865.96, 'extra_large_order_net': -37046.95999999999, 'main_force_net': -27180.999999999993, 'main_force_ratio': -0.011244555614818736, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-09-02', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -28.727380198373552, 'flow_continuity_3d': -1, 'flow_continuity_5d': -1, 'flow_continuity_10d': -2, 'positive_flow_days_5d': 2, 'positive_flow_days_10d': 4, 'flow_reversal_1d': True, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
