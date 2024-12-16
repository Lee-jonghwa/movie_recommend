from rest_framework import serializers
from .models import Movie, Comment, MovieComment, MovieLike, Rate
from django.contrib.auth import get_user_model

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'username']
        read_only_fields = ['user']  # user 필드는 읽기 전용으로 설정
        
    def get_username(self, obj):
        return obj.user.username
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class MovieCommentSerializer(serializers.ModelSerializer):
    comment = CommentSerializer()
    
    class Meta:
        model = MovieComment
        fields = ['id', 'movie', 'comment']

class MovieRatingSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Rate
        fields = ['id', 'tdmb_id', 'movie', 'user', 'rate', 'username']
        read_only_fields = ['user']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Rate.objects.all(),
                fields=['movie', 'user'],
                message="이미 평가하셨습니다."
            )
        ]
        
    def get_username(self, obj):
        return obj.user.username

    def validate_rate(self, value):
        if not (0 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 0 and 5")
        return value
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class MovieLikeSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = MovieLike
        fields = ['id', 'movie', 'user', 'username']
        read_only_fields = ['user']
        
    def get_username(self, obj):
        return obj.user.username
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class MovieListSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Movie
        fields = ['id', 'title', 'genre', 'is_prized', 'rates', 
                 'likes_count', 'average_rating','poster_path', 'runtime', 'age', 'director', 'actors']
        
    def get_likes_count(self, obj):
        return obj.movielike_set.count()
        
    def get_average_rating(self, obj):
        return obj.rates

class MovieDetailSerializer(serializers.ModelSerializer):
    comments = MovieCommentSerializer(many=True, read_only=True, source='moviecomment_set')
    likes_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    user_has_liked = serializers.SerializerMethodField()
    user_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = '__all__'
        
    def get_likes_count(self, obj):
        return obj.movielike_set.count()
        
    def get_average_rating(self, obj):
        return obj.rates
        
    def get_user_has_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.movielike_set.filter(user=request.user).exists()
        return False

    def get_user_rating(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                rating = Rate.objects.get(movie=obj, user=request.user)
                return rating.rate
            except Rate.DoesNotExist:
                return None
        return None