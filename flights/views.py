from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from flights.models import Airport, Flight, Passenger

# Create your views here.
def index(request):
    context={
        'title':'Main Page',
        'flights': Flight.objects.all(),
        'airports':Airport.objects.all()
    }
    return render(request,'flights/index.html',context)

def flight(request,flight_id):
    try:
        flight=Flight.objects.get(pk=flight_id)
        passengers=flight.passengers.all()
    except Flight.DoesNotExist:
        raise Http404('Flight does not exist.')
    context={ 
        'flight':flight,
        'passengers':passengers,
        'non_passengers':Passenger.objects.exclude(flight=flight).all()
    }
    return render(request,'flights/flight.html',context)

def book(request, flight_id):
    try:
        passenger_id=int(request.POST['passenger'])
        passenger=Passenger.objects.get(pk=passenger_id)
        flight=Flight.objects.get(pk=flight_id)
    except KeyError:
        return render(request, 'flights/error.html',{'message':'No selection'})
    except Flight.DoesNotExist:
        return render(request, 'flights/error.html',{'message':'No flight.'})
    except Passenger.DoesNotExist:
        return render(request, 'flights/error.html',{'message':'No passenger.'})
    
    passenger.flight.add(flight)
    return HttpResponseRedirect(reverse('flight',args=(flight_id,)))