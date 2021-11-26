from django.db import models


class Slot(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return str(self.date) + " " + str(self.start_time) + " - " + str(self.end_time)

    def is_overlapping(self, o):
        if self.date == o.date:
            if o.start_time <= self.end_time and o.end_time >= self.start_time:
                return True
        else:
            return False


class Interviewer(models.Model):
    interviewer_name = models.CharField(max_length=50)
    interviewer_email = models.EmailField(blank=True, null=True)
    scheduled_slots = models.ManyToManyField(Slot, blank=True)

    def __str__(self):
            return self.interviewer_name


class Candidate(models.Model):
    candidate_name = models.CharField(max_length=50)
    candidate_email = models.EmailField(blank=True, null=True)
    scheduled_slots = models.ManyToManyField(Slot, blank=True)
    
    def __str__(self):
        return self.candidate_name


class Interview(models.Model):
    interviewers = models.ManyToManyField(Interviewer)
    candidates = models.ManyToManyField(Candidate)
    slot = models.ForeignKey(Slot, on_delete=models.SET_NULL, null=True)
    # resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    
    def __str__(self):
        return str(self.id)

    def check_no_participants(self):
        return len(self.interviewers) >= 1 and len(self.candidates) >= 1

