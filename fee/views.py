from django.contrib.admin.decorators import register
from django.shortcuts import render, HttpResponse, redirect
from school.models import Classes, School, Student, Session, Current
from fee.models import *
from fee.customs import partialUpdateFeeStructByMonth, txnNumber
from django.contrib import messages
import json
from datetime import date

# Create your views here.
def selectClass(request):
    # return HttpResponse("selectClass")
    user = request.user
    schoolobj = School.objects.get(user=user)
    # print(schoolobj)
    class_qs = Classes.objects.filter(school=schoolobj).order_by('class_no')
    # print(class_qs)
    return render(request, 'selectclass.html', {'classes': class_qs})

def selectMonth(request, class_id):
    classobj = Classes.objects.get(id=class_id)
    print(classobj)
    # fee_qs = FeeStruct.objects.filter(clas=classobj)
    # print(fee_qs)
    fee_struct_by_month_qs = FeeStructByMonth.objects.filter(clas=classobj, session=Current.objects.all()[0].session) 
    print(fee_struct_by_month_qs)
    return render(request, 'selectmonth.html', {'fee_struct_qs': fee_struct_by_month_qs, 'class': classobj}) 

def feeEdit(request, clas_id, month_id):
    clas = Classes.objects.get(id = clas_id)
    month = Month.objects.get(id = month_id)
    # total = 0
    admin = request.user
    school = School.objects.get(user = admin)
    classes = Classes.objects.filter(school = school) 
    current = Current.objects.all()[0]
    fees = FeeStruct.objects.filter(clas__in = classes, session=current.session) 
    month_fee = FeeStruct.objects.filter(clas = clas, month = month, session=current.session)
    fee_struct_by_month_obj = FeeStructByMonth.objects.get(clas = clas, month = month, session=current.session)
    total_month_fee = fee_struct_by_month_obj.amount
    # for fee in month_fee: 
    #     total = total + fee.amount 
    return render(request, 'feeEdit.html', {'class': clas, 'total_month_fee': total_month_fee, 'fees': fees, 'month_fee': month_fee, 'month': month})

def structUpdate(request):
    if request.method == "PATCH":
        # print(request.PATCH)
        # print(request.body.decode('utf-8'))
        m = request.body.decode('utf-8')
        # print(type(m))
        fee_data = json.loads(m)
        print(fee_data) 
        # print(fee_data['fee_name'])  
        fee_struct_obj = FeeStruct.objects.get(id=fee_data['fee_struct_id'])
        print(fee_struct_obj)
        # fee_struct_obj["fee_type"] = fee_data['fee_name']
        fee_struct_obj.fee_type = fee_data['fee_name']
        fee_amount = int(float(fee_data["fee_amount"]))
        fee_struct_obj.amount = fee_amount
        fee_struct_obj.save()
        # update fee struct by month
        partialUpdateFeeStructByMonth(fee_struct_obj.month, fee_struct_obj.clas) 
        return HttpResponse(json.dumps({"msg": "updated fee structure"}), content_type="application/json")
    elif request.method == "POST":
        print(request.body)
        m = request.body.decode('utf-8')
        fee_data = json.loads(m)
        print(fee_data)
        current = Current.objects.all()[0] 
        fee_struct_obj = FeeStruct(fee_type=fee_data['fee_name'], amount=fee_data['fee_amount'], clas=Classes.objects.get(id=fee_data['class_id']), month=Month.objects.get(id=fee_data['month_id']), session=current.session)
        # print(fee_struct_obj)
        fee_struct_obj.save()
        # update fee struct by month
        partialUpdateFeeStructByMonth(fee_struct_obj.month, fee_struct_obj.clas) 
        return HttpResponse(json.dumps({"msg": "added new fee structure"}), content_type="application/json")
    elif request.method == "DELETE":
        print(request.body)
        m = request.body.decode('utf-8')
        fee_data = json.loads(m)
        print(fee_data) 
        fee_struct_obj = FeeStruct.objects.get(id=fee_data['fee_struct_id'])
        print(fee_struct_obj)
        fee_struct_obj.delete()
        # update fee struct by month
        partialUpdateFeeStructByMonth(fee_struct_obj.month, fee_struct_obj.clas) 
        return HttpResponse(json.dumps({"msg": "deleted fee structure"}), content_type="application/json")    
    return HttpResponse(json.dumps({"error": "http not a patch request"}), content_type="application/json")

