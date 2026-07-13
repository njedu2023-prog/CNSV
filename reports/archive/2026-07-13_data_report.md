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
- snapshot_id: cnsvdata-2026-07-13-6a69c54046df
- latest_trade_date: 2026-07-13
- generated_at: 2026-07-13 23:51:29
- file_count: 14

## Loaded Data
- daily_rows: 3855
- one_min_rows: 5784
- moneyflow_rows: 3855
- latest_trade_date: 2026-07-13

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-07-13', 'latest_open': 36.94, 'latest_high': 36.94, 'latest_low': 33.77, 'latest_close': 34.21, 'latest_pre_close': 37.04, 'latest_pct_chg': -7.6404, 'latest_volume': 2166009.19, 'latest_amount': 7478641.3, 'ma5': 36.124, 'ma10': 35.875, 'ma20': 35.7375, 'ma60': 37.10116666666667, 'ret_1d': -0.07640388768898487, 'ret_3d': -0.04919399666481372, 'ret_5d': -0.09112646121147716, 'ret_10d': 0.01845787436737112, 'ret_20d': -0.019489825164803687, 'ret_60d': 0.036666666666666625, 'volume_ma5': 1523180.402, 'volume_ma20': 1255323.1390000002, 'volume_ratio_5d': 1.5536030128833713, 'volume_ratio_20d': 1.8071964827563487, 'amount_ma5': 5493500.303, 'amount_ma20': 4498707.681050001, 'amount_ratio_5d': 1.4536098640116502, 'amount_ratio_20d': 1.7369241188014706, 'price_position_20d': 0.25000000000000033, 'price_position_60d': 0.17620751341681565, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-07-13', 'latest_intraday_open': 36.94, 'latest_intraday_high': 36.94, 'latest_intraday_low': 33.77, 'latest_intraday_close': 34.21, 'intraday_range_pct': 0.09266296404560054, 'close_position_in_day_range': 0.13880126182965252, 'morning_return': -0.0785694933622324, 'afternoon_return': 0.005880623346074865, 'last_30min_return': -0.0011678832116788218, 'last_60min_return': -0.0072547881601857656, 'morning_volume_ratio': 0.7544142275776771, 'afternoon_volume_ratio': 0.2455857724223229, 'last_30min_volume_ratio': 0.07276760907925788, 'last_60min_volume_ratio': 0.10955896729136223, 'intraday_volume_sum': 216600919.0, 'intraday_amount_sum': 7478641274.0, 'late_session_strength': False, 'late_session_weakness': True, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -80975.89, 'net_mf_ratio': -0.010827620519786127, 'small_order_net': -11472.520000000019, 'medium_order_net': -14848.279999999999, 'large_order_net': 17278.97, 'extra_large_order_net': 9041.82, 'main_force_net': 26320.79, 'main_force_ratio': 0.003519461482930061, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-07-13', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'mixed', 'flow_strength_basic': 'mixed', 'flow_strength_score': -7.3081590368560665, 'flow_continuity_3d': -1, 'flow_continuity_5d': -3, 'flow_continuity_10d': -2, 'positive_flow_days_5d': 1, 'positive_flow_days_10d': 4, 'flow_reversal_1d': True, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'outflow_confirmed', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
