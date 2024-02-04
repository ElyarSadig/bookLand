from django.db import models
import os
import hashlib
from django.utils import timezone
from users.api.utils import generate_random_code
from users.api.file_handler import process_and_upload_identity_path, process_and_upload_publications_image

PUBLISHER_ROLE_ID = 1
CUSTOMER_ROLE_ID = 2

class User(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    username = models.CharField(max_length=255, unique=True, db_column='username')
    email = models.EmailField(unique=True, db_column='email')
    password = models.CharField(max_length=255, db_column='hashedpassword')
    salt = models.CharField(max_length=255, db_column='salt')
    is_active = models.BooleanField(db_column='isactive', default=True)
    registration_date = models.DateTimeField(db_column='registrationdate', auto_now_add=True)
    last_login_date = models.DateTimeField(null=True, blank=True, db_column='lastlogindate')
    is_publisher = models.BooleanField(db_column='ispublisher')
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True, db_column='phonenumber')
    phone_number2 = models.CharField(max_length=20, null=True, blank=True, db_column='phonenumber2')
    address = models.TextField(null=True, blank=True, db_column='address')
    identity_image = models.CharField(null=True, blank=True, db_column='identityimage', max_length=255)
    card_number = models.CharField(max_length=50, null=True, blank=True, db_column='cardnumber')
    publications_name = models.CharField(max_length=255, unique=True, null=True, blank=True, db_column='publicationsname')
    publications_image = models.CharField(null=True, blank=True, db_column='publicationsimage')
    is_confirm = models.BooleanField(db_column='isconfirm')

    def set_password(self, raw_password):
        salt = os.urandom(32).hex()

        password_salt = raw_password + salt
        self.password = hashlib.sha256(password_salt.encode()).hexdigest()
        self.salt = salt

        self.save()

    def password_valid(self, raw_password):
        password_salt = raw_password + self.salt
        hashed_password = hashlib.sha256(password_salt.encode()).hexdigest()

        return hashed_password == self.password

    @classmethod
    def update_publisher_files(cls, user_id, publications_image, identity_image):
        user = cls.objects.get(pk=user_id)

        if publications_image:
            user.publications_image = process_and_upload_publications_image(publications_image)

        if identity_image:
            user.identity_image = process_and_upload_identity_path(identity_image)

        user.save()

    def __str__(self):
        return self.username

    class Meta:
        managed = False
        db_table = 'users'


class UserActivityCode(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    email = models.EmailField(db_column='email')
    activity_code = models.CharField(max_length=6, db_column='activationcode')
    created_date_time = models.DateTimeField(auto_now_add=True, db_column='createddatetime')
    expire_date_time = models.DateTimeField(db_column='expiredatetime')

    @classmethod
    def valid_user_activity_code(cls, email, activation_code):
        try:
            latest_code = cls.objects.filter(email=email).latest('created_date_time')
        except cls.DoesNotExist:
            return False

        current_datetime = timezone.now()

        if current_datetime > latest_code.expire_date_time.replace(tzinfo=timezone.utc):
            return False

        if latest_code.activity_code != activation_code:
            return False

        return True

    @classmethod
    def create_user_activity_code(cls, email):
        activation_code = generate_random_code()
        expire_duration = timezone.timedelta(hours=3, minutes=32)
        expire_datetime = timezone.now() + expire_duration

        user_activity_code = cls(email=email, activity_code=activation_code, expire_date_time=expire_datetime)
        user_activity_code.save()

        return user_activity_code

    def __str__(self):
        return self.email + " | " + self.activity_code

    class Meta:
        managed = False
        db_table = 'useractivitycodes'


class Role(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    role = models.CharField(max_length=50, unique=True, db_column='role')
    description = models.TextField(db_column='description', blank=True, null=True)

    def __str__(self):
        return self.role

    class Meta:
        managed = False
        db_table = 'roles'


class UserRole(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    user = models.ForeignKey(User, db_column='userid', on_delete=models.CASCADE)
    role = models.ForeignKey(Role, db_column='roleid', on_delete=models.CASCADE)

    @classmethod
    def get_user_role_id(cls, user_id):
        try:
            role_id = cls.objects.filter(user_id=user_id).values_list('role_id', flat=True).first()
            return role_id if role_id is not None else CUSTOMER_ROLE_ID
        except cls.DoesNotExist:
            return CUSTOMER_ROLE_ID

    @classmethod
    def assign_customer_role(cls, user_id):
        cls.objects.create(user_id=user_id, role_id=CUSTOMER_ROLE_ID)
        return CUSTOMER_ROLE_ID

    @classmethod
    def assign_publisher_role(cls, user_id):
        cls.objects.create(user_id=user_id, role_id=PUBLISHER_ROLE_ID)
        return PUBLISHER_ROLE_ID



    def __str__(self):
        return self.user.username + " is a " + str(self.role)

    class Meta:
        managed = False
        db_table = 'userroles'

