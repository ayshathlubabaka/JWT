from .models import UserProfile

def create_or_update_user_profile(user, profile_data):
    """
    Create or update a user's profile.

    Args:
        user (User): The user for whom the profile should be created or updated.
        profile_data (dict): A dictionary containing profile data to create or update.

    Returns:
        UserProfile: The created or updated UserProfile instance.
    """
    # Get the user's existing profile if it exists, or create a new one
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    # Update the profile fields with the provided data
    for field, value in profile_data.items():
        setattr(user_profile, field, value)

    # Save the profile
    user_profile.save()

    return user_profile
