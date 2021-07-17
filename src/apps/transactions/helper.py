from .models import DetailTransaction
def income(obj):
    total_income = []
    for o in obj:
        total_income.append(o.sub_total)

    return sum(total_income)
