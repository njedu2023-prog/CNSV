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
- snapshot_id: cnsvdata-2026-08-05-7d4d4e979f11
- latest_trade_date: 2026-08-05
- generated_at: 2026-08-05 20:06:04
- file_count: 14

## Loaded Data
- daily_rows: 3872
- one_min_rows: 9881
- moneyflow_rows: 3872
- latest_trade_date: 2026-08-05

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-08-05', 'latest_open': 34.59, 'latest_high': 35.36, 'latest_low': 34.2, 'latest_close': 35.2, 'latest_pre_close': 34.48, 'latest_pct_chg': 2.0882, 'latest_volume': 993463.9, 'latest_amount': 3468342.506, 'ma5': 34.91799999999999, 'ma10': 34.316, 'ma20': 34.144, 'ma60': 35.8405, 'ret_1d': 0.02088167053364276, 'ret_3d': 0.0005685048322912056, 'ret_5d': 0.013532968615030505, 'ret_10d': 0.06602059357964873, 'ret_20d': -0.021678710394663514, 'ret_60d': -0.1308641975308641, 'volume_ma5': 831758.564, 'volume_ma20': 1089979.9384999997, 'volume_ratio_5d': 1.0958050935423034, 'volume_ratio_20d': 0.8955166031710456, 'amount_ma5': 2892356.356, 'amount_ma20': 3732270.5365500003, 'amount_ratio_5d': 1.104942884847963, 'amount_ratio_20d': 0.9104118902262575, 'price_position_20d': 0.5032467532467537, 'price_position_60d': 0.3118712273641853, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-08-05', 'latest_intraday_open': 34.59, 'latest_intraday_high': 35.36, 'latest_intraday_low': 34.2, 'latest_intraday_close': 35.2, 'intraday_range_pct': 0.032954545454545354, 'close_position_in_day_range': 0.8620689655172439, 'morning_return': 0.012720439433362207, 'afternoon_return': 0.0048529831572938775, 'last_30min_return': 0.0017074558907228532, 'last_60min_return': 0.0, 'morning_volume_ratio': 0.5593048323144908, 'afternoon_volume_ratio': 0.44069516768550926, 'last_30min_volume_ratio': 0.10821859757561397, 'last_60min_volume_ratio': 0.21546461829161584, 'intraday_volume_sum': 99346390.0, 'intraday_amount_sum': 3468342502.0, 'late_session_strength': True, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': 45984.52, 'net_mf_ratio': 0.01325835609385459, 'small_order_net': -8062.440000000002, 'medium_order_net': -19944.350000000006, 'large_order_net': 4176.970000000001, 'extra_large_order_net': 23829.820000000007, 'main_force_net': 28006.790000000008, 'main_force_ratio': 0.008074978163647373, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-08-05', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'positive', 'flow_strength_basic': 'positive', 'flow_strength_score': 21.33333425750196, 'flow_continuity_3d': -1, 'flow_continuity_5d': -1, 'flow_continuity_10d': 0, 'positive_flow_days_5d': 2, 'positive_flow_days_10d': 5, 'flow_reversal_1d': True, 'flow_reversal_3d': True, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'inflow_confirmed', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
