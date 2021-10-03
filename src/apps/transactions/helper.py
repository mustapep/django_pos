from .models import DetailTransaction
from datetime import date, timedelta
def income(obj):
    total_income = [o.sub_total for o in obj]
    return sum(total_income)

def dateRange(date1, date2):
    for n in range(int((date2-date1).days)+1):
        yield date1 + timedelta(n)