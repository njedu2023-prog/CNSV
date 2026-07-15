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
- snapshot_id: cnsvdata-2026-07-14-39131a8e93f4
- latest_trade_date: 2026-07-14
- generated_at: 2026-07-15 14:57:29
- file_count: 14

## Loaded Data
- daily_rows: 3856
- one_min_rows: 6025
- moneyflow_rows: 3856
- latest_trade_date: 2026-07-14

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-07-14', 'latest_open': 34.16, 'latest_high': 34.68, 'latest_low': 33.08, 'latest_close': 33.77, 'latest_pre_close': 34.21, 'latest_pct_chg': -1.2862, 'latest_volume': 1508390.78, 'latest_amount': 5099797.473, 'ma5': 35.412, 'ma10': 35.873, 'ma20': 35.6305, 'ma60': 37.118833333333335, 'ret_1d': -0.012861736334405127, 'ret_3d': -0.06350526899611753, 'ret_5d': -0.0953656576480042, 'ret_10d': -0.0005918910920389431, 'ret_20d': -0.05959342801448042, 'ret_60d': 0.03240599205136041, 'volume_ma5': 1629847.172, 'volume_ma20': 1272190.8085, 'volume_ratio_5d': 0.9902903018049729, 'volume_ratio_20d': 1.2015956156130407, 'amount_ma5': 5784638.7872, 'amount_ma20': 4543805.80035, 'amount_ratio_5d': 0.92833297382636, 'amount_ratio_20d': 1.1336138808222598, 'price_position_20d': 0.16851851851851923, 'price_position_60d': 0.1368515205724509, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-07-14', 'latest_intraday_open': 34.16, 'latest_intraday_high': 34.68, 'latest_intraday_low': 33.08, 'latest_intraday_close': 33.77, 'intraday_range_pct': 0.04737933076695296, 'close_position_in_day_range': 0.43125000000000263, 'morning_return': -0.02488290398126447, 'afternoon_return': 0.013809666766736672, 'last_30min_return': 0.004162949747249511, 'last_60min_return': 0.00805970149253743, 'morning_volume_ratio': 0.7083547673236242, 'afternoon_volume_ratio': 0.2916452326763758, 'last_30min_volume_ratio': 0.087798852761484, 'last_60min_volume_ratio': 0.13921938716703108, 'intraday_volume_sum': 150839078.0, 'intraday_amount_sum': 5099797480.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': -55285.99, 'net_mf_ratio': -0.010840820697822247, 'small_order_net': 14893.320000000007, 'medium_order_net': 143.86999999999534, 'large_order_net': -3225.949999999997, 'extra_large_order_net': -11811.25, 'main_force_net': -15037.199999999997, 'main_force_ratio': -0.0029485876801209976, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-07-14', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -13.789408377943245, 'flow_continuity_3d': -1, 'flow_continuity_5d': -3, 'flow_continuity_10d': -2, 'positive_flow_days_5d': 1, 'positive_flow_days_10d': 4, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
