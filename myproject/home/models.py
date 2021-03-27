from django.db import models


action_type_choices = [("ask for info", "ask for info"),("technical support", "technical support"),( "view product info", "view product info"),( "view product list", "view product list"),( "visit home page", "visit home page"),( 
                        "purchase", "purchase"),( "add to cart", "add to cart"),( "remove to cart", "remove to cart"),( "search", "search"),( "view ad", "view ad"),( "join program", "join program"),( "complaint", "complaint"),( "review", "review"),( "rate", "rate"),( "read blog", "read blog"),( "make survey", "make survey"),( "return product", "return product"),( "guarantee", "guarantee")]
channel_choices = [("web", "web"), ("app", "app"), ("email", "email"), ("call", "call"), ("sms", "sms"), ("store", "store")]
browser_choices = [("chrome", "chrome"), ("safari", "safari"), ("firefox", "firefox")]
os_choices = [("android", "android"), ("ios", "ios"), ("windows", "windows"), ("macos", "macos"), ("linux", "linux")]
device_category_choices = [("mobile", "mobile"), ("tablet", "tablet"), ("laptop", "laptop"), ("desktop", "desktop")]
source_name_choices = [("Facebook", "Facebook"), ("Google", "Google"), ("Youtube", "Youtube"), ("Twitter", "Twitter")]
interract_item_type_choices = [("product", "product"), ("post", "post"), ("blog", "blog"), ("survey", "survey"), ("campaign", "campaign"), ("loyaltyprogram", "loyalty program"), ("review", "review"), ("advertisement", "advertisement"), ("mail", "mail")]
user_item_type_choices = [("transaction", "transaction"), ("post", "post"), ("blog", "blog"), ("survey", "survey"), ("review", "review"), ("mail", "mail")]
transaction_status_choices = [("packaging", "packaging"), ("delivering", "delivering"), ("received", "received")]

class contactForm(models.Model):
    username = models.BigIntegerField(primary_key=True)
    email = models.DateField(blank=True, null=True)
    bod = models.DateField(blank=True, null=True)
    

