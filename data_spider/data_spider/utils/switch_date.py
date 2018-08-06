def switch_time(month,day,year):
    month = swith_month(month)
    if len(day) == 1:
        day = "0"+day
    return "{}-{}-{}".format(year,month,day)

def swith_month(month):
    if month == "January" or month == "Jan":
        return "01"
    elif month == "February" or month == "Feb":
        return "02"
    elif month == "March" or month == "Mar":
        return "03"
    elif month == "April" or month == "Apr":
        return "04"
    elif month == "May" or month == "May":
        return "05"
    elif month == "June" or month == "Jun":
        return "06"
    elif month == "July" or month == "Jul":
        return "07"
    elif month == "August" or month == "Aug":
        return "08"
    elif month == "September" or month == "Sep":
        return "09"
    elif month == "October" or month == "Oct":
        return "10"
    elif month == "November" or month == "Nov":
        return "11"
    elif month == "December" or month == "Dec":
        return "12"
    else:
        return month

