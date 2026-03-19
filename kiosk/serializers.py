from rest_framework import serializers
from .models import ClientConfig, LeaderboardEntry


class ClientConfigOutputSerializer(serializers.ModelSerializer):
    """
    Outputs config in the EXACT same nested format that games-kiosk expects
    (same structure as client-config.json).
    """

    class Meta:
        model = ClientConfig
        fields = '__all__'

    def to_representation(self, instance):
        request = self.context.get('request')
        logo_url = ''
        favicon_url = ''
        if instance.client_logo:
            logo_url = request.build_absolute_uri(instance.client_logo.url) if request else instance.client_logo.url
        if instance.client_favicon:
            favicon_url = request.build_absolute_uri(instance.client_favicon.url) if request else instance.client_favicon.url

        return {
            'code': instance.code,
            'isActive': instance.is_active,
            'client': {
                'name': instance.client_name,
                'subtitle': instance.client_subtitle,
                'logo': logo_url,
                'favicon': favicon_url,
            },
            'branding': {
                'primaryColor': instance.branding_primary_color,
                'primaryHover': instance.branding_primary_hover,
                'primaryDark': instance.branding_primary_dark,
                'primaryLight': instance.branding_primary_light,
                'accentColor': instance.branding_accent_color,
                'accentLight': instance.branding_accent_light,
                'backgroundColor': instance.branding_background_color,
                'cardBackground': instance.branding_card_background,
                'textPrimary': instance.branding_text_primary,
                'textMuted': instance.branding_text_muted,
                'borderColor': instance.branding_border_color,
            },
            'kiosk': {
                'exitPassword': instance.kiosk_exit_password,
                'inactivityTimeoutSeconds': instance.kiosk_inactivity_timeout_seconds,
                'showBestScores': instance.kiosk_show_best_scores,
            },
            'games': {
                'memory': {
                    'enabled': instance.game_memory_enabled,
                    'pairs': instance.game_memory_pairs,
                },
                'puzzle': {'enabled': instance.game_puzzle_enabled},
                'reaction': {'enabled': instance.game_reaction_enabled},
                'simon': {
                    'enabled': instance.game_simon_enabled,
                    'colors': instance.game_simon_colors,
                    'speedMs': instance.game_simon_speed_ms,
                },
                'whack': {
                    'enabled': instance.game_whack_enabled,
                    'durationSeconds': instance.game_whack_duration_seconds,
                },
                'speedtap': {
                    'enabled': instance.game_speedtap_enabled,
                    'durationSeconds': instance.game_speedtap_duration_seconds,
                },
                'balloonpop': {
                    'enabled': instance.game_balloonpop_enabled,
                    'durationSeconds': instance.game_balloonpop_duration_seconds,
                },
            },
            'records': {
                'enabled': instance.records_enabled,
                'requireRut': instance.records_require_rut,
                'requireName': instance.records_require_name,
                'maxEntriesPerGame': instance.records_max_entries_per_game,
            },
            'updatedAt': instance.updated_at.isoformat() if instance.updated_at else None,
        }


class ClientConfigListSerializer(serializers.ModelSerializer):
    leaderboard_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = ClientConfig
        fields = ['id', 'code', 'is_active', 'client_name', 'client_subtitle',
                  'branding_primary_color', 'leaderboard_count', 'updated_at']


class ClientConfigWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientConfig
        exclude = ['id', 'created_at', 'updated_at', 'client_logo', 'client_favicon']


class LeaderboardEntrySerializer(serializers.ModelSerializer):
    client_code = serializers.SlugRelatedField(
        source='client',
        slug_field='code',
        queryset=ClientConfig.objects.all()
    )

    class Meta:
        model = LeaderboardEntry
        fields = [
            'id', 'client_code', 'game_id', 'player_name', 'player_rut',
            'score', 'is_higher_better', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
