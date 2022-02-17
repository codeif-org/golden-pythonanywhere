from django.shortcuts import render, HttpResponse, redirect
import json
from django.urls import reverse
# zip -r /tmp/backup.zip /home/mayurguptacode/fms-golden
# from sympy import print_rcode
from fee.models import *
from school.models import Classes, Student, Current, Session
from reports.models import Backup
import pandas as pd
import os
from datetime import date, timedelta
import pyminizip
import xlsxwriter

from FeeManagement.settings import MEDIA_BASE, DOMAIN_BASE

# Create your views here.

def generate(request):
    class_qs = Classes.objects.all().order_by('class_no')
    return render(request, 'generate.html', {'class_qs': class_qs})

# ?date=YYYY-MM-DD
def dayReportAPI(request):
    current = Current.objects.all()[0]
    if 'date' in request.GET:
        print(request.GET['date'])
        date = request.GET['date']
        fee_submit_qs = FeeSubmit.objects.filter(submit_date=request.GET['date'], session=current.session)
        print(fee_submit_qs)
        report_dict = {
            'add_no': [],
            'name': [],
            'father_name': [],
            'class': [],
            'memo_no': [],
            'amount': [],
        }
        for fee_submit_q in fee_submit_qs:
            report_dict['add_no'].append(fee_submit_q.student.add_no)
            report_dict['name'].append(fee_submit_q.student.fname)
            report_dict['father_name'].append(fee_submit_q.student.fathername)
            report_dict['class'].append(fee_submit_q.student.Class.clas)
            report_dict['memo_no'].append(fee_submit_q.memo_no)
            report_dict['amount'].append(fee_submit_q.amount)
        # print("report_dict", report_dict)
        report_df = pd.DataFrame(report_dict)
        # print("report_df", report_df)

        # # number of files in reports folder
        # print("Number of files in reports folder: ", len(os.listdir("media/excel_reports/day_wise")))
        # # file_number = len(os.listdir("media/excel_reports/day_wise")) + 1
        # # excel export
        # report_df.index += 1
        # writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
        # # df.to_excel(writer, sheet_name='Sheet1')
        # writer.save()
        # report_df.to_excel('/home/mayurguptacode/fms-golden/media/excel_reports/day_wise/fee_report1.xlsx')
        # print("report saved")


        # xlsx writer
        file_path = f"{MEDIA_BASE}media/excel_reports/day_wise/day_fee_report.xlsx"
        workbook = xlsxwriter.Workbook(file_path)
        bold = workbook.add_format({'bold': True})
        # By default worksheet names in the spreadsheet will be
        # Sheet1, Sheet2 etc., but we can also specify a name.
        # worksheet.write(row, column, data, cell_format)
        worksheet = workbook.add_worksheet("Sheet1")
        worksheet.write(0, 0, date, bold)
        worksheet.write(1, 0, "Add No", bold)
        worksheet.write(1, 1, "Name", bold)
        worksheet.write(1, 2, "Father Name", bold)
        worksheet.write(1, 3, "Class", bold)
        worksheet.write(1, 4, "Memo No", bold)
        worksheet.write(1, 5, "Amount", bold)

        # Start from the first cell. Rows and
        # columns are zero indexed.
        row = 2

        # Iterate over the data and write it out row by row.
        for index, item in report_df.iterrows():
            worksheet.write(row, 0, item[0])
            worksheet.write(row, 1, item[1])
            worksheet.write(row, 2, item[2])
            worksheet.write(row, 3, item[3])
            worksheet.write(row, 4, item[4])
            worksheet.write(row, 5, item[5])
            row += 1

        workbook.close()
        return HttpResponse(json.dumps({"msg": "Report generated successfully", "file_path": "/media/excel_reports/day_wise/day_fee_report.xlsx"}), content_type="application/json")
        # return HttpResponse(json.dumps({"msg": "Report generated successfully"}), content_type="application/json")

    return HttpResponse(json.dumps({"msg": "dayReportAPI is being baked"}), content_type="application/json")

