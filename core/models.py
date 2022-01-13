from re import S
from statistics import mode
from django.db import models


class Criteria(models.Model):
    name = models.CharField(max_length=100)
    mark = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class SubCriteria(models.Model):
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    subunit = models.CharField(max_length=20)
    mark = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Observation(models.Model):
    message = models.CharField(max_length=300)

    def __str__(self):
        return self.message


class Soldier(models.Model):
    personal_no = models.PositiveBigIntegerField(unique=True)
    name = models.CharField(max_length=100)
    rank = models.CharField(max_length=20)
    address = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=20, blank=True)
    subunit = models.CharField(max_length=20)
    appointment = models.CharField(max_length=50)
    unit_join_date = models.DateField(blank=True)
    last_promotion_date = models.DateField(blank=True, null=True)
    contact = models.CharField(max_length=50)
    date_of_enrollment = models.DateField(blank=True)
    previous_subunit = models.CharField(max_length=20, blank=True, null=True)
    due_date_of_next_rank = models.DateField(blank=True)
    observations = models.ManyToManyField(Observation)

    def __str__(self):
        return self.name


class SoldierMark(models.Model):
    soldier = models.ForeignKey(Soldier, on_delete=models.CASCADE)
    sub_criteria = models.ForeignKey(SubCriteria, on_delete=models.CASCADE)
    mark = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.sub_criteria.name + ": " + str(self.mark)


class SoldierReport(models.Model):
    soldier = models.OneToOneField(Soldier, on_delete=models.CASCADE)
    evaluation_date_from = models.DateField()
    evaluation_date_to = models.DateField()
    medical_category = models.CharField(max_length=1)

    IPFT_first_biannual = models.PositiveIntegerField()
    IPFT_second_biannual = models.PositiveIntegerField()
    RET = models.PositiveBigIntegerField()
    DIV_order_letter_no_1 = models.CharField(max_length=100)
    DIV_order_letter_no_2 = models.CharField(max_length=100)
    DIV_order_letter_no_3 = models.CharField(max_length=100)

    fit_for_next_promotion = models.PositiveIntegerField(blank=True)
    fit_for_next_promotion_yes_text = models.CharField(max_length=100, blank=True)
    fit_for_next_promotion_no_text = models.CharField(max_length=100, blank=True)
    
    fit_for_being_instructor = models.PositiveIntegerField(blank=True)
    fit_for_being_instructor_yes_text = models.CharField(max_length=100, blank=True)
    fit_for_being_instructor_no_text = models.CharField(max_length=100, blank=True)

    fit_for_foreign_mission = models.PositiveIntegerField(blank=True)
    fit_for_foreign_mission_yes_text = models.CharField(max_length=100, blank=True)
    fit_for_foreign_mission_no_text = models.CharField(max_length=100, blank=True)

    recommendation_for_next_appt = models.CharField(max_length=100, blank=True)
    special_quality = models.CharField(max_length=100, blank=True)
    remarks_by_initiating_officer = models.CharField(max_length=100, blank=True)

    grade = models.PositiveBigIntegerField()

    def __str__(self):
        return f"Annual Report for {self.soldier.name}"


class SoldierExtra(models.Model):
    soldier = models.OneToOneField(Soldier, on_delete=models.CASCADE)
    medical_category = models.CharField(max_length=1)
    IPFT_first_biannual = models.BooleanField()
    IPFT_second_biannual = models.BooleanField()
    RET = models.BooleanField()