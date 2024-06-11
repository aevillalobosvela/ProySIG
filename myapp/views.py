from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from datetime import datetime
from datetime import time
from django.db import IntegrityError
import pandas as pd
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import puntos_recorrido
from .models import punto_carnaval
from .models import punto_planifica
from .models import punto_conoce
from django.views.decorators.csrf import csrf_exempt


def inicio(request):
    usuario = request.user
    return render(request, "inicio.html", {"usuario": usuario})


def obtener_puntos_recorrido(request):
    datos = puntos_recorrido.objects.all()
    res = [
        {"latitud": coord.latitud_rc, "longitud": coord.longitud_rc} for coord in datos
    ]
    return JsonResponse(res, safe=False)


def obtener_punto_carnaval(request):
    datos = [
        punto_carnaval.to_dict() for punto_carnaval in punto_carnaval.objects.all()
    ]
    return JsonResponse(datos, safe=False)


def obtener_punto_planifica(request):
    datos = [
        punto_planifica.to_dict() for punto_planifica in punto_planifica.objects.all()
    ]
    return JsonResponse(datos, safe=False)


def obtener_punto_conoce(request):
    datos = [punto_conoce.to_dict() for punto_conoce in punto_conoce.objects.all()]
    return JsonResponse(datos, safe=False)


def login_user(request):
    if request.method == "GET":
        return render(request, "login_user.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "login_user.html",
                {
                    "form": AuthenticationForm,
                    "error": "Usuario o Password incorrecto(s)",
                },
            )
        else:
            if user.is_superuser:
                print("Ingresa admin")
                login(request, user)
                return redirect("usuarios_admin")
            else:
                print("Ingresa bien")
                login(request, user)
                return redirect("inicio")


@login_required
def usuarios_admin(request):
    usuario = request.user
    usuarios = User.objects.filter(is_superuser=False)
    return render(
        request,
        "usuarios_admin.html",
        {
            "usuario": usuario,
            "usuarios": usuarios,
        },
    )


@login_required
def inicio_admin(request):

    if request.method == "POST":
        coord_lat = request.POST.get("coord_lat")
        coord_lng = request.POST.get("coord_lng")
        titulo = request.POST.get("titulo")
        direccion = request.POST.get("direccion")

    if request.POST.get("titulo") == "Puesto de Salud":
        imagen = "static/img/mapa/salud/salud7.png"
    if request.POST.get("titulo") == "Paso Peatonal":
        imagen = "static/img/mapa/paso1.jpg"
    if request.POST.get("titulo") == "Deposito residual":
        imagen = "static/img/mapa/deposito1.jpg"
    if request.POST.get("titulo") == "Puesto Policial":
        imagen = "static/img/mapa/policia/policia1.jpg"

        punto = punto_carnaval.objects.create(
            coord_lat=coord_lat,
            coord_lng=coord_lng,
            titulo=titulo,
            direccion=direccion,
            imagen_ruta=imagen,
        )
        puntos = punto_carnaval.objects.all()
        return render(request, "inicio_admin.html", {"puntos": puntos})
    else:
        puntos = punto_carnaval.objects.all()
        return render(request, "inicio_admin.html", {"puntos": puntos})


@login_required
def planifica_admin(request):

    if request.method == "POST":
        coord_lat = request.POST.get("coord_lat")
        coord_lng = request.POST.get("coord_lng")
        titulo = request.POST.get("titulo")
        nombre = request.POST.get("nombre")

        punto = punto_planifica.objects.create(
            coord_lat=coord_lat,
            coord_lng=coord_lng,
            titulo=titulo,
            name=nombre,
        )
        puntos = punto_planifica.objects.all()
        return render(request, "planifica_admin.html", {"puntos": puntos})
    else:
        puntos = punto_planifica.objects.all()
        return render(request, "planifica_admin.html", {"puntos": puntos})


@login_required
def conoce_admin(request):

    if request.method == "POST":
        coord_lat = request.POST.get("coord_lat")
        coord_lng = request.POST.get("coord_lng")
        titulo = request.POST.get("titulo")
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        detalles = request.POST.get("detalles")

        if request.POST.get("titulo") == "Hotel":
            imagen = "/static/img/conoceoruro/hot.png"
        if request.POST.get("titulo") == "Comida":
            imagen = "/static/img/conoceoruro/resta.png"
        if request.POST.get("titulo") == "Museo":
            imagen = "/static/img/conoceoruro/mm.png"
        if request.POST.get("titulo") == "Iglesia":
            imagen = "/static/img/conoceoruro/i.png"

        punto = punto_conoce.objects.create(
            coord_lat=coord_lat,
            coord_lng=coord_lng,
            titulo=titulo,
            name=nombre,
            descripcion=descripcion,
            detalles=detalles,
            imagen_ruta=imagen,
        )
        puntos = punto_conoce.objects.all()
        return render(request, "conoce_admin.html", {"puntos": puntos})
    else:
        puntos = punto_conoce.objects.all()
        return render(request, "conoce_admin.html", {"puntos": puntos})