# ?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
def dateReportAPI(request):
    current = Current.objects.all()[0]
    if 'start_date' in request.GET:
        print(request.GET)
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        delta = timedelta(days=1)
        start_date_ = date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
        end_date_ = date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))

        # report generation
        report_dict = {
            'date': [],
            'amount': [],
            'no_of_transactions': [],
        }
        while start_date_ <= end_date_:
            print(start_date_)
            fee_submit_qs = FeeSubmit.objects.filter(submit_date=start_date_, session=current.session)
            # print("fee submit qs", fee_submit_qs)
            # iterate over fee_submit_qs to get the total amount and no of transactions for a date
            report_dict['date'].append(start_date_)
            current_date_amount = 0
            current_date_transactions = 0
            for fee_submit_q in fee_submit_qs:
                current_date_amount += fee_submit_q.amount
                current_date_transactions += 1
            report_dict['amount'].append(current_date_amount)
            report_dict['no_of_transactions'].append(current_date_transactions)
            start_date_ += delta
        # print("report_dict", report_dict)     # report_dict = {'date': ['2020-01-01', '2020-01-02', '2020-01-03'], 'amount': [0, 0, 0], 'no_of_transactions': [0, 0, 0]}

        # create dataframe
        report_df = pd.DataFrame(report_dict)
        # print("report_df", report_df)

        # # number of files in reports folder
        # print("Number of files in reports folder: ", len(os.listdir("media/excel_reports/date_wise")))
        # file_number = len(os.listdir("media/excel_reports/date_wise")) + 1
        # # excel export
        # report_df.index += 1
        # file_path = f'media/excel_reports/date_wise/{start_date}to{end_date}_fee_report_{file_number}.xlsx'
        # report_df.to_excel(file_path)
        # print("report saved")

        # xlsx writer
        file_path = f"{MEDIA_BASE}media/excel_reports/date_wise/datewise_fee_report.xlsx"
        workbook = xlsxwriter.Workbook(file_path)
        bold = workbook.add_format({'bold': True})
        # By default worksheet names in the spreadsheet will be
        # Sheet1, Sheet2 etc., but we can also specify a name.
        # worksheet.write(row, column, data, cell_format)
        worksheet = workbook.add_worksheet("Sheet1")
        worksheet.write(0, 0, "Date", bold)
        worksheet.write(0, 1, "Amount Recieved", bold)
        worksheet.write(0, 2, "No. of Transactions", bold)

        # Start from the first cell. Rows and
        # columns are zero indexed.
        row = 1

        # Iterate over the data and write it out row by row.
        for index, item in report_df.iterrows():
            worksheet.write(row, 0, item[0].strftime("%d-%m-%Y"))
            worksheet.write(row, 1, item[1])
            worksheet.write(row, 2, item[2])
            row += 1

        workbook.close()
        return HttpResponse(json.dumps({"msg": "Report generated successfully", "file_path": "/media/excel_reports/date_wise/datewise_fee_report.xlsx"}), content_type="application/json")
    return HttpResponse(json.dumps({"msg": "dateReportAPI is being baked"}), content_type="application/json")

