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
- snapshot_id: cnsvdata-2026-06-18-4c7619afdb56
- latest_trade_date: 2026-06-18
- generated_at: 2026-06-21 13:31:14
- file_count: 14

## Loaded Data
- daily_rows: 3839
- one_min_rows: 1928
- moneyflow_rows: 3839
- latest_trade_date: 2026-06-18

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-06-18', 'latest_open': 37.02, 'latest_high': 37.43, 'latest_low': 35.72, 'latest_close': 36.14, 'latest_pre_close': 37.15, 'latest_pct_chg': -2.7187, 'latest_volume': 1182191.19, 'latest_amount': 4313475.328, 'ma5': 36.016, 'ma10': 35.501999999999995, 'ma20': 36.49999999999999, 'ma60': 36.02283333333333, 'ret_1d': -0.02718707940780618, 'ret_3d': 0.006404901141743302, 'ret_5d': 0.049056603773584895, 'ret_10d': -0.020330712930333394, 'ret_20d': -0.05885416666666665, 'ret_60d': 0.09019607843137267, 'volume_ma5': 1060891.4300000002, 'volume_ma20': 902787.2265000001, 'volume_ratio_5d': 1.2478544833680014, 'volume_ratio_20d': 1.3069293150292616, 'amount_ma5': 3824186.1082, 'amount_ma20': 3304855.1599999997, 'amount_ratio_5d': 1.2744407792473547, 'amount_ratio_20d': 1.2955382364879384, 'price_position_20d': 0.3646864686468647, 'price_position_60d': 0.45752608047690013, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-06-18', 'latest_intraday_open': 37.02, 'latest_intraday_high': 37.43, 'latest_intraday_low': 35.72, 'latest_intraday_close': 36.14, 'intraday_range_pct': 0.04731599335915885, 'close_position_in_day_range': 0.24561403508772017, 'morning_return': -0.02674230145867107, 'afternoon_return': 0.0030530113794060565, 'last_30min_return': -0.0024841291747169647, 'last_60min_return': -0.0024841291747169647, 'morning_volume_ratio': 0.6327600529657136, 'afternoon_volume_ratio': 0.3672399470342864, 'last_30min_volume_ratio': 0.11951319819935387, 'last_60min_volume_ratio': 0.18897935620717998, 'intraday_volume_sum': 118219119.0, 'intraday_amount_sum': 4313475325.0, 'late_session_strength': False, 'late_session_weakness': True, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -57131.22, 'net_mf_ratio': -0.013244823641193667, 'small_order_net': -6728.140000000014, 'medium_order_net': 744.7200000000012, 'large_order_net': -5713.25, 'extra_large_order_net': 11696.669999999998, 'main_force_net': 5983.419999999998, 'main_force_ratio': 0.0013871459890265074, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-06-18', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'mixed', 'flow_strength_basic': 'mixed', 'flow_strength_score': -11.857677652167158, 'flow_continuity_3d': -1, 'flow_continuity_5d': 1, 'flow_continuity_10d': -4, 'positive_flow_days_5d': 3, 'positive_flow_days_10d': 3, 'flow_reversal_1d': True, 'flow_reversal_3d': True, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'outflow_confirmed', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
