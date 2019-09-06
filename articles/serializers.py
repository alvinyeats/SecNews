from rest_framework import serializers

from articles.models import CVE, CNNVD, News


class CVESerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CVE
        fields = ['id',]


class CNNVDSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CNNVD
        fields = ['id',]


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = News
        fields = ['id',]
