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
- snapshot_id: cnsvdata-2026-07-30-d68c5891b29c
- latest_trade_date: 2026-07-30
- generated_at: 2026-07-30 20:04:43
- file_count: 14

## Loaded Data
- daily_rows: 3868
- one_min_rows: 8917
- moneyflow_rows: 3868
- latest_trade_date: 2026-07-30

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-07-30', 'latest_open': 34.63, 'latest_high': 34.73, 'latest_low': 34.32, 'latest_close': 34.63, 'latest_pre_close': 34.73, 'latest_pct_chg': -0.2879, 'latest_volume': 780075.59, 'latest_amount': 2691536.763, 'ma5': 33.888, 'ma10': 33.452999999999996, 'ma20': 34.551, 'ma60': 36.231833333333334, 'ret_1d': -0.0028793550244743393, 'ret_3d': 0.032806441992245805, 'ret_5d': 0.02577014218009488, 'ret_10d': 0.049393939393939545, 'ret_20d': 0.007857974388824296, 'ret_60d': -0.15905779504613882, 'volume_ma5': 882862.358, 'volume_ma20': 1208992.5705, 'volume_ratio_5d': 0.8296584761472563, 'volume_ratio_20d': 0.6361675356676417, 'amount_ma5': 2989807.5438, 'amount_ma20': 4205333.37605, 'amount_ratio_5d': 0.8508150283932255, 'amount_ratio_20d': 0.6306769745501176, 'price_position_20d': 0.41071428571428614, 'price_position_60d': 0.25452716297786737, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-07-30', 'latest_intraday_open': 34.63, 'latest_intraday_high': 34.73, 'latest_intraday_low': 34.32, 'latest_intraday_close': 34.63, 'intraday_range_pct': 0.011839445567426986, 'close_position_in_day_range': 0.7560975609756216, 'morning_return': -0.0023101357204737827, 'afternoon_return': 0.002315484804631174, 'last_30min_return': 0.0008670520231213175, 'last_60min_return': 0.0031865585168018296, 'morning_volume_ratio': 0.64212593807736, 'afternoon_volume_ratio': 0.3578740619226401, 'last_30min_volume_ratio': 0.13946366402773863, 'last_60min_volume_ratio': 0.1885569063890334, 'intraday_volume_sum': 78007559.0, 'intraday_amount_sum': 2691536757.0, 'late_session_strength': True, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': -31600.79, 'net_mf_ratio': -0.011740798206589461, 'small_order_net': 2226.8899999999994, 'medium_order_net': -5588.460000000006, 'large_order_net': -4378.020000000004, 'extra_large_order_net': 7739.5999999999985, 'main_force_net': 3361.5799999999945, 'main_force_ratio': 0.0012489444863659084, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-07-30', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'mixed', 'flow_strength_basic': 'mixed', 'flow_strength_score': -10.491853720223553, 'flow_continuity_3d': -1, 'flow_continuity_5d': -1, 'flow_continuity_10d': -2, 'positive_flow_days_5d': 2, 'positive_flow_days_10d': 4, 'flow_reversal_1d': True, 'flow_reversal_3d': True, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
