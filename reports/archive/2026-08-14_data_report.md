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
- snapshot_id: cnsvdata-2026-08-14-16617095a372
- latest_trade_date: 2026-08-14
- generated_at: 2026-08-14 20:05:52
- file_count: 14

## Loaded Data
- daily_rows: 3879
- one_min_rows: 11568
- moneyflow_rows: 3879
- latest_trade_date: 2026-08-14

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-08-14', 'latest_open': 33.75, 'latest_high': 34.19, 'latest_low': 33.33, 'latest_close': 33.42, 'latest_pre_close': 33.78, 'latest_pct_chg': -1.0657, 'latest_volume': 718782.55, 'latest_amount': 2418045.066, 'ma5': 33.977999999999994, 'ma10': 34.442, 'ma20': 34.0895, 'ma60': 35.246166666666674, 'ret_1d': -0.010657193605683846, 'ret_3d': -0.01619075654989688, 'ret_5d': -0.041032998565279755, 'ret_10d': -0.05002842524161455, 'ret_20d': 0.033395176252319025, 'ret_60d': -0.12968749999999996, 'volume_ma5': 762158.116, 'volume_ma20': 865985.661, 'volume_ratio_5d': 0.8879425318141055, 'volume_ratio_20d': 0.819569569376965, 'amount_ma5': 2605832.2101999996, 'amount_ma20': 2947910.38485, 'amount_ratio_5d': 0.8665922217039755, 'amount_ratio_20d': 0.8115603963202014, 'price_position_20d': 0.404907975460123, 'price_position_60d': 0.1673003802281369, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-08-14', 'latest_intraday_open': 33.75, 'latest_intraday_high': 34.19, 'latest_intraday_low': 33.33, 'latest_intraday_close': 33.42, 'intraday_range_pct': 0.025733093955715124, 'close_position_in_day_range': 0.1046511627907017, 'morning_return': -0.002666666666666817, 'afternoon_return': -0.007130124777183444, 'last_30min_return': -0.0008968609865470656, 'last_60min_return': -0.002388059701492473, 'morning_volume_ratio': 0.5785762189134948, 'afternoon_volume_ratio': 0.42142378108650524, 'last_30min_volume_ratio': 0.11790995760818067, 'last_60min_volume_ratio': 0.18792569463462908, 'intraday_volume_sum': 71878255.0, 'intraday_amount_sum': 2418045066.0, 'late_session_strength': False, 'late_session_weakness': True, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -24660.27, 'net_mf_ratio': -0.01019843275327938, 'small_order_net': 9216.380000000005, 'medium_order_net': 11292.080000000002, 'large_order_net': -12609.720000000008, 'extra_large_order_net': -7898.720000000001, 'main_force_net': -20508.44000000001, 'main_force_ratio': -0.008481413472547748, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-08-14', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -18.679846225827127, 'flow_continuity_3d': -3, 'flow_continuity_5d': -5, 'flow_continuity_10d': -8, 'positive_flow_days_5d': 0, 'positive_flow_days_10d': 1, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
