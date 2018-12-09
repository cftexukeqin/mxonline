from haystack import indexes
from apps.organization.models import Teacher,CourseOrg

class TeacherIndex(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True,use_template=True)

    def get_model(self):
        return Teacher

    def index_queryset(self, using=None):
        # print(self.get_model().objects.all().count())
        return self.get_model().objects.all()

class OrgIndex(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True,use_template=True)

    def get_model(self):
        return CourseOrg

    def index_queryset(self, using=None):
        # print(self.get_model().objects.all().count())
        return self.get_model().objects.all()