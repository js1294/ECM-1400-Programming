"""This is exercise 5."""
__author__ = "Jack Shaw"


def monthly_users(year: int) -> list:
    """This will tell you the new user for each month in a specified year."""

    monthly_user = [0 for _ in range(0, 12)]
    for each_access in access_log:
        if each_access[:11] in each_access:
            access_log.remove(each_access)  # Removes duplicates
        each_access = each_access.split()
        each_access[3:5] = ["".join(each_access[3:5])]  # Combines request line

        if each_access[2][-5:-1] == str(year):
            index = int(each_access[2][4:6]) - 1
            value = monthly_user[index] + 1
            monthly_user[index] = value
    return monthly_user


def annual_user_count(year: int) -> int:
    """This will tell you the number of new users in the specified year."""

    yearly_user = 0
    for each_access in access_log:
        if each_access[:11] in each_access:
            access_log.remove(each_access)  # Removes duplicates
        each_access = each_access.split()
        each_access[3:5] = ["".join(each_access[3:5])]  # Combines request line

        if each_access[2][-5:-1] == str(year):
            yearly_user += 1
    return yearly_user


def annual_user_download_average(year: int) -> int:
    """This will tell you the number of bytes of data downloaded on average across the year."""

    yearly_download = 0
    for each_access in access_log:
        each_access = each_access.split()
        each_access[3:5] = ["".join(each_access[3:5])]  # Combines request line

        if each_access[2][-5:-1] == str(year):
            yearly_download += int(each_access[5])

    average = round(yearly_download / len(access_log))
    return average

access_log = []
