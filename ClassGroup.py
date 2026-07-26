#ClassGroup.py

import random
from ClassMatch import Match

class Group:
    """کلاس گروه: نگه‌داری 4 تیم یک گروه، اجرای بازی‌های دوره‌ای و رتبه‌بندی آن‌ها."""

    def __init__(self, name, teams):
        """سازنده کلاس گروه.
        """
        self.name = name
        self.teams = teams
        # لیست بازی‌های انجام‌شده گروه؛ برای پیاده‌سازی قانون بازی مستقیم لازم است
        self.matches = []

    def matches_all_play(self):
        """اجرای تمام بازی‌های گروه (هر تیم فقط یک بار با سه تیم دیگر بازی می‌کند)."""
        self.matches = []
        team_count = len(self.teams)
        for i in range(team_count):
            for j in range(i + 1, team_count):
                match = Match(self.teams[i], self.teams[j], is_knockout=False)
                match.play()
                self.matches.append(match)

    def _head_to_head_winner(self, team_a, team_b):
        """نتیجه بازی مستقیم بین دو تیم مشخص را در بین بازی‌های همین گروه پیدا می‌کند.
        این متد برای پیاده‌سازی قانون «بازی مستقیم» به عنوان یکی از معیارهای
        شکستن تساوی (پیش از قرعه‌کشی تصادفی) استفاده می‌شود.
        """
        for match in self.matches:
            same_pair = {match.team1.name, match.team2.name} == {team_a.name, team_b.name}
            if same_pair:
                if match.goals1 == match.goals2:
                    return None
                return match.team1 if match.goals1 > match.goals2 else match.team2
        return None

    def ranking_get(self):
        """رتبه‌بندی تیم‌های گروه طبق قوانین فیفا.
        """
        sorted_teams = sorted(
            self.teams,
            key=lambda t: (t.points, t.goal_difference(), t.for_goals),
            reverse=True,
        )

        final_order = []
        i = 0
        while i < len(sorted_teams):
            j = i
            while j + 1 < len(sorted_teams) and self._same_rank_key(sorted_teams[j], sorted_teams[j + 1]):
                j += 1

            tied_group = sorted_teams[i:j + 1]

            if len(tied_group) == 1:
                final_order.append(tied_group[0])
            elif len(tied_group) == 2:
                # دقیقاً دو تیم مساوی هستند -> ابتدا نتیجه بازی مستقیم را چک می‌کنیم
                winner = self._head_to_head_winner(tied_group[0], tied_group[1])
                if winner is not None:
                    loser = tied_group[1] if winner is tied_group[0] else tied_group[0]
                    final_order.extend([winner, loser])
                else:
                    random.shuffle(tied_group)
                    final_order.extend(tied_group)
            else:
                # بیش از دو تیم با هم مساوی هستند -> قرعه‌کشی تصادفی
                random.shuffle(tied_group)
                final_order.extend(tied_group)

            i = j + 1

        return final_order

    @staticmethod
    def _same_rank_key(team_a, team_b):
        """بررسی می‌کند آیا دو تیم از نظر امتیاز، تفاضل گل و گل زده کاملاً برابرند یا نه."""
        key_a = (team_a.points, team_a.goal_difference(), team_a.for_goals)
        key_b = (team_b.points, team_b.goal_difference(), team_b.for_goals)
        return key_a == key_b

    def advance_teams(self):
        """دو تیم اول گروه (صعودکننده به مرحله حذفی) را برمی‌گرداند.
        """
        ranking = self.ranking_get()
        return ranking[0], ranking[1]