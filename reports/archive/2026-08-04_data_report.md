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
- snapshot_id: cnsvdata-2026-08-04-a78da8414d61
- latest_trade_date: 2026-08-04
- generated_at: 2026-08-04 20:08:17
- file_count: 14

## Loaded Data
- daily_rows: 3871
- one_min_rows: 9640
- moneyflow_rows: 3871
- latest_trade_date: 2026-08-04

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-08-04', 'latest_open': 34.93, 'latest_high': 35.05, 'latest_low': 34.4, 'latest_close': 34.48, 'latest_pre_close': 35.1, 'latest_pct_chg': -1.7664, 'latest_volume': 754154.12, 'latest_amount': 2608412.378, 'ma5': 34.824, 'ma10': 34.098, 'ma20': 34.183, 'ma60': 35.92883333333332, 'ret_1d': -0.01766381766381775, 'ret_3d': -0.004331504475888148, 'ret_5d': 0.029561063003881616, 'ret_10d': 0.0461165048543688, 'ret_20d': -0.07634610233056527, 'ret_60d': -0.16270033997085975, 'volume_ma5': 906606.39, 'volume_ma20': 1109375.1879999998, 'volume_ratio_5d': 0.8145422246294527, 'volume_ratio_20d': 0.6730992832035179, 'amount_ma5': 3138933.7436, 'amount_ma20': 3809641.0462500006, 'amount_ratio_5d': 0.8192348009571391, 'amount_ratio_20d': 0.6755050062322513, 'price_position_20d': 0.38636363636363585, 'price_position_60d': 0.23943661971830946, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-08-04', 'latest_intraday_open': 34.93, 'latest_intraday_high': 35.05, 'latest_intraday_low': 34.4, 'latest_intraday_close': 34.48, 'intraday_range_pct': 0.01885150812064961, 'close_position_in_day_range': 0.12307692307692072, 'morning_return': -0.00772974520469516, 'afternoon_return': -0.005193306405077869, 'last_30min_return': -0.001448016217781789, 'last_60min_return': -0.0031801098583407184, 'morning_volume_ratio': 0.5695701562964345, 'afternoon_volume_ratio': 0.4304298437035655, 'last_30min_volume_ratio': 0.15906020642040647, 'last_60min_volume_ratio': 0.2644951803750671, 'intraday_volume_sum': 75415412.0, 'intraday_amount_sum': 2608412380.0, 'late_session_strength': False, 'late_session_weakness': True, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -45621.84, 'net_mf_ratio': -0.01749027124115265, 'small_order_net': 28546.02999999999, 'medium_order_net': 12740.579999999987, 'large_order_net': -14619.520000000004, 'extra_large_order_net': -26667.090000000004, 'main_force_net': -41286.61000000001, 'main_force_ratio': -0.01582825259848541, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-08-04', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -33.31852383963806, 'flow_continuity_3d': -1, 'flow_continuity_5d': -1, 'flow_continuity_10d': -2, 'positive_flow_days_5d': 2, 'positive_flow_days_10d': 4, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
