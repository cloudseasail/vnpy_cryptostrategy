

class OrderOptimizer():

    def __init__(self):
        pass
    def opt_stop_atr(self, price, atr, rp_min=0.002, rp_max=0.02):
        rp = abs(atr)/price
        rp = rp_min if rp<rp_min else rp
        rp = rp_max if rp>rp_max else rp
        return rp*price
    def opt_position(self, price, cap, pos_ratio=1.0):
        return cap*pos_ratio/price