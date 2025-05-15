from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Worker, AccessRecord
from django.db.models import Max
from django.shortcuts import render
from rest_framework.decorators import api_view



class RFIDAccessView(APIView):
    def post(self, request):
        tag_uid = request.data.get('tag_uid')
        
        try:
            # Tenta encontrar o trabalhador pela tag
            worker = Worker.objects.get(tag_uid=tag_uid)
        except Worker.DoesNotExist:
            # Gera um nome de usuário sequencial (usuario1, usuario2...)
            last_user_number = Worker.objects.filter(name__startswith="usuario").aggregate(Max('name'))['name__max']
            
            if last_user_number:
                # Extrai o número do último usuário (ex: "usuario3" → 3)
                last_number = int(last_user_number.replace("usuario", ""))
                new_number = last_number + 1
            else:
                new_number = 1  # Primeiro usuário
            
            # Cria o novo trabalhador
            worker = Worker.objects.create(
                name=f"usuario{new_number}",
                tag_uid=tag_uid
            )
        
        # Verifica se há registro de entrada aberto
        open_record = AccessRecord.objects.filter(
            worker=worker, 
            exit_time__isnull=True
        ).first()

        if open_record:
            # Registra a saída
            open_record.exit_time = timezone.now()
            open_record.save()
            return Response(
                {
                    "status": "exit",
                    "message": f"Saída registrada para {worker.name}",
                    "duration": open_record.exposure_duration
                },
                status=status.HTTP_200_OK
            )
        else:
            # Registra a entrada
            AccessRecord.objects.create(worker=worker)
            return Response(
                {
                    "status": "entry",
                    "message": f"Entrada registrada para {worker.name}",
                    "entry_time": timezone.now()
                },
                status=status.HTTP_201_CREATED
            )



def access_form(request):
    return render(request, 'workers/access_form.html')




def dashboard(request):
    active_records = AccessRecord.objects.filter(exit_time__isnull=True)
    return render(request, 'workers/dashboard.html', {'active_records': active_records})



@api_view(['GET'])
def active_workers_api(request):
    active_records = AccessRecord.objects.filter(exit_time__isnull=True).select_related('worker')
    data = []
    for record in active_records:
        duration = (timezone.now() - record.entry_time).total_seconds()
        data.append({
            'id': record.id,
            'name': record.worker.name,
            'entry_time': record.entry_time.timestamp(),
            'duration': duration,
            'max_duration': record.worker.max_exposure_minutes * 60  # Convertendo para segundos
        })
    return Response(data)
