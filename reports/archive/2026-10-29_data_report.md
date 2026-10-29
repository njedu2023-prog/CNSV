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
- snapshot_id: cnsvdata-2026-10-27-1be584d823cc
- latest_trade_date: 2026-10-27
- generated_at: 2026-10-27 23:50:01
- file_count: 14

## Loaded Data
- daily_rows: 3925
- one_min_rows: 22654
- moneyflow_rows: 3925
- latest_trade_date: 2026-10-27

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-10-27', 'latest_open': 35.0, 'latest_high': 35.23, 'latest_low': 34.59, 'latest_close': 34.64, 'latest_pre_close': 35.17, 'latest_pct_chg': -1.507, 'latest_volume': 549304.65, 'latest_amount': 1921836.014, 'ma5': 34.86, 'ma10': 35.491, 'ma20': 37.167, 'ma60': 36.166000000000004, 'ret_1d': -0.015069661643446142, 'ret_3d': 0.0031856356791195584, 'ret_5d': -0.016467915956842605, 'ret_10d': -0.11519795657726684, 'ret_20d': -0.1555338859093126, 'ret_60d': 0.03310468237399333, 'volume_ma5': 672780.7999999999, 'volume_ma20': 894481.9610000001, 'volume_ratio_5d': 0.7742680947099722, 'volume_ratio_20d': 0.5887496397857783, 'amount_ma5': 2334808.8886, 'amount_ma20': 3345101.21285, 'amount_ratio_5d': 0.7792632542981126, 'amount_ratio_20d': 0.5466490806638276, 'price_position_20d': 0.1261261261261266, 'price_position_60d': 0.23190045248868757, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-10-27', 'latest_intraday_open': 35.0, 'latest_intraday_high': 35.23, 'latest_intraday_low': 34.59, 'latest_intraday_close': 34.64, 'intraday_range_pct': 0.018475750577367018, 'close_position_in_day_range': 0.07812499999999635, 'morning_return': 0.003714285714285781, 'afternoon_return': -0.013948192428124173, 'last_30min_return': -0.009719839908519101, 'last_60min_return': -0.014228799089356814, 'morning_volume_ratio': 0.47184983779037737, 'afternoon_volume_ratio': 0.5281501622096226, 'last_30min_volume_ratio': 0.21558606867791852, 'last_60min_volume_ratio': 0.3377766964106348, 'intraday_volume_sum': 54930465.0, 'intraday_amount_sum': 1921836009.0, 'late_session_strength': False, 'late_session_weakness': True, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -14122.07, 'net_mf_ratio': -0.007348218004618994, 'small_order_net': -14525.459999999992, 'medium_order_net': 13342.840000000004, 'large_order_net': 3561.8199999999997, 'extra_large_order_net': -2379.2000000000007, 'main_force_net': 1182.619999999999, 'main_force_ratio': 0.0006153594746820053, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-10-27', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'mixed', 'flow_strength_basic': 'mixed', 'flow_strength_score': -6.732858529936988, 'flow_continuity_3d': -1, 'flow_continuity_5d': -3, 'flow_continuity_10d': -6, 'positive_flow_days_5d': 1, 'positive_flow_days_10d': 2, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
