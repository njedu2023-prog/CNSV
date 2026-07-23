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
- snapshot_id: cnsvdata-2026-07-23-9cc7c812e1ad
- latest_trade_date: 2026-07-23
- generated_at: 2026-07-23 20:04:43
- file_count: 14

## Loaded Data
- daily_rows: 3863
- one_min_rows: 7712
- moneyflow_rows: 3863
- latest_trade_date: 2026-07-23

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-07-23', 'latest_open': 33.27, 'latest_high': 33.87, 'latest_low': 32.68, 'latest_close': 33.76, 'latest_pre_close': 33.02, 'latest_pct_chg': 2.2411, 'latest_volume': 1066948.76, 'latest_amount': 3559901.612, 'ma5': 33.018, 'ma10': 33.742, 'ma20': 34.5955, 'ma60': 36.805000000000014, 'ret_1d': 0.02241066020593574, 'ret_3d': 0.02272038776128449, 'ret_5d': 0.023030303030302957, 'ret_10d': -0.06378258458125363, 'ret_20d': -0.04443815454288147, 'ret_60d': -0.12989690721649483, 'volume_ma5': 1004398.708, 'volume_ma20': 1263589.9565, 'volume_ratio_5d': 1.0305614729131058, 'volume_ratio_20d': 0.8492648538137763, 'amount_ma5': 3311982.9852, 'amount_ma20': 4400443.4925999995, 'amount_ratio_5d': 1.042689668180733, 'amount_ratio_20d': 0.8117801849211788, 'price_position_20d': 0.2694805194805191, 'price_position_60d': 0.14664310954063572, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-07-23', 'latest_intraday_open': 33.27, 'latest_intraday_high': 33.87, 'latest_intraday_low': 32.68, 'latest_intraday_close': 33.76, 'intraday_range_pct': 0.03524881516587671, 'close_position_in_day_range': 0.9075630252100844, 'morning_return': 0.0045085662759241085, 'afternoon_return': 0.010173548773189545, 'last_30min_return': 0.0017804154302669684, 'last_60min_return': 0.0020777678836449986, 'morning_volume_ratio': 0.6024882394539735, 'afternoon_volume_ratio': 0.3975117605460266, 'last_30min_volume_ratio': 0.10717464070158346, 'last_60min_volume_ratio': 0.16003029048930148, 'intraday_volume_sum': 106694876.0, 'intraday_amount_sum': 3559901627.0, 'late_session_strength': True, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': 23317.38, 'net_mf_ratio': 0.006550006865751547, 'small_order_net': 419.61999999999534, 'medium_order_net': -4676.4800000000105, 'large_order_net': 376.5100000000093, 'extra_large_order_net': 3880.3499999999985, 'main_force_net': 4256.860000000008, 'main_force_ratio': 0.0011957802388837503, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-07-23', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'positive', 'flow_strength_basic': 'positive', 'flow_strength_score': 7.745787104635297, 'flow_continuity_3d': -1, 'flow_continuity_5d': -1, 'flow_continuity_10d': -2, 'positive_flow_days_5d': 2, 'positive_flow_days_10d': 4, 'flow_reversal_1d': True, 'flow_reversal_3d': True, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'inflow_confirmed', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
