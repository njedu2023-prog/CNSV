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
- snapshot_id: cnsvdata-2026-09-16-21c3b9e055f6
- latest_trade_date: 2026-09-16
- generated_at: 2026-09-16 22:48:00
- file_count: 14

## Loaded Data
- daily_rows: 3902
- one_min_rows: 17111
- moneyflow_rows: 3902
- latest_trade_date: 2026-09-16

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-09-16', 'latest_open': 38.25, 'latest_high': 38.38, 'latest_low': 37.41, 'latest_close': 37.79, 'latest_pre_close': 38.16, 'latest_pct_chg': -0.9696, 'latest_volume': 899263.73, 'latest_amount': 3394111.546, 'ma5': 39.099999999999994, 'ma10': 38.428000000000004, 'ma20': 36.221999999999994, 'ma60': 35.016666666666666, 'ret_1d': -0.009696016771488458, 'ret_3d': -0.049308176100628986, 'ret_5d': -0.0440172021249684, 'ret_10d': 0.1137636310050103, 'ret_20d': 0.14031382015691007, 'ret_60d': 0.06902404526166905, 'volume_ma5': 1434284.3280000002, 'volume_ma20': 1163047.451, 'volume_ratio_5d': 0.602263492996032, 'volume_ratio_20d': 0.7818567359215661, 'amount_ma5': 5654265.961000001, 'amount_ma20': 4315576.2275, 'amount_ratio_5d': 0.5739947329615458, 'amount_ratio_20d': 0.7982241741599151, 'price_position_20d': 0.6053550640279393, 'price_position_60d': 0.6266519823788544, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-09-16', 'latest_intraday_open': 38.25, 'latest_intraday_high': 38.38, 'latest_intraday_low': 37.41, 'latest_intraday_close': 37.79, 'intraday_range_pct': 0.025668166181529662, 'close_position_in_day_range': 0.39175257731958785, 'morning_return': -0.01594771241830062, 'afternoon_return': 0.00398512221041436, 'last_30min_return': 0.0023872679045091605, 'last_60min_return': 0.000529520783690618, 'morning_volume_ratio': 0.6541247249013368, 'afternoon_volume_ratio': 0.3458752750986632, 'last_30min_volume_ratio': 0.11327600191325408, 'last_60min_volume_ratio': 0.1720921069506495, 'intraday_volume_sum': 89926373.0, 'intraday_amount_sum': 3394111551.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': -7991.73, 'net_mf_ratio': -0.0023545867281287046, 'small_order_net': 16559.729999999996, 'medium_order_net': 5183.5899999999965, 'large_order_net': -3486.3699999999953, 'extra_large_order_net': -18256.959999999992, 'main_force_net': -21743.329999999987, 'main_force_ratio': -0.006406191931324342, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-09-16', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -8.760778659453045, 'flow_continuity_3d': -3, 'flow_continuity_5d': -3, 'flow_continuity_10d': 0, 'positive_flow_days_5d': 1, 'positive_flow_days_10d': 5, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
