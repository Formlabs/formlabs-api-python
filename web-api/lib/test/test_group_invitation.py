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

from formlabs_web_api.models.group_invitation import GroupInvitation

class TestGroupInvitation(unittest.TestCase):
    """GroupInvitation unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GroupInvitation:
        """Test GroupInvitation
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GroupInvitation`
        """
        model = GroupInvitation()
        if include_optional:
            return GroupInvitation(
                email = '',
                is_admin = True
            )
        else:
            return GroupInvitation(
                email = '',
        )
        """

    def testGroupInvitation(self):
        """Test GroupInvitation"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
