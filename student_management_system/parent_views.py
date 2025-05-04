from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from app.models import Parent, Student, Subject, Session_Year, Attendance_Report, StudentResult
from django.contrib import messages
import openpyxl
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import io

@login_required(login_url='/')
def HOME(request):
    parent = Parent.objects.get(admin=request.user)
    student = parent.student
    results = StudentResult.objects.filter(student_id=student)
    attendance_reports = Attendance_Report.objects.filter(student_id=student).count()
    context = {
        'student': student,
        'results_count': results.count(),
        'attendance_count': attendance_reports,
    }
    return render(request, 'Parent/home.html', context)

@login_required(login_url='/')
def VIEW_ATTENDANCE(request):
    parent = Parent.objects.get(admin=request.user)
    student = parent.student
    subjects = Subject.objects.filter(course=student.course_id)
    session_years = Session_Year.objects.all()
    action = request.GET.get('action')
    get_subject = None
    get_session_year = None
    attendance_report = None

    if action == 'show_attendance' and request.method == "POST":
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        try:
            if subject_id and subject_id.isdigit() and session_year_id and session_year_id.isdigit():
                get_subject = Subject.objects.get(id=int(subject_id))
                get_session_year = Session_Year.objects.get(id=int(session_year_id))
                if get_subject.course != student.course_id or get_session_year.id != student.session_year_id.id:
                    messages.error(request, "Invalid subject or session year selected.")
                    return redirect('parent_view_attendance')
                attendance_report = Attendance_Report.objects.filter(
                    student_id=student,
                    attendance_id__subject_id=get_subject,
                    attendance_id__session_year_id=get_session_year
                ).order_by('attendance_id__attendance_data')
            else:
                messages.error(request, "Please select a valid subject and session year.")
                return redirect('parent_view_attendance')
        except Subject.DoesNotExist:
            messages.error(request, "Selected subject does not exist.")
            return redirect('parent_view_attendance')
        except Session_Year.DoesNotExist:
            messages.error(request, "Selected session year does not exist.")
            return redirect('parent_view_attendance')

    if 'download' in request.GET and request.GET['download'] == 'excel':
        subject_id = request.GET.get('subject_id')
        session_year_id = request.GET.get('session_year_id')
        try:
            get_subject = Subject.objects.get(id=int(subject_id))
            get_session_year = Session_Year.objects.get(id=int(session_year_id))
            if get_subject.course != student.course_id or get_session_year.id != student.session_year_id.id:
                messages.error(request, "Invalid subject or session year selected.")
                return redirect('parent_view_attendance')
            attendance_report = Attendance_Report.objects.filter(
                student_id=student,
                attendance_id__subject_id=get_subject,
                attendance_id__session_year_id=get_session_year
            ).order_by('attendance_id__attendance_data')
        except (Subject.DoesNotExist, Session_Year.DoesNotExist, ValueError):
            messages.error(request, "Invalid subject or session year selected.")
            return redirect('parent_view_attendance')

        if attendance_report.exists():
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Attendance"
            ws.append(["Date", "Status"])
            for report in attendance_report:
                ws.append([report.attendance_id.attendance_data.strftime('%Y-%m-%d'), "Present" if report.status == 1 else "Absent"])
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename=attendance_{student.admin.first_name}_{get_subject.name}.xlsx'
            wb.save(response)
            return response
        else:
            messages.error(request, "No attendance data available to export.")
            return redirect('parent_view_attendance')

    context = {
        'subjects': subjects,
        'session_years': session_years,
        'action': action,
        'get_subject': get_subject,
        'get_session_year': get_session_year,
        'attendance_report': attendance_report,
        'student': student,
    }
    return render(request, 'Parent/view_attendance.html', context)

@login_required(login_url='/')
def VIEW_RESULT(request):
    parent = Parent.objects.get(admin=request.user)
    student = parent.student
    results = StudentResult.objects.filter(student_id=student)

    if 'download' in request.GET and request.GET['download'] == 'pdf':
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        normal_style = styles['Normal']

        elements.append(Paragraph(f"Results for {student.admin.first_name}", title_style))
        elements.append(Paragraph(f"ID: {student.admin.id}", normal_style))
        elements.append(Paragraph("<br/><br/>", normal_style))

        data = [['Subject', 'Assignment', 'Exam', 'IA1', 'IA2', 'Attendance', 'Mid Sem', 'End Sem', 'Total', 'CGPA']]
        for result in results:
            data.append([
                result.subject_id.name,
                str(result.assignment_mark) if result.assignment_mark is not None else '-',
                str(result.exam_mark) if result.exam_mark is not None else '-',
                str(result.ia1_mark) if result.ia1_mark is not None else '-',
                str(result.ia2_mark) if result.ia2_mark is not None else '-',
                str(result.attendance_mark) if result.attendance_mark is not None else '-',
                str(result.midsem_mark) if result.midsem_mark is not None else '-',
                str(result.end_sem_mark) if result.end_sem_mark is not None else '-',
                str(result.total_mark) if result.total_mark is not None else '-',
                str(result.calculate_cgpa()) if result.calculate_cgpa() is not None else '-'
            ])

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)

        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=results_{student.admin.username}.pdf'
        response.write(pdf)
        return response

    context = {
        'results': results,
        'student': student,
    }
    return render(request, 'Parent/view_result.html', context)