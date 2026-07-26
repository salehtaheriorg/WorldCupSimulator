#ClassWorldCupSimulator.py

from fa_func import fa

import csv,random,os

from ClassKnockoutStage import KnockoutStage
from ClassGroup import Group
from ClassTeam import Team
from ClassMatch import Match

# نام گروه‌های جام جهانی (8 گروه چهارتیمی)
GROUP_NAMES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

# جفت‌شدن تیم‌های صعودکننده در مرحله یک‌هشتم نهایی طبق قانون ثابت فیفا
# هر خط به صورت (نام گروه اول, رتبه در گروه اول, نام گروه دوم, رتبه در گروه دوم) است
ROUND_OF_16_PAIRINGS = [
    ('A', 1, 'B', 2),
    ('C', 1, 'D', 2),
    ('E', 1, 'F', 2),
    ('G', 1, 'H', 2),
    ('B', 1, 'A', 2),
    ('D', 1, 'C', 2),
    ('F', 1, 'E', 2),
    ('H', 1, 'G', 2),
]





class WorldCupSimulator:
    """کلاس اصلی برنامه: مدیریت کل روند شبیه‌سازی جام جهانی از بارگذاری تیم‌ها تا اعلام قهرمان."""

    def __init__(self):
        self.teams = []
        self.groups = []
        self.round_of_16 = None
        self.quarterfinals = None
        self.semifinals = None
        self.final = None
        self.champion = None

    def load_teams_from_csv(self, filename):
        """خواندن فایل CSV تیم‌ها و ساخت لیست اشیاء Team.
        """
        if not os.path.exists(filename):
           
            print(fa(f"خطا: فایل '{filename}' پیدا نشد."))
            return False

        try:
            loaded_teams = []
            with open(filename, 'r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    team = Team(
                        name=row['name'].strip(),
                        attack=int(row['attack']),
                        defense=int(row['defense']),
                        rank=int(row['rank']),
                    )
                    loaded_teams.append(team)

            if len(loaded_teams) == 0:
                print(fa("خطا: فایل CSV خالی است یا ساختار درستی ندارد."))
                return False

            self.teams = loaded_teams
            # با هر بارگذاری جدید، نتایج قرعه‌کشی و شبیه‌سازی قبلی دیگر معتبر نیستند
            self.groups = []
            self.round_of_16 = None
            self.quarterfinals = None
            self.semifinals = None
            self.final = None
            self.champion = None

            print(fa(f"تعداد {len(self.teams)} تیم با موفقیت از فایل '{filename}' بارگذاری شد."))
            return True

        except (KeyError, ValueError) as error:
            print(fa(f"خطا: ساختار فایل CSV نامعتبر است ({error})."))
            return False
        except Exception as error:  # جلوگیری از کرش برنامه در صورت هر خطای پیش‌بینی‌نشده
            print(fa(f"خطا در خواندن فایل CSV: {error}"))
            return False

    def groups_draw_and_seed(self):
        """قرعه‌کشی گروه‌ها بر اساس سیدبندی رنکینگ فیفا.
        """
        sorted_teams = sorted(self.teams, key=lambda t: t.rank)

        pots = [
            sorted_teams[0:8],
            sorted_teams[8:16],
            sorted_teams[16:24],
            sorted_teams[24:32],
        ]

        group_teams = {name: [] for name in GROUP_NAMES}

        for pot in pots:
            # انتخاب تصادفی بدون جایگزینی از سید فعلی (طبق راهنمایی رفع اشکال پروژه)
            shuffled_pot = random.sample(pot, len(pot))
            for group_name, team in zip(GROUP_NAMES, shuffled_pot):
                group_teams[group_name].append(team)

        self.groups = []
        for name in GROUP_NAMES:
            group = Group(name, group_teams[name])
            for team in group.teams:
                team.group = name
            self.groups.append(group)

        print(fa("قرعه‌کشی گروه‌ها با موفقیت انجام شد."))

    def _play_group_stage(self):
        """اجرای بازی‌های تمام گروه‌ها بدون چاپ (متد کمکی داخلی، برای جلوگیری از
        چاپ هزاران بار جدول گروه‌ها هنگام اجرای شبیه‌سازی 1000 باره).
        """

        for group in self.groups:
            group.matches_all_play()

    def stage_group_run(self):
        """اجرای مرحله گروهی (تمام 8 گروه) و چاپ جدول رده‌بندی هر گروه."""
        self._play_group_stage()

        for group in self.groups:
            print(f"===== Group {group.name} =====")
            ranking = group.ranking_get()
            for position, team in enumerate(ranking, start=1):
                gd = team.goal_difference()
                gd_text = f"+{gd}" if gd > 0 else str(gd)
                print(f"{position}. {team.name}: {team.points} pts, GD {gd_text}, GF {team.for_goals}")

    def bracket_knockout_setup(self):
        """ساخت براکت مرحله یک‌هشتم نهایی بر اساس قانون ثابت فیفا:
        A1-B2, C1-D2, E1-F2, G1-H2, B1-A2, D1-C2, F1-E2, H1-G2
        """
        advancers = {}
        for group in self.groups:
            first_team, second_team = group.advance_teams()
            advancers[group.name] = (first_team, second_team)

        matches = []
        for group_a, pos_a, group_b, pos_b in ROUND_OF_16_PAIRINGS:
            team_a = advancers[group_a][pos_a - 1]
            team_b = advancers[group_b][pos_b - 1]
            matches.append(Match(team_a, team_b, is_knockout=True))

        self.round_of_16 = KnockoutStage('Round of 16', matches)
        # مراحل بعدی هنوز ساخته نشده‌اند، تا اجرای stage_knockout_run پاک می‌شوند
        self.quarterfinals = None
        self.semifinals = None
        self.final = None
        self.champion = None

    def stage_knockout_run(self):
        """اجرای تمام مراحل حذفی (یک‌هشتم، یک‌چهارم، نیمه‌نهایی، فینال) و تعیین قهرمان."""
        self.round_of_16.round_play()
        winners_16 = self.round_of_16.winners_get()

        qf_matches = [
            Match(winners_16[i], winners_16[i + 1], is_knockout=True)
            for i in range(0, len(winners_16), 2)
        ]
        self.quarterfinals = KnockoutStage('Quarterfinals', qf_matches)
        self.quarterfinals.round_play()
        winners_qf = self.quarterfinals.winners_get()

        sf_matches = [
            Match(winners_qf[i], winners_qf[i + 1], is_knockout=True)
            for i in range(0, len(winners_qf), 2)
        ]
        self.semifinals = KnockoutStage('Semifinals', sf_matches)
        self.semifinals.round_play()
        winners_sf = self.semifinals.winners_get()

        final_match = Match(winners_sf[0], winners_sf[1], is_knockout=True)
        self.final = KnockoutStage('Final', [final_match])
        self.final.round_play()

        self.champion = self.final.winners_get()[0]

    def simulation_full_run(self):
        """اجرای کامل یک دوره جام جهانی (مرحله گروهی + تمام مراحل حذفی).

        پیش از شروع، آمار تمام تیم‌ها (امتیاز، گل زده، گل خورده) صفر می‌شود.
        از قرعه‌کشی گروه‌ها (self.groups) که قبلاً انجام شده استفاده می‌شود.
        """
        for team in self.teams:
            team.reset_stats()

        self._play_group_stage()
        self.bracket_knockout_setup()
        self.stage_knockout_run()

        return self.champion

    def champion_likely_most(self, simulations_num=1000):
        """اجرای شبیه‌سازی کامل جام به تعداد دلخواه و محاسبه درصد قهرمانی هر تیم.
        """
        champion_counts = {team.name: 0 for team in self.teams}

        for _ in range(simulations_num):
            champion = self.simulation_full_run()
            champion_counts[champion.name] += 1

        print(fa(f"شبیه‌سازی {simulations_num} بار انجام شد."))
        print(fa("درصد قهرمانی هر تیم:"))

        sorted_results = sorted(champion_counts.items(), key=lambda item: item[1], reverse=True)
        for name, count in sorted_results:
            if count == 0:
                continue
            percentage = (count / simulations_num) * 100
            print(f"{name}: {percentage:.1f}%")

        # : رسم نمودار میله‌ای درصد قهرمانی با matplotlib
        self._plot_champion_percentages(champion_counts, simulations_num)

    @staticmethod
    def _plot_champion_percentages(champion_counts, simulations_num):
        """رسم و ذخیره نمودار میله‌ای درصد قهرمانی تیم‌ها.

        این متد اختیاری است و در صورت نصب‌ نبودن matplotlib، بدون کرش برنامه
        فقط یک پیام هشدار چاپ می‌کند.
        """
        try:
            import matplotlib
            matplotlib.use('Agg')  # اجرای بدون رابط گرافیکی (مناسب برای ذخیره فایل)
            import matplotlib.pyplot as plt
        except ImportError:
            print(fa("کتابخانه matplotlib نصب نیست؛ نمودار رسم نشد."))
            return

        # فقط تیم‌هایی که حداقل یک بار قهرمان شده‌اند و حداکثر 15 تیم برتر نمایش داده می‌شوند
        results = [(name, count) for name, count in champion_counts.items() if count > 0]
        results.sort(key=lambda item: item[1], reverse=True)
        results = results[:15]

        if not results:
            return

        names = [item[0] for item in results]
        percentages = [item[1] / simulations_num * 100 for item in results]

        plt.figure(figsize=(10, 6))
        plt.bar(names, percentages, color='#2e7d32')
        # matplotlib هم مثل ترمینال، الگوریتم BiDi ندارد؛ برچسب‌های فارسی هم
        # باید با fa() آماده شوند تا در تصویر خروجی درست و راست‌به‌چپ دیده شوند.
        plt.xlabel('تیم')
        plt.ylabel('درصد قهرمانی (%)')
        plt.title(f'درصد قهرمانی تیم‌ها در {simulations_num} شبیه‌سازی')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('champion_probabilities.png')
        plt.close()
        print(fa("نمودار درصد قهرمانی در فایل champion_probabilities.png ذخیره شد."))

    def bracket_display(self):
        """نمایش براکت کامل حذفی مربوط به آخرین شبیه‌سازی انجام‌شده."""
        print("===== Knockout Bracket =====")
        for stage in (self.round_of_16, self.quarterfinals, self.semifinals, self.final):
            if stage is not None:
                stage.results_display()
        if self.champion is not None:
            print(f"Champion: {self.champion.name}")
