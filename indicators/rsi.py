class RSI:
    def __init__(self, period):
        self.period = period
    
    def averages(self, prices, start_index):
        gains, losses = 0, 0

        for i in range(self.period):
            if (i + start_index) >= len(prices):
                break
            diff = prices[i + start_index] - prices[i + start_index - 1]
            if diff >= 0:
                gains += diff
            else:
                losses += abs(diff)

        avg_gains = gains / self.period
        avg_losses = losses / self.period
        return avg_gains, avg_losses
    
    def calculate(self, prices):
        avg_gains, avg_losses = 0, 0

        for i in range(1, len(prices)):
            new_avg_gains, new_avg_losses = self.averages(prices, i)

            if i == 1:
                avg_gains = new_avg_gains
                avg_losses = new_avg_losses
                continue

            avg_gains = (avg_gains * (self.period - 1) + new_avg_gains) / self.period
            avg_losses = (avg_losses * (self.period - 1) + new_avg_losses) / self.period

        rs = avg_gains / avg_losses if avg_losses != 0 else float('inf')
        return 100 - (100 / (1 + rs))
        
        
