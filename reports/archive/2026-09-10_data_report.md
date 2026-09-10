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
- snapshot_id: cnsvdata-2026-09-10-febf058c742a
- latest_trade_date: 2026-09-10
- generated_at: 2026-09-10 22:16:23
- file_count: 14

## Loaded Data
- daily_rows: 3898
- one_min_rows: 16147
- moneyflow_rows: 3898
- latest_trade_date: 2026-09-10

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-09-10', 'latest_open': 39.25, 'latest_high': 41.18, 'latest_low': 39.25, 'latest_close': 40.82, 'latest_pre_close': 39.53, 'latest_pct_chg': 3.2633, 'latest_volume': 1757402.21, 'latest_amount': 7144558.405, 'ma5': 39.056, 'ma10': 36.682, 'ma20': 35.17300000000001, 'ma60': 34.84916666666667, 'ret_1d': 0.03263344295471793, 'ret_3d': 0.06357477853048454, 'ret_5d': 0.18939393939393945, 'ret_10d': 0.18250289687137888, 'ret_20d': 0.2084073416222616, 'ret_60d': 0.09878869448183036, 'volume_ma5': 2028904.304, 'volume_ma20': 1013936.6545, 'volume_ratio_5d': 0.93528401458383, 'volume_ratio_20d': 1.8329481361442763, 'amount_ma5': 7784197.4054000005, 'amount_ma20': 3665624.39075, 'amount_ratio_5d': 1.0131126868143927, 'amount_ratio_20d': 2.089323073523891, 'price_position_20d': 0.9580908032596043, 'price_position_60d': 0.960352422907489, 'new_high_20d': True, 'new_low_20d': False, 'new_high_60d': True, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-09-10', 'latest_intraday_open': 39.25, 'latest_intraday_high': 41.18, 'latest_intraday_low': 39.25, 'latest_intraday_close': 40.82, 'intraday_range_pct': 0.04728074473297403, 'close_position_in_day_range': 0.8134715025906738, 'morning_return': 0.04040660736975843, 'afternoon_return': -0.002931118710307712, 'last_30min_return': -0.002199951112197396, 'last_60min_return': -0.002199951112197396, 'morning_volume_ratio': 0.742981124394967, 'afternoon_volume_ratio': 0.25701887560503295, 'last_30min_volume_ratio': 0.08734825706176846, 'last_60min_volume_ratio': 0.13889832311067823, 'intraday_volume_sum': 175740221.0, 'intraday_amount_sum': 7144558421.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': 45311.62, 'net_mf_ratio': 0.006342116255679206, 'small_order_net': -34716.95999999999, 'medium_order_net': 1897.679999999993, 'large_order_net': 30616.410000000003, 'extra_large_order_net': 2202.859999999986, 'main_force_net': 32819.26999999999, 'main_force_ratio': 0.0045936037106270936, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-09-10', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'positive', 'flow_strength_basic': 'positive', 'flow_strength_score': 10.9357199663063, 'flow_continuity_3d': 3, 'flow_continuity_5d': 3, 'flow_continuity_10d': 2, 'positive_flow_days_5d': 4, 'positive_flow_days_10d': 6, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
