from django.contrib import admin
from Home.models import Customer,Dealer,Project,Plot,Deal,Payment,Due,CommissionPayment

# Register your models here.


admin.site.register(Customer)
admin.site.register(Dealer)
admin.site.register(Project)
admin.site.register(Plot)
admin.site.register(Deal)
admin.site.register(Due)
admin.site.register(Payment)
admin.site.register(CommissionPayment)