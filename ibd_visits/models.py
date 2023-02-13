from django.db import models


TIME = (
    (1, "8:00"),
    (2, "8:30"),
    (3, "9:00"),
    (4, "9:30"),
    (5, "10:00"),
    (6, "10:30"),
    (7, "11:00"),
    (8, "11:30"),
    (9, "12:00"),
    (10, "12:30"),
    (11, "13:00"),
    (12, "13:30"),
    (13, "14:00"),
    (14, "14:30"),
    (15, "15:00"),
    (16, "15:30"),
    (17, "16:00"),
    (18, "16:30"),
    (19, "17:00"),
    (20, "17:30")
)


class VisitTerm(models.Model):
    date = models.DateField(null=False)
    time = models.IntegerField(choices=TIME, null=False)


class DoctorVisit(models.Model):
    doctor = models.ForeignKey('ibd_website.Doctor', on_delete=models.CASCADE)
    visit_term = models.ForeignKey(VisitTerm, on_delete=models.CASCADE)
    is_free = models.BooleanField(default=True, null=False)


class MedicalVisit(models.Model):
    patient = models.ForeignKey('ibd_website.User', on_delete=models.CASCADE, related_name="pat")
    doctor = models.ForeignKey('ibd_website.User', on_delete=models.CASCADE, related_name="doc")
    visit_term = models.OneToOneField(DoctorVisit, on_delete=models.PROTECT, default=None)
    reservation_date = models.DateTimeField(auto_now_add=True)