def conoce(request):
    usuario = request.user
    return render(request, "conoce.html", {"usuario": usuario})


def planifica(request):
    usuario = request.user
    return render(request, "planifica.html", {"usuario": usuario})

@login_required
def mis_marcadores(request):
    usuario = request.user
    return render(request, "mis_marcadores.html", {"usuario": usuario})

@login_required
def foro(request):
    usuario = request.user
    return render(request, "foro.html", {"usuario": usuario})


def aprende(request):
    return render(request, "aprende.html")


def registro(request):
    if request.method == "GET":
        return render(request, "registro.html", {"form": UserCreationForm})
    else:
        print(request.POST)

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["user"],
                    password=request.POST["password1"],
                    first_name=request.POST["nombre"],
                )
                user.save()
                print("Usuario registrado")
                return redirect("login_user")
            except IntegrityError:
                return render(
                    request,
                    "registro.html",
                    {"form": UserCreationForm, "error": "Usuario ya registrado"},
                )
            except ValueError:
                return render(
                    request,
                    "registro.html",
                    {"form": UserCreationForm, "error": "Datos no validos"},
                )
            except:
                return render(
                    request,
                    "registro.html",
                    {"form": UserCreationForm, "error": "Error en el registro"},
                )

        return render(
            request,
            "registro.html",
            {"form": UserCreationForm, "error": "Los Passwords no coinciden"},
        )


@login_required
def eliminar_usuario(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return JsonResponse({"status": "success"}, status=200)
    return JsonResponse({"status": "error"}, status=400)


@login_required
def eliminar_punto_carnaval(request, punto_id):
    if request.method == "POST":
        punto = get_object_or_404(punto_carnaval, id=punto_id)
        punto.delete()
        return JsonResponse({"status": "success"}, status=200)
    return JsonResponse({"status": "error"}, status=400)


@login_required
def eliminar_punto_planifica(request, punto_id):
    if request.method == "POST":
        punto = get_object_or_404(punto_planifica, id=punto_id)
        punto.delete()
        return JsonResponse({"status": "success"}, status=200)
    return JsonResponse({"status": "error"}, status=400)


@login_required
def eliminar_punto_conoce(request, punto_id):
    if request.method == "POST":
        punto = get_object_or_404(punto_conoce, id=punto_id)
        punto.delete()
        return JsonResponse({"status": "success"}, status=200)
    return JsonResponse({"status": "error"}, status=400)


""" //---------------------------------------------------------------------------------- """


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        print(request.POST)
        try:
            if request.POST["is_superuser"] == "on":
                superusuario = True
        except:
            superusuario = False
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                    first_name=request.POST["first_name"],
                    last_name=request.POST["last_name"],
                    email=request.POST["email"],
                    fec_nac=request.POST["fec_nac"],
                    salario=request.POST["salario"],
                    is_superuser=superusuario,
                )
                user.save()
                login(request, user)
                return redirect("signin")
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "Usuario ya registrado"},
                )
            except ValueError:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "Datos no validos"},
                )
            except:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "Error en el registro"},
                )
        return render(
            request,
            "signup.html",
            {"form": UserCreationForm, "error": "Los Passwords no coinciden"},
        )


def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            print(request.POST["username"])
            return render(
                request,
                "signin.html",
                {
                    "form": AuthenticationForm,
                    "error": "Usuario o Password incorrecto(s)",
                },
            )
        else:
            login(request, user)
            if user.is_superuser == True:
                return redirect("control")
            else:
                return redirect("marcar")


def about(request):
    return render(request, "about.html")


def control(request):
    usuario = request.user
    empleados = User.objects.filter(is_superuser=False)
    return render(request, "control.html", {"usuario": usuario, "empleados": empleados})


def marcar(request):
    ahora = datetime.now()
    usuario = request.user
    return render(request, "marcar.html", {"usuario": usuario, "fec_hora": ahora})


def signout(request):
    logout(request)
    return redirect("inicio")


