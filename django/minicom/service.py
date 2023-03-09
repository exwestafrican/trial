import typing
from dataclasses import dataclass
from minicom.models import (
    CompanyModel,
    CompanyMessagePromptModel,
    MessageModel,
    ConversationModel,
    EmployeeModel,
)
from minicom.constants import UserRoleEnum


class CustomerIntercomMessanger:
    def __init__(self):
        self.company_model = CompanyModel
        self.company_prompt_model = CompanyMessagePromptModel
        self.message_model = MessageModel
        self.conversation_model = ConversationModel

    def get_prompt(self, company_domain: str) -> CompanyMessagePromptModel:
        cleaned_domain = company_domain.lower()
        prompt = self.company_prompt_model.objects.filter(
            company__domain=cleaned_domain
        ).last()
        return prompt

    def start_conversation(self, msg: str, company_domain: str):
        company = self.company_model.objects.get(domain=company_domain)
        conv_model = self.conversation_model.objects.create(
            user_role=UserRoleEnum.LEAD.value,
            in_conversation_with=company,
        )
        return self.message_model.objects.create(
            conversation=conv_model,
            content=msg,
            from_organisation=False,
        )

    def send_message(self, msg: str, conversation_ref: int) -> MessageModel:
        print(msg, conversation_ref)
        return self.message_model.objects.create(
            conversation=self.conversation_model(id=conversation_ref),
            content=msg,
            from_organisation=False,
        )

    def fetch_unseen_messages(self, conversation_id: int) -> typing.List[MessageModel]:
        # view unseen from organization
        unseen_msg_query = self.message_model.objects.filter(
            conversation__id=conversation_id, seen=False, from_organisation=True
        ).prefetch_related("conversation")
        unseen_messages = list(unseen_msg_query)
        unseen_msg_query.update(seen=True)
        return unseen_messages


class SupportIntercomMessanger:
    def __init__(self):
        self.company_model = CompanyModel
        self.company_prompt_model = CompanyMessagePromptModel
        self.message_model = MessageModel
        self.conversation_model = ConversationModel
        self.employee_model = EmployeeModel

    def send_message(self, msg: str, conversation_ref: int) -> MessageModel:
        print(msg, conversation_ref)
        # get sender_id
        convo_model = self.conversation_model.objects.get(id=conversation_ref)
        emp_model = self.employee_model.objects.filter(
            company=convo_model.in_conversation_with
        ).last()
        return self.message_model.objects.create(
            conversation=self.conversation_model(id=conversation_ref),
            content=msg,
            from_organisation=True,
            sender=emp_model,
        )

    def fetch_unseen_messages(self, conversation_id: int) -> typing.List[MessageModel]:
        # view unseen from organization
        unseen_msg_query = self.message_model.objects.filter(
            conversation__id=conversation_id, seen=False, from_organisation=False
        ).prefetch_related("conversation")
        unseen_messages = list(unseen_msg_query)
        print("unseen-->", unseen_messages)
        unseen_msg_query.update(seen=True)
        return unseen_messages
