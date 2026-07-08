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
- snapshot_id: cnsvdata-2026-07-08-cfbe1e187b83
- latest_trade_date: 2026-07-08
- generated_at: 2026-07-08 23:33:08
- file_count: 14

## Loaded Data
- daily_rows: 3852
- one_min_rows: 5061
- moneyflow_rows: 3852
- latest_trade_date: 2026-07-08

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-07-08', 'latest_open': 37.32, 'latest_high': 37.32, 'latest_low': 35.46, 'latest_close': 35.98, 'latest_pre_close': 37.33, 'latest_pct_chg': -3.6164, 'latest_volume': 1381368.89, 'latest_amount': 5015752.7, 'ma5': 36.492, 'ma10': 35.37599999999999, 'ma20': 35.592, 'ma60': 36.95116666666667, 'ret_1d': -0.03616394320921512, 'ret_3d': -0.03149394347240919, 'ret_5d': 0.02244955953395844, 'ret_10d': 0.017821782178217616, 'ret_20d': 0.03838383838383841, 'ret_60d': 0.11635122556624267, 'volume_ma5': 1376682.558, 'volume_ma20': 1117587.517, 'volume_ratio_5d': 1.0053263438712174, 'volume_ratio_20d': 1.26562450714324, 'amount_ma5': 5034052.8912, 'amount_ma20': 3994075.9650499998, 'amount_ratio_5d': 1.0056807769995342, 'amount_ratio_20d': 1.288890438125125, 'price_position_20d': 0.5864661654135334, 'price_position_60d': 0.3351206434316352, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-07-08', 'latest_intraday_open': 37.32, 'latest_intraday_high': 37.32, 'latest_intraday_low': 35.46, 'latest_intraday_close': 35.98, 'intraday_range_pct': 0.05169538632573651, 'close_position_in_day_range': 0.2795698924731162, 'morning_return': -0.010718113612004254, 'afternoon_return': -0.025460455037919938, 'last_30min_return': -0.008542298153761396, 'last_60min_return': -0.013976431899150543, 'morning_volume_ratio': 0.7111283720889356, 'afternoon_volume_ratio': 0.28887162791106435, 'last_30min_volume_ratio': 0.12104401019194808, 'last_60min_volume_ratio': 0.17440274769761174, 'intraday_volume_sum': 138136889.0, 'intraday_amount_sum': 5015752707.0, 'late_session_strength': False, 'late_session_weakness': True, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -18617.93, 'net_mf_ratio': -0.0037118915372362756, 'small_order_net': 144.89999999999418, 'medium_order_net': -932.9900000000198, 'large_order_net': 1058.229999999996, 'extra_large_order_net': -270.1399999999994, 'main_force_net': 788.0899999999965, 'main_force_ratio': 0.00015712297777360445, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-07-08', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'mixed', 'flow_strength_basic': 'mixed', 'flow_strength_score': -3.554768559462671, 'flow_continuity_3d': -1, 'flow_continuity_5d': -1, 'flow_continuity_10d': -4, 'positive_flow_days_5d': 2, 'positive_flow_days_10d': 3, 'flow_reversal_1d': False, 'flow_reversal_3d': True, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'outflow_confirmed', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
