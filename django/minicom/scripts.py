from minicom.models import (
    CompanyModel,
    CompanyMessagePromptModel,
    ConversationModel,
    MessageModel,
    EmployeeModel
)
from minicom.constants import UserRoleEnum
from django.contrib.auth.models import User as UserModel
from minicom.service import *


company = CompanyModel.objects.create(
    name="Udemy inc.",
    address="2 Windmill Lane",
    city="Dublin",
    country_iso="IR",
    industry="E-Learning",
    domain="udemy.com",
)

sender = EmployeeModel.objects.create(
    user=UserModel.objects.create(username="summer"),
    company=company,
    is_author=True
)



prompt = CompanyMessagePromptModel.objects.create(
    company=company, 
    content="Lets get you the best learning experince there is"
)



support_messanger = SupportIntercomMessanger()






conversation = ConversationModel.objects.create(
    inconversatin_with=company,
    customer_name="Eddy Lang",
    customer_country_iso="IR",
    user_role=UserRoleEnum.LEAD.value,
)

new_customer_message = MessageModel.objects.create(
    conversation=ConversationModel(id=4),
    content="does it work!",
    from_organisation=False
)

new_company_message = EmployeeModel.objects.first()
