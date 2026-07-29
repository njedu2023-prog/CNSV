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
- snapshot_id: cnsvdata-2026-07-29-6d0cafe8e925
- latest_trade_date: 2026-07-29
- generated_at: 2026-07-29 20:09:24
- file_count: 14

## Loaded Data
- daily_rows: 3867
- one_min_rows: 8676
- moneyflow_rows: 3867
- latest_trade_date: 2026-07-29

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-07-29', 'latest_open': 33.9, 'latest_high': 34.96, 'latest_low': 33.69, 'latest_close': 34.73, 'latest_pre_close': 33.49, 'latest_pct_chg': 3.7026, 'latest_volume': 1367703.03, 'latest_amount': 4701229.444, 'ma5': 33.714, 'ma10': 33.290000000000006, 'ma20': 34.5375, 'ma60': 36.341, 'ret_1d': 0.03702597790385176, 'ret_3d': 0.05051421657592248, 'ret_5d': 0.051786795881283876, 'ret_10d': 0.012241329058583439, 'ret_20d': -0.013071895424836666, 'ret_60d': -0.1683429118773947, 'volume_ma5': 940236.992, 'volume_ma20': 1226210.9370000002, 'volume_ratio_5d': 1.5481631083715715, 'volume_ratio_20d': 1.1153667532522997, 'amount_ma5': 3163480.5136, 'amount_ma20': 4267694.67035, 'amount_ratio_5d': 1.5968279209438911, 'amount_ratio_20d': 1.1005361946453294, 'price_position_20d': 0.42694805194805147, 'price_position_60d': 0.26458752515090506, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-07-29', 'latest_intraday_open': 33.9, 'latest_intraday_high': 34.96, 'latest_intraday_low': 33.69, 'latest_intraday_close': 34.73, 'intraday_range_pct': 0.03656780881082647, 'close_position_in_day_range': 0.8188976377952729, 'morning_return': 0.026253687315634266, 'afternoon_return': -0.0017246335153779935, 'last_30min_return': 0.001730602826651051, 'last_60min_return': -0.00028785261945896146, 'morning_volume_ratio': 0.6855048643125401, 'afternoon_volume_ratio': 0.31449513568745985, 'last_30min_volume_ratio': 0.08766706468435623, 'last_60min_volume_ratio': 0.14648952704301604, 'intraday_volume_sum': 136770303.0, 'intraday_amount_sum': 4701229431.0, 'late_session_strength': True, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': 75803.5, 'net_mf_ratio': 0.016124186428880877, 'small_order_net': -2753.6300000000047, 'medium_order_net': 3693.640000000014, 'large_order_net': -2039.0099999999948, 'extra_large_order_net': 1099.0, 'main_force_net': -940.0099999999948, 'main_force_ratio': -0.00019994982401884122, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-07-29', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'mixed', 'flow_strength_basic': 'mixed', 'flow_strength_score': 15.924236604862035, 'flow_continuity_3d': 1, 'flow_continuity_5d': 1, 'flow_continuity_10d': -2, 'positive_flow_days_5d': 3, 'positive_flow_days_10d': 4, 'flow_reversal_1d': True, 'flow_reversal_3d': True, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'inflow_confirmed', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
