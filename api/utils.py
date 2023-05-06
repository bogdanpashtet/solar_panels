from numpy import array, sin, cos, tan, radians, degrees, sqrt, pi, arccos, arctan, fmax, fmin, sum, concatenate, asfarray

ghi = "GHI"
dhi = "DHI"
albedo = "Albedo"
doy = "DOY"


class CalculateByBase:
    class Meta:
        abstract = True

    def __init__(self, data, request):
        self.data = data
        self.latitude = int(request.POST.get('latitude'))
        self.azimuth = int(request.POST.get('azimuth'))
        self.max_angle = request.POST.get('max-angle')
        if request.POST.get('tilt-angle') is None:
            self.tilt_angle = 0
        else:
            self.tilt_angle = int(request.POST.get('tilt-angle'))

    def max_tilt_angle(self, func):
        latitude, self.latitude = self.latitude, 0
        azimuth, self.azimuth = self.azimuth, 0
        maximum = sum(func())
        self.latitude = latitude
        self.azimuth = azimuth
        angle = 0
        for i in range(1, 91):
            self.tilt_angle = i
            temp = sum(func())  # выход не сразу
            if temp < maximum:
                break
            maximum = temp
            angle = i
        return angle, maximum

    def calculate(self):
        pass

    def get_dataset(self):
        if self.max_angle == 'false':
            return self.calculate()
        else:
            return self.max_tilt_angle(self.calculate)


class CalculateByDay(CalculateByBase):
    def __init__(self, data, request):
        super().__init__(data, request)
        self.calculate_func = self.calc_day_by_hours
        self.month = int(request.POST.get('by-day-month'))
        self.day = int(request.POST.get('by-day-day'))

    def calc_day_by_hours(self):
        e_sum = array(self.data[(self.data.Month == self.month) & (self.data.Day == self.day)][ghi])
        e_dif = array(self.data[(self.data.Month == self.month) & (self.data.Day == self.day)][dhi])
        ro = array(self.data[(self.data.Month == self.month) & (self.data.Day == self.day)][albedo])
        num_day_y = array(self.data[(self.data.Month == self.month) & (self.data.Day == self.day)][doy])
        return fun_calc_new(num_day_y, e_sum, e_dif, ro, self.latitude, self.tilt_angle, self.azimuth)

    def calculate(self):
        return self.calc_day_by_hours()


class CalculateByMonth(CalculateByBase):
    def __init__(self, data, request):
        super().__init__(data, request)
        self.solve_radio = request.POST.get('calculation-type-month')
        self.month = int(request.POST.get('by-month-month'))

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

    def calculate(self):
        if self.solve_radio == 'day':
            return self.calc_month_by_day()
        else:
            return self.calc_month_by_hours()


class CalculateByYear(CalculateByMonth):
    def __init__(self, data, request):
        CalculateByBase.__init__(self, data, request)
        self.solve_radio = request.POST.get('calculation-type-year')
        self.month = 0

    def calc_year_by_hours(self):
        e_sum = array(self.data.GHI)
        e_dif = array(self.data.DHI)
        ro = array(self.data.Albedo)
        num_day_y = array(self.data.DOY)
        return fun_calc_new(num_day_y, e_sum, e_dif, ro, self.latitude, self.tilt_angle, self.azimuth)

    def calc_year_by_day(self):
        year_by_day = array([])
        for num_month in range(1, 13):
            self.month = num_month
            year_by_day = concatenate((year_by_day, self.calc_month_by_day()))
        return year_by_day

    def calc_year_by_month(self):
        year_by_month = []
        for num_month in range(1, 13):
            self.month = num_month
            year_by_month.append(sum(self.calc_month_by_hours()))
        return array(year_by_month)

    def calculate(self):
        if self.solve_radio == 'hour':
            return self.calc_year_by_hours()
        elif self.solve_radio == 'day':
            return self.calc_year_by_day()
        else:
            return self.calc_year_by_month()


class CalculateByCustom(CalculateByBase):
    def __init__(self, data, request):
        super().__init__(data, request)
        self.num_month_start = int(request.POST.get('num-month-start'))
        self.num_month_end = int(request.POST.get('num-month-end'))
        self.num_day_m_start = int(request.POST.get('num-day-m-start'))
        self.num_day_m_end = int(request.POST.get('num-day-m-end'))

    def calc_by_range(self):
        data = self.data[(self.data.Month >= self.num_month_start) & (self.data.Month <= self.num_month_end)]
        data = data.drop(data[(data.Month == self.num_month_start) & (data.Day < self.num_day_m_start)].index)
        data = data.drop(data[(data.Month == self.num_month_end) & (data.Day > self.num_day_m_end)].index)
        e_sum = array(data.GHI)
        e_dif = array(data.DHI)
        ro = array(data.Albedo)
        num_day_y = array(data.DOY)
        return fun_calc_new(num_day_y, e_sum, e_dif, ro, self.latitude, self.tilt_angle, self.azimuth)

    def calculate(self):
        return self.calc_by_range()


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


def get_file(request):
    for file in request.FILES.values():
        return file
