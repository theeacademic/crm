from django.db import models

class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15,blank=True)
    address = models.TextField(blank=True)
    passport = models.CharField(max_length=100, blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)
    contact2 = models.CharField(max_length=15, blank=True, null=True)
    medical = models.CharField(max_length=100, blank=True, null=True)
    pcc = models.CharField(max_length=100, blank=True, null=True)
    registration_status = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    travel = models.CharField(max_length=100, blank=True, null=True)
    interview = models.CharField(max_length=100,null=True, blank=True)
    office = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.CharField(max_length=100,null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    field = models.CharField(max_length=100, blank=True, null=True)  # Example field
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)  # New comments field
    created_at = models.DateTimeField(auto_now_add=True)
    
class Housemaid(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15, blank=True, null=True)
    passport = models.CharField(max_length=100, blank=True, null=True)
    training = models.CharField(max_length=100, blank=True, null=True)
    exit = models.CharField(max_length=100, blank=True, null=True)
    office = models.CharField(max_length=100, blank=True, null=True)
    next_of_kin = models.JSONField(null=True, blank=True)
    medical = models.CharField(max_length=100, blank=True, null=True)
    pcc = models.CharField(max_length=100, blank=True, null=True)
    travel = models.CharField(max_length=100, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)  # New comments field
    created_at = models.DateTimeField(auto_now_add=True)

class NextOfKin(models.Model):
    housemaid = models.ForeignKey(Housemaid, related_name="next_of_kins", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)
    contact = models.CharField(max_length=15, blank=True, null=True)
    phone = models.CharField(max_length=15)
    contact2 = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.field})"
    
    
