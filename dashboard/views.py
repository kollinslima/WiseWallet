from django.views.generic import TemplateView

class DashboardView(TemplateView):
    template_name = "dashboard/dashboard.html"

    #  def get_context_data(self, **kwargs):
    #      context = super().get_context_data(**kwargs)
    #      context["latest_articles"] = Article.objects.all()[:5]
    #      return context

