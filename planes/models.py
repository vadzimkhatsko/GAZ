from django.db import models
from django.contrib.auth.models import User


class Curator(models.Model):
    title = models.CharField(max_length=120)

    def __str__(self):
        try:
            return str(self.title)
        except:
            return 'Ошибка в данных'

    class Meta:
        verbose_name = 'Подразделение/куратор'
        verbose_name_plural = 'Подразделение/кураторы'


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    curator = models.ForeignKey(Curator, on_delete=models.DO_NOTHING)

    def __str__(self):
        try:
            return str(self.user)
        except:
            return 'Ошибка в данных'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class FinanceCosts(models.Model): #  A 1000      B 2000
    total = models.FloatField(verbose_name="сумма 4-x кварталов")
    title = models.CharField(
        verbose_name="название статьи",
        max_length=100,
    )

    def __str__(self):
        try:
            return str(self.title)
        except:
            return 'Ошибка в данных'

    class Meta:
        verbose_name = 'Статья финансирования'
        verbose_name_plural = 'Статьи финансирования'

import datetime
class Quart(models.Model): # A1-250|A2-250|A3-250|A4-250|B1-500|B2-500|B3-500|B4-500
    finance_cost = models.ForeignKey(FinanceCosts, on_delete=models.DO_NOTHING)
    total = models.FloatField(verbose_name="сумма по кварталу")
    title = models.CharField(max_length=50)

    # TODO сделать возможным выбор кварталов от 1 до 4
    class QuartNum(models.IntegerChoices):
        I = 1
        II = 2
        III = 3
        IV = 4
    number = models.IntegerField(verbose_name='Квартал', choices=QuartNum.choices)
    year = models.PositiveIntegerField(default=(datetime.date.today().year), max_length=4)


    def __str__(self):
        try:
            return 'Квартал %s, статьи %s' % (self.title, self.finance_cost)
        except:
            return 'Ошибка в данных'

    class Meta:
        verbose_name = 'Квартал'
        verbose_name_plural = 'Кварталы'
        constraints = [
            models.CheckConstraint(check=models.Q(year=2019), name='test')
        ]



class CuratorQuartCosts(models.Model): # vadim a1 100    ser a1 100
    quart = models.ForeignKey(
        Quart,
        on_delete=models.DO_NOTHING,
        verbose_name="квартал куратора"
    )
    curator = models.ForeignKey(
        Curator,
        on_delete=models.DO_NOTHING,
        verbose_name="куратор"
    )
    total = models.FloatField(
        verbose_name="деньги выделенные данному куратору в данной статье данного квартала"
    )

    def __str__(self):
        try:
            return 'Куратор %s, квартал %s' % (self.curator, self.quart)
        except:
            return 'Ошибка в данных'

    class Meta:
        verbose_name_plural = 'Поквартальные финансы кураторов'



class PurchaseType(models.Model): # TODO что это такое в ТЗ?
    title = models.CharField(max_length=200)

    def __str__(self):
        try:
            return str(self.title)
        except:
            return 'Ошибка в данных'

    class Meta:
        verbose_name = 'Тип договора'
        verbose_name_plural = 'Типы договоров'


class ActivityForm(models.Model): # TODO что это такое в ТЗ?
    title = models.CharField(max_length=200)

    def __str__(self):
        try:
            return str(self.title)
        except:
            return 'Ошибка в данных'

    class Meta:
        verbose_name = 'Вид договора'
        verbose_name_plural = 'Виды договоров'