class Product(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)
    category = models.CharField(max_length=300, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    sku = models.IntegerField(blank=True, null=True)
    promotion = models.CharField(max_length=300, blank=True, null=True)
    record_time = models.DateTimeField(auto_now=True)


class Post(models.Model):
    userID = models.BigIntegerField(blank=True, null=True)
    url = models.CharField(max_length=300, blank=True, null=True)
    content = models.CharField(max_length=300, blank=True, null=True)
    record_time = models.DateTimeField(auto_now=True)

class Blog(models.Model):
    userID = models.BigIntegerField(blank=True, null=True)
    url = models.CharField(max_length=300, blank=True, null=True)
    content = models.CharField(max_length=300, blank=True, null=True)
    record_time = models.DateTimeField(auto_now=True)


class Survey(models.Model):
    userID = models.BigIntegerField(blank=True, null=True)
    url = models.CharField(max_length=300, blank=True, null=True)
    content = models.CharField(max_length=300, blank=True, null=True)
    record_time = models.DateTimeField(auto_now=True)

class Campaign(models.Model):
    url = models.CharField(max_length=300, blank=True, null=True)
    content = models.CharField(max_length=300, blank=True, null=True)
    record_time = models.DateTimeField(auto_now=True)

class Review(models.Model):
    userID = models.BigIntegerField(blank=True, null=True)
    url = models.CharField(max_length=300, blank=True, null=True)
    content = models.CharField(max_length=300, blank=True, null=True)
    record_time = models.DateTimeField(auto_now=True)

class Mail(models.Model):
    userID = models.BigIntegerField(blank=True, null=True)
    url = models.CharField(max_length=300, blank=True, null=True)
    content = models.CharField(max_length=300, blank=True, null=True)
    senderEmail = models.CharField(max_length=300, blank=True, null=True)
    receiverEmail = models.CharField(max_length=300, blank=True, null=True)
    record_time = models.DateTimeField(auto_now=True)

class Advertisement(models.Model):
    url = models.CharField(max_length=300, blank=True, null=True)
    content = models.CharField(max_length=300, blank=True, null=True)
    record_time = models.DateTimeField(auto_now=True)

class LoyaltyProgram(models.Model):
    url = models.CharField(max_length=300, blank=True, null=True)
    content = models.CharField(max_length=300, blank=True, null=True)
    record_time = models.DateTimeField(auto_now=True)

class Transaction(models.Model):
    userID = models.BigIntegerField(blank=True, null=True)
    revenue = models.FloatField(blank=True, null=True)
    shippingFee = models.FloatField(blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    status = models.CharField(max_length=300, blank=True, null=True, choices=transaction_status_choices)
    record_time = models.DateTimeField(auto_now=True)

class User(models.Model):
    username = models.CharField(max_length=300, blank=True, null=True)
    password = models.CharField(max_length=300, blank=True, null=True)
    email = models.CharField(max_length=300, blank=True, null=True)
    dob = models.DateField(max_length=300, blank=True, null=True)
    gender = models.CharField(max_length=300, blank=True, choices = [("M", "M"), ("F", "F")])
    address = models.CharField(max_length=300, blank=True, null=True)
    phoneNumber = models.CharField(max_length=300, blank=True)

class Touchpoint(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(blank=True, null=True)
    action_type = models.CharField(max_length=300, blank=True, null=True)
    visit_time = models.DateTimeField(null=True)
    active_time = models.BigIntegerField(blank=True, null=True, default=0)
    channel_type = models.CharField(max_length=300, blank=True, null=True)
    browser = models.CharField(max_length=300, blank=True, null=True, choices=browser_choices)
    os = models.CharField(max_length=300, blank=True, null=True, choices=os_choices)
    device_category = models.CharField(max_length=300, blank=True, null=True, choices=device_category_choices)
    geo_continent = models.CharField(max_length=300, blank=True, null=True)
    geo_country = models.CharField(max_length=300, blank=True, null=True)
    geo_city = models.CharField(max_length=300, blank=True, null=True)
    source_name = models.CharField(max_length=300, blank=True, null=True)
    source_url = models.CharField(max_length=300, blank=True, null=True)
    ad_url = models.CharField(max_length=300, blank=True, null=True)
    ad_content = models.CharField(max_length=300, blank=True, null=True)
    campaign_url = models.CharField(max_length=300, blank=True, null=True)
    campaign_content = models.CharField(max_length=300, blank=True, null=True)
    store_id = models.BigIntegerField(blank=True, null=True)
    employee_id = models.BigIntegerField(blank=True, null=True)
    webpage_url = models.CharField(max_length=300, blank=True, null=True)
    webpage_title = models.CharField(max_length=300, blank=True, null=True)
    webpage_id = models.BigIntegerField(blank=True, null=True)
    app_name = models.CharField(max_length=300, blank=True, null=True)
    app_screen = models.CharField(max_length=300, blank=True, null=True)
    app_screen_title = models.CharField(max_length=300, blank=True, null=True)
    app_screen_id = models.BigIntegerField(blank=True, null=True)
    interract_item_type = models.CharField(max_length=300, blank=True, null=True, choices=interract_item_type_choices)
    interract_item_id = models.BigIntegerField(blank=True, null=True)
    interract_item_url = models.CharField(max_length=300, blank=True, null=True)
    interract_item_content = models.CharField(max_length=300, blank=True, null=True)
    user_item_type = models.CharField(max_length=300, blank=True, null=True, choices=user_item_type_choices)
    user_item_id = models.BigIntegerField(blank=True, null=True)
    user_item_url = models.CharField(max_length=300, blank=True, null=True)
    user_item_content = models.CharField(max_length=300, blank=True, null=True)
    experience_score = models.FloatField(blank=True, null=True)
    experience_emotion = models.CharField(max_length=300, blank=True, null=True)
    other_content = models.CharField(max_length=300, blank=True, null=True)
    record_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_id}, {self.visit_time}, {self.action_type}, {self.channel_type}, {self.device_category}, {self.source_name}, {self.experience_emotion}"


class Cluster(models.Model):
    id = models.AutoField(primary_key=True)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    numberClusters = models.IntegerField(blank=True, null=True)
    algorithm = models.CharField(max_length=300, blank=True, null=True)
    preprocessing = models.CharField(max_length=300, blank=True, null=True)
    accuracy = models.FloatField(blank=True, null=True)
    error = models.FloatField(blank=True, null=True)
    preprocessingModelFile = models.CharField(max_length=300, blank=True, null=True)
    clusterModelFile = models.CharField(max_length=300, blank=True, null=True)
    runDate = models.DateTimeField(auto_now=True)


class ClusterGraph(models.Model):
    id = models.AutoField(primary_key=True)
    clusterID = models.IntegerField(blank=True, null=True)
    clusterNumber = models.IntegerField(blank=True, null=True)
    clusterName = models.CharField(max_length=300, blank=True, default="undefined")
    type = models.CharField(max_length=300, blank=True, null=True)
    link = models.CharField(max_length=300, blank=True, null=True)


class ProcessGraph(models.Model):
    id = models.AutoField(primary_key=True)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    runDate = models.DateTimeField()
    type = models.CharField(max_length=300, blank=True, null=True)
    link = models.CharField(max_length=300, blank=True, null=True)

class ClusteredUser(models.Model):
    userID = models.BigIntegerField(blank=True, null=True)
    clusterDate = models.DateTimeField(auto_now=True)
    fromDate = models.DateField()
    toDate = models.DateField()
    journey = models.JSONField()
    clusterID = models.IntegerField(blank=True, null=True)
    clusterNumber = models.IntegerField(blank=True, null=True)
    clusterName = models.CharField(max_length=300, blank=True, null=True)
    clusterGraphLink = models.CharField(max_length=300, blank=True, null=True)

