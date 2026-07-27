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
- snapshot_id: cnsvdata-2026-07-24-264425c99a01
- latest_trade_date: 2026-07-24
- generated_at: 2026-07-24 20:04:47
- file_count: 14

## Loaded Data
- daily_rows: 3864
- one_min_rows: 7953
- moneyflow_rows: 3864
- latest_trade_date: 2026-07-24

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-07-24', 'latest_open': 33.7, 'latest_high': 33.87, 'latest_low': 32.93, 'latest_close': 33.06, 'latest_pre_close': 33.76, 'latest_pct_chg': -2.0735, 'latest_volume': 794522.46, 'latest_amount': 2651994.948, 'ma5': 33.162, 'ma10': 33.344, 'ma20': 34.5785, 'ma60': 36.71583333333333, 'ret_1d': -0.020734597156398027, 'ret_3d': 0.0030339805825243538, 'ret_5d': 0.02226345083487935, 'ret_10d': -0.10745140388768892, 'ret_20d': -0.01017964071856281, 'ret_60d': -0.139286644103098, 'volume_ma5': 975391.538, 'volume_ma20': 1242289.013, 'volume_ratio_5d': 0.7910428932969117, 'volume_ratio_20d': 0.628781873354499, 'amount_ma5': 3232410.2368, 'amount_ma20': 4326294.4743, 'amount_ratio_5d': 0.8007272259099044, 'amount_ratio_20d': 0.6026653796281497, 'price_position_20d': 0.15584415584415606, 'price_position_60d': 0.08480565371024743, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-07-24', 'latest_intraday_open': 33.7, 'latest_intraday_high': 33.87, 'latest_intraday_low': 32.93, 'latest_intraday_close': 33.06, 'intraday_range_pct': 0.028433151845129997, 'close_position_in_day_range': 0.1382978723404286, 'morning_return': -0.005934718100890302, 'afternoon_return': -0.013134328358208935, 'last_30min_return': -0.004516711833784992, 'last_60min_return': -0.0039168424224163, 'morning_volume_ratio': 0.5088198261884251, 'afternoon_volume_ratio': 0.4911801738115748, 'last_30min_volume_ratio': 0.198949177597824, 'last_60min_volume_ratio': 0.2930917396595686, 'intraday_volume_sum': 79452246.0, 'intraday_amount_sum': 2651994929.0, 'late_session_strength': False, 'late_session_weakness': True, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -50760.59, 'net_mf_ratio': -0.01914053042909492, 'small_order_net': -2370.6800000000076, 'medium_order_net': -155.25999999999476, 'large_order_net': 509.8399999999965, 'extra_large_order_net': 2016.0900000000001, 'main_force_net': 2525.9299999999967, 'main_force_ratio': 0.0009524641070319252, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-07-24', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'mixed', 'flow_strength_basic': 'mixed', 'flow_strength_score': -18.188066322062994, 'flow_continuity_3d': -1, 'flow_continuity_5d': -1, 'flow_continuity_10d': -4, 'positive_flow_days_5d': 2, 'positive_flow_days_10d': 3, 'flow_reversal_1d': True, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
