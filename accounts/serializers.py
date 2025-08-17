from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model

# Get the active User model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Maps API 'name' field to model's 'full_name' field.
    Handles password validation and user creation.
    """
    name = serializers.CharField(
        source="full_name",  # Maps the API field 'name' to model field 'full_name'
        required=True,
        error_messages={
            'required': 'Name is required.',
            'blank': 'Name cannot be blank.'
        }
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={
            "min_length": "Password must be at least 8 characters long."
        }
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'name']

    def validate_email(self, value):
        """
        Check if the email is already registered.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already taken.")
        return value

    def create(self, validated_data):
        """
        Create a new user using `create_user` to handle hashing password.
        """
        return User.objects.create_user(**validated_data)


class EmailAuthTokenSerializer(serializers.Serializer):
    """
    Serializer for email-based authentication.
    Validates email and password and returns the authenticated user.
    """
    email = serializers.EmailField()
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """
        Authenticate the user using provided email and password.
        """
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                email=email,
                password=password
            )
            if not user:
                raise serializers.ValidationError("Invalid email or password.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        attrs['user'] = user
        return attrs
