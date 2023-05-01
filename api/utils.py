from numpy import array, sin, cos, tan, radians, degrees, sqrt, pi, arccos, arctan, fmax, fmin, sum, concatenate, \
    asfarray

ghi = "GHI"
dhi = "DHI"
albedo = "Albedo"
doy = "DOY"


class ByDay:
    def __init__(self, data, request):
        self.data = data
        self.month = int(request.POST.get('by-day-month'))
        self.day = int(request.POST.get('by-day-day'))
        self.latitude = int(request.POST.get('latitude'))
        self.azimuth = int(request.POST.get('azimuth'))
        self.max_angle = request.POST.get('max-angle')
        if request.POST.get('tilt-angle') is None:
            self.tilt_angle = 0
        else:
            self.tilt_angle = int(request.POST.get('tilt-angle'))

    def calc_day_by_hours(self):
        e_sum = array(self.data[(self.data.Month == self.month) & (self.data.Day == self.day)][ghi])
        e_dif = array(self.data[(self.data.Month == self.month) & (self.data.Day == self.day)][dhi])
        ro = array(self.data[(self.data.Month == self.month) & (self.data.Day == self.day)][albedo])
        num_day_y = array(self.data[(self.data.Month == self.month) & (self.data.Day == self.day)][doy])
        return fun_calc_new(num_day_y, e_sum, e_dif, ro, self.latitude, self.tilt_angle, self.azimuth)

    def by_day_max_tilt_angle(self):
        latitude, self.latitude = self.latitude, 0
        azimuth, self.azimuth = self.azimuth, 0
        maximum = sum(self.calc_day_by_hours())
        self.latitude = latitude
        self.azimuth = azimuth
        angle = 0
        for i in range(1, 91):
            self.tilt_angle = i
            temp = sum(self.calc_day_by_hours())  # выход не сразу
            if temp < maximum:
                break
            maximum = temp
            angle = i
        return angle, maximum

    def get_dataset(self):
        if self.max_angle == 'false':
            return self.calc_day_by_hours()
        else:
            return self.by_day_max_tilt_angle()


class ByMonth:
    def __init__(self, data, request):
        self.data = data
        self.day_or_hour = request.POST.get('day-or-hour')
        self.month = int(request.POST.get('by-month-month'))
        self.latitude = int(request.POST.get('latitude'))
        self.azimuth = int(request.POST.get('azimuth'))
        self.max_angle = request.POST.get('max-angle')
        if request.POST.get('tilt-angle') is None:
            self.tilt_angle = 0
        else:
            self.tilt_angle = int(request.POST.get('tilt-angle'))

    def calc_month_by_hours(self):
        e_sum = array(self.data[(self.data.Month == self.month)].GHI)
        e_dif = array(self.data[(self.data.Month == self.month)].DHI)
        ro = array(self.data[(self.data.Month == self.month)].Albedo)
        num_day_y = array(self.data[(self.data.Month == self.month)].DOY)
        return fun_calc_new(num_day_y, e_sum, e_dif, ro, self.latitude, self.tilt_angle, self.azimuth)

    def calc_month_by_day(self):
        month_by_hours = self.calc_month_by_hours()
        month_by_day = sum(month_by_hours.reshape(self.data[(self.data.Month == self.month)].Day.max(), 24), axis=1)
        return month_by_day

    def by_day_max_tilt_angle(self):
        latitude, self.latitude = self.latitude, 0
        azimuth, self.azimuth = self.azimuth, 0
        maximum = sum(self.calculate())
        self.latitude = latitude
        self.azimuth = azimuth
        angle = 0
        for i in range(1, 91):
            self.tilt_angle = i
            temp = sum(self.calculate())  # выход не сразу
            if temp < maximum:
                break
            maximum = temp
            angle = i
        return angle, maximum

    def calculate(self):
        if self.day_or_hour == 'day':
            return self.calc_month_by_day()
        else:
            return self.calc_month_by_hours()

    def get_dataset(self):
        if self.max_angle == 'false':
            return self.calculate()
        else:
            return self.by_day_max_tilt_angle()