class StateASEZ(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        try:
            return str(self.title)
        except:
            return 'Ошибка в данных'

    class Meta:
        verbose_name = 'Состояние АСЭЗ'
        verbose_name_plural = 'Состояние АСЭЗ'


class NumberPZTRU(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        try:
            return str(self.title)
        except:
            return 'Ошибка в данных'

    class Meta:
        verbose_name = 'Номер ППЗ АСЭЗ'
        verbose_name_plural = 'Номер ППЗ АСЭЗ'


class ContractStatus(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        try:
            return str(self.title)
        except:
            return 'Ошибка в данных'

    class Meta:
        verbose_name = 'Статус договора'
        verbose_name_plural = 'Статусы договоров'


class Currency(models.Model):
    title = models.CharField(max_length=10)

    def __str__(self):
        try:
            return str(self.title)
        except:
            return 'Ошибка в данных'

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Типы валют'


class Price(models.Model): # TODO что это в тз? Потеряна связь с договором или так и должно быть?
    value = models.FloatField(verbose_name="цена")
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING)

    def __str__(self):
        try:
            return str(self.value) + str(self.currency)
        except:
            return 'Ошибка в данных'

    class Meta:
        verbose_name = 'Сумма договора'
        verbose_name_plural = 'Суммы договоров'


class ContractTerm(models.Model): # TODO нет ссылки на договор?
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        try:
            return 'с %s по %s' % (str(self.start_date), str(self.end_date))
        except:
            return 'Ошибка в данных'

    class Meta:
        verbose_name = 'Период действия договора'
        verbose_name_plural = 'Период действия договора'


class Counterpart(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    reg_addr = models.CharField(max_length=255)
    UNP = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    def __str__(self):
        try:
            return '%s УНП: %s' % (self.name, str(self.UNP))
        except:
            return 'Ошибка в данных'

    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'


class Contract(models.Model):
    title = models.CharField(max_length=150, verbose_name="наименование договора")
    finance_cost = models.ForeignKey(
        FinanceCosts,
        on_delete=models.DO_NOTHING,
        verbose_name="статья финансирования")
    curator = models.ForeignKey(
        Curator,
        on_delete=models.DO_NOTHING,
        verbose_name="Куратор"
    )
    contract_type = models.BooleanField(
        default=True,
        verbose_name="Тип договора (филиал)",
        help_text="Да - филиал, нет - центр"
    )   # default fillial
    contract_mode = models.BooleanField(
        default=True,
        verbose_name="Вид договора (основной)",
        help_text="Да - основной, нет - доп. согл")   # default main
    purchase_type = models.ForeignKey(
        PurchaseType,
        verbose_name="тип закупки",
        on_delete=models.DO_NOTHING,
        help_text="вводить тип закупки которая может меняться"
    )
    activity_form = models.ForeignKey(
        ActivityForm,
        verbose_name="вид деятельности",
        on_delete=models.DO_NOTHING
    )
    stateASEZ = models.ForeignKey(
        StateASEZ,
        verbose_name="автоматизированая система эллектронных закупок",
        on_delete=models.DO_NOTHING
    )
    number_ppz = models.CharField(
        max_length=150,
        verbose_name="номер позиция плана закупок",
        null=True,
        blank=True
    )
    number_PZTRU = models.ForeignKey(
        NumberPZTRU,
        verbose_name="ПЗТРУ",
        help_text="положение о закупках товаров, работ, услуг",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    contract_status = models.ForeignKey(
        ContractStatus,
        verbose_name="статус договора",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
        )
    plane_load_date_ASEZ = models.DateField(verbose_name="планируемая дата загрузки в АСЭЗ")
    fact_load_date_ASEZ = models.DateField(
        verbose_name="фактическая дата загрузки в АСЭЗ",
        null=True,
        blank=True
    )
    start_max_price_ASEZ_NDS = models.ForeignKey(
        Price,
        verbose_name="начальная максимальная цена АСЭЗ с НДС рос. руб.",
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING
    )
    currency_rate_on_load_date_ASEZ_NDS = models.FloatField(
        verbose_name="курс валюты на дату загрузки в бел.руб.",
        null=True,
        blank=True
    )
    contract_sum_NDS_RUB = models.FloatField(verbose_name="сумма договора с НДС рос.руб.")
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING)
    delta_data_ASEZ = models.FloatField(verbose_name="отклонение от НМЦ в АСЭЗ")
    number_KGG = models.CharField(
        max_length=100,
        verbose_name="номер договора от центрального органа",
        null=True,
        blank=True
    )
    plane_sum_SAP_total = models.FloatField(verbose_name="плановая сумма САП")
    plane_sum_SAP_1 = models.FloatField(default=0, verbose_name="сумма САП 1-й квартал")
    plane_sum_SAP_2 = models.FloatField(default=0, verbose_name="сумма САП 2-й квартал")
    plane_sum_SAP_3 = models.FloatField(default=0, verbose_name="сумма САП 3-й квартал")
    plane_sum_SAP_4 = models.FloatField(default=0, verbose_name="сумма САП 4-й квартал")
    register_number_SAP = models.CharField(max_length=100)
    contract_number = models.CharField(
        max_length=100,
        verbose_name="номер договора",
        null=True,
        blank=True
    )
    plane_sign_date = models.DateField()
    fact_sign_date = models.DateField(null=True, blank=True)
    contract_term = models.ForeignKey(
        ContractTerm,
        verbose_name="период действия",
        on_delete=models.DO_NOTHING
    )
    counterpart = models.ForeignKey(Counterpart, on_delete=models.DO_NOTHING)
    contract_sum = models.FloatField(verbose_name="сумма всего договора без НДС")
    contract_sum_1 = models.FloatField(
        verbose_name="сумма 1-й квартал договора без НДС",
        null=True,
        blank=True
    )
    contract_sum_2 = models.FloatField(
        verbose_name="сумма 2-й квартал договора без НДС",
        null=True,
        blank=True
    )
    contract_sum_3 = models.FloatField(
        verbose_name="сумма 3-й квартал договора без НДС",
        null=True,
        blank=True
    )
    contract_sum_4 = models.FloatField(
        verbose_name="сумма 4-й квартал договора без НДС",
        null=True,
        blank=True
    )
    contract_sum_NDS_BYN = models.FloatField(
        verbose_name="сумма договора с НДС бел.руб.",
        blank=True,
        null=True,
    )
    contract_total_sum_with_sub_BYN = models.FloatField(
        verbose_name='общая сумма договора всего с доп соглашениями, б.р. без ндс',
        null=True,
        blank=True
    )

    forecast_total = models.FloatField( # вычисляемое
        verbose_name='прогонз, всего',
    )
    forecast_jan = models.FloatField(
        verbose_name='прогноз январь',
        default=0
    )
    forecast_feb = models.FloatField(
        verbose_name='прогноз февраль',
        default=0
    )
    forecast_mar = models.FloatField(
        verbose_name='прогноз март',
        default=0
    )
    forecast_Iq = models.FloatField( # вычисляемое
        verbose_name='прогноз 1-й квартал'
    )

    forecast_apr = models.FloatField(
        verbose_name='прогноз апрель',
        default=0
    )
    forecast_may = models.FloatField(
        verbose_name='прогноз май',
        default=0
    )
    forecast_jun = models.FloatField(
        verbose_name='прогноз июнь',
        default=0
    )
    forecast_IIq = models.FloatField( # вычисляемое
        verbose_name='прогноз 2-й квартал'
    )
    forecast_1_half = models.FloatField( # вычисляемое
        verbose_name='прогноз 1-е полугодие'
    )

    forecast_jul = models.FloatField(
        verbose_name='прогноз июль',
        default=0
    )
    forecast_aug = models.FloatField(
        verbose_name='прогноз август',
        default=0
    )
    forecast_sep = models.FloatField(
        verbose_name='прогноз сентябрь',
        default=0
    )
    forecast_IIIq = models.FloatField(  # вычисляемое
        verbose_name='прогноз 3-й квартал'
    )

    forecast_9mnth = models.FloatField(  # вычисляемое
        verbose_name='прогноз за 9 месяцев'
    )

    forecast_oct = models.FloatField(
        verbose_name='прогноз октябрь',
        default=0
    )
    forecast_nov = models.FloatField(
        verbose_name='прогноз ноябрь',
        default=0
    )
    forecast_dec = models.FloatField(
        verbose_name='прогноз декабрь',
        default=0
    )
    forecast_IVq = models.FloatField(  # вычисляемое
        verbose_name='прогноз 4-й квартал'
    )

    economy_total = models.FloatField(
        verbose_name='Экономия по заключенному договору, всего',
    )
    economy_Iq = models.FloatField(
        verbose_name='Экономия по заключенному договору за 1-й квартал',
    )
    economy_IIq = models.FloatField(
        verbose_name='Экономия по заключенному договору за 2-й квартал',
    )
    economy_IIIq = models.FloatField(
        verbose_name='Экономия по заключенному договору за 3-й квартал',
    )
    economy_IVq = models.FloatField(
        verbose_name='Экономия по заключенному договору за 4-й квартал',
    )

    fact_total = models.FloatField(  # вычисляемое
        verbose_name='факт, всего',
    )
    fact_Iq = models.FloatField(  # вычисляемое
        verbose_name='1-й квартал',
    )
    fact_jan = models.FloatField(
        verbose_name='факт январь',
        default=0
    )
    fact_feb = models.FloatField(
        verbose_name='факт февраль',
        default=0
    )
    fact_mar = models.FloatField(
        verbose_name='факт март',
        default=0
    )

    fact_IIq = models.FloatField(  # вычисляемое
        verbose_name='2-й квартал',
    )
    fact_apr = models.FloatField(
        verbose_name='факт апрель',
        default=0
    )
    fact_may = models.FloatField(
        verbose_name='факт май',
        default=0
    )
    fact_jun = models.FloatField(
        verbose_name='факт июнь',
        default=0
    )

    plane_sum_SAP_6mth = models.FloatField( # вычисляемое
        verbose_name='плановая сумма SAP за 6 месяцев'
    )

    fact_6mth = models.FloatField( # вычисляемое
        verbose_name='Факт за 6 месяцев'
    )

    fact_IIIq = models.FloatField(  # вычисляемое
        verbose_name='3-й квартал',
    )
    fact_jul = models.FloatField(
        verbose_name='факт июль',
    )
    fact_aug = models.FloatField(
        verbose_name='факт август',
        default=0
    )
    fact_sep = models.FloatField(
        verbose_name='факт сентябрь',
        default=0
    )

    plane_sum_SAP_9mth = models.FloatField(  # вычисляемое
        verbose_name='плановая сумма SAP за 9 месяцев'
    )

    fact_9mth = models.FloatField( # вычисляемое
        verbose_name='Факт за 9 месяцев'
    )

    fact_IVq = models.FloatField( # вычисляемое
        verbose_name='Факт за 4 квартал'
    )
    fact_oct = models.FloatField(
        verbose_name='факт октябрь',
        default=0
    )
    fact_10mth = models.FloatField( # вычисляемое
        verbose_name='факт 10 месяцев',
    )
    fact_nov = models.FloatField(
        verbose_name='факт ноябрь',
        default=0
    )
    fact_dec = models.FloatField(
        verbose_name='факт декабрь',
        default=0
    )

    economy_contract_result = models.FloatField(
        verbose_name='Экономия по результатам исполенения договоров всего'
    )
    economy_result_Iq = models.FloatField(
        verbose_name='Экономия по результатам исполенения договоров 1-й квартал',
        default=0
    )
    economy_result_IIq = models.FloatField(
        verbose_name='Экономия по результатам исполенения договоров 2-й квартал',
        default=0
    )
    economy_result_IIIq = models.FloatField(
        verbose_name='Экономия по результатам исполенения договоров 3-й квартал',
        default=0
    )
    economy_result_IVq = models.FloatField(
        verbose_name='Экономия по результатам исполенения договоров 4-й квартал',
        default=0
    )

    total_sum_unsigned_contracts = models.FloatField( # вычисляемое
        verbose_name='Сумма средств по незаключенным договорам'
    )

    economy_total_absolute = models.FloatField( # вычисляемое
        verbose_name='Абсолютная экономия по договору, всего'
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # TODO   contract_mode

    def __str__(self):
        try:
            return 'Договор %s, куратор %s, ст. фин %s' % (self.title,
                                                           self.curator,
                                                           self.finance_cost)
        except:
            return 'Ошибка в данных'

    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договоры'


class Planing(models.Model):
    pass

    def __str__(self):
        try:
            return 'Здесь пока ничего нет'
        except:
            return 'Ошибка в данных'

    class Meta:
        verbose_name = 'Планирование'
        verbose_name_plural = 'Планирование'
