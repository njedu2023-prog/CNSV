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
- snapshot_id: cnsvdata-2026-08-25-be479a53e6bd
- latest_trade_date: 2026-08-25
- generated_at: 2026-08-25 20:05:54
- file_count: 14

## Loaded Data
- daily_rows: 3886
- one_min_rows: 13255
- moneyflow_rows: 3886
- latest_trade_date: 2026-08-25

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-08-25', 'latest_open': 33.73, 'latest_high': 34.08, 'latest_low': 33.58, 'latest_close': 33.84, 'latest_pre_close': 33.8, 'latest_pct_chg': 0.1183, 'latest_volume': 425124.03, 'latest_amount': 1435938.642, 'ma5': 33.49, 'ma10': 33.568000000000005, 'ma20': 34.177499999999995, 'ma60': 34.73416666666667, 'ret_1d': 0.0011834319526629056, 'ret_3d': 0.025765383449530166, 'ret_5d': 0.010450880859958156, 'ret_10d': -0.003826906093611915, 'ret_20d': 0.010450880859958156, 'ret_60d': -0.07893304300489923, 'volume_ma5': 605214.006, 'volume_ma20': 753411.723, 'volume_ratio_5d': 0.6858600924756246, 'volume_ratio_20d': 0.5487756662061106, 'amount_ma5': 2026419.1026, 'amount_ma20': 2580475.783, 'amount_ratio_5d': 0.6928606963573287, 'amount_ratio_20d': 0.5417907514421093, 'price_position_20d': 0.4512635379061378, 'price_position_60d': 0.2824675324675329, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-08-25', 'latest_intraday_open': 33.73, 'latest_intraday_high': 34.08, 'latest_intraday_low': 33.58, 'latest_intraday_close': 33.84, 'intraday_range_pct': 0.014775413711583923, 'close_position_in_day_range': 0.5200000000000102, 'morning_return': -0.0011858879335902017, 'afternoon_return': 0.004452359750668045, 'last_30min_return': 0.0002955956251848857, 'last_60min_return': 0.002666666666666817, 'morning_volume_ratio': 0.5617773006150699, 'afternoon_volume_ratio': 0.4382226993849301, 'last_30min_volume_ratio': 0.1472062635461938, 'last_60min_volume_ratio': 0.2382105758641778, 'intraday_volume_sum': 42512403.0, 'intraday_amount_sum': 1435938643.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': -9028.09, 'net_mf_ratio': -0.006287239395845996, 'small_order_net': -1887.9199999999983, 'medium_order_net': -3183.8199999999997, 'large_order_net': 6848.520000000004, 'extra_large_order_net': -1776.7599999999984, 'main_force_net': 5071.760000000006, 'main_force_ratio': 0.0035320172127521906, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-08-25', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'mixed', 'flow_strength_basic': 'mixed', 'flow_strength_score': -2.755222183093804, 'flow_continuity_3d': -1, 'flow_continuity_5d': -3, 'flow_continuity_10d': -6, 'positive_flow_days_5d': 1, 'positive_flow_days_10d': 2, 'flow_reversal_1d': False, 'flow_reversal_3d': True, 'price_flow_confirm': False, 'price_flow_divergence': True, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
