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
- snapshot_id: cnsvdata-2026-08-18-3fca4c1cf0bc
- latest_trade_date: 2026-08-18
- generated_at: 2026-08-18 20:05:52
- file_count: 14

## Loaded Data
- daily_rows: 3881
- one_min_rows: 12050
- moneyflow_rows: 3881
- latest_trade_date: 2026-08-18

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-08-18', 'latest_open': 33.7, 'latest_high': 33.79, 'latest_low': 33.28, 'latest_close': 33.49, 'latest_pre_close': 33.65, 'latest_pct_chg': -0.4755, 'latest_volume': 498257.72, 'latest_amount': 1666233.791, 'ma5': 33.646, 'ma10': 34.198, 'ma20': 34.147999999999996, 'ma60': 35.09349999999999, 'ret_1d': -0.0047548291233282525, 'ret_3d': -0.00858496151568977, 'ret_5d': -0.014130114807182736, 'ret_10d': -0.028712296983758545, 'ret_20d': 0.016080097087378675, 'ret_60d': -0.11635883905013189, 'volume_ma5': 612584.5939999999, 'volume_ma20': 822967.2225000001, 'volume_ratio_5d': 0.6986941494391318, 'volume_ratio_20d': 0.5898674563323211, 'amount_ma5': 2062615.7731999997, 'amount_ma20': 2809897.3164999997, 'amount_ratio_5d': 0.6889223254255386, 'amount_ratio_20d': 0.5785139040967557, 'price_position_20d': 0.3048327137546472, 'price_position_60d': 0.17617237008871997, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-08-18', 'latest_intraday_open': 33.7, 'latest_intraday_high': 33.79, 'latest_intraday_low': 33.28, 'latest_intraday_close': 33.49, 'intraday_range_pct': 0.015228426395939026, 'close_position_in_day_range': 0.4117647058823562, 'morning_return': -0.010979228486647008, 'afternoon_return': 0.004800480048004818, 'last_30min_return': 0.003596044351213745, 'last_60min_return': 0.004197901049475261, 'morning_volume_ratio': 0.6140294424339275, 'afternoon_volume_ratio': 0.38597055756607246, 'last_30min_volume_ratio': 0.13772683742863032, 'last_60min_volume_ratio': 0.22203762342106811, 'intraday_volume_sum': 49825772.0, 'intraday_amount_sum': 1666233792.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': -24406.27, 'net_mf_ratio': -0.01464756634502799, 'small_order_net': 9144.830000000002, 'medium_order_net': -269.4400000000023, 'large_order_net': -3632.909999999996, 'extra_large_order_net': -5242.489999999998, 'main_force_net': -8875.399999999994, 'main_force_ratio': -0.005326623459408641, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-08-18', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -19.974189804436627, 'flow_continuity_3d': -1, 'flow_continuity_5d': -3, 'flow_continuity_10d': -6, 'positive_flow_days_5d': 1, 'positive_flow_days_10d': 2, 'flow_reversal_1d': True, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
