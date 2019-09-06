from rest_framework import viewsets

from articles.models import CVE, CNNVD, News
from articles.serializers import CVESerializer, CNNVDSerializer, NewsSerializer


class CVEViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CVE.objects.all()
    serializer_class = CVESerializer


class CNNVDViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = CNNVD.objects.all()
    serializer_class = CNNVDSerializer


class NewsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer

