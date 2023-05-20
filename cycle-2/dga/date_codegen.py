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
              var day = thisWeek.getDay();
              var diff = thisWeek.getDate() - day;
              thisWeek.setDate(diff);
              thisWeek.setHours(0,0,0,0);

              const lastWeek = new Date(thisWeek);
              lastWeek.setDate(thisWeek.getDate() -7);
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
              this_week = today - datetime.timedelta(days=today.weekday() + 1)
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
              return [last_month, this_month]
            """)
        else:
            raise Exception(f"Unknown frequency type: {self._frequency}")
        