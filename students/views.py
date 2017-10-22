#Emergency Edit Protocol : 10/20/2017

from __future__ import unicode_literals

import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from home.models import *
from django.utils import timezone




@login_required(login_url="/login/")
def dashboard(request):
    return render(request, "student/dashboard.html", {})



@login_required(login_url="/login/")
def viewattendance(request):
    try:
        user = request.user;                                                 
        userPersonnelObj=Personnel.objects.filter(LDAP=user)
        MyCourses = Students_Courses.objects.filter(Student_ID=userPersonnelObj[0].Person_ID); 
        CourseAttendanceContext  = [];

        for course in MyCourses:
            AttendanceSessions = Attendance_Session.objects.filter(Course_Slot = course.Course_ID.Course_ID)
            classesPresent = 0
            totalClasses = 0
            absentDays = []
            for sessions in AttendanceSessions:
                try:
                    attendanceObject = Attendance.objects.filter(Student_ID = userPersonnelObj[0].Person_ID,ASession_ID=sessions.Session_ID)
                    
                    totalClasses += 1
                    if(attendanceObject[0].Marked == 'P'):
                        classesPresent += 1
                    elif(attendanceObject[0].Marked == 'A'):
                        absentDays.append(attendanceObject[0].Date_time)
                except:
                    pass
            retObj = dict(course=course,present = classesPresent,total = totalClasses,absentDays = absentDays)
            CourseAttendanceContext.append(retObj)
        context = dict(CourseAttendanceContext=CourseAttendanceContext)
    except:
        context = dict(ErrorMessage = "No Registered Classes")
    return render(request, "student/ViewAttendance.html", context)




def AssgnSubStatusPending(request):
    user =  request.user;
    pendingAssignments = []
    StudentObject=Personnel.objects.filter(LDAP=user.id)
    CoursesByStudent = Students_Courses.objects.filter(Student_ID=StudentObject[0].Person_ID)
    for course in CoursesByStudent:
        AssignmentsForCourse = Assignment.objects.filter(Course_ID = course.Course_ID.Course_ID)
        for assignment in AssignmentsForCourse:
            submissionsByStudent = Submissions.objects.filter(Assign_ID = assignment,Student_ID = StudentObject[0].Person_ID)
            if(submissionsByStudent.count() == 0):
                now = timezone.now()
                if (assignment.End_Time > now):
                    assignContextObject = dict(Course = course,assignment = assignment)
                    pendingAssignments.append(assignContextObject)
    return render(request, 'student/AssgnSubStatusPending.html', dict(pendingAssignments=pendingAssignments))




def AssgnSubStatusOverdue(request):
    user =  request.user;
    overdueAssignments = []
    StudentObject=Personnel.objects.filter(LDAP=user.id)
    CoursesByStudent = Students_Courses.objects.filter(Student_ID=StudentObject[0].Person_ID)
    for course in CoursesByStudent:
        AssignmentsForCourse = Assignment.objects.filter(Course_ID = course.Course_ID.Course_ID)
        for assignment in AssignmentsForCourse:
            submissionsByStudent = Submissions.objects.filter(Assign_ID = assignment,Student_ID = StudentObject[0].Person_ID)
            if(submissionsByStudent.count() == 0):
                now = timezone.now()
                if (assignment.End_Time < now):
                    assignContextObject = dict(Course = course,assignment = assignment)
                    overdueAssignments.append(assignContextObject)
    return render(request, 'student/AssgnSubStatusOverdue.html', dict(overdueAssignments=overdueAssignments))





def AssgnSubStatusSubmitted(request):
    user =  request.user;
    submittedAssignments = []
    StudentObject=Personnel.objects.filter(LDAP=user.id)
    CoursesByStudent = Students_Courses.objects.filter(Student_ID=StudentObject[0].Person_ID)
    for course in CoursesByStudent:
        AssignmentsForCourse = Assignment.objects.filter(Course_ID = course.Course_ID.Course_ID)
        for assignment in AssignmentsForCourse:
            submissionsByStudent = Submissions.objects.filter(Assign_ID = assignment,Student_ID = StudentObject[0].Person_ID)
            if(submissionsByStudent.count() != 0):
                assignContextObject = dict(Course = course,assignment = assignment,submission = submissionsByStudent)
                submittedAssignments.append(assignContextObject)
    return render(request, 'student/AssgnSubStatusSubmitted.html', dict(submittedAssignments=submittedAssignments))
