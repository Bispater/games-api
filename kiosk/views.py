from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.db.models import Count

from .models import ClientConfig, LeaderboardEntry
from .serializers import (
    ClientConfigOutputSerializer,
    ClientConfigListSerializer,
    ClientConfigWriteSerializer,
    LeaderboardEntrySerializer,
)


# ══════════════════════════════════════════
# CLIENT CONFIG
# ══════════════════════════════════════════

class ClientConfigViewSet(viewsets.ModelViewSet):
    """
    CRUD for client configurations.
    - GET  /api/clients/              → list all clients
    - POST /api/clients/              → create new client
    - GET  /api/clients/<code>/       → full config (games-kiosk compatible format)
    - PUT  /api/clients/<code>/       → update config
    - PATCH /api/clients/<code>/      → partial update
    - DELETE /api/clients/<code>/     → delete client
    """
    queryset = ClientConfig.objects.annotate(
        leaderboard_count=Count('leaderboard_entries')
    )
    lookup_field = 'code'

    def get_serializer_class(self):
        if self.action == 'list':
            return ClientConfigListSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return ClientConfigWriteSerializer
        return ClientConfigOutputSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ClientConfigOutputSerializer(instance, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='upload-logo')
    def upload_logo(self, request, code=None):
        config = self.get_object()
        if 'logo' not in request.FILES:
            return Response({'error': 'No logo file provided'}, status=400)
        config.client_logo = request.FILES['logo']
        config.save()
        url = request.build_absolute_uri(config.client_logo.url)
        return Response({'logo': url})

    @action(detail=True, methods=['post'], url_path='upload-favicon')
    def upload_favicon(self, request, code=None):
        config = self.get_object()
        if 'favicon' not in request.FILES:
            return Response({'error': 'No favicon file provided'}, status=400)
        config.client_favicon = request.FILES['favicon']
        config.save()
        url = request.build_absolute_uri(config.client_favicon.url)
        return Response({'favicon': url})


# ══════════════════════════════════════════
# LEADERBOARD
# ══════════════════════════════════════════

class LeaderboardViewSet(viewsets.ModelViewSet):
    """
    CRUD for leaderboard entries.
    Filter by: ?client=<code>, ?game_id=<game>, ?search=<name or rut>
    """
    queryset = LeaderboardEntry.objects.select_related('client')
    serializer_class = LeaderboardEntrySerializer
    search_fields = ['player_name', 'player_rut']
    ordering_fields = ['score', 'created_at']

    def get_queryset(self):
        qs = super().get_queryset()
        client_code = self.request.query_params.get('client')
        game_id = self.request.query_params.get('game_id')
        if client_code:
            qs = qs.filter(client__code=client_code)
        if game_id:
            qs = qs.filter(game_id=game_id)
        return qs

    @action(detail=False, methods=['delete'], url_path='clear')
    def clear(self, request):
        """
        DELETE /api/leaderboard/clear/?client=ENT01&game_id=memory
        Both params optional. If no params, clears everything.
        """
        qs = LeaderboardEntry.objects.all()
        client_code = request.query_params.get('client')
        game_id = request.query_params.get('game_id')
        if client_code:
            qs = qs.filter(client__code=client_code)
        if game_id:
            qs = qs.filter(game_id=game_id)
        count, _ = qs.delete()
        return Response({'deleted': count})

    @action(detail=False, methods=['get'], url_path='top/(?P<client_code>[^/.]+)/(?P<game_id>[^/.]+)')
    def top_scores(self, request, client_code=None, game_id=None):
        """GET /api/leaderboard/top/<client_code>/<game_id>/?limit=10"""
        limit = int(request.query_params.get('limit', 10))
        entries = LeaderboardEntry.objects.filter(
            client__code=client_code, game_id=game_id
        )
        if not entries.exists():
            return Response([])

        first = entries.first()
        if first.is_higher_better:
            entries = entries.order_by('-score')
        else:
            entries = entries.order_by('score')

        serializer = LeaderboardEntrySerializer(entries[:limit], many=True)
        return Response(serializer.data)