def write_data_hourly(writer, data):
    writer.writerow(
        ['hour_num', 'month_1', 'month_2', 'month_3', 'month_4', 'month_5', 'month_6', 'month_7', 'month_8', 'month_9',
         'month_10', 'month_11', 'month_12'])

    for i in data:
        writer.writerow(
            [i["hour_num"], i["month_1"], i["month_2"], i["month_3"], i["month_4"], i["month_5"], i["month_6"],
             i["month_7"], i["month_8"], i["month_9"], i["month_10"], i["month_11"], i["month_12"]])


def fun_calc_new(num_day_y, e_sum, e_dif, ro, latitude, tilt_angle, azimuth):  # основная функция расчета

    if type(num_day_y[0]) == str:
        num_day_y = asfarray(num_day_y, int)
    if type(e_sum[0]) == str:
        e_sum = asfarray(e_sum, float)
    if type(e_dif[0]) == str:
        e_dif = asfarray(e_dif, float)
    if type(ro[0]) == str:
        ro = asfarray(ro, float)

    t1 = array([i for i in range(len(num_day_y))])

    delta = 23.45 * sin(radians(360 * (284 + num_day_y) / 365))  # delta in degrees

    a = (sin(radians(latitude)) * cos(radians(tilt_angle)) -
         cos(radians(latitude)) * sin(radians(tilt_angle))
         * cos(radians(azimuth))) * sin(radians(delta))  # a in radians

    b = (cos(radians(latitude)) * cos(radians(tilt_angle)) + sin(radians(latitude)) * sin(radians(tilt_angle))
         * cos(radians(azimuth))) * cos(radians(delta))  # a in radians

    c = sin(radians(tilt_angle)) * sin(radians(azimuth)) * cos(radians(delta))  # c in radians

    omega3 = degrees(arccos(-tan(radians(latitude)) * tan(radians(delta))))  # omega3 in degrees

    omegaB = degrees(-arccos(-tan(radians(latitude)) * tan(radians(delta))))  # omegaB in degrees

    c_a_b = c ** 2 - a ** 2 + b ** 2
    c_a_b[c_a_b < 0] = 0  # чтобы под коренм не было нуля

    a_b = a - b

    _2arctg_ABC_minus = 2 * arctan(-c - sqrt(c_a_b) / a_b)  # in radians

    _2arctg_ABC_plus = 2 * arctan(-c + sqrt(c_a_b) / a_b)  # in radians

    omega3_By = fmax(omega3, _2arctg_ABC_minus * 180 / pi)  # in degrees

    omegaB_By = fmax(omegaB, _2arctg_ABC_plus * 180 / pi)  # in degrees

    omega1 = fmin(omega3, fmax(omegaB, 15 * (t1 % 24 - 12)))  # in degrees

    omega2 = fmin(omega3, fmax(omegaB, 15 * (t1 % 24 - 11)))  # in degrees

    omega1_By = fmin(omega3_By, fmax(omegaB_By, 15 * (t1 % 24 - 12)))  # in degrees

    omega2_By = fmin(omega3_By, fmax(omegaB_By, 15 * (t1 % 24 - 11)))  # in degrees

    kpr1 = b * (sin(radians(omega2_By)) - sin(radians(omega1_By)))  # in o.e

    kpr2 = a * pi / 180 * (omega2_By - omega1_By)  # in o.e

    kpr3 = c * (cos(radians(omega2_By)) - cos(radians(omega1_By)))  # in o.e

    kpr4 = cos(radians(latitude)) * cos(radians(delta)) * (sin(radians(omega2)) - sin(radians(omega1)))  # in o.e

    omeg2_omeg1 = (omega2 - omega1) * pi / 180
    kpr5 = sin(radians(latitude)) * sin(radians(delta)) * omeg2_omeg1  # in o.e

    kpr = []
    for i in range(len(num_day_y)):
        if kpr4[i] + kpr5[i] != 0:
            kpr.append((kpr1[i] + kpr2[i] - kpr3[i]) / (kpr4[i] + kpr5[i]))
        else:
            kpr.append(0)
    kpr = array(kpr)

    r_pr = kpr * (e_sum - e_dif)

    r_d = e_dif * (180 - tilt_angle) / 180

    r_otr = 0.5 * ro * e_sum * sin(radians(tilt_angle))

    r = r_pr + r_d + r_otr

    return r