def feeSubmit(request):
    current = Current.objects.all()[0] 
    student_qs = Student.objects.filter(session = current.session)
    # print(student_qs)
    try:
        last_fee_submit_obj = FeeSubmit.objects.filter(session = current.session).order_by('-id')[0]
        last_memo_no = last_fee_submit_obj.memo_no
    except:
        last_memo_no = 0
    print("last_memo_no", last_memo_no)          
    if request.method == "POST":
        print("here")
        # print(request.body) 
        try:
            m = request.body.decode('utf-8')
            fee_data = json.loads(m)
            request.POST = fee_data
        except:
            print("error")
        try:        
            student_obj = Student.objects.get(add_no = request.POST['student'], session = current.session)
        except:
            student_obj = Student.objects.get(id = request.POST['student'], session = current.session)      
        # print(student_obj)
        amount = request.POST['amount']
        mop = request.POST['mop']
        memo_no = request.POST['memo_no']
        submit_date = request.POST['submit_date']
        txn_id = txnNumber()
        
        # check for misc fees
        amount = int(amount)
        misc_qs = MiscFee.objects.filter(student=student_obj, paid=False, session=current.session)
        for misc_q in misc_qs:
            misc_q_amount = misc_q.amount
            if misc_q_amount <= amount: 
                misc_q.paid_amount = misc_q_amount
                misc_q.paid = True
                misc_q.save()
                amount = amount - misc_q_amount
            else:
                misc_q.paid_amount = amount
                misc_q.save()
                amount = 0    
        
        if amount != 0:
            fee_submit_obj = FeeSubmit(student=student_obj, txn_id=txn_id, amount=amount, mop=mop, memo_no=memo_no, submit_date=submit_date, session=current.session)   
            fee_submit_obj.save()
         
        # Cheque details
        if mop == "Cheque":
            cheque_details_obj = ChequeDetails(fee_submit=fee_submit_obj, cheque_no=request.POST['cheque_no'], issued_by=request.POST['issued_by'], bank=request.POST['bank'], issue_date=request.POST['issue_date'])
            cheque_details_obj.save()
        elif mop == "Online/NEFT":  # Online/NEFT Details 
            online_pay_details_obj = OnlineNeftDetails(fee_submit=fee_submit_obj, utr_no=request.POST['utr_no'], pay_by=request.POST['pay_by'], pay_date=request.POST['pay_date'])
            online_pay_details_obj.save()
        elif mop == "Concession":
            fee_concession_obj = FeeConcession(fee_submit=fee_submit_obj, student=student_obj, concession_type=request.POST['concession-type'], reason=request.POST['reason'])
            fee_concession_obj.save() 
               
            
        # total fee submitted by student
        fee_submit_qs = FeeSubmit.objects.filter(student=student_obj)
        # print(fee_submit_qs)
        total_fee_submit = 0
        for fee in fee_submit_qs:
            total_fee_submit = total_fee_submit + fee.amount
        # print(total_fee_submit) 
        
        # iterate over all fee struct by month
        fee_struct_by_month_qs = FeeStructByMonth.objects.filter(clas=student_obj.Class, session=current.session)
        # print(fee_struct_by_month_qs)
        fee_submit_left = total_fee_submit
        month_no = 0
        # total_session_fee = 0
        total_session_fee = sum([x.amount for x in fee_struct_by_month_qs])
        print("here total", total_session_fee) 
        for fee_struct_by_month in fee_struct_by_month_qs:
            curr_month_amount = fee_struct_by_month.amount
            # total_session_fee = total_session_fee + curr_month_amount
            if curr_month_amount <= fee_submit_left:
                # print("FeeStructByMonth: ", fee_struct_by_month.month.month)
                fee_submit_left = fee_submit_left - curr_month_amount
                month_no = month_no + 1
            else:
                # print("Advanced Fee: ", fee_submit_left)  
                break 
        # print(month_no)
        session_fee_left = total_session_fee - total_fee_submit 
        fee_submit_by_month_obj = FeeSubmitByMonth.objects.update_or_create(student=student_obj, defaults={'month_no':month_no, 'advanced_amount':fee_submit_left, 'total_session_fee': total_session_fee, 'session_fee_submitted':total_fee_submit, 'session_fee_left':session_fee_left})     
        # print(fee_submit_by_month_obj)
        messages.success(request, f'Fee submitted successfully! Student: {student_obj.fname}; Class: {student_obj.Class.clas}; Amount: {amount}; MOP: {mop}; Submit Date: {submit_date}; Transaction ID: {txn_id}') 
        # fee_submit_by_month_obj = FeeSubmitByMonth(student=student_obj, month_no=month_no, advanced_amount=fee_submit_left, session_fee_submitted=total_fee_submit) 
        # fee_submit_by_month_obj.update()     
        return redirect('fee:feeSubmit')    
    return render(request, 'feesubmission.html', {'students': student_qs, 'today_date': date.today().strftime("%Y-%m-%d"), 'curr_memo_no': last_memo_no + 1})

