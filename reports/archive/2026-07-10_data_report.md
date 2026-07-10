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
- snapshot_id: cnsvdata-2026-07-10-3ad77ca29fb1
- latest_trade_date: 2026-07-10
- generated_at: 2026-07-10 23:40:41
- file_count: 14

## Loaded Data
- daily_rows: 3854
- one_min_rows: 5543
- moneyflow_rows: 3854
- latest_trade_date: 2026-07-10

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-07-10', 'latest_open': 36.0, 'latest_high': 38.26, 'latest_low': 35.73, 'latest_close': 37.04, 'latest_pre_close': 36.06, 'latest_pct_chg': 2.7177, 'latest_volume': 1946672.95, 'latest_amount': 7247729.676, 'ma5': 36.809999999999995, 'ma10': 35.813, 'ma20': 35.7715, 'ma60': 37.081, 'ret_1d': 0.02717692734331667, 'ret_3d': -0.007768550763460946, 'ret_5d': -0.002960969044414563, 'ret_10d': 0.1089820359281437, 'ret_20d': 0.07518142235123348, 'ret_60d': 0.1341090018371096, 'volume_ma5': 1394184.4679999999, 'volume_ma20': 1198546.5945000001, 'volume_ratio_5d': 1.4094551830552589, 'volume_ratio_20d': 1.719760203718944, 'amount_ma5': 5144875.172599999, 'amount_ma20': 4305681.07095, 'amount_ratio_5d': 1.4316347757700891, 'amount_ratio_20d': 1.789972840641541, 'price_position_20d': 0.7740740740740742, 'price_position_60d': 0.42933810375670817, 'new_high_20d': True, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-07-10', 'latest_intraday_open': 36.0, 'latest_intraday_high': 38.26, 'latest_intraday_low': 35.73, 'latest_intraday_close': 37.04, 'intraday_range_pct': 0.06830453563714906, 'close_position_in_day_range': 0.5177865612648228, 'morning_return': 0.05166666666666675, 'afternoon_return': -0.02165874273639723, 'last_30min_return': 0.0016224986479178582, 'last_60min_return': -0.0008092797410305108, 'morning_volume_ratio': 0.5668664271520288, 'afternoon_volume_ratio': 0.4331335728479712, 'last_30min_volume_ratio': 0.125888449829233, 'last_60min_volume_ratio': 0.19657072339757944, 'intraday_volume_sum': 194667295.0, 'intraday_amount_sum': 7247729687.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': 15639.49, 'net_mf_ratio': 0.002157846760177649, 'small_order_net': -5541.920000000013, 'medium_order_net': -6604.599999999977, 'large_order_net': 9562.170000000013, 'extra_large_order_net': 2584.350000000006, 'main_force_net': 12146.520000000019, 'main_force_ratio': 0.001675906876083111, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-07-10', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'positive', 'flow_strength_basic': 'positive', 'flow_strength_score': 3.8337536362607594, 'flow_continuity_3d': -1, 'flow_continuity_5d': -1, 'flow_continuity_10d': -2, 'positive_flow_days_5d': 2, 'positive_flow_days_10d': 4, 'flow_reversal_1d': True, 'flow_reversal_3d': True, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'inflow_confirmed', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
