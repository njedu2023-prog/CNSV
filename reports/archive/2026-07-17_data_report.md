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
- snapshot_id: cnsvdata-2026-07-17-1aee2598b1ca
- latest_trade_date: 2026-07-17
- generated_at: 2026-07-17 20:04:52
- file_count: 14

## Loaded Data
- daily_rows: 3859
- one_min_rows: 6748
- moneyflow_rows: 3859
- latest_trade_date: 2026-07-17

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-07-17', 'latest_open': 32.69, 'latest_high': 32.88, 'latest_low': 32.12, 'latest_close': 32.34, 'latest_pre_close': 33.0, 'latest_pct_chg': -2.0, 'latest_volume': 939558.31, 'latest_amount': 3049858.69, 'ma5': 33.526, 'ma10': 35.168000000000006, 'ma20': 35.148999999999994, 'ma60': 37.09583333333333, 'ret_1d': -0.019999999999999907, 'ret_3d': -0.04234527687296419, 'ret_5d': -0.12688984881209497, 'ret_10d': -0.12947510094212644, 'ret_20d': -0.10514665190924177, 'ret_60d': -0.08333333333333326, 'volume_ma5': 1366133.504, 'volume_ma20': 1274857.1130000001, 'volume_ratio_5d': 0.5993776624687411, 'volume_ratio_20d': 0.7300439144395726, 'amount_ma5': 4617413.8592, 'amount_ma20': 4503988.0087, 'amount_ratio_5d': 0.5588904828961648, 'amount_ratio_20d': 0.6677788355201977, 'price_position_20d': 0.03583061889250911, 'price_position_60d': 0.019469026548673087, 'new_high_20d': False, 'new_low_20d': True, 'new_high_60d': False, 'new_low_60d': True}
- minute_structure: {'latest_intraday_date': '2026-07-17', 'latest_intraday_open': 32.69, 'latest_intraday_high': 32.88, 'latest_intraday_low': 32.12, 'latest_intraday_close': 32.34, 'intraday_range_pct': 0.023500309214595085, 'close_position_in_day_range': 0.2894736842105322, 'morning_return': -0.0012236157846435836, 'afternoon_return': -0.009494640122511333, 'last_30min_return': -0.009494640122511333, 'last_60min_return': -0.004616805170821747, 'morning_volume_ratio': 0.5793221285009974, 'afternoon_volume_ratio': 0.42067787149900254, 'last_30min_volume_ratio': 0.11251583736191956, 'last_60min_volume_ratio': 0.2075608910318722, 'intraday_volume_sum': 93955831.0, 'intraday_amount_sum': 3049858697.0, 'late_session_strength': False, 'late_session_weakness': True, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -15449.94, 'net_mf_ratio': -0.005065788802169061, 'small_order_net': 5857.659999999989, 'medium_order_net': 338.08000000000175, 'large_order_net': -2698.760000000002, 'extra_large_order_net': -3496.980000000003, 'main_force_net': -6195.740000000005, 'main_force_ratio': -0.0020314842849325603, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-07-17', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -7.0972730871016205, 'flow_continuity_3d': -1, 'flow_continuity_5d': -3, 'flow_continuity_10d': -4, 'positive_flow_days_5d': 1, 'positive_flow_days_10d': 3, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
