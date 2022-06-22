<mark >This repo is under development,  and not yet finished.</mark >

# vnpy_cryptostrategy 
crypto backtest and live strategy optomization based on vnpy.

## Motivation
Seems current ctastrategy inside vnpy are not friendly to crypto strategy.
This package is intend to make necessary optimization.

## Aiming for script trategy
Trying to make the package useful for script running.
VN trader UI is not the priority
Will use notebook for all the examples/analysis.

## Features planning
### 1. CCXT gateway support
vnpy_ccxt
### 2. Backtest engine optimization
* [ ] Trading cannot exceed initial capital
* [ ] Allow dynamic capital management
* [ ] Use real volumn to send order
* [ ] Better statistics for short open strategy
* [ ] Output of trading/dailyresult 
### 3. Live Strategy optimization
* [ ] Advanced strategy methods
* [ ] Memory optimization for long time running
* [ ] Reduce gateway API time consumption 
* [ ] realtime strategy management
### 4. Database enhancement
* [ ] Add interval 15m/30m/2h/4h database
* [ ] DataManager module for database maintain