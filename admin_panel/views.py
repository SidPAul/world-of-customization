from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum, Count
from products.models import Product
from orders.models import Order
from authentication.models import CustomUser

class DashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'admin_panel/dashboard.html'

    def test_func(self):
        return self.request.user.role == 'admin'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_users'] = CustomUser.objects.count()
        context['total_products'] = Product.objects.count()
        context['total_orders'] = Order.objects.count()
        context['total_revenue'] = Order.objects.aggregate(total=Sum('items__price'))['total'] or 0
        
        # Data for charts
        orders_by_status = Order.objects.values('status').annotate(count=Count('id'))
        context['chart_labels'] = [item['status'] for item in orders_by_status]
        context['chart_data'] = [item['count'] for item in orders_by_status]
        
        return context
