#ClassTeam.py

import random
import numpy as np

class Team:
    """کلاس تیم ملی فوتبال. مشخصات و آمار یک تیم و منطق شبیه‌سازی یک بازی را نگه می‌دارد."""

    def __init__(self, name, attack, defense, rank):
        """سازنده کلاس تیم.
        """
        self.name = name
        self.attack = attack
        self.defense = defense
        self.rank = rank

        self.for_goals = 0       # جمع گل زده در کل مسابقات
        self.against_goals = 0   # جمع گل خورده در کل مسابقات
        self.points = 0          # امتیاز (فقط در مرحله گروهی معنا دارد)
        self.group = None        # نام گروهی که تیم در آن قرار گرفته (بعد از قرعه‌کشی)

    def goal_difference(self):
        """تفاضل گل تیم را برمی‌گرداند.
        """
        return self.for_goals - self.against_goals

    def reset_stats(self):
        """آمار تیم (گل زده، گل خورده و امتیاز) را قبل از شروع یک شبیه‌سازی جدید صفر می‌کند."""
        self.for_goals = 0
        self.against_goals = 0
        self.points = 0

    # ---------------------------------------------------------------------
    # متدهای کمکی خصوصی (داخلی) برای محاسبه‌ی گل بازی، وقت اضافه و پنالتی
    # نام این متدها با آندرلاین شروع شده تا مشخص باشد فقط داخل کلاس استفاده می‌شوند
    # ---------------------------------------------------------------------

    def _lambda_calc(self, opponent):
        """محاسبه‌ی میانگین گل مورد انتظار (لامبدای پواسون) طبق فرمول پیشنهادی پروژه.
        """
        lam = (self.attack / 100) * 1.5 + (1 - opponent.defense / 100) * 0.8
        # به صورت ایمنی از لامبدای صفر یا منفی جلوگیری می‌کنیم (نباید طبق فرمول اتفاق بیفتد)
        return max(lam, 0.05)

    @staticmethod
    def _goals_poisson(lam):
        """تولید تعداد گل با استفاده از توزیع پواسون numpy.
        """
        return int(np.random.poisson(lam=lam))

    def _penalty_probability(self, opponent):
        """احتمال گل‌شدن یک ضربه پنالتی این تیم مقابل حریف را محاسبه می‌کند.
        """
        p = 0.75 + (self.attack - opponent.defense) / 250
        return min(max(p, 0.6), 0.9)

    def _penalty_shootout(self, opponent):
        """شبیه‌سازی کامل ضربات پنالتی شامل 5 پنالتی اول و پنالتی‌های ناگهانی.
        """
        self_pen = 0
        opp_pen = 0
        p_self = self._penalty_probability(opponent)
        p_opp = opponent._penalty_probability(self)

        # پنج ضربه اول هر تیم
        for _ in range(5):
            if random.random() < p_self:
                self_pen += 1
            if random.random() < p_opp:
                opp_pen += 1

        # اگر بعد از 5 ضربه هم مساوی بود، پنالتی ناگهانی (هر دور یک ضربه برای هر تیم)
        while self_pen == opp_pen:
            self_scored = random.random() < p_self
            opp_scored = random.random() < p_opp
            self_pen += int(self_scored)
            opp_pen += int(opp_scored)
            # اگر فقط یکی از دو تیم در همین دور گل زد، همان تیم برنده است
            if self_scored != opp_scored:
                break
            # در غیر این صورت (هر دو گل زدند یا هر دو گل نزدند) دور بعدی ادامه پیدا می‌کند

        winner = self if self_pen > opp_pen else opponent
        return self_pen, opp_pen, winner

    def simulate_match(self, opponent, is_knockout=False):
        """شبیه‌سازی نتیجه بازی با تیم حریف.
        """
        lam_self = self._lambda_calc(opponent)
        lam_opp = opponent._lambda_calc(self)

        # 90 دقیقه بازی اصلی
        self_goals = self._goals_poisson(lam_self)
        opp_goals = self._goals_poisson(lam_opp)

        winner = None
        penalty_result = None

        if not is_knockout:
            # در مرحله گروهی تساوی مجاز است، نیازی به ادامه بازی نیست
            return self_goals, opp_goals, winner, penalty_result

        if self_goals != opp_goals:
            winner = self if self_goals > opp_goals else opponent
            return self_goals, opp_goals, winner, penalty_result

        # نتیجه در 90 دقیقه مساوی شده -> وقت اضافه (لامبدای 0.33 برابر اصلی)
        et_self_goals = self._goals_poisson(lam_self * 0.33)
        et_opp_goals = self._goals_poisson(lam_opp * 0.33)
        self_goals += et_self_goals
        opp_goals += et_opp_goals

        if self_goals != opp_goals:
            winner = self if self_goals > opp_goals else opponent
            return self_goals, opp_goals, winner, penalty_result

        # همچنان مساوی -> ضربات پنالتی، نتیجه پنالتی برنده را مشخص می‌کند
        self_pen, opp_pen, winner = self._penalty_shootout(opponent)
        penalty_result = (self_pen, opp_pen)

        return self_goals, opp_goals, winner, penalty_result
