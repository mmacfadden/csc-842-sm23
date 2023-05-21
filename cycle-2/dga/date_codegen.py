from .codegen import CodeGenerator;
from textwrap import dedent;

class DateCodeGenerator(CodeGenerator):
    """
    The DateCodeGenerator class writes functions that generate
    dates to use for time based seeds based on how frequently
    the domains should change.
    """
    
    def __init__(self, frequency) -> None:
        super().__init__()
        self._frequency = frequency

    
    def generate_js_code(self):
        if self._frequency == "week":
            return dedent("""
            function getDates() {
              const thisWeek = new Date();
              let day = thisWeek.getDay();
              if (day === 0) {
                day = 7;
              }
              const diff = thisWeek.getDate() - day - 7;
              thisWeek.setDate(diff);
              thisWeek.setHours(0,0,0,0);

              const lastWeek = new Date(thisWeek);
              lastWeek.setDate(thisWeek.getDate() - 7);
              return [lastWeek, thisWeek];
            }
            """)
        
        elif self._frequency == "month":
            return dedent("""
            function getDates() {
              const now = new Date();
              const thisMonth = new Date(now.getFullYear(), now.getMonth(), 1);
              const lastMonth = new Date(thisMonth);
              lastMonth.setMonth(thisMonth.getMonth() - 1);

              thisMonth.setDate(thisMonth.getDate() - 5);
              lastMonth.setDate(lastMonth.getDate() - 5);
              
              return [lastMonth, thisMonth];
            }
            """)
        else:
            raise Exception("unknown date type")

    
    def generate_py_code(self):
        if self._frequency == "week":
            return dedent("""
            import datetime
            
            def get_dates():
              today = datetime.date.today()
              this_week = today - datetime.timedelta(days=today.weekday() + 8)
              last_week = this_week - datetime.timedelta(days=7)
              return [last_week, this_week]
            """)
        
        elif self._frequency == "month":
            return dedent("""
            import datetime

            def get_dates():
              today = datetime.date.today()
              this_month = today.replace(day=1)
              last_month = this_month - datetime.timedelta(days=1)
              last_month = last_month.replace(day=1)

              this_month = this_month - datetime.timedelta(days=5)
              last_month = last_month - datetime.timedelta(days=5)

              return [last_month, this_month]
            """)
        else:
            raise Exception(f"Unknown frequency type: {self._frequency}")
        