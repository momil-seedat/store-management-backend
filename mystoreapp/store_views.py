from rest_framework import generics
from .models import Store
from rest_framework.response import Response
from rest_framework import status
from .models import Store, StoreContact
from .serializers import StoreSerializer,StoreContactSerializer,UpdateContactSerializer
from django.utils import timezone


class StoreCreateListView(generics.ListCreateAPIView):
    queryset = Store.objects.prefetch_related('contacts').all().order_by('-created_at') 
    serializer_class = StoreSerializer

    def create(self, request, *args, **kwargs):
         serializer = self.get_serializer(data=request.data)
         if serializer.is_valid():
            store = serializer.save()  # Create Store object
            contacts_data = request.data.get('contacts')  # Get contacts data from request

            if contacts_data:
                 for contact_data in contacts_data:
                     # Create StoreContact instances associated with the created Store
                     StoreContact.objects.create(store=store, **contact_data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    
class StoreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all() 
    serializer_class = StoreSerializer


class StoreWithContactsView(generics.RetrieveAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Fetch contacts associated with the retrieved store instance
        contacts_queryset = instance.contacts.all()
        contacts_serializer = StoreContactSerializer(contacts_queryset, many=True)

        response_data = {
            'store_details': serializer.data,
            'contacts': contacts_serializer.data
        }

        return Response(response_data)
    
class StoreContactListCreateView(generics.ListCreateAPIView):
    serializer_class = StoreContactSerializer

    def get_queryset(self):
        store_id = self.kwargs['store_id']
        return StoreContact.objects.filter(store_id=store_id)

    def perform_create(self, serializer):
        store_id = self.kwargs['store_id']
        serializer.save(store_id=store_id)

class StoreContactUpdateView(generics.UpdateAPIView):
    serializer_class = UpdateContactSerializer
    lookup_field = 'store_id'

    def update(self, request, *args, **kwargs):
        store_id = self.kwargs['store_id']
        store = Store.objects.filter(pk=store_id).first()
        
        if not store:
            return Response({"detail": "Store not found."}, status=status.HTTP_404_NOT_FOUND)

        # Delete existing contacts for the store
        StoreContact.objects.filter(store_id=store_id).delete()
        
        # Create new contacts from the request data
        data = request.data
        new_contacts = []
        for contact_data in data:
            new_contact = StoreContact(
                store=store,
                name=contact_data['name'],
                email=contact_data['email'],
                phone=contact_data['phone']
            )
            new_contacts.append(new_contact)
        
        # Bulk create new contacts
        StoreContact.objects.bulk_create(new_contacts)

        return Response(status=status.HTTP_200_OK)

