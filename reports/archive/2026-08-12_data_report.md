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
- snapshot_id: cnsvdata-2026-08-12-e8147ed2cad7
- latest_trade_date: 2026-08-12
- generated_at: 2026-08-12 20:05:52
- file_count: 14

## Loaded Data
- daily_rows: 3877
- one_min_rows: 11086
- moneyflow_rows: 3877
- latest_trade_date: 2026-08-12

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-08-12', 'latest_open': 33.76, 'latest_high': 33.94, 'latest_low': 33.51, 'latest_close': 33.89, 'latest_pre_close': 33.97, 'latest_pct_chg': -0.2355, 'latest_volume': 618362.26, 'latest_amount': 2086291.975, 'ma5': 34.488, 'ma10': 34.702999999999996, 'ma20': 33.99650000000001, 'ma60': 35.41116666666666, 'ret_1d': -0.0023550191345304006, 'ret_3d': -0.027546628407460583, 'ret_5d': -0.037215909090909105, 'ret_10d': -0.024186582205585894, 'ret_20d': -0.01224132905858355, 'ret_60d': -0.0960256068284876, 'volume_ma5': 814221.574, 'volume_ma20': 905381.3365, 'volume_ratio_5d': 0.6953813789130239, 'volume_ratio_20d': 0.6690611222424601, 'amount_ma5': 2817524.4063999997, 'amount_ma20': 3071878.4619, 'amount_ratio_5d': 0.6743167854728691, 'amount_ratio_20d': 0.6650670281298968, 'price_position_20d': 0.549079754601227, 'price_position_60d': 0.2146282973621103, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-08-12', 'latest_intraday_open': 33.76, 'latest_intraday_high': 33.94, 'latest_intraday_low': 33.51, 'latest_intraday_close': 33.89, 'intraday_range_pct': 0.01268810858660371, 'close_position_in_day_range': 0.8837209302325647, 'morning_return': 0.0002958579881657819, 'afternoon_return': 0.00236616385684707, 'last_30min_return': 0.0, 'last_60min_return': -0.0002949852507374562, 'morning_volume_ratio': 0.6341946547643448, 'afternoon_volume_ratio': 0.3658053452356552, 'last_30min_volume_ratio': 0.12510322023857018, 'last_60min_volume_ratio': 0.195827976306316, 'intraday_volume_sum': 61836226.0, 'intraday_amount_sum': 2086291967.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': -11720.78, 'net_mf_ratio': -0.0056179960141964315, 'small_order_net': 16145.620000000003, 'medium_order_net': -990.1100000000006, 'large_order_net': -4507.590000000004, 'extra_large_order_net': -10647.920000000006, 'main_force_net': -15155.51000000001, 'main_force_ratio': -0.007264328378581818, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-08-12', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -12.882324392778248, 'flow_continuity_3d': -3, 'flow_continuity_5d': -5, 'flow_continuity_10d': -6, 'positive_flow_days_5d': 0, 'positive_flow_days_10d': 2, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
