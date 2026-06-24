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
- snapshot_id: cnsvdata-2026-06-23-f91718793826
- latest_trade_date: 2026-06-23
- generated_at: 2026-06-23 23:21:11
- file_count: 14

## Loaded Data
- daily_rows: 3841
- one_min_rows: 2410
- moneyflow_rows: 3841
- latest_trade_date: 2026-06-23

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-06-23', 'latest_open': 37.5, 'latest_high': 37.92, 'latest_low': 35.58, 'latest_close': 35.81, 'latest_pre_close': 37.33, 'latest_pct_chg': -4.0718, 'latest_volume': 1249031.01, 'latest_amount': 4571717.552, 'ma5': 36.484, 'ma10': 35.738, 'ma20': 36.342, 'ma60': 36.196666666666665, 'ret_1d': -0.040717921242968025, 'ret_3d': -0.03606998654104965, 'ret_5d': -0.002784739626844779, 'ret_10d': 0.028136663795578665, 'ret_20d': -0.055145118733509135, 'ret_60d': 0.13394553514882857, 'volume_ma5': 1127277.91, 'volume_ma20': 940510.2115, 'volume_ratio_5d': 1.1235534727372327, 'volume_ratio_20d': 1.3606408434426929, 'amount_ma5': 4116655.2574, 'amount_ma20': 3428149.783, 'amount_ratio_5d': 1.1310872538450945, 'amount_ratio_20d': 1.3642575555274874, 'price_position_20d': 0.31023102310231054, 'price_position_60d': 0.43293591654247404, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-06-23', 'latest_intraday_open': 37.5, 'latest_intraday_high': 37.92, 'latest_intraday_low': 35.58, 'latest_intraday_close': 35.81, 'intraday_range_pct': 0.06534487573303556, 'close_position_in_day_range': 0.09829059829059984, 'morning_return': -0.022133333333333338, 'afternoon_return': -0.023452413416962026, 'last_30min_return': 0.004206393718452217, 'last_60min_return': -0.005277777777777715, 'morning_volume_ratio': 0.5685150042832003, 'afternoon_volume_ratio': 0.4314849957167997, 'last_30min_volume_ratio': 0.12866589277074875, 'last_60min_volume_ratio': 0.23662076252214106, 'intraday_volume_sum': 124903101.0, 'intraday_amount_sum': 4571717556.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -115777.59, 'net_mf_ratio': -0.025324746921285744, 'small_order_net': -12287.640000000014, 'medium_order_net': -8108.299999999988, 'large_order_net': 4403.5, 'extra_large_order_net': 15992.429999999997, 'main_force_net': 20395.929999999997, 'main_force_ratio': 0.0044613276669021994, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-06-23', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'mixed', 'flow_strength_basic': 'mixed', 'flow_strength_score': -20.86341925438354, 'flow_continuity_3d': -1, 'flow_continuity_5d': -1, 'flow_continuity_10d': -2, 'positive_flow_days_5d': 2, 'positive_flow_days_10d': 4, 'flow_reversal_1d': True, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'outflow_confirmed', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
