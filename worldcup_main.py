#worldcup_main.py



# ================================
# دانشجو: محمدصالح نرگسی طاهری
# شماره دانشجویی: 404131273
# عنوان پروژه: شبیه‌ساز جام جهانی 2026 (World Cup Simulator 2026)
# تاریخ تحویل: 1405/05/04
# ================================



"""
پروژه پایانی درس برنامه‌سازی پیشرفته
هدف این برنامه شبیه‌سازی جام جهانی فوتبال با 32 تیم است. تیم‌ها از یک فایل CSV
خوانده می‌شوند، بر اساس رنکینگ فیفا سیدبندی و قرعه‌کشی می‌شوند، مرحله گروهی و
مراحل حذفی (یک‌هشتم تا فینال) شبیه‌سازی می‌شوند و در نهایت با اجرای هزاران بار
تورنمنت، درصد شانس قهرمانی هر تیم محاسبه می‌گردد.
"""

import csv
import os
import random
import sys

import numpy as np

from ClassTeam import Team

from ClassWorldCupSimulator import WorldCupSimulator

from fa_func import fa

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stdin.reconfigure(encoding='utf-8')
except (AttributeError, ValueError):
    # برخی محیط‌های اجرا (مثل بعضی IDEها) اجازه تغییر انکودینگ را نمی‌دهند؛
    # در این صورت برنامه باید بدون کرش به کار خود ادامه دهد.
    pass



def print_menu():
    """چاپ منوی اصلی برنامه."""
    print()
    print(fa("===== شبیه‌ساز جام جهانی ====="))
    print(fa("1) بارگذاری تیم‌ها از فایل CSV"))
    print(fa("2) انجام قرعه‌کشی گروه‌ها (سیدبندی خودکار)"))
    print(fa("3) اجرای مرحله گروهی و نمایش جدول هر گروه"))
    print(fa("4) اجرای کامل جام (گروهی + حذفی) و نمایش قهرمان"))
    print(fa("5) شبیه‌سازی 1000 باره و گزارش درصد قهرمانی"))
    print(fa("6) نمایش براکت حذفی آخرین شبیه‌سازی"))
    print(fa("7) خروج"))


def main():
    """تابع اصلی برنامه: نمایش منو در حلقه و مدیریت انتخاب‌های کاربر همراه با مدیریت خطا."""
    simulator = WorldCupSimulator()
    teams_loaded = False

    while True:
        print_menu()
        choice = input(fa("گزینه مورد نظر را انتخاب کنید: ")).strip()

        # ----- گزینه 1: بارگذاری تیم‌ها -----
        if choice == '1':
            filename = input(fa("نام فایل CSV را وارد کنید (خالی بگذارید برای worldcup_2026_teams.csv): "))

            filename = filename.strip()

            if not filename:
                filename = "worldcup_2026_teams.csv"
            teams_loaded = simulator.load_teams_from_csv(filename)
            continue

        # از این‌جا به بعد (گزینه‌های 2 تا 6) ابتدا باید تیم‌ها بارگذاری شده باشند
        if choice in ('2', '3', '4', '5', '6') and not teams_loaded:
            print(fa("ابتدا تیم‌ها را بارگذاری کنید."))
            continue

        # ----- گزینه 2: قرعه‌کشی گروه‌ها -----
        if choice == '2':
            simulator.groups_draw_and_seed()

        # ----- گزینه 3: اجرای مرحله گروهی -----
        elif choice == '3':
            if not simulator.groups:
                print(fa("ابتدا قرعه‌کشی گروه‌ها را انجام دهید (گزینه 2)."))
                continue
            simulator.stage_group_run()

        # ----- گزینه 4: اجرای کامل جام و نمایش قهرمان -----
        elif choice == '4':
            if not simulator.groups:
                print(fa("ابتدا قرعه‌کشی گروه‌ها را انجام دهید (گزینه 2)."))
                continue
            champion = simulator.simulation_full_run()
            simulator.final.results_display()
            print(fa(f"قهرمان جام جهانی: {champion.name}"))

        # ----- گزینه 5: شبیه‌سازی چندباره -----
        elif choice == '5':
            if not simulator.groups:
                print(fa("ابتدا قرعه‌کشی گروه‌ها را انجام دهید (گزینه 2)."))
                continue
            raw_input_value = input(fa("تعداد شبیه‌سازی را وارد کنید (خالی بگذارید برای 1000): ")).strip()
            if not raw_input_value:
                simulations_num = 1000
            else:
                try:
                    simulations_num = int(raw_input_value)
                except ValueError:
                    print(fa("خطا: تعداد شبیه‌سازی باید یک عدد صحیح باشد."))
                    continue
                if simulations_num <= 0:
                    print(fa("خطا: تعداد شبیه‌سازی باید عددی مثبت باشد."))
                    continue
            simulator.champion_likely_most(simulations_num)

        # ----- گزینه 6: نمایش براکت آخرین شبیه‌سازی -----
        elif choice == '6':
            if simulator.final is None:
                print(fa("ابتدا یک شبیه‌سازی کامل انجام دهید (گزینه 4 یا 5)."))
                continue
            simulator.bracket_display()

        # ----- گزینه 7: خروج -----
        elif choice == '7':
            print(fa("خروج از برنامه. موفق باشید!"))
            break

        else:
            print(fa("گزینه نامعتبر است. لطفاً عددی بین 1 تا 7 وارد کنید."))


if __name__ == '__main__':
    main()