# date wise report with details
# ?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
def dateWithDReportAPI(request):
    current = Current.objects.all()[0]
    if 'start_date' in request.GET:
        print(request.GET)
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        delta = timedelta(days=1)
        start_date_ = date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
        end_date_ = date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))

        # report generation
        report_dict = {
            'date': [],
            'add_no': [],
            'name': [],
            'father_name': [],
            'class': [],
            'memo_no': [],
            'amount': [],
        }
        while start_date_ <= end_date_:
            print(start_date_)
            fee_submit_qs = FeeSubmit.objects.filter(submit_date=start_date_, session=current.session)
            # print("fee submit qs", fee_submit_qs)
            # iterate over fee_submit_qs to get the total amount and no of transactions for a date
            # report_dict['date'].append(start_date_)
            # current_date_amount = 0
            # current_date_transactions = 0
            # for fee_submit_q in fee_submit_qs:
            #     current_date_amount += fee_submit_q.amount
            #     current_date_transactions += 1
            # report_dict['amount'].append(current_date_amount)
            # report_dict['no_of_transactions'].append(current_date_transactions)
            for fee_submit_q in fee_submit_qs:
                report_dict['date'].append(start_date_)
                report_dict['add_no'].append(fee_submit_q.student.add_no)
                report_dict['name'].append(fee_submit_q.student.fname)
                report_dict['father_name'].append(fee_submit_q.student.fathername)
                report_dict['class'].append(fee_submit_q.student.Class.clas)
                report_dict['memo_no'].append(fee_submit_q.memo_no)
                report_dict['amount'].append(fee_submit_q.amount)
            start_date_ += delta
        # print("report_dict", report_dict)     # report_dict = {'date': ['2020-01-01', '2020-01-02', '2020-01-03'], 'amount': [0, 0, 0], 'no_of_transactions': [0, 0, 0]}

        # create dataframe
        report_df = pd.DataFrame(report_dict)
        # print("report_df", report_df)

        # number of files in reports folder
        # print("Number of files in reports folder: ", len(os.listdir("media/excel_reports/date_wise_with_detail")))
        # file_number = len(os.listdir("media/excel_reports/date_wise_with_detail")) + 1
        # # excel export
        # report_df.index += 1
        # file_path = f'media/excel_reports/date_wise_with_detail/{start_date}to{end_date}_DWWD_fee_report_{file_number}.xlsx'
        # report_df.to_excel(file_path)
        # print("report saved")

        workbook = xlsxwriter.Workbook(f'{MEDIA_BASE}media/excel_reports/date_wise_with_detail/DWWD_fee_report.xlsx')
        bold = workbook.add_format({'bold': True})
        # By default worksheet names in the spreadsheet will be
        # Sheet1, Sheet2 etc., but we can also specify a name.
        # worksheet.write(row, column, data, cell_format)
        worksheet = workbook.add_worksheet("Sheet1")
        # worksheet.write(0, 0, date, bold)
        worksheet.write(0, 0, "Date", bold)
        worksheet.write(0, 1, "Add No", bold)
        worksheet.write(0, 2, "Name", bold)
        worksheet.write(0, 3, "Father Name", bold)
        worksheet.write(0, 4, "Class", bold)
        worksheet.write(0, 5, "Memo No", bold)
        worksheet.write(0, 6, "Amount", bold)

        # Start from the first cell. Rows and
        # columns are zero indexed.
        row = 1

        # Iterate over the data and write it out row by row.
        for index, item in report_df.iterrows():
            worksheet.write(row, 0, item[0].strftime("%d-%m-%Y"), bold)
            worksheet.write(row, 1, item[1])
            worksheet.write(row, 2, item[2])
            worksheet.write(row, 3, item[3])
            worksheet.write(row, 4, item[4])
            worksheet.write(row, 5, item[5])
            worksheet.write(row, 6, item[6])
            row += 1


        workbook.close()
        return HttpResponse(json.dumps({"msg": "Report generated successfully", "file_path": "/media/excel_reports/date_wise_with_detail/DWWD_fee_report.xlsx"}), content_type="application/json")
    return HttpResponse(json.dumps({"msg": "dateReportAPI is being baked"}), content_type="application/json")
# must create whole FeeSubmitByMonth objects for all of the students in start

# list of defaulters
# to get the month name
# datetime.date.today().strftime("%B")
# strftime is used to convert date to string
# https://www.programiz.com/python-programming/datetime/strftime
# make a list of all the students who have not paid the fee
# take time delta between today and the due_date of the fee then divide it by 30
# if it is greater than 1, then it is a defaulter

