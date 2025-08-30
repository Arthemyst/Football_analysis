from rest_framework import serializers

from players.models import Player, PlayerStatistics


class PlayerStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerStatistics
        fields = '__all__'


class PlayersSerializer(serializers.ModelSerializer):
    statistics = PlayerStatisticsSerializer(many=True, source='playerstatistics_set')

    class Meta:
        model = Player
        fields = ["id", "short_name", "long_name", "nationality", "statistics"]


class PlayerBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["id", "short_name", "long_name", "nationality"]
