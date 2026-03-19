from django.db import models


class ClientConfig(models.Model):
    """
    Configuration for a specific kiosk client.
    Each client is identified by a unique code (e.g. "ENT01").
    The kiosk fetches its config via: GET /api/config/ENT01/
    """

    code = models.CharField(
        max_length=50, unique=True, db_index=True,
        help_text='Código único del cliente, ej: ENT01'
    )
    is_active = models.BooleanField(default=True)

    # ── Client ──
    client_name = models.CharField(max_length=200, default='Mi Cliente')
    client_subtitle = models.CharField(max_length=300, default='Zona de entretenimiento')
    client_logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    client_favicon = models.ImageField(upload_to='favicons/', blank=True, null=True)

    # ── Branding ──
    branding_primary_color = models.CharField(max_length=9, default='#1400FF')
    branding_primary_hover = models.CharField(max_length=9, default='#0f00cc')
    branding_primary_dark = models.CharField(max_length=9, default='#0a0099')
    branding_primary_light = models.CharField(max_length=9, default='#6b5cff')
    branding_accent_color = models.CharField(max_length=9, default='#FF6600')
    branding_accent_light = models.CharField(max_length=9, default='#ff8533')
    branding_background_color = models.CharField(max_length=9, default='#f0f4f8')
    branding_card_background = models.CharField(max_length=9, default='#ffffff')
    branding_text_primary = models.CharField(max_length=9, default='#1e293b')
    branding_text_muted = models.CharField(max_length=9, default='#636e72')
    branding_border_color = models.CharField(max_length=9, default='#e2e8f0')

    # ── Kiosk ──
    kiosk_exit_password = models.CharField(max_length=50, default='1234')
    kiosk_inactivity_timeout_seconds = models.PositiveIntegerField(default=120)
    kiosk_show_best_scores = models.BooleanField(default=True)

    # ── Games config ──
    game_memory_enabled = models.BooleanField(default=True)
    game_memory_pairs = models.PositiveIntegerField(default=8)
    game_puzzle_enabled = models.BooleanField(default=True)
    game_reaction_enabled = models.BooleanField(default=True)
    game_simon_enabled = models.BooleanField(default=True)
    game_simon_colors = models.PositiveIntegerField(default=9)
    game_simon_speed_ms = models.PositiveIntegerField(default=400)
    game_whack_enabled = models.BooleanField(default=True)
    game_whack_duration_seconds = models.PositiveIntegerField(default=30)
    game_speedtap_enabled = models.BooleanField(default=True)
    game_speedtap_duration_seconds = models.PositiveIntegerField(default=30)
    game_balloonpop_enabled = models.BooleanField(default=True)
    game_balloonpop_duration_seconds = models.PositiveIntegerField(default=45)

    # ── Records ──
    records_enabled = models.BooleanField(default=True)
    records_require_rut = models.BooleanField(default=True)
    records_require_name = models.BooleanField(default=True)
    records_max_entries_per_game = models.PositiveIntegerField(default=10)

    # ── Meta ──
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuración de Cliente'
        verbose_name_plural = 'Configuraciones de Clientes'
        ordering = ['code']

    def __str__(self):
        return f'{self.code} — {self.client_name}'


class LeaderboardEntry(models.Model):
    """A player's score entry for a specific game on a specific client."""

    GAME_CHOICES = [
        ('memory', 'Memory Match'),
        ('puzzle', 'Slide Puzzle'),
        ('reaction', 'Reaction Time'),
        ('simon', 'Simon Says'),
        ('whack', 'Atrapa el Logo'),
        ('speedtap', 'Speed Tap'),
        ('balloonpop', 'Balloon Pop'),
    ]

    client = models.ForeignKey(
        ClientConfig, on_delete=models.CASCADE, related_name='leaderboard_entries'
    )
    game_id = models.CharField(max_length=50, choices=GAME_CHOICES)
    player_name = models.CharField(max_length=200)
    player_rut = models.CharField(max_length=20, blank=True, default='')
    score = models.IntegerField()
    is_higher_better = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Entrada de Leaderboard'
        verbose_name_plural = 'Entradas de Leaderboard'
        indexes = [
            models.Index(fields=['client', 'game_id', '-created_at']),
        ]

    def __str__(self):
        return f'{self.client.code} | {self.player_name} - {self.game_id}: {self.score}'
