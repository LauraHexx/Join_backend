from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """
    Erlaubt Zugriff nur für authentifizierte Benutzer.
    Admins dürfen alles sehen, normale Benutzer nur ihre eigenen Daten.
    """

    def has_permission(self, request, view):
        # Nur authentifizierte Benutzer dürfen auf die View zugreifen
        if not request.user or not request.user.is_authenticated:
            return False

        # Admins dürfen alles sehen
        if request.user.is_superuser:
            return True

        return True

    def has_object_permission(self, request, view, obj):
        # Admins dürfen alles
        if request.user and request.user.is_superuser:
            return True

        # Normale Benutzer dürfen nur ihre eigenen Objekte sehen
        if hasattr(obj, "user"):
            return bool(request.user and obj.user == request.user)

        return False


class IsSubtaskOwnerOrAdmin(IsOwnerOrAdmin):
    """
    Berechtigung für Subtasks:
    Der Benutzer muss entweder der Besitzer des zugehörigen Tasks sein.
    """

    def has_object_permission(self, request, view, obj):
        return obj.task.user == request.user
