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
- snapshot_id: cnsvdata-2026-07-09-5aef277f9b1f
- latest_trade_date: 2026-07-09
- generated_at: 2026-07-10 00:09:27
- file_count: 14

## Loaded Data
- daily_rows: 3853
- one_min_rows: 5302
- moneyflow_rows: 3853
- latest_trade_date: 2026-07-09

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-07-09', 'latest_open': 35.99, 'latest_high': 36.63, 'latest_low': 35.0, 'latest_close': 36.06, 'latest_pre_close': 35.98, 'latest_pct_chg': 0.2223, 'latest_volume': 1146794.05, 'latest_amount': 4081272.787, 'ma5': 36.832, 'ma10': 35.449, 'ma20': 35.641999999999996, 'ma60': 37.008, 'ret_1d': 0.0022234574763759785, 'ret_3d': -0.041976620616365534, 'ret_5d': 0.049476135040745106, 'ret_10d': 0.020662326634588224, 'ret_20d': 0.02852253280091266, 'ret_60d': 0.10444104134762644, 'volume_ma5': 1381152.7839999998, 'volume_ma20': 1131944.4105, 'volume_ratio_5d': 0.8330126965987174, 'volume_ratio_20d': 1.0261335533510616, 'amount_ma5': 5062554.9188, 'amount_ma20': 4049072.42805, 'amount_ratio_5d': 0.8107329968929111, 'amount_ratio_20d': 1.021831538186307, 'price_position_20d': 0.6015037593984968, 'price_position_60d': 0.34226988382484397, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-07-09', 'latest_intraday_open': 35.99, 'latest_intraday_high': 36.63, 'latest_intraday_low': 35.0, 'latest_intraday_close': 36.06, 'intraday_range_pct': 0.04520244037714927, 'close_position_in_day_range': 0.650306748466258, 'morning_return': -0.017504862461795057, 'afternoon_return': 0.01979638009049789, 'last_30min_return': 0.009518477043673146, 'last_60min_return': 0.012068481616615223, 'morning_volume_ratio': 0.6367538617766634, 'afternoon_volume_ratio': 0.3632461382233366, 'last_30min_volume_ratio': 0.1322396641314977, 'last_60min_volume_ratio': 0.20997201720744887, 'intraday_volume_sum': 114679405.0, 'intraday_amount_sum': 4081272793.0, 'late_session_strength': True, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': -22502.6, 'net_mf_ratio': -0.005513623120629697, 'small_order_net': 9096.050000000017, 'medium_order_net': -1406.7699999999895, 'large_order_net': -6807.900000000009, 'extra_large_order_net': -881.3799999999974, 'main_force_net': -7689.280000000006, 'main_force_ratio': -0.0018840397104777026, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-07-09', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -7.397662831107398, 'flow_continuity_3d': -3, 'flow_continuity_5d': -1, 'flow_continuity_10d': -4, 'positive_flow_days_5d': 2, 'positive_flow_days_10d': 3, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': False, 'price_flow_divergence': True, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
