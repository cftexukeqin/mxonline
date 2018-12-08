from haystack import indexes
from apps.course.models import Course,CourseOrg
from apps.organization.models import Teacher


class CourseIndex(indexes.SearchIndex,indexes.Indexable):

    text = indexes.CharField(document=True,use_template=True)

    def get_model(self):
        return Course

    def index_queryset(self, using=None):
        # print(self.get_model().objects.all().count())
        return self.get_model().objects.all()


