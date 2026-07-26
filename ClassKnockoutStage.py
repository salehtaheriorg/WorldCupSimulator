#ClassKnockoutStage.py
class KnockoutStage:
    """کلاس یک مرحله از بخش حذفی تورنمنت (مثلاً یک‌هشتم، یک‌چهارم، نیمه‌نهایی یا فینال)."""

    def __init__(self, round_name, matches):
        """سازنده کلاس مرحله حذفی.
        """
        self.round_name = round_name
        self.matches = matches

    def round_play(self):
        """اجرای تمام مسابقات این مرحله."""
        for match in self.matches:
            match.play()

    def winners_get(self):
        """لیست تیم‌های برنده این مرحله را به همان ترتیب مسابقات برمی‌گرداند.
        """
        return [match.winner for match in self.matches]

    def results_display(self):
        """چاپ خلاصه نتایج تمام مسابقات این مرحله."""
        print(f"===== {self.round_name} =====")
        for match in self.matches:
            print(match.result_text())

