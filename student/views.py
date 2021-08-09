from django.shortcuts import render,redirect,reverse
from Stumgrdemo.settings import *
from django.http import HttpResponse
import pymysql

# Create your views here.
def index(request):
    """
    展示所有的学生数据   --- fetchall()
    :param request:
    :return:
    """
    # 实例化一个数据库连接
    mysqldb = pymysql.connect(host=HOST,user=USER,password=PASSWORD,database=DB)
    # 为数据库连接准备一个游标
    cursor = mysqldb.cursor()
    # 准备要执行的sql语句
    sql =   """
            SELECT SNO,SName,Gender,Birthday,Mobile,Email,Address 
            FROM Student;
            """
    # 执行语句并且获得返回结果
    try:
        # 执行语句
        cursor.execute(sql)
        # 获取返回结果
        students = cursor.fetchall()    # 返回的结果是一个嵌套的元组
        return render(request, 'index.html',context={"students":students})
    except Exception as e:
        return HttpResponse("获取数据异常，具体原因:"+str(e))
    finally:
        # 关闭连接
        mysqldb.close()

def login(request):
    return render(request,'login.html')

def view(request):
    # 获取请求的学号sno
    sno = request.GET.get("sno")
    # 创建一个数据库连接
    mysqldb = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DB)
    # 为数据库连接准备一个游标
    cursor = mysqldb.cursor()
    # 准备要执行的sql语句
    sql = "SELECT SNO,SName,Gender,Birthday,Mobile,Email,Address FROM Student WHERE SNO=%s" % (sno)

    # 执行语句并且获得返回结果
    try:
        # 执行语句
        cursor.execute(sql)
        # 获取返回结果
        student = cursor.fetchone()  # 返回一个学生
        return render(request, 'view.html', context={"student": student})
    except Exception as e:
        return HttpResponse("获取数据异常，具体原因:" + str(e))
    finally:
        # 关闭连接
        mysqldb.close()

def modify(request):
    """
    修改学生信息
    :param request:
    :return:
    """
    if request.method == "GET":
        # 获取请求的学号sno
        sno = request.GET.get("sno")
        # 创建一个数据库连接
        mysqldb = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DB)
        # 为数据库连接准备一个游标
        cursor = mysqldb.cursor()
        # 准备要执行的sql语句
        sql = "SELECT SNO,SName,Gender,Birthday,Mobile,Email,Address FROM Student WHERE SNO=%s" % (sno)

        # 执行语句并且获得返回结果
        try:
            # 执行语句
            cursor.execute(sql)
            # 获取返回结果
            student = cursor.fetchone()  # 返回一个学生
            return render(request, 'modify.html', context={"student": student})
        except Exception as e:
            return HttpResponse("获取数据异常，具体原因:" + str(e))
        finally:
            # 关闭连接
            mysqldb.close()
    elif request.method == "POST":
        # 取出提交的值
        sno = request.POST.get("sno")
        name = request.POST.get("name")
        gender = request.POST.get("gender")
        birthday = request.POST.get("birthday")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")
        address = request.POST.get("address")
        # 获取请求的学号sno
        sno = request.GET.get("sno")
        # 创建一个数据库连接
        mysqldb = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DB)
        # 为数据库连接准备一个游标
        cursor = mysqldb.cursor()
        # 准备要执行的sql语句
        sql = "update Student set SName='%s',Gender='%s',Birthday='%s',Mobile='%s',Email='%s',Address='%s'"\
                "WHERE SNO=%s" % (name,gender,birthday,mobile,email,address,sno)


        # 执行语句并且获得返回结果
        try:
            # 执行语句
            cursor.execute(sql)
            # 写入到数据库
            mysqldb.commit()
            # 返回首页
            return redirect(reverse('index'))
        except Exception as e:
            mysqldb.rollback()
            return HttpResponse("获取数据异常，具体原因:" + str(e))
        finally:
            # 关闭连接
            mysqldb.close()
