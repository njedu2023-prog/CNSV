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
- snapshot_id: cnsvdata-2026-07-28-abe5c3e7f153
- latest_trade_date: 2026-07-28
- generated_at: 2026-07-28 20:04:49
- file_count: 14

## Loaded Data
- daily_rows: 3866
- one_min_rows: 8435
- moneyflow_rows: 3866
- latest_trade_date: 2026-07-28

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-07-28', 'latest_open': 33.12, 'latest_high': 33.86, 'latest_low': 32.91, 'latest_close': 33.49, 'latest_pre_close': 33.53, 'latest_pct_chg': -0.1193, 'latest_volume': 850434.79, 'latest_amount': 2833553.066, 'ma5': 33.372, 'ma10': 33.248000000000005, 'ma20': 34.560500000000005, 'ma60': 36.45816666666666, 'ret_1d': -0.0011929615269907767, 'ret_3d': -0.007997630331753491, 'ret_5d': 0.016080097087378675, 'ret_10d': -0.008291382884216825, 'ret_20d': -0.008878366380585923, 'ret_60d': -0.1863459669582117, 'volume_ma5': 883436.004, 'volume_ma20': 1226236.1470000003, 'volume_ratio_5d': 0.945022903555566, 'volume_ratio_20d': 0.6924657259925509, 'amount_ma5': 2944105.2365999995, 'amount_ma20': 4271762.67975, 'amount_ratio_5d': 0.9470942287772965, 'amount_ratio_20d': 0.6621915903694472, 'price_position_20d': 0.22564935064935088, 'price_position_60d': 0.12279151943462903, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-07-28', 'latest_intraday_open': 33.12, 'latest_intraday_high': 33.86, 'latest_intraday_low': 32.91, 'latest_intraday_close': 33.49, 'intraday_range_pct': 0.028366676619886618, 'close_position_in_day_range': 0.6105263157894776, 'morning_return': 0.008152173913043681, 'afternoon_return': 0.002994908655286066, 'last_30min_return': 0.0005975500448163196, 'last_60min_return': 0.0, 'morning_volume_ratio': 0.6733269460907167, 'afternoon_volume_ratio': 0.32667305390928325, 'last_30min_volume_ratio': 0.13111029947399025, 'last_60min_volume_ratio': 0.19294287102248017, 'intraday_volume_sum': 85043479.0, 'intraday_amount_sum': 2833553056.0, 'late_session_strength': True, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': -36252.85, 'net_mf_ratio': -0.012794131309909267, 'small_order_net': -5394.069999999992, 'medium_order_net': 688.1600000000035, 'large_order_net': -729.8399999999965, 'extra_large_order_net': 5435.749999999996, 'main_force_net': 4705.91, 'main_force_ratio': 0.0016607806137342337, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-07-28', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'mixed', 'flow_strength_basic': 'mixed', 'flow_strength_score': -11.13335069617503, 'flow_continuity_3d': -1, 'flow_continuity_5d': -1, 'flow_continuity_10d': -2, 'positive_flow_days_5d': 2, 'positive_flow_days_10d': 4, 'flow_reversal_1d': True, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
