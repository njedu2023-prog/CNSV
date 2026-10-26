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
- snapshot_id: cnsvdata-2026-10-23-59bf937f511b
- latest_trade_date: 2026-10-23
- generated_at: 2026-10-23 22:53:57
- file_count: 14

## Loaded Data
- daily_rows: 3923
- one_min_rows: 22172
- moneyflow_rows: 3923
- latest_trade_date: 2026-10-23

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-10-23', 'latest_open': 33.94, 'latest_high': 35.1, 'latest_low': 33.66, 'latest_close': 35.1, 'latest_pre_close': 34.07, 'latest_pct_chg': 3.0232, 'latest_volume': 923094.75, 'latest_amount': 3176323.911, 'ma5': 35.154, 'ma10': 36.225, 'ma20': 37.70100000000001, 'ma60': 36.11233333333334, 'ret_1d': 0.01650738488271064, 'ret_3d': -0.0034071550255535543, 'ret_5d': -0.018730779983226253, 'ret_10d': -0.08925791385573423, 'ret_20d': -0.09907597535934287, 'ret_60d': 0.03969194312796209, 'volume_ma5': 691247.2, 'volume_ma20': 954765.477, 'volume_ratio_5d': 1.311324232603325, 'volume_ratio_20d': 0.9535365344983656, 'amount_ma5': 2418910.7096, 'amount_ma20': 3616936.2363999994, 'amount_ratio_5d': 1.2745141297199978, 'amount_ratio_20d': 0.8616017875217573, 'price_position_20d': 0.18532818532818587, 'price_position_60d': 0.2839366515837103, 'new_high_20d': False, 'new_low_20d': True, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-10-23', 'latest_intraday_open': 33.94, 'latest_intraday_high': 35.1, 'latest_intraday_low': 33.66, 'latest_intraday_close': 35.1, 'intraday_range_pct': 0.041025641025641164, 'close_position_in_day_range': 1.0, 'morning_return': 0.01591043017088989, 'afternoon_return': 0.017981438515081383, 'last_30min_return': 0.00659592773157458, 'last_60min_return': 0.010653613590555944, 'morning_volume_ratio': 0.569841644099915, 'afternoon_volume_ratio': 0.430158355900085, 'last_30min_volume_ratio': 0.13476426986503823, 'last_60min_volume_ratio': 0.22910459625081825, 'intraday_volume_sum': 92309475.0, 'intraday_amount_sum': 3176323908.0, 'late_session_strength': True, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': 273.35, 'net_mf_ratio': 8.605860348604732e-05, 'small_order_net': -15737.690000000002, 'medium_order_net': 5889.479999999996, 'large_order_net': 6329.860000000001, 'extra_large_order_net': 3518.3600000000006, 'main_force_net': 9848.220000000001, 'main_force_ratio': 0.003100508725163201, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-10-23', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'positive', 'flow_strength_basic': 'positive', 'flow_strength_score': 3.186567328649248, 'flow_continuity_3d': -1, 'flow_continuity_5d': -1, 'flow_continuity_10d': -4, 'positive_flow_days_5d': 2, 'positive_flow_days_10d': 3, 'flow_reversal_1d': True, 'flow_reversal_3d': True, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'inflow_confirmed', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
