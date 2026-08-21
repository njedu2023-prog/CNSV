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
- snapshot_id: cnsvdata-2026-08-21-707c3ab56104
- latest_trade_date: 2026-08-21
- generated_at: 2026-08-21 20:05:53
- file_count: 14

## Loaded Data
- daily_rows: 3884
- one_min_rows: 12773
- moneyflow_rows: 3884
- latest_trade_date: 2026-08-21

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-08-21', 'latest_open': 32.83, 'latest_high': 33.79, 'latest_low': 32.59, 'latest_close': 33.68, 'latest_pre_close': 32.99, 'latest_pct_chg': 2.0915, 'latest_volume': 760206.95, 'latest_amount': 2543460.716, 'ma5': 33.39, 'ma10': 33.684, 'ma20': 34.146499999999996, 'ma60': 34.842166666666664, 'ret_1d': 0.020915428917853918, 'ret_3d': 0.005673335323977291, 'ret_5d': 0.007779772591262724, 'ret_10d': -0.03357245337159254, 'ret_20d': 0.018753781004234638, 'ret_60d': -0.11786275536930335, 'volume_ma5': 609849.11, 'volume_ma20': 774600.054, 'volume_ratio_5d': 1.2637170099026664, 'volume_ratio_20d': 0.9792495800190301, 'amount_ma5': 2033598.2963999999, 'amount_ma20': 2648207.3997500003, 'amount_ratio_5d': 1.2663388151351727, 'amount_ratio_20d': 0.9584820699738626, 'price_position_20d': 0.39350180505415083, 'price_position_60d': 0.2484276729559746, 'new_high_20d': False, 'new_low_20d': True, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-08-21', 'latest_intraday_open': 32.83, 'latest_intraday_high': 33.79, 'latest_intraday_low': 32.59, 'latest_intraday_close': 33.68, 'intraday_range_pct': 0.03562945368171009, 'close_position_in_day_range': 0.9083333333333334, 'morning_return': 0.02436795613767906, 'afternoon_return': 0.0014867677668746193, 'last_30min_return': 0.0005941770647654998, 'last_60min_return': 0.0008915304606240682, 'morning_volume_ratio': 0.6715307719825503, 'afternoon_volume_ratio': 0.3284692280174497, 'last_30min_volume_ratio': 0.1190359677716706, 'last_60min_volume_ratio': 0.18635545228835385, 'intraday_volume_sum': 76020695.0, 'intraday_amount_sum': 2543460712.0, 'late_session_strength': True, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': 55856.19, 'net_mf_ratio': 0.02196070481789977, 'small_order_net': -11784.980000000003, 'medium_order_net': -14469.350000000006, 'large_order_net': 9107.210000000006, 'extra_large_order_net': 17147.119999999995, 'main_force_net': 26254.33, 'main_force_ratio': 0.010322286416630466, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-08-21', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'positive', 'flow_strength_basic': 'positive', 'flow_strength_score': 32.28299123453023, 'flow_continuity_3d': -1, 'flow_continuity_5d': -1, 'flow_continuity_10d': -6, 'positive_flow_days_5d': 2, 'positive_flow_days_10d': 2, 'flow_reversal_1d': True, 'flow_reversal_3d': True, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'inflow_confirmed', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
