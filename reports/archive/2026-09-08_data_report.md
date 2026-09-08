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
- snapshot_id: cnsvdata-2026-09-08-3937b120f22f
- latest_trade_date: 2026-09-08
- generated_at: 2026-09-08 22:22:41
- file_count: 14

## Loaded Data
- daily_rows: 3896
- one_min_rows: 15665
- moneyflow_rows: 3896
- latest_trade_date: 2026-09-08

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-09-08', 'latest_open': 38.56, 'latest_high': 39.69, 'latest_low': 38.29, 'latest_close': 39.08, 'latest_pre_close': 38.38, 'latest_pct_chg': 1.8239, 'latest_volume': 1496584.62, 'latest_amount': 5847910.341, 'ma5': 36.636, 'ma10': 35.51, 'ma20': 34.539, 'ma60': 34.729000000000006, 'ret_1d': 0.0182386659718603, 'ret_3d': 0.1386946386946386, 'ret_5d': 0.13505663665408063, 'ret_10d': 0.15484633569739925, 'ret_20d': 0.1504268472181336, 'ret_60d': 0.08827624617098317, 'volume_ma5': 1782326.666, 'volume_ma20': 930025.4725000001, 'volume_ratio_5d': 0.9090676909765537, 'volume_ratio_20d': 1.6532375590431416, 'amount_ma5': 6597841.4196, 'amount_ma20': 3289446.9195, 'amount_ratio_5d': 0.9763042661527556, 'amount_ratio_20d': 1.8451383635066665, 'price_position_20d': 0.9140845070422535, 'price_position_60d': 0.9196310935441371, 'new_high_20d': True, 'new_low_20d': False, 'new_high_60d': True, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-09-08', 'latest_intraday_open': 38.56, 'latest_intraday_high': 39.69, 'latest_intraday_low': 38.29, 'latest_intraday_close': 39.08, 'intraday_range_pct': 0.0358239508700102, 'close_position_in_day_range': 0.5642857142857143, 'morning_return': 0.012707468879668005, 'afternoon_return': 0.0007682458386684132, 'last_30min_return': 0.0017944116893104933, 'last_60min_return': -0.003061224489796066, 'morning_volume_ratio': 0.6862075062618244, 'afternoon_volume_ratio': 0.31379249373817564, 'last_30min_volume_ratio': 0.09470909837360215, 'last_60min_volume_ratio': 0.17531427658263654, 'intraday_volume_sum': 149658462.0, 'intraday_amount_sum': 5847910353.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': 41505.8, 'net_mf_ratio': 0.007097543836984077, 'small_order_net': 17868.830000000016, 'medium_order_net': -16151.430000000022, 'large_order_net': -17260.699999999983, 'extra_large_order_net': 15543.300000000003, 'main_force_net': -1717.3999999999796, 'main_force_ratio': -0.00029367755315248253, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-09-08', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'mixed', 'flow_strength_basic': 'mixed', 'flow_strength_score': 6.803866283831594, 'flow_continuity_3d': 1, 'flow_continuity_5d': 1, 'flow_continuity_10d': 2, 'positive_flow_days_5d': 3, 'positive_flow_days_10d': 6, 'flow_reversal_1d': True, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
