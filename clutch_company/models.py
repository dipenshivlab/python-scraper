from django.db import models

# Create your models here.


class Company(models.Model):
    company_name = models.TextField()
    website = models.TextField()
    location=models.TextField()
    min_project_size=models.TextField()
    hourly_rate=models.TextField()
    employee_size=models.TextField()
    linkedin_url=models.TextField() 
    position=models.TextField(default=None)

    # def __str__(self) -> str:
    #     return self.company_name


class Review(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE,related_name='company_review')
    client_name = models.TextField()
    client_company = models.TextField()
    position = models.TextField()
    industry = models.TextField()
    employee_size = models.TextField()
    location = models.TextField()
    review_for = models.TextField()
    review=models.TextField()
    review_date = models.TextField()
    project_category = models.TextField()
    project_budgets = models.TextField()
    project_duration = models.TextField()

