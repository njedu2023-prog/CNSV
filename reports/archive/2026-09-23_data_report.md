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
- snapshot_id: cnsvdata-2026-09-23-c432b80fbdd4
- latest_trade_date: 2026-09-23
- generated_at: 2026-09-23 22:52:37
- file_count: 14

## Loaded Data
- daily_rows: 3907
- one_min_rows: 18316
- moneyflow_rows: 3907
- latest_trade_date: 2026-09-23

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-09-23', 'latest_open': 40.04, 'latest_high': 40.14, 'latest_low': 38.53, 'latest_close': 38.59, 'latest_pre_close': 40.12, 'latest_pct_chg': -3.8136, 'latest_volume': 841874.55, 'latest_amount': 3282325.668, 'ma5': 39.632000000000005, 'ma10': 39.366, 'ma20': 37.709, 'ma60': 35.464333333333336, 'ret_1d': -0.03813559322033888, 'ret_3d': -0.022295414238662215, 'ret_5d': 0.021169621593014165, 'ret_10d': -0.023779408044523054, 'ret_20d': 0.13133978305482286, 'ret_60d': 0.09661835748792291, 'volume_ma5': 1094962.866, 'volume_ma20': 1285326.889, 'volume_ratio_5d': 0.7608853763949837, 'volume_ratio_20d': 0.6600499316485638, 'amount_ma5': 4324038.3244, 'amount_ma20': 4885941.4109000005, 'amount_ratio_5d': 0.7551833854052168, 'amount_ratio_20d': 0.6792790999037908, 'price_position_20d': 0.657407407407408, 'price_position_60d': 0.7147577092511017, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-09-23', 'latest_intraday_open': 40.04, 'latest_intraday_high': 40.14, 'latest_intraday_low': 38.53, 'latest_intraday_close': 38.59, 'intraday_range_pct': 0.0417206530189168, 'close_position_in_day_range': 0.03726708074534304, 'morning_return': -0.027222777222777106, 'afternoon_return': -0.009242618741976849, 'last_30min_return': -0.0005180005180004388, 'last_60min_return': -0.0059247810407006, 'morning_volume_ratio': 0.6047002846207906, 'afternoon_volume_ratio': 0.3952997153792094, 'last_30min_volume_ratio': 0.14782151331216747, 'last_60min_volume_ratio': 0.22255098458553, 'intraday_volume_sum': 84187455.0, 'intraday_amount_sum': 3282325658.0, 'late_session_strength': False, 'late_session_weakness': True, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -21872.34, 'net_mf_ratio': -0.0066636714976936896, 'small_order_net': 41760.810000000005, 'medium_order_net': 9750.990000000005, 'large_order_net': -25575.100000000006, 'extra_large_order_net': -25936.710000000006, 'main_force_net': -51511.81000000001, 'main_force_ratio': -0.015693692585777876, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-09-23', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -22.357364083471563, 'flow_continuity_3d': -1, 'flow_continuity_5d': 1, 'flow_continuity_10d': -2, 'positive_flow_days_5d': 3, 'positive_flow_days_10d': 4, 'flow_reversal_1d': False, 'flow_reversal_3d': True, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