""" def marcar_llegada(request):
    fecha_actual = timezone.now().date()
    hora_actual = datetime.now().time()
    hora_format = hora_actual.strftime("%H:%M:%S")
    ahora = datetime.now()
    usuario = request.user
    verificacion = diario.objects.filter(fech_reg=fecha_actual, empleado=usuario.id)
    if verificacion.exists():
        mensaje = "\nUsted ya ha registrado su entrada el dia de hoy \n"
    else:
        if time(5, 0, 0) <= hora_actual <= time(8, 10, 0):
            tiempo_retraso = False
            mensaje = (
                "Bienvenido empleado \n\n Su hora registrada de ingreso es: "
                + str(hora_format)
                + "\n\nSu solicitud ha sido registrada correctamente"
            )
        else:
            tiempo_retraso = True
            mensaje = (
                "Bienvenido empleado \n\n Su hora registrada de ingreso es: "
                + str(hora_format)
                + "\n\nTiempo con retraso registrado"
            )
        registro = diario(
            fech_reg=fecha_actual,
            hora_in=hora_actual,
            hora_out="00:00:00",
            retraso=tiempo_retraso,
            salida=False,
            empleado_id=usuario.id,
        )
        registro.save()

    return render(
        request,
        "marcar.html",
        {"usuario": usuario, "fec_hora": ahora, "mensaje": mensaje},
    )


def marcar_salida(request):
    fecha_actual = timezone.now().date()
    hora_actual = datetime.now().time()
    hora_format = hora_actual.strftime("%H:%M:%S")
    ahora = datetime.now()
    usuario = request.user
    verificacion = diario.objects.filter(
        fech_reg=fecha_actual, empleado=usuario.id, hora_out=time(0, 0, 0)
    )
    print(hora_actual)
    if time(18, 0, 0) <= hora_actual <= time(23, 59, 0):
        print("Salida correcta")
    else:
        print("Salida temprana")
    if verificacion.exists():
        diario_obj = diario.objects.get(
            fech_reg=fecha_actual, empleado=usuario.id, hora_out=time(0, 0, 0)
        )
        if time(18, 0, 0) <= hora_actual <= time(23, 59, 0):
            mensaje = (
                "Bienvenido empleado \n\n Su hora registrada de salida es: "
                + str(hora_format)
                + "\n\nSu solicitud ha sido registrada correctamente"
            )
        else:
            diario_obj.salida = True
            mensaje = (
                "Bienvenido empleado \n\n Su hora registrada de salida es: "
                + str(hora_format)
                + "\n\nSalida temprana registrada"
            )
        diario_obj.hora_out = hora_actual
        diario_obj.save()
    else:
        mensaje = "\nUsted aun no registra su entrada el dia de hoy o su salida ya fue registrada\n"

    return render(
        request,
        "marcar.html",
        {"usuario": usuario, "fec_hora": ahora, "mensaje": mensaje},
    )





def exportar_excel(request):
    registros = User.objects.filter(is_superuser=False)

    data = {
        "id": [],
        "first_name": [],
        "last_name": [],
        "email": [],
        "fec_nac": [],
        "salario": [],
    }
    for registro in registros:
        data["id"].append(registro.id)
        data["first_name"].append(registro.first_name)
        data["last_name"].append(registro.last_name)
        data["email"].append(registro.email)
        data["fec_nac"].append(registro.fec_nac)
        data["salario"].append(registro.salario)

    df = pd.DataFrame(data)
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = 'attachment; filename="registros.xlsx"'
    df.to_excel(response, index=False, engine="openpyxl")

    return response


def calcular(request, empleado_id):
    now = timezone.now()
    primer_dia_del_mes = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    ultimo_dia_del_mes = (now.replace(day=28) + timedelta(days=4)).replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )

    usuario = request.user
    empleados = User.objects.filter(is_superuser=False)
    if request.method == "GET":
        return render(
            request, "control.html", {"usuario": usuario, "empleados": empleados}
        )
    else:
        empleado = User.objects.get(id=empleado_id)
        reg_retraso = diario.objects.filter(
            empleado=empleado_id,
            retraso=True,
            fech_reg__gte=primer_dia_del_mes,
            fech_reg__lt=ultimo_dia_del_mes,
        )
        retrasos = reg_retraso.count()
        reg_salida = diario.objects.filter(
            empleado=empleado_id,
            salida=True,
            fech_reg__gte=primer_dia_del_mes,
            fech_reg__lt=ultimo_dia_del_mes,
        )
        salidas = reg_salida.count()
        print(empleado_id)
        print(retrasos)
        print(salidas)
        descuento = 100 * retrasos + 100 * salidas
        total = empleado.salario - descuento

        mensaje = (
            "El empleado "
            + str(empleado.first_name)
            + " "
            + str(empleado.last_name)
            + " cuenta con un historial de "
            + str(retrasos)
            + " retraso(s) y "
            + str(salidas)
            + " salida(s) temprana(s) en el presente mes\n\nEsto da como resultado de un descuento de "
            + str(descuento)
            + " Bs. que seran retirados del salario mensual del empleado\n\nSalario neto: "
            + str(empleado.salario)
            + "\n\nSalario descontado: "
            + str(total)
        )

        registro = pagomes(
            anio_pago=2023,
            mes_pago=now.month,
            retrasos=retrasos,
            salidas=salidas,
            tot_descento=descuento,
            empleado_id=empleado_id,
        )
        registro.save()

        return render(
            request,
            "control.html",
            {
                "usuario": usuario,
                "id": empleado_id,
                "empleados": empleados,
                "obj_empleado": empleado,
                "mensaje": mensaje,
            },
        ) """


""" ------------------------------------------------------------------ """


""" def task_detail(request, task_id):
    if request.method == "GET":
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, "task_detail.html", {"task": task, "form": form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect("tasks")
        except ValueError:
            return render(
                request,
                "task_detail.html",
                {"form": form, "error": "No se pudo actualizar"},
            )


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect("tasks")


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("tasks")
 """
