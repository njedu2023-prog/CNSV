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
- snapshot_id: cnsvdata-2026-07-06-8c729029a501
- latest_trade_date: 2026-07-06
- generated_at: 2026-07-07 00:30:09
- file_count: 14

## Loaded Data
- daily_rows: 3850
- one_min_rows: 4579
- moneyflow_rows: 3850
- latest_trade_date: 2026-07-06

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-07-06', 'latest_open': 36.95, 'latest_high': 38.09, 'latest_low': 36.95, 'latest_close': 37.64, 'latest_pre_close': 37.15, 'latest_pct_chg': 1.319, 'latest_volume': 1521029.52, 'latest_amount': 5735515.648, 'ma5': 35.626, 'ma10': 35.160999999999994, 'ma20': 35.40050000000001, 'ma60': 36.80683333333334, 'ret_1d': 0.01318977119784659, 'ret_3d': 0.06962205171923852, 'ret_5d': 0.12057159869008616, 'ret_10d': 0.008304312885079046, 'ret_20d': 0.04700973574408884, 'ret_60d': 0.17698561601000629, 'volume_ma5': 1356683.06, 'volume_ma20': 1085282.8805000002, 'volume_ratio_5d': 1.233153986174133, 'volume_ratio_20d': 1.443380422213812, 'amount_ma5': 4854472.0956, 'amount_ma20': 3859537.9218, 'amount_ratio_5d': 1.3305983261220433, 'amount_ratio_20d': 1.5355374678176108, 'price_position_20d': 0.9139579349904393, 'price_position_60d': 0.5021533161068045, 'new_high_20d': True, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-07-06', 'latest_intraday_open': 36.95, 'latest_intraday_high': 38.09, 'latest_intraday_low': 36.95, 'latest_intraday_close': 37.64, 'intraday_range_pct': 0.030286928799149855, 'close_position_in_day_range': 0.6052631578947345, 'morning_return': 0.012422360248447228, 'afternoon_return': 0.00400106695118696, 'last_30min_return': -0.002649708532061479, 'last_60min_return': -0.005285412262156508, 'morning_volume_ratio': 0.6713096797753143, 'afternoon_volume_ratio': 0.3286903202246857, 'last_30min_volume_ratio': 0.08734771301480065, 'last_60min_volume_ratio': 0.16732501023385793, 'intraday_volume_sum': 152102952.0, 'intraday_amount_sum': 5735515666.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': 7942.03, 'net_mf_ratio': 0.0013847107195617922, 'small_order_net': 3939.5, 'medium_order_net': 4904.529999999999, 'large_order_net': -6167.2699999999895, 'extra_large_order_net': -2676.7599999999948, 'main_force_net': -8844.029999999984, 'main_force_ratio': -0.0015419764399185166, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-07-06', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'mixed', 'flow_strength_basic': 'mixed', 'flow_strength_score': -0.15726572035672426, 'flow_continuity_3d': 1, 'flow_continuity_5d': 1, 'flow_continuity_10d': -4, 'positive_flow_days_5d': 3, 'positive_flow_days_10d': 3, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'inflow_confirmed', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
