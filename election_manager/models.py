from django.contrib.auth.models import User
from django.db import models


class ElectionEvent(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    election = models.ForeignKey('ElectionEvent', related_name='positions', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} ({self.election.name})"


class Option(models.Model):
    ballot = models.ForeignKey('Ballot', related_name='options', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='option_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.ballot.title})"


class Ballot(models.Model):
    election_event = models.ForeignKey('ElectionEvent', related_name='ballots', on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    instructions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.election_event.name}"


class VoterProfile(models.Model):
    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField('auth.User', related_name='voter_profile', on_delete=models.CASCADE)
    cnp = models.CharField(max_length=13, unique=True)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=20)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state_or_region = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)
    occupation = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.cnp}"

class Vote(models.Model):
    voter = models.ForeignKey(User, related_name='vote_records', on_delete=models.CASCADE)
    option = models.ForeignKey('Option', related_name='vote_records', on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter', 'option')

    def __str__(self):
        return f"{self.voter.username} voted for {self.option.name}"


class ElectionLog(models.Model):
    election_event = models.ForeignKey(ElectionEvent, related_name='audit_logs', on_delete=models.CASCADE)
    action_performed_by = models.ForeignKey(User, related_name='audit_actions', on_delete=models.SET_NULL, null=True)
    action_description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_display = self.action_performed_by.username if self.action_performed_by else "System"
        return f"{user_display}: {self.action_description} at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"