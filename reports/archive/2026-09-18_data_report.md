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
- snapshot_id: cnsvdata-2026-09-18-2c32836fe390
- latest_trade_date: 2026-09-18
- generated_at: 2026-09-18 22:20:35
- file_count: 14

## Loaded Data
- daily_rows: 3904
- one_min_rows: 17593
- moneyflow_rows: 3904
- latest_trade_date: 2026-09-18

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-09-18', 'latest_open': 38.6, 'latest_high': 39.97, 'latest_low': 38.28, 'latest_close': 39.47, 'latest_pre_close': 38.96, 'latest_pct_chg': 1.309, 'latest_volume': 1137487.06, 'latest_amount': 4468183.848, 'ma5': 38.672, 'ma10': 39.092, 'ma20': 36.809999999999995, 'ma60': 35.17833333333333, 'ret_1d': 0.013090349075975283, 'ret_3d': 0.034329140461216046, 'ret_5d': -0.007044025157232681, 'ret_10d': 0.053376034160661945, 'ret_20d': 0.17191211401425166, 'ret_60d': 0.18173652694610776, 'volume_ma5': 1181606.266, 'volume_ma20': 1212574.6974999998, 'volume_ratio_5d': 0.8613017224004252, 'volume_ratio_20d': 0.9529001186160105, 'amount_ma5': 4583086.3188000005, 'amount_ma20': 4544483.8518, 'amount_ratio_5d': 0.8694642067013422, 'amount_ratio_20d': 1.004481799163638, 'price_position_20d': 0.7749999999999999, 'price_position_60d': 0.8116740088105726, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-09-18', 'latest_intraday_open': 38.6, 'latest_intraday_high': 39.97, 'latest_intraday_low': 38.28, 'latest_intraday_close': 39.47, 'intraday_range_pct': 0.042817329617430906, 'close_position_in_day_range': 0.7041420118343191, 'morning_return': 0.02590673575129543, 'afternoon_return': -0.0032828282828283317, 'last_30min_return': 0.0020309723280020897, 'last_60min_return': 0.002540005080010177, 'morning_volume_ratio': 0.7034600991416993, 'afternoon_volume_ratio': 0.29653990085830073, 'last_30min_volume_ratio': 0.09642357601852632, 'last_60min_volume_ratio': 0.14572871712492272, 'intraday_volume_sum': 113748706.0, 'intraday_amount_sum': 4468183860.0, 'late_session_strength': True, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': 15784.98, 'net_mf_ratio': 0.003532750785772949, 'small_order_net': -10514.380000000005, 'medium_order_net': -6976.669999999998, 'large_order_net': 7603.190000000002, 'extra_large_order_net': 9887.869999999995, 'main_force_net': 17491.059999999998, 'main_force_ratio': 0.003914579300005562, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-09-18', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'positive', 'flow_strength_basic': 'positive', 'flow_strength_score': 7.4473300857785105, 'flow_continuity_3d': 1, 'flow_continuity_5d': -1, 'flow_continuity_10d': 0, 'positive_flow_days_5d': 2, 'positive_flow_days_10d': 5, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
