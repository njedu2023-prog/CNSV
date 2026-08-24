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
- snapshot_id: cnsvdata-2026-08-24-2dd0ae9dd0a6
- latest_trade_date: 2026-08-24
- generated_at: 2026-08-24 20:05:44
- file_count: 14

## Loaded Data
- daily_rows: 3885
- one_min_rows: 13014
- moneyflow_rows: 3885
- latest_trade_date: 2026-08-24

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-08-24', 'latest_open': 33.59, 'latest_high': 34.39, 'latest_low': 33.58, 'latest_close': 33.8, 'latest_pre_close': 33.68, 'latest_pct_chg': 0.3563, 'latest_volume': 623120.06, 'latest_amount': 2113705.587, 'ma5': 33.42, 'ma10': 33.581, 'ma20': 34.15999999999999, 'ma60': 34.782500000000006, 'ret_1d': 0.0035629453681709222, 'ret_3d': 0.019915509957754818, 'ret_5d': 0.004457652303120341, 'ret_10d': -0.029572207866781497, 'ret_20d': 0.008052490307187465, 'ret_60d': -0.09577314071696108, 'volume_ma5': 619840.7440000001, 'volume_ma20': 774677.261, 'volume_ratio_5d': 1.0217610385624734, 'volume_ratio_20d': 0.8044410231863992, 'amount_ma5': 2072478.1323999998, 'amount_ma20': 2650356.5042, 'amount_ratio_5d': 1.0393918950177186, 'amount_ratio_20d': 0.7981646706370282, 'price_position_20d': 0.4368231046931392, 'price_position_60d': 0.2759740259740254, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-08-24', 'latest_intraday_open': 33.59, 'latest_intraday_high': 34.39, 'latest_intraday_low': 33.58, 'latest_intraday_close': 33.8, 'intraday_range_pct': 0.023964497041420188, 'close_position_in_day_range': 0.27160493827160276, 'morning_return': 0.010419767788031997, 'afternoon_return': -0.004124926340601132, 'last_30min_return': 0.0029673590504448732, 'last_60min_return': 0.0029673590504448732, 'morning_volume_ratio': 0.6967257160682646, 'afternoon_volume_ratio': 0.3032742839317354, 'last_30min_volume_ratio': 0.10388715458783336, 'last_60min_volume_ratio': 0.18174672470021266, 'intraday_volume_sum': 62312006.0, 'intraday_amount_sum': 2113705582.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -15444.99, 'net_mf_ratio': -0.007307067784175753, 'small_order_net': -2111.290000000001, 'medium_order_net': 6375.07, 'large_order_net': -1900.8500000000058, 'extra_large_order_net': -2362.9300000000003, 'main_force_net': -4263.780000000006, 'main_force_ratio': -0.002017206192869852, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-08-24', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -9.324273977045605, 'flow_continuity_3d': -1, 'flow_continuity_5d': -3, 'flow_continuity_10d': -6, 'positive_flow_days_5d': 1, 'positive_flow_days_10d': 2, 'flow_reversal_1d': True, 'flow_reversal_3d': True, 'price_flow_confirm': False, 'price_flow_divergence': True, 'volume_flow_confirm': 'outflow_confirmed', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
