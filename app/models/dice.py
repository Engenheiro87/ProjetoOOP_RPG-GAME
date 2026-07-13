import random

class Dice:
    def __init__(self):
        
        self.sides = 6 
        
    def roll(self) -> int:
        
        return random.randint(1, self.sides)
        
    def skill_test(self, nh_attribute: int) -> dict:
        
        d1 = self.roll()
        d2 = self.roll()
        d3 = self.roll()
        
        total_sum = d1 + d2 + d3
        is_success = total_sum < nh_attribute
        
        return {
            "rolls": [d1, d2, d3],
            "sum": total_sum,
            "target_nh": nh_attribute,
            "success": is_success
        }
