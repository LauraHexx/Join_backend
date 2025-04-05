from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """
    Erlaubt Zugriff nur für authentifizierte Benutzer.
    Admins dürfen alles sehen, normale Benutzer nur ihre eigenen Daten.
    """

    def has_permission(self, request, view):
        # Nur authentifizierte Benutzer dürfen auf die View zugreifen
        if not (request.user and request.user.is_authenticated):
            return False

        # Admins dürfen alles sehen
        if request.user.is_superuser:
            return True

        # Normale Benutzer dürfen nur ihre eigenen Daten sehen
        # Filtere das queryset des ViewSets
        if hasattr(view, "queryset"):
            view.queryset = view.queryset.filter(user=request.user)

        return True

    def has_object_permission(self, request, view, obj):
        # Admins dürfen alles
        if request.user and request.user.is_superuser:
            return True

        # Normale Benutzer dürfen nur ihre eigenen Objekte sehen
        return bool(request.user and obj.user == request.user)
