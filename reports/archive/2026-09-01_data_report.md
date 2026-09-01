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
- snapshot_id: cnsvdata-2026-09-01-2fdda0a5521c
- latest_trade_date: 2026-09-01
- generated_at: 2026-09-01 22:43:59
- file_count: 14

## Loaded Data
- daily_rows: 3891
- one_min_rows: 14460
- moneyflow_rows: 3891
- latest_trade_date: 2026-09-01

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-09-01', 'latest_open': 33.99, 'latest_high': 34.68, 'latest_low': 33.89, 'latest_close': 34.43, 'latest_pre_close': 34.08, 'latest_pct_chg': 1.027, 'latest_volume': 816376.93, 'latest_amount': 2807923.705, 'ma5': 34.384, 'ma10': 33.937, 'ma20': 34.067499999999995, 'ma60': 34.592, 'ret_1d': 0.010269953051643244, 'ret_3d': -0.0026071842410198, 'ret_5d': 0.01743498817966893, 'ret_10d': 0.02806808002388772, 'ret_20d': -0.0014501160092806886, 'ret_60d': -0.011484352569623879, 'volume_ma5': 719976.6240000001, 'volume_ma20': 706754.2815, 'volume_ratio_5d': 1.2721580145187315, 'volume_ratio_20d': 1.1602144360275943, 'amount_ma5': 2470911.3826, 'amount_ma20': 2413470.19275, 'amount_ratio_5d': 1.2783543524006173, 'amount_ratio_20d': 1.1682671033077203, 'price_position_20d': 0.6642599277978336, 'price_position_60d': 0.37824675324675316, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-09-01', 'latest_intraday_open': 33.99, 'latest_intraday_high': 34.68, 'latest_intraday_low': 33.89, 'latest_intraday_close': 34.43, 'intraday_range_pct': 0.022945106012198638, 'close_position_in_day_range': 0.683544303797468, 'morning_return': 0.015592821418064062, 'afternoon_return': -0.0026071842410198, 'last_30min_return': -0.0011604293588627357, 'last_60min_return': -0.002896032435563356, 'morning_volume_ratio': 0.6744736527525343, 'afternoon_volume_ratio': 0.3255263472474657, 'last_30min_volume_ratio': 0.08793376853508098, 'last_60min_volume_ratio': 0.14546867462313026, 'intraday_volume_sum': 81637693.0, 'intraday_amount_sum': 2807923707.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': 6555.73, 'net_mf_ratio': 0.0023347251167566887, 'small_order_net': -5178.989999999998, 'medium_order_net': -13345.61, 'large_order_net': 10639.669999999998, 'extra_large_order_net': 7884.93, 'main_force_net': 18524.6, 'main_force_ratio': 0.0065972590234605385, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-09-01', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'positive', 'flow_strength_basic': 'positive', 'flow_strength_score': 8.931984140217226, 'flow_continuity_3d': -1, 'flow_continuity_5d': 1, 'flow_continuity_10d': -2, 'positive_flow_days_5d': 3, 'positive_flow_days_10d': 4, 'flow_reversal_1d': True, 'flow_reversal_3d': True, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'inflow_confirmed', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
