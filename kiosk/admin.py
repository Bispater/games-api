from django.contrib import admin
from .models import ClientConfig, LeaderboardEntry


@admin.register(ClientConfig)
class ClientConfigAdmin(admin.ModelAdmin):
    list_display = ['code', 'client_name', 'is_active', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['code', 'client_name']

    fieldsets = (
        ('Identificación', {
            'fields': ('code', 'is_active')
        }),
        ('Cliente', {
            'fields': ('client_name', 'client_subtitle', 'client_logo', 'client_favicon')
        }),
        ('Branding', {
            'fields': (
                'branding_primary_color', 'branding_primary_hover',
                'branding_primary_dark', 'branding_primary_light',
                'branding_accent_color', 'branding_accent_light',
                'branding_background_color', 'branding_card_background',
                'branding_text_primary', 'branding_text_muted', 'branding_border_color',
            )
        }),
        ('Kiosko', {
            'fields': ('kiosk_exit_password', 'kiosk_inactivity_timeout_seconds', 'kiosk_show_best_scores')
        }),
        ('Juegos', {
            'fields': (
                'game_memory_enabled', 'game_memory_pairs',
                'game_puzzle_enabled',
                'game_reaction_enabled',
                'game_simon_enabled', 'game_simon_colors', 'game_simon_speed_ms',
                'game_whack_enabled', 'game_whack_duration_seconds',
                'game_speedtap_enabled', 'game_speedtap_duration_seconds',
                'game_balloonpop_enabled', 'game_balloonpop_duration_seconds',
            )
        }),
        ('Records', {
            'fields': ('records_enabled', 'records_require_rut', 'records_require_name', 'records_max_entries_per_game')
        }),
    )


@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ['client', 'player_name', 'game_id', 'score', 'created_at']
    list_filter = ['client', 'game_id']
    search_fields = ['player_name', 'player_rut']
