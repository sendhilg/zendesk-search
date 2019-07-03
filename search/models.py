from django.db import models


class Organization(models.Model):
    _id = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=1000, blank=True, null=True, default='')
    external_id = models.CharField(max_length=1000, blank=True, null=True, default='')
    name = models.CharField(max_length=1000, blank=True, null=True, default='')
    domain_names = models.CharField(max_length=1000, blank=True, null=True, default='')
    created_at = models.CharField(max_length=1000, blank=True, null=True, default='')
    details = models.CharField(max_length=1000, blank=True, null=True, default='')
    shared_tickets = models.CharField(max_length=1000, blank=True, null=True, default='')
    tags = models.CharField(max_length=1000, blank=True, null=True, default='')

    def __str__(self):
        user_representation = ''
        for user in self.users.all():
            user_representation = (
                f'user_id                       {user._id}\n'
                f'user_name                     {user.name}\n'
            )

        ticket_representation = ''
        for ticket in self.tickets.all():
            ticket_representation = (
                f'ticket_id                     {ticket._id}\n'
                f'ticket_subject                {ticket.subject}\n'
            )
        return (
            '\n'
            f'_id                           {self._id}\n'
            f'url                           {self.url}\n'
            f'external_id                   {self.external_id}\n'
            f'name                          {self.name}\n'
            f'domain_names                  {self.domain_names}\n'
            f'created_at                    {self.created_at}\n'
            f'details                       {self.details}\n'
            f'shared_tickets                {self.shared_tickets}\n'
            f'tags                          {self.tags}\n'
            f'{user_representation}'
            f'{ticket_representation}'
        )


class User(models.Model):
    _id = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=1000, blank=True, null=True, default='')
    external_id = models.CharField(max_length=1000, blank=True, null=True, default='')
    name = models.CharField(max_length=1000, blank=True, null=True, default='')
    alias = models.CharField(max_length=1000, blank=True, null=True, default='')
    created_at = models.CharField(max_length=1000, blank=True, null=True, default='')
    active = models.CharField(max_length=1000, blank=True, null=True, default='')
    verified = models.CharField(max_length=1000, blank=True, null=True, default='')
    shared = models.CharField(max_length=1000, blank=True, null=True, default='')
    locale = models.CharField(max_length=1000, blank=True, null=True, default='')
    timezone = models.CharField(max_length=1000, blank=True, null=True, default='')
    last_login_at = models.CharField(max_length=1000, blank=True, null=True, default='')
    email = models.CharField(max_length=1000, blank=True, null=True, default='')
    phone = models.CharField(max_length=1000, blank=True, null=True, default='')
    signature = models.CharField(max_length=1000, blank=True, null=True, default='')
    organization_id = models.ForeignKey(
        'Organization',
        on_delete=models.PROTECT,
        related_name='users',
        null=True,
        to_field='_id',
    )
    tags = models.CharField(max_length=1000, blank=True, null=True, default='')
    suspended = models.CharField(max_length=1000, blank=True, null=True, default='')
    role = models.CharField(max_length=1000, blank=True, null=True, default='')

    def __str__(self):
        organization_representation = ''
        if self.organization_id:
            organization_representation = (
                f'organization_id               {self.organization_id._id}\n'
                f'orgnaization_name             {self.organization_id.name}\n'
            )

        submitted_ticket_representation = ''
        for ticket in self.submitted_tickets.all():
            submitted_ticket_representation = (
                f'submitted_ticket_id           {ticket._id}\n'
                f'submitted_ticket_subject      {ticket.subject}\n'
            )

        assigned_ticket_representation = ''
        for ticket in self.assigned_tickets.all():
            assigned_ticket_representation = (
                f'assigned_ticket_id            {ticket._id}\n'
                f'assigned_ticket_subject       {ticket.subject}\n'
            )
        return (
            '\n'
            f'_id                           {self._id}\n'
            f'url                           {self.url}\n'
            f'external_id                   {self.external_id}\n'
            f'name                          {self.name}\n'
            f'alias                         {self.alias}\n'
            f'created_at                    {self.created_at}\n'
            f'active                        {self.active}\n'
            f'verified                      {self.verified}\n'
            f'shared                        {self.shared}\n'
            f'locale                        {self.locale}\n'
            f'timezone                      {self.timezone}\n'
            f'last_login_at                 {self.last_login_at}\n'
            f'email                         {self.email}\n'
            f'phone                         {self.phone}\n'
            f'signature                     {self.signature}\n'
            f'tags                          {self.tags}\n'
            f'suspended                     {self.suspended}\n'
            f'role                          {self.role}\n'
            f'{organization_representation}'
            f'{submitted_ticket_representation}'
            f'{assigned_ticket_representation}'
        )


class Ticket(models.Model):
    _id = models.CharField(max_length=1000, primary_key=True)
    url = models.CharField(max_length=1000, blank=True, null=True, default='')
    external_id = models.CharField(max_length=1000, blank=True, null=True, default='')
    created_at = models.CharField(max_length=1000, blank=True, null=True, default='')
    type = models.CharField(max_length=1000, blank=True, null=True, default='')
    subject = models.CharField(max_length=1000, blank=True, null=True, default='')
    description = models.CharField(max_length=1000, blank=True, null=True, default='')
    priority = models.CharField(max_length=1000, blank=True, null=True, default='')
    status = models.CharField(max_length=1000, blank=True, null=True, default='')
    submitter_id = models.ForeignKey(
        'User',
        on_delete=models.PROTECT,
        related_name='submitted_tickets',
        null=True,
        to_field='_id',
    )
    assignee_id = models.ForeignKey(
        'User',
        on_delete=models.PROTECT,
        related_name='assigned_tickets',
        null=True,
        to_field='_id',
    )
    organization_id = models.ForeignKey(
        'Organization',
        on_delete=models.PROTECT,
        related_name='tickets',
        null=True,
        to_field='_id',
    )
    tags = models.CharField(max_length=1000, blank=True, null=True, default='')
    has_incidents = models.CharField(max_length=1000, blank=True, null=True, default='')
    due_at = models.CharField(max_length=1000, blank=True, null=True, default='')
    via = models.CharField(max_length=1000, blank=True, null=True, default='')

    def __str__(self):
        organization_representation = ''
        if self.organization_id:
            organization_representation = (
                f'organization_id               {self.organization_id._id}\n'
                f'orgnaization_name             {self.organization_id.name}\n'
            )

        submitter_representation = ''
        if self.submitter_id:
            submitter_representation = (
                f'submitter_id                  {self.submitter_id._id}\n'
                f'submitter_name                {self.submitter_id.name}\n'
            )

        assignee_representation = ''
        if self.assignee_id:
            assignee_representation = (
                f'assignee_id                   {self.assignee_id._id}\n'
                f'assignee_name                 {self.assignee_id.name}\n'
            )

        return (
            '\n'
            f'_id                           {self._id}\n'
            f'url                           {self.url}\n'
            f'external_id                   {self.external_id}\n'
            f'created_at                    {self.created_at}\n'
            f'type                          {self.type}\n'
            f'subject                       {self.subject}\n'
            f'description                   {self.description}\n'
            f'priority                      {self.priority}\n'
            f'status                        {self.status}\n'
            f'tags                          {self.tags}\n'
            f'has_incidents                 {self.has_incidents}\n'
            f'due_at                        {self.due_at}\n'
            f'via                           {self.via}\n'
            f'{organization_representation}'
            f'{submitter_representation}'
            f'{assignee_representation}'
        )
