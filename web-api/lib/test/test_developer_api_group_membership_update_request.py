# coding: utf-8

"""
    Formlabs Developer API

    The Formlabs Dashboard Developer API provides resources to integrate Formlabs products into customer’s workflow and existing systems

    The version of the OpenAPI document: 0.1.0
    Contact: api-inquiry@formlabs.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from formlabs_web_api.models.developer_api_group_membership_update_request import DeveloperAPIGroupMembershipUpdateRequest

class TestDeveloperAPIGroupMembershipUpdateRequest(unittest.TestCase):
    """DeveloperAPIGroupMembershipUpdateRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DeveloperAPIGroupMembershipUpdateRequest:
        """Test DeveloperAPIGroupMembershipUpdateRequest
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DeveloperAPIGroupMembershipUpdateRequest`
        """
        model = DeveloperAPIGroupMembershipUpdateRequest()
        if include_optional:
            return DeveloperAPIGroupMembershipUpdateRequest(
                user = '0',
                is_admin = True
            )
        else:
            return DeveloperAPIGroupMembershipUpdateRequest(
                user = '0',
        )
        """

    def testDeveloperAPIGroupMembershipUpdateRequest(self):
        """Test DeveloperAPIGroupMembershipUpdateRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
