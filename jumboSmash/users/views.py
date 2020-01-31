from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User, Profile
from users.serializers import UserSerializer, ProfileSerializer
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

class ListUsers(APIView):
    """
    View to get list of all users
    """
    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

class GetProfile(APIView):
    """
    Get a profile and photos for user
    """
    def get(self, request):
        curr_user_id = str(request.user.id)
        user_id = request.query_params.get("id")
        same_user = curr_user_id == user_id

        profile = None
        # get all active profiles where there approval is not null
        profiles = Profile.objects.filter(user=user_id).exclude(approved=None)
        if len(profiles) == 0:
            # no active profiles found
            pass
        elif len(profiles) == 1:
            # one active profile found
            temp = profiles[0]
            if not temp.approved:
                if same_user:
                    # if profile is not approved, only let the profile's user see it
                    profile = temp
            else:
                #if profile is approved, show everyone
                profile = temp
        elif len(profiles) == 2:
            # two active profiles found, figure out which is approved, which is not approved
            approved_profile = profiles[0] if profiles[0].approved else profiles[1]
            unapproved_profile = profiles[0] if not profiles[0].approved else profiles[1]

            if same_user:
                # if the request is from the profile's user, show unapproved profile
                profile = unapproved_profile
            else:
                # otherwise, show the approved profile
                profile = approved_profile
        else:
            # more than two active profiles
            print("Multiple active profiles found for user: %s" % user_id)
            Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if not profile:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

class EditProfile(APIView):
    """
    Edit profile for currently logged in user
    """
    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            curr_user_id = str(request.user.id)
            user_id = str(serializer.validated_data["user"].id)
            if curr_user_id != user_id:
                print("User %s tried editing profile of user %s." % (curr_user_id, user_id))
                return Response(status=status.HTTP_403_FORBIDDEN)

            profile = Profile.objects.edit(curr_user_id, serializer.validated_data)
            return Response(ProfileSerializer(profile).data)
        else:
            print("Bad profile edit request with following errors:")
            print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)