# find due month first
# if today is 13 date and this month_no is 4 then due_month_no is 3
# if today is 16 date and this month_no is 4 then due_month_no is 4
# now find the defaulters by comparing the month_no of the fee_submit_by_month with the due_month_no
def defaulters(request):
    current = Current.objects.all()[0]
    # order by class of students
    fee_submit_by_month_qs = FeeSubmitByMonth.objects.filter(session=current.session).order_by('student__Class__class_no')
    # print(fee_submit_by_month_qs)
    # today = date.today()
    # today = date(2020, 8, 18) # for testing
    today = datetime.date.today()
    today_month = today.strftime("%B")
    # print("today_month", today_month)
    today_month_no = Month.objects.get(month=today_month).month_no
    # print("today_month_no", today_month_no)
    if today.day > 15:
        due_month_no = today_month_no
    else:
        due_month_no = today_month_no - 1
    # print("due_month_no", due_month_no)

    # now check for defaulters
    # fee_submit_by_month_q: [defaulters_months_string, defaulter_amount]
    defaulters_list = []
    global defaulters_dict
    defaulters_dict = {}
    for fee_submit_by_month_q in fee_submit_by_month_qs:
        def_class = fee_submit_by_month_q.student.Class
        due_months = due_month_no - fee_submit_by_month_q.month_no
        # print("due_months", due_months)
        if due_months > 0:
            defaulters_list.append(fee_submit_by_month_q)
            due_month_start = fee_submit_by_month_q.month_no + 1
            def_month_str = ""
            def_amount = 0
            while due_month_start <= due_month_no:
                # print("due_month_start", due_month_start)
                # due_month_start += 1
                due_month_obj = Month.objects.get(month_no=due_month_start)
                def_month_str = def_month_str + due_month_obj.month + " "
                def_amount += FeeStructByMonth.objects.get(clas=def_class, month=due_month_obj, session=current.session).amount
                due_month_start += 1
            # print("def_month_str", def_month_str)
            # print("def_amount", def_amount)
            defaulters_dict[fee_submit_by_month_q] = [def_amount, def_month_str]
    # print("defaulters_list", defaulters_list)
    # print("defaulters_dict", defaulters_dict)

    defaulters.default = defaulters_dict
    return render(request, 'defaulters.html', {'defaulters_dict': defaulters_dict})

# db_backup by pyminizip
# creates password protected zip file
# pyminizip.compress("db.sqlite3", "/temp", "db_backups/example2.zip", "help", 5)


# students cumulative fee report
def studCumulative(request):
    current = Current.objects.all()[0]
    if 'class_id' in request.GET:
        class_id = request.GET['class_id']
        if class_id == "all":
            student_qs = Student.objects.filter(session=current.session)
            class_name = "All Classes"
        else:
            student_qs = Student.objects.filter(Class=class_id, session=current.session)
            class_name = student_qs[0].Class.name
        # print("student_qs", student_qs)
        fee_submit_by_month_qs = FeeSubmitByMonth.objects.filter(student__in=student_qs)
        # print("fee_submit_by_month_qs", fee_submit_by_month_qs)
        # report dict
        report_dict = {
            'Admission No.': [],
            'Name': [],
            'Father Name': [],
            'Class': [],
            'Total Session Fee': [],
            'Fee Paid': [],
            'Fee Left': [],
            'Advances': [],
            'Month No. Paids': [],
            'Last Fee Date': [],
        }
        for fee_submit_by_month_q in fee_submit_by_month_qs:
            report_dict['Admission No.'].append(fee_submit_by_month_q.student.add_no)
            report_dict['Name'].append(fee_submit_by_month_q.student.fname)
            report_dict['Father Name'].append(fee_submit_by_month_q.student.fathername)
            report_dict['Class'].append(fee_submit_by_month_q.student.Class.clas)
            report_dict['Total Session Fee'].append(fee_submit_by_month_q.total_session_fee)
            report_dict['Fee Paid'].append(fee_submit_by_month_q.session_fee_submitted)
            report_dict['Fee Left'].append(fee_submit_by_month_q.session_fee_left)
            report_dict['Advances'].append(fee_submit_by_month_q.advanced_amount)
            report_dict['Month No. Paids'].append(fee_submit_by_month_q.month_no)
            report_dict['Last Fee Date'].append(fee_submit_by_month_q.date)
        # print("report_dict", report_dict)
        # dataframe
        report_df = pd.DataFrame(report_dict)
        # print("report_df", report_df)

        # # number of files in reports folder
        # print("Number of files in reports folder: ", len(os.listdir("media/excel_reports/students_cumulative")))
        # file_number = len(os.listdir("media/excel_reports/students_cumulative")) + 1
        # # excel export
        # report_df.index += 1
        # file_path = f'media/excel_reports/students_cumulative/students_cumulative_fee_report_{file_number}.xlsx'
        # report_df.to_excel(file_path)

        workbook = xlsxwriter.Workbook(f'{MEDIA_BASE}media/excel_reports/students_cumulative/students_cumulative_fee_report.xlsx')
        bold = workbook.add_format({'bold': True})
        # By default worksheet names in the spreadsheet will be
        # Sheet1, Sheet2 etc., but we can also specify a name.
        # worksheet.write(row, column, data, cell_format)
        worksheet = workbook.add_worksheet("Sheet1")
        # worksheet.write(0, 0, date, bold)
        worksheet.write(0, 0, "Add No", bold)
        worksheet.write(0, 1, "Name", bold)
        worksheet.write(0, 2, "Father Name", bold)
        worksheet.write(0, 3, "Class", bold)
        worksheet.write(0, 4, "Total Session Fee", bold)
        worksheet.write(0, 5, "Fee Paid", bold)
        worksheet.write(0, 6, "Fee Left", bold)
        worksheet.write(0, 7, "Advances", bold)
        worksheet.write(0, 8, "Month No. Paids", bold)
        worksheet.write(0, 9, "Last Fee Date", bold)

        # Start from the first cell. Rows and
        # columns are zero indexed.
        row = 1

        # Iterate over the data and write it out row by row.
        for index, item in report_df.iterrows():
            worksheet.write(row, 0, item[0])
            worksheet.write(row, 1, item[1])
            worksheet.write(row, 2, item[2])
            worksheet.write(row, 3, item[3])
            worksheet.write(row, 4, item[4])
            worksheet.write(row, 5, item[5])
            worksheet.write(row, 6, item[6])
            worksheet.write(row, 7, item[7])
            worksheet.write(row, 8, item[8])
            worksheet.write(row, 9, item[9])
            row += 1


        workbook.close()
        print("report saved")
        return HttpResponse(json.dumps({"msg": "Report generated successfully", "file_path": "/media/excel_reports/students_cumulative/students_cumulative_fee_report.xlsx", "class_name": class_name}), content_type="application/json")
    return HttpResponse(json.dumps({"msg": "student cumulative report is being baked"}), content_type="application/json")