def studentDetailsAPI(request):
    current = Current.objects.all()[0]
    if "add_no" in request.GET:
        add_no = request.GET['add_no']
        try:
            student_obj = Student.objects.get(add_no=add_no, session=current.session)
        except:
            return HttpResponse(json.dumps({"error": "Student not found"}), content_type="application/json")    
        # print(student_obj)
        try:
            fee_submit_by_month_obj = FeeSubmitByMonth.objects.get(student=student_obj)
            # print("FeeSubmitByMonth: ", fee_submit_by_month_obj)
        except:
            fee_struct_by_month_qs = FeeStructByMonth.objects.filter(clas=student_obj.Class, session = current.session)
            # print(fee_struct_by_month_qs)
            total_session_fee = 0
            for fee_struct_by_month_q in fee_struct_by_month_qs:
                total_session_fee = total_session_fee + fee_struct_by_month_q.amount
            # print(total_session_fee)    
            fee_submit_by_month_obj = FeeSubmitByMonth(student=student_obj, total_session_fee=total_session_fee, session_fee_left=total_session_fee, session=current.session)
            fee_submit_by_month_obj.save()
            # print("No FeeSubmitByMonth object found for student: ", student_obj)
            # print("Creating FeeSubmitByMonth object: ", fee_submit_by_month_obj)
        student_info_dict = {
            'add_no': student_obj.add_no,
            'name': student_obj.fname,
            'father_name': student_obj.fathername,
            'class': student_obj.Class.clas,
            'total_session_fee': fee_submit_by_month_obj.total_session_fee,
            'session_fee_submitted': fee_submit_by_month_obj.session_fee_submitted,
            'session_fee_left': fee_submit_by_month_obj.session_fee_left,
        }
        return HttpResponse(json.dumps(student_info_dict), content_type="application/json")        
    student_qs = Student.objects.filter(session=current.session).values()
    # print(student_qs)
    return HttpResponse(json.dumps({'students': student_qs[1]}), content_type='application/json') 

def feeConcession(request):
    if request.method == "POST":
        print(request.POST)
        student_id = request.POST['student_id']
        # request.POST['student'] = 194571 
        # print("after request", request.POST)
        # student_obj = Student.objects.get(id = student_id)
        # fee_concession_obj = FeeConcession(student_id=student_obj, concession_type=request.POST['concession-type'], reason=request.POST['reason'])
        feeSubmit(request)
    return redirect(f'/studentoutline/{student_id}')

# copy feeSubmit, cheque and online to deleted ones
def feeDelete(request):
    current = Current.objects.all()[0]
    if "id" in request.GET:
        fee_submit_obj = FeeSubmit.objects.get(id=request.GET['id'])
        # print(fee_submit_obj)
        deleted_fee_submit_obj = DeletedFeeSubmit(student=fee_submit_obj.student, txn_id=fee_submit_obj.txn_id , amount=fee_submit_obj.amount, mop=fee_submit_obj.mop, submit_date=fee_submit_obj.submit_date, session=current.session)
        deleted_fee_submit_obj.save()
        # cheque
        try:
            cheque_obj = fee_submit_obj.fee_cheque
            # print(cheque_obj) 
            deleted_cheque_obj = DeletedChequeDetails(fee_submit=deleted_fee_submit_obj,cheque_no=cheque_obj.cheque_no, issued_by=cheque_obj.issued_by, bank=cheque_obj.bank, branch=cheque_obj.branch, issue_date=cheque_obj.issue_date)
            deleted_cheque_obj.save() 
            cheque_obj.delete()
            # print("Deleted cheque object: ", deleted_cheque_obj)  
        except:
            print("No cheque object found")
        # online 
        try:
            online_obj = fee_submit_obj.fee_online
            # print(online_obj) 
            deleted_online_obj = DeletedOnlineNeftDetails(fee_submit=deleted_fee_submit_obj, utr_no=online_obj.utr_no, pay_by=online_obj.pay_by, pay_date=online_obj.pay_date)
            deleted_online_obj.save()   
            online_obj.delete()
            # print("Deleted online object: ", deleted_online_obj) 
        except: 
            print("No online object found") 
        fee_submit_obj.delete()
        # print("Deleted fee submit object: ", deleted_fee_submit_obj) 
        fee_submit_last_obj = FeeSubmit.objects.last()
        fee_submit_last_obj.delete()
        # print("Deleted fee submit last object: ", fee_submit_last_obj)  
    return HttpResponse(json.dumps({'success': 'success'}), content_type='application/json')

def misc(request):
    current = Current.objects.all()[0]
    if request.method == "POST":
        print(request.POST)
        student_add_no = request.POST['student']
        student_obj = Student.objects.get(add_no=student_add_no, session=current.session)
        student_id = student_obj.id 
        misc_types = request.POST.getlist('misc-type') 
        # print("misc_types", misc_types)
        misc_amounts = request.POST.getlist('misc-amount')
        misc_reasons = request.POST.getlist('misc-reason')
        i = 0
        for misc_type in misc_types:
            print("misc_type", misc_type) 
            misc_fee_obj = MiscFee(student=student_obj, fee_type=misc_type, amount=misc_amounts[i], reason=misc_reasons[i], session=current.session)
            misc_fee_obj.save()
            i+=1
    feeSubmit(request)         
    return redirect(f'/fee/submit/')   

def miscDelete(request):
    if 'id' in request.GET:
        print(request.GET['id'])
        misc_obj = MiscFee.objects.get(id=request.GET['id'])
        misc_obj.delete()
    return HttpResponse(json.dumps({'success': 'success'}), content_type='application/json')
    