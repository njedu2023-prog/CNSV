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
- snapshot_id: cnsvdata-2026-09-07-af99539c6b66
- latest_trade_date: 2026-09-07
- generated_at: 2026-09-07 23:44:35
- file_count: 14

## Loaded Data
- daily_rows: 3895
- one_min_rows: 15424
- moneyflow_rows: 3895
- latest_trade_date: 2026-09-07

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-09-07', 'latest_open': 37.74, 'latest_high': 38.82, 'latest_low': 37.5, 'latest_close': 38.38, 'latest_pre_close': 37.47, 'latest_pct_chg': 2.4286, 'latest_volume': 2319545.54, 'latest_amount': 8847109.788, 'ma5': 35.706, 'ma10': 34.986000000000004, 'ma20': 34.2835, 'ma60': 34.67616666666667, 'ret_1d': 0.024286095543101238, 'ret_3d': 0.131152372531683, 'ret_5d': 0.12617370892018798, 'ret_10d': 0.13550295857988193, 'ret_20d': 0.10192362905541219, 'ret_60d': 0.10002866150759537, 'volume_ma5': 1646285.128, 'volume_ma20': 905244.7494999999, 'volume_ratio_5d': 1.7054948142049473, 'volume_ratio_20d': 2.7940160549514674, 'amount_ma5': 5989844.0923999995, 'amount_ma20': 3169361.4184499998, 'amount_ratio_5d': 1.8334535110480172, 'amount_ratio_20d': 3.082856155280369, 'price_position_20d': 0.9293739967897274, 'price_position_60d': 0.9345238095238099, 'new_high_20d': True, 'new_low_20d': False, 'new_high_60d': True, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-09-07', 'latest_intraday_open': 37.74, 'latest_intraday_high': 38.82, 'latest_intraday_low': 37.5, 'latest_intraday_close': 38.38, 'intraday_range_pct': 0.03439291297550808, 'close_position_in_day_range': 0.6666666666666684, 'morning_return': 0.013793103448275668, 'afternoon_return': 0.00418628990057579, 'last_30min_return': 0.0018271991647089703, 'last_60min_return': 0.003136434918975528, 'morning_volume_ratio': 0.7093909395717232, 'afternoon_volume_ratio': 0.29060906042827683, 'last_30min_volume_ratio': 0.08881596694152424, 'last_60min_volume_ratio': 0.144698939603488, 'intraday_volume_sum': 231954554.0, 'intraday_amount_sum': 8847109760.0, 'late_session_strength': True, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': -2839.97, 'net_mf_ratio': -0.0003210053981529724, 'small_order_net': 90521.79999999999, 'medium_order_net': 5254.25999999998, 'large_order_net': -52311.600000000035, 'extra_large_order_net': -43464.47, 'main_force_net': -95776.07000000004, 'main_force_ratio': -0.010825690230487284, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-09-07', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -11.146695628640257, 'flow_continuity_3d': 1, 'flow_continuity_5d': 1, 'flow_continuity_10d': 0, 'positive_flow_days_5d': 3, 'positive_flow_days_10d': 5, 'flow_reversal_1d': True, 'flow_reversal_3d': True, 'price_flow_confirm': False, 'price_flow_divergence': True, 'volume_flow_confirm': 'outflow_confirmed', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