# 3 функции расчета дня(график есть), месяца(график 2 +-) и года по часам(слишком много точек)
# def calc_day_by_hours(data, num_month, num_day_m, latitude=0, tilt_angle=0, azimuth=0, ghi="GHI",
#                       dhi="DHI", albedo="Albedo", doy="DOY"):
#     e_sum = array(data[(data.Month == num_month) & (data.Day == num_day_m)][ghi])
#     e_dif = array(data[(data.Month == num_month) & (data.Day == num_day_m)][dhi])
#     ro = array(data[(data.Month == num_month) & (data.Day == num_day_m)][albedo])
#     num_day_y = array(data[(data.Month == num_month) & (data.Day == num_day_m)][doy])
#     return fun_calc_new(num_day_y, e_sum, e_dif, ro, latitude, tilt_angle, azimuth)


def calc_month_by_hours(data, num_month, latitude=0, tilt_angle=0, azimuth=0):
    e_sum = array(data[(data.Month == num_month)].GHI)
    e_dif = array(data[(data.Month == num_month)].DHI)
    ro = array(data[(data.Month == num_month)].Albedo)
    num_day_y = array(data[(data.Month == num_month)].DOY)
    return fun_calc_new(num_day_y, e_sum, e_dif, ro, latitude, tilt_angle, azimuth)


def calc_year_by_hours(data, latitude=0, tilt_angle=0, azimuth=0):
    e_sum = array(data.GHI)
    e_dif = array(data.DHI)
    ro = array(data.Albedo)
    num_day_y = array(data.DOY)
    return fun_calc_new(num_day_y, e_sum, e_dif, ro, latitude, tilt_angle, azimuth)


# Расчет месяца по дням(график есть)
def calc_month_by_day(data, num_month, latitude=0, tilt_angle=0, azimuth=0):
    month_by_hours = calc_month_by_hours(data, num_month, latitude, tilt_angle, azimuth)
    month_by_day = sum(month_by_hours.reshape(data[(data.Month == num_month)].Day.max(), 24), axis=1)
    return month_by_day


# Расчет года по месяцам(график есть)
def calc_year_by_month(data, latitude=0, tilt_angle=0, azimuth=0):
    year_by_month = []
    for num_month in range(1, 13):
        year_by_month.append(sum(calc_month_by_hours(data, num_month, latitude, tilt_angle, azimuth)))
    return array(year_by_month)


# Расчет года по дням(график 2 +-)
def calc_year_by_day(data, latitude=0, tilt_angle=0, azimuth=0):
    year_by_day = array([])
    for num_month in range(1, 13):
        year_by_day = concatenate((year_by_day, calc_month_by_day(data, num_month, latitude, tilt_angle, azimuth)))
    return year_by_day


# расчет по замкнутому интервалу(если не задавать параметры, то расчет по году)
def calc_by_range(data, num_month_start=1, num_day_m_start=1, num_month_end=12,
                  num_day_m_end=31, latitude=0, tilt_angle=0, azimuth=0):
    data = data[(data.Month >= num_month_start) & (data.Month <= num_month_end)]
    data = data.drop(data[(data.Month == num_month_start) & (data.Day < num_day_m_start)].index)
    data = data.drop(data[(data.Month == num_month_end) & (data.Day > num_day_m_end)].index)
    e_sum = array(data.GHI)
    e_dif = array(data.DHI)
    ro = array(data.Albedo)
    num_day_y = array(data.DOY)
    return fun_calc_new(num_day_y, e_sum, e_dif, ro, latitude, tilt_angle, azimuth)


# поиск угла при котором выработка максимальна (день, месяц, год или произвольный период)
def max_tilt_angle(fun, *args, latitude, azimuth):
    maximum = sum(fun(*args))
    angle = 0
    for i in range(1, 91):
        temp = sum(fun(*args, tilt_angle=i, latitude=latitude, azimuth=azimuth))  # выход не сразу
        if temp < maximum:
            break
        maximum = temp
        angle = i
    return angle, maximum


def get_file(request):
    for file in request.FILES.values():
        return file
