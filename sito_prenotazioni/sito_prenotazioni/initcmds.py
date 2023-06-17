from django.contrib.auth.models import Group, Permission


def crea_gruppi():
    try:
        Group.objects.get(name='Medici')
    except Group.DoesNotExist:
        nuovo_gruppo = Group.objects.create(name='Medici')
        lista_permessi = ('view_esame', 'add_esame', 'change_esame', 'view_medico', 'change_medico')
        permessi = Permission.objects.filter(codename__in=lista_permessi)
        nuovo_gruppo.permissions.set(permessi)
        nuovo_gruppo.save()
    
    try:
        Group.objects.get(name='Assistenza')
    except Group.DoesNotExist:
        nuovo_gruppo = Group.objects.create(name='Assistenza')
        lista_permessi = ('add_utentecustom', 'change_utentecustom', 'view_utentecustom', 'add_esame', 'change_esame', 
                          'view_esame', 'add_medico', 'change_medico', 'view_medico', 'add_commento', 'change_commento',
                          'delete_commento', 'view_commento')
        permessi = Permission.objects.filter(codename__in=lista_permessi)
        nuovo_gruppo.permissions.set(permessi)
        nuovo_gruppo.save()

def crea_db():
    pass

def elimina_db():
    pass