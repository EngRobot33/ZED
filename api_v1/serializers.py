from rest_framework import serializers

from user.models import User
from content.models import Post, Topic
from relation.models import Relation


# serialize user model to just return the fields we want
class UserSerialized(serializers.ModelSerializer):

    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name','profile_photo','banner_photo','bio','follower_count','following_count')   
    
    def get_follower_count(self, obj):
        return Relation.objects.filter(following=obj).count()
    
    def get_following_count(self, obj):
        return Relation.objects.filter(follower=obj).count()
    
# serialize posts model to just return the fields we want
class PostSerialized(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ('author','topic')

class FollowerListSerialized(serializers.ModelSerializer):
    
    follower__full_name = serializers.SerializerMethodField()
    follower__username = serializers.CharField(source='follower.username')
    follower__profile_photo = serializers.CharField(source='follower.profile_photo')

    class Meta:
        model = Relation
        fields = ('follower__full_name', 'follower__username','follower__profile_photo')

    def get_follower__full_name(self, obj):
        if (obj.follower.first_name and obj.follower.last_name):
            full_name = "%s %s" % (obj.follower.first_name, obj.follower.last_name)
            return full_name.strip()
        else:
            username = "%s" % (obj.follower.username, )
            return username.strip()
        
class FollowingListSerialized(serializers.ModelSerializer):
    
    following__full_name = serializers.SerializerMethodField()
    following__username = serializers.CharField(source='following.username')
    following__profile_photo = serializers.CharField(source='following.profile_photo')

    class Meta:
        model = Relation
        fields = ('following__full_name', 'following__username','following__profile_photo')

    def get_following__full_name(self, obj):
        if (obj.following.first_name and obj.following.last_name):
            full_name = "%s %s" % (obj.following.first_name, obj.following.last_name)
            return full_name.strip()
        else:
            username = "%s" % (obj.following.username, )
            return username.strip()
        
class TopicSerialized(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'name')