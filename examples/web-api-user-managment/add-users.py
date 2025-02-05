"""
Script to invite a list of users to a list of Dashboard groups.
The script assumes that the authenticated user is admin in the dashboard groups,
otherwise permission errors will be returned from the backend.

Get your Client ID and Secret at https://dashboard.formlabs.com/#developer
"""

import os
from typing import List

from formlabs_web_api import PrinterGroupsApi, ApiClient, AuthenticationApi
from formlabs_web_api.rest import ApiException
from formlabs_web_api.exceptions import BadRequestException, ForbiddenException

from formlabs_web_api.models.request_an_access_token200_response import RequestAnAccessToken200Response
from formlabs_web_api.models.workgroup import Workgroup
from formlabs_web_api.models.workgroup_membership import WorkgroupMembership
from formlabs_web_api.models.developer_api_group_membership_create_request import DeveloperAPIGroupMembershipCreateRequest

api_client: ApiClient = ApiClient()
group_api: PrinterGroupsApi = PrinterGroupsApi(api_client=api_client)


def authenticate_client(api_client: ApiClient, grant_type: str, client_id: str, client_secret: str) -> None:
    """ Obtain an OAuth2 Access Token and set it on the client """
    authentication_api: AuthenticationApi = AuthenticationApi(api_client)
    api_response: RequestAnAccessToken200Response = authentication_api.request_an_access_token(grant_type, client_id, client_secret)
    access_token: str = api_response.access_token
    api_client.set_default_header("Authorization", f"Bearer {access_token}")


def send_invitation(group: Workgroup, email: str, is_admin: bool = False):
    """ Sends an invitation to a Workgroup for user with email """
    group_create_request = DeveloperAPIGroupMembershipCreateRequest.from_dict({
        'user': email,
        'is_admin': is_admin
    })
    try:
        group_api.groups_members_create(group.id, developer_api_group_membership_create_request=group_create_request)
        print(f"successfully added user with '{email}' to '{group.name}' group")
    except BadRequestException as e:
        print(f"bad request when adding user with '{email}' to '{group.name}' group: {e.body}")
    except ForbiddenException as e:
        print(f"permission denied when adding '{email}' to '{group.name}' group: {e.body}")

if __name__ == '__main__':
    # Client secrets from Environment
    CLIENT_ID = os.getenv("CLIENT_ID", "")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")

    groups_to_add: List[str] = ["My group", "My other group"]
    user_emails: List[str] = ["some_user@my_company.com", "some_other_user@my_company.com"]

    try:
        authenticate_client(api_client, "client_credentials", CLIENT_ID, CLIENT_SECRET)
    except ApiException as e:
        print("exception when obtaining access token: %s\n" % e)
        print("invalid credential, exiting...")
        exit(1)

    groups: List[Workgroup] = group_api.groups_list()
    filtered_group: List[Workgroup] = [group for group in groups if group.name in groups_to_add]

    if len(filtered_group) == 0:
        print("no groups found, make sure the group names are correct!")
        exit(0)

    for group in filtered_group:
        for email in user_emails:
            send_invitation(group, email)

    print("Done.")
