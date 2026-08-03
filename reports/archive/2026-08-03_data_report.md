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
- snapshot_id: cnsvdata-2026-08-03-51ed10774c34
- latest_trade_date: 2026-08-03
- generated_at: 2026-08-03 21:15:53
- file_count: 14

## Loaded Data
- daily_rows: 3870
- one_min_rows: 9399
- moneyflow_rows: 3870
- latest_trade_date: 2026-08-03

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-08-03', 'latest_open': 35.02, 'latest_high': 35.18, 'latest_low': 34.62, 'latest_close': 35.1, 'latest_pre_close': 35.18, 'latest_pct_chg': -0.2274, 'latest_volume': 647688.47, 'latest_amount': 2259131.75, 'ma5': 34.626, 'ma10': 33.946000000000005, 'ma20': 34.3255, 'ma60': 36.040499999999994, 'ret_1d': -0.0022740193291642674, 'ret_3d': 0.010653613590555944, 'ret_5d': 0.046823739934387154, 'ret_10d': 0.0633141472281129, 'ret_20d': -0.06748140276301806, 'ret_60d': -0.1470230862697448, 'volume_ma5': 925862.524, 'volume_ma20': 1120420.3285, 'volume_ratio_5d': 0.703519790744181, 'volume_ratio_20d': 0.5563916253809129, 'amount_ma5': 3183961.8811999997, 'amount_ma20': 3861425.6799500003, 'amount_ratio_5d': 0.7180325922289427, 'amount_ratio_20d': 0.5598499769072818, 'price_position_20d': 0.4870129870129873, 'price_position_60d': 0.30181086519114697, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-08-03', 'latest_intraday_open': 35.02, 'latest_intraday_high': 35.18, 'latest_intraday_low': 34.62, 'latest_intraday_close': 35.1, 'intraday_range_pct': 0.015954415954416018, 'close_position_in_day_range': 0.8571428571428608, 'morning_return': -0.008280982295831185, 'afternoon_return': 0.010653613590555944, 'last_30min_return': 0.0008554319931566301, 'last_60min_return': 0.005442566599828336, 'morning_volume_ratio': 0.5949324063156474, 'afternoon_volume_ratio': 0.4050675936843526, 'last_30min_volume_ratio': 0.12056268347651765, 'last_60min_volume_ratio': 0.2429274987711299, 'intraday_volume_sum': 64768847.0, 'intraday_amount_sum': 2259131756.0, 'late_session_strength': True, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': -18080.99, 'net_mf_ratio': -0.008003512853998002, 'small_order_net': -1694.4700000000012, 'medium_order_net': 2170.3600000000006, 'large_order_net': -1669.25, 'extra_large_order_net': 1193.3600000000006, 'main_force_net': -475.8899999999994, 'main_force_ratio': -0.0002106517249381314, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-08-03', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -8.214164578936133, 'flow_continuity_3d': -1, 'flow_continuity_5d': -1, 'flow_continuity_10d': -2, 'positive_flow_days_5d': 2, 'positive_flow_days_10d': 4, 'flow_reversal_1d': True, 'flow_reversal_3d': True, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
