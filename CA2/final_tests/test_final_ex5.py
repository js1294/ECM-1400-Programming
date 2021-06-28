from ex5 import monthly_users
from ex5 import annual_user_count
from ex5 import annual_user_download_average
import ex5


def test_keyword_year():
    ex5.access_log = ["19.69.248.1 mmc2 [12/12/2018] `GET /m/' 200 10"]
    assert monthly_users(year=2018)


def test_empty_log():
    ex5.access_log = []
    assert monthly_users()
    assert annual_user_count() == 0
    assert annual_user_download_average() == None


def test_monthly_users():
    ex5.access_log = ["19.69.248.1 mmc2 [12/12/2018] `GET /m/' 200 10",
                      "19.69.248.2 mmc2 [12/01/2018] `GET /m/index.php' 200 10",
                      "19.69.248.3 mmc2 [12/01/2018] `GET /m/index.php' 200 10",
                      "19.69.248.4 mmc2 [12/02/2018] `GET /m/index.php' 200 10",
                      "19.69.248.5 mmc2 [12/03/2018] `GET /m/index.php' 200 10",
                      "19.69.248.6 mmc2 [12/10/2018] `GET /m/index.php' 200 10",
                      "46.72.177.7 gr4 [12/12/2018] `GET /video/v.php' 200 10"]
    assert (monthly_users(2018) == [2, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 2]) or \
           (monthly_users(2018) == [3, 2, 2, 0, 0, 0, 0, 0, 0, 2, 0, 3])


def test_annual_user_count():
    ex5.access_log = ["19.69.248.1 mmc2 [12/12/2018] `GET /m/' 200 10",
                      "19.69.248.2 mmc2 [12/01/2018] `GET /m/index.php' 200 10",
                      "19.69.248.3 mmc2 [12/01/2018] `GET /m/index.php' 200 10",
                      "19.69.248.4 mmc2 [12/02/2018] `GET /m/index.php' 200 10",
                      "19.69.248.5 mmc2 [12/03/2018] `GET /m/index.php' 200 10",
                      "19.69.248.6 mmc2 [12/10/2018] `GET /m/index.php' 200 10",
                      "46.72.177.7 gr4 [12/12/2018] `GET /video/v.php' 200 10"]
    assert (annual_user_count(2018) == 2) or (annual_user_count(2018) == 3)


def test_annual_user_download_average():
    ex5.access_log = ["19.69.248.1 mmc2 [12/12/2019] `GET /m/' 200 10000",
                      "19.69.248.2 mmc1 [12/01/2019] `GET /m/index.php' 200 10",
                      "19.69.248.3 mmc2 [12/01/2018] `GET /m/index.php' 200 12",
                      "19.69.248.4 mmc3 [12/02/2018] `GET /m/index.php' 200 12",
                      "19.69.248.5 mmc4 [12/03/2018] `GET /m/index.php' 200 12",
                      "19.69.248.6 mmc5 [12/10/2018] `GET /m/index.php' 200 12",
                      "46.72.177.7 gr4 [12/12/2018] `GET /video/v.php' 200 12"]
    assert (annual_user_download_average(2018) == 10) or \
           (annual_user_download_average(2018) == 12)


test_empty_log()
test_annual_user_download_average()
test_annual_user_count()
test_monthly_users()
test_keyword_year()
