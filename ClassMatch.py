#ClassMatch.py

from fa_func import fa

class Match:
    """کلاس نگه‌دارنده‌ی یک مسابقه بین دو تیم و اجرای آن."""

    def __init__(self, team1, team2, is_knockout=False):
        """سازنده کلاس مسابقه.
        """
        self.team1 = team1
        self.team2 = team2
        self.goals1 = 0
        self.goals2 = 0
        self.is_knockout = is_knockout
        self.winner = None
        self.penalty_result = None

    def play(self):
        """اجرای مسابقه: شبیه‌سازی نتیجه، به‌روزرسانی آمار هر دو تیم و تعیین برنده (در مرحله حذفی)."""
        goals1, goals2, winner, penalty_result = self.team1.simulate_match(
            self.team2, self.is_knockout
        )
        self.goals1 = goals1
        self.goals2 = goals2
        self.penalty_result = penalty_result

        # به‌روزرسانی آمار گل هر دو تیم (در کل مسابقات)
        self.team1.for_goals += goals1
        self.team1.against_goals += goals2
        self.team2.for_goals += goals2
        self.team2.against_goals += goals1

        if not self.is_knockout:
            if goals1 > goals2:
                self.team1.points += 3
            elif goals2 > goals1:
                self.team2.points += 3
            else:
                self.team1.points += 1
                self.team2.points += 1
        else:
            self.winner = winner

    def result_text(self):
        """رشته متنی خلاصه نتیجه بازی (برای چاپ در براکت حذفی).
        """
        text = f"{self.team1.name} {self.goals1}-{self.goals2} {self.team2.name}"
        if self.penalty_result is not None:
            p1, p2 = self.penalty_result
            text += f" ({p1}-{p2} pens)"
        if self.winner is not None:
            text += f" -> برنده: {self.winner.name}"
        return fa(text)

