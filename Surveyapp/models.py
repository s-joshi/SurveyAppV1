from django.db import models

from django.core.exceptions import ValidationError


class Organization(models.Model):
    """
    This is table for organization.
    """
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.company_name


class Employee(models.Model):
    emp_name = models.CharField(max_length=200)
    emp_username = models.CharField(max_length=100)
    emp_password = models.CharField(max_length=100)
    emp_designation = models.CharField(max_length=100)

    emp_address = models.CharField(max_length=200)
    company = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.emp_name

    class Meta:
        verbose_name_plural = 'Employees'


class Survey(models.Model):
    survey_name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    date = models.DateField()

    def __str__(self):
        return self.survey_name

    class Meta:
        verbose_name_plural = 'surveys'


def validate_list(value):
    """
    takes a text value and verifies that there is at least one comma
    :param value:
    :return:
    """
    values = value.split(',')
    if len(values) < 2:
        raise ValidationError(
            "The selected field requires an associated list of choices. Choices must contain more than one item.")


class Question(models.Model):
    TEXT = 'text'
    RADIO = ' radio '
    SELECT = 'select'
    SELECT_MULTIPLE = 'select-multiple'
    INTEGER = 'integer'

    Question_types = (
        (TEXT, 'text'),
        (RADIO, 'radio'),
        (SELECT, 'select'),
        (SELECT_MULTIPLE, 'Select Multiple'),
        (INTEGER, 'integer'),
    )
    question = models.TextField()
    is_required = models.BooleanField()
    question_type = models.CharField(max_length=200, choices=Question_types, default=TEXT)

    choices = models.TextField(blank=True,
                               null=True,
                               help_text='if the question type is "radio," "select," or '
                                         '"select multiple" provide a comma-separated list '
                                         'of options for this question .')

    def save(self, *args, **kwargs):
        if (self.question_type == Question.RADIO or self.question_type == Question.SELECT
                or self.question_type == Question.SELECT_MULTIPLE):
            validate_list(self.choices)
        super(Question, self).save(*args, **kwargs)

    def get_choices(self):
        """
        parse the choices field and return a tuple formatted appropriately
        for the 'choices' argument of a form widget.
        """
        choices = self.choices.split(',')
        return choices

    def __str__(self):
        return self.question


class SurveyEmployee(models.Model):
    employee = models.ManyToManyField(Employee)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)


class SurveyQuestion(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ManyToManyField(Question)


class SurveyResponse(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.TextField(blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)
    SaveStatus = models.BooleanField(default=False)
