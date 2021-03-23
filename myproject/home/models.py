from django.db import models


action_type_choices = [("ask for info", "ask for info"),("technical support", "technical support"),( "view product info", "view product info"),( "view product list", "view product list"),( "visit home page", "visit home page"),( 
                        "purchase", "purchase"),( "add to cart", "add to cart"),( "remove to cart", "remove to cart"),( "search", "search"),( "view ad", "view ad"),( "join program", "join program"),( "complaint", "complaint"),( "review", "review"),( "rate", "rate"),( "read blog", "read blog"),( "make survey", "make survey"),( "return product", "return product"),( "guarantee", "guarantee")]
channel_choices = [("web", "web"), ("app", "app"), ("email", "email"), ("call", "call"), ("sms", "sms"), ("store", "store")]
browser_choices = [("chrome", "chrome"), ("safari", "safari"), ("firefox", "firefox")]
os_choices = [("android", "android"), ("ios", "ios"), ("windows", "windows"), ("macos", "macos"), ("linux", "linux")]
device_category_choices = [("mobile", "mobile"), ("tablet", "tablet"), ("laptop", "laptop"), ("desktop", "desktop")]
source_name_choices = [("Facebook", "Facebook"), ("Google", "Google"), ("Youtube", "Youtube"), ("Twitter", "Twitter")]
interract_item_type_choices = [("Product", "Product"), ("Post", "Post"), ("Blog", "Blog"), ("Survey", "Survey"), ("Campaign", "Campaign"), ("Loyalty Program", "Loyalty Program"), ("Review", "Review"), ("Advertisement", "Advertisement"), ("Mail", "Mail")]
user_item_type_choices = [("Transaction", "Transaction"), ("Post", "Post"), ("Blog", "Blog"), ("Survey", "Survey"), ("Review", "Review"), ("Mail", "Mail")]

class contactForm(models.Model):
    username = models.BigIntegerField(primary_key=True)
    email = models.DateField(blank=True, null=True)
    bod = models.DateField(blank=True, null=True)



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


class Graph(models.Model):
    id = models.AutoField(primary_key=True)
    runDate = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=300, blank=True, null=True)
    startDate = models.DateTimeField(blank=True, null=True)
    endDate = models.DateTimeField(blank=True, null=True)
    link = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return f"{self.runDate}, {self.type}, {self.startDate}, {self.endDate}, {self.link}"