def backup(request):
    backup_paths = [ "/media/db_backups/" + file for file in os.listdir(MEDIA_BASE+"media/db_backups/")]
    # backup_size = [round(os.path.getsize(file)/1024, 1) for file in backup_paths]
    backup_names = os.listdir(MEDIA_BASE + "media/db_backups/")
    backup_index = list(range(len(backup_paths)))
    backup_dict = dict(zip(backup_index, zip(backup_paths, backup_names)))
    backup_dict_rev = dict(reversed(list(backup_dict.items())))
    if 'action' in request.GET:
        # number of files in reports folder
        print("Number of files in db_backups folder: ", len(os.listdir(MEDIA_BASE + "media/db_backups/")))
        file_number = len(os.listdir(MEDIA_BASE + "media/db_backups/")) + 1
        today_date = date.today()
        file_path = f"{MEDIA_BASE}media/db_backups/backup_{today_date}_{file_number}.zip"
        pyminizip.compress("/home/mayurguptacode/fms-golden/db.sqlite3", "/temp", file_path, "help", 5)
        backup_obj = Backup()
        backup_obj.save()
        return HttpResponse(json.dumps({"msg": "Backup generated successfully", "backup_url": f'/media/db_backups/backup_{today_date}_{file_number}.zip'}), content_type="application/json")
    # print("backup_paths", backup_paths)
    # print("backup_size", backup_size)
    # print("backup_names", backup_names)
    # print("backup_index", backup_index)
    # print("backup_dict", backup_dict)
    # print("backup_dict_rev", backup_dict_rev)
    return render(request, 'backup.html', {'backup_dict': backup_dict_rev})

def defaultersNotice(request):
    class_qs = Classes.objects.all()
    defaulters(request)
    # print(defaulters.default)
    defaulters_dict = defaulters.default
    # print("defaulters_dict", defaulters_dict)

    return render(request, 'defaultersnotice.html', {'class_qs': class_qs, 'defaulters_dict': defaulters_dict})