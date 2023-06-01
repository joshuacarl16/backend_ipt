from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    userId = models.CharField(primary_key=True, max_length=100)
    username = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)

    def __str__(self):
        return self.userId

class Category(models.Model):
    categoryId = models.CharField(max_length=100, primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    categoryName = models.CharField(max_length=100)

    def create_initial_category(sender, **kwargs):
        if sender.name == 'api':
            Category.objects.get_or_create(
                categoryId='category_id',
                categoryName='all'
            )

class Topic(models.Model):
    title = models.CharField(max_length=200)
    topicId = models.CharField(max_length=100, primary_key=True)
    description = models.TextField()
    categoryId = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    commentId = models.CharField(max_length=100, primary_key=True)
    topicId = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=100)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    replies = models.CharField(max_length=100, null=True)



    def save(self, *args, **kwargs):
        super(Comment, self).save(*args, **kwargs)
        self.topicId.save()

class Reply(models.Model):
    replyId = models.CharField(max_length=100, primary_key=True)
    commentId = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    replyContent = models.CharField(max_length=1000)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Reply, self).save(*args, **kwargs)
        self.commentId.save()
        self.commentId.topicId.save()
