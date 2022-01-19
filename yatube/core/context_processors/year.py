import datetime


def year(request):
    now = datetime.datetime.now()
    year = int(now.year)
    return {
        "year": year,
    }
