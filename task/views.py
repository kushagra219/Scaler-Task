from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Candidate, Interview, Interviewer, Slot
from .forms import InterviewScheduleForm, SlotForm
from django.contrib import messages
from datetime import datetime
from django.db.models import Q

# Create your views here.
# interviews list function 
def interview_list(request):
    interviews = Interview.objects.filter(Q(slot__date__gt=datetime.now().date()) | (Q(slot__date=datetime.now().date()) & Q(slot__start_time__gte=datetime.now().time())))
    context = {"interviews": interviews}
    return render(request, 'task/interview_list.html', context=context)

# check availability
def check_availability(slot_obj, interviewers, candidates):
    flag = False
    message_text = ""
    for i in interviewers:
        i_obj = Interviewer.objects.get(id=i)
        for j in i_obj.scheduled_slots.all():
            if slot_obj.is_overlapping(j):
                message_text += i_obj.interviewer_name + ", "
                flag = True
    for i in candidates:
        i_obj = Candidate.objects.get(id=i)
        for j in i_obj.scheduled_slots.all():
            if slot_obj.is_overlapping(j):
                message_text += i_obj.candidate_name + ", "
                flag = True
    return flag, message_text

# interview schedule function
def schedule_interview(request):
    if request.method == "POST":
        interviewers = request.POST['interviewers']
        candidates = request.POST['candidates']
        date = request.POST['date']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        interview_form = InterviewScheduleForm(request.POST)
        slot_form = SlotForm(request.POST)
        date_obj = datetime.strptime(request.POST['date'], "%Y-%m-%d").date()
        start_time_obj = datetime.strptime(request.POST['start_time'], "%H:%M").time()
        end_time_obj = datetime.strptime(request.POST['end_time'], "%H:%M").time()
        curr_date_obj = datetime.now().date()
        curr_time_obj = datetime.now().time()
        # print(date_obj, start_time_obj, end_time_obj)
        # print(end_time_obj < start_time_obj)
        # print(date_obj < datetime.now().date() )
        # print(start_time_obj < datetime.now().time())
        if not (start_time_obj <= end_time_obj and 
        (date_obj > curr_date_obj or (date_obj == curr_date_obj and start_time_obj >= curr_time_obj))):
            messages.error(request, 'Invalid Date, Start time or End time')
        else:
            slot_obj = Slot.objects.get_or_create(date=date, start_time=start_time, end_time=end_time)[0]
            flag, message_text = check_availability(slot_obj, interviewers, candidates)
            if flag:
                messages.error(request, message_text + 'are not available at this slot')
            else:
                interview_obj = Interview.objects.create(slot=slot_obj)
                for i in interviewers:
                    i_obj = Interviewer.objects.get(id=i)
                    interview_obj.interviewers.add(i_obj)
                    i_obj.scheduled_slots.add(slot_obj)
                for i in candidates:
                    i_obj = Candidate.objects.get(id=i)
                    interview_obj.candidates.add(i_obj)
                    i_obj.scheduled_slots.add(slot_obj)
                interview_obj.save()
                return redirect('task:thank-you')
    else:
        interview_form = InterviewScheduleForm()
        slot_form = SlotForm()
    return render(request, 'task/index.html', {'interview_form': interview_form, 'slot_form': slot_form})


# thank you function 
def thank_you(request):
    return render(request, 'task/thankyou.html')

 