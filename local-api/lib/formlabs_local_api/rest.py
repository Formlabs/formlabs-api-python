# coding: utf-8

"""
    Formlabs Local API

    # Introduction The Formlabs Local API is designed for integrations that want to automate job preparation, getting local-network printer status, or sending jobs to Formlabs printers without launching the PreForm graphical user interface. A server application must be installed and run on a user's computer to use this API.  Example use cases: - Scripted job preparation that takes a folder of models, sets up a print,   and uploads it to a printer without user input. - Deep and custom integrations into 3D Modeling and Design software to   prepare print scenes beyond the scope of the PreForm Command Line Arguments.  This API uses RESTful principles. This means the API is organized around resources and collections of resources. Resources and collections are each available at their own URI. You can interact with these resources using standard HTTP Methods on the resource's URI.  Example endpoint: ``` GET http://localhost:44388/scene/ ```  Responses from the API server will be in JSON and are documented throughout the reference docs. This API is described by an [OpenAPI Specification](https://spec.openapis.org/oas/v3.1.0). This interactive documentation is automatically generated from the specification file.  # Technical Overview  ## PreFormServer Background Application All Local API integrations involve starting the PreFormServer background application to expose its HTTP API, then making local HTTP API calls in your own code. This application is like [PreForm](https://formlabs.com/software/preform/), Formlabs' regular job preparation application, but it does not open a graphical window, and interaction is done via HTTP API requests. The PreFormServer application is supported on Windows and MacOS with separate downloads for each Operating System.  ### Installing PreFormServer The PreFormServer application can be downloaded from the [Formlabs API downloads and release notes page](https://support.formlabs.com/s/article/Formlabs-API-downloads-and-release-notes). After downloading, unzip the file and move the application to the desired location on your computer. Any location can be used as the path to the application should be referenced from your integration code.  ### Starting PreFormServer The PreFormServer application can started manually from your Operating System's command prompt or terminal, but most integrations will start the application programmatically from integration code. The command line argument `--port` is required to specify the port number the HTTP Server will listen on.  The HTTP API server started by the PreFormServer application cannot immediately respond to requests. When the server is ready to accept requests, it will output `READY FOR INPUT` in the standard output.  For example, running the PreFormServer application on Windows from the command prompt: ``` PreFormServer.exe --port 44388 ``` will output something like the following: ``` starting HTTP server Listening... HTTP server listening on port 44388 READY FOR INPUT ```  ## Making API Requests The code to make HTTP API requests to a running PreFormServer can be written directly in your integration code or by using a generated library that does the API calls. The endpoints and format of the HTTP API are described on this page and in the openapi.yaml file.  Formlabs provides an example [Python library](https://github.com/Formlabs/formlabs-api-python) that handles the setup and request formatting.  ## Glossary - **Scene**: The current state of a job that can be printed on a particular printer model.   This includes both the “Scene Settings” and all of the currently loaded models and their support structures. - **Scene Settings**: Printer type and material information of scene. Describes the   build platform size, the printer capabilities, and what material and print settings   it is set up to be printed with.  ## Stateful Interactions The PreForm Server is stateful in that while it is running, it keeps a cache of scenes. By default, it caches 100 scenes in memory, with unlimited scenes stored on disk, though this may be changed with the `--scene-cache-size` parameter. Scenes are identified by their IDs, returned from the `/scene/` endpoint. `/scene/` endpoints also accept a scene ID of \"default\", which will use a single global scene. Endpoints with no scene id provided (e.g. `/scene/auto-layout/`) are deprecated. They will use the most recently created scene, and possibly modify it. All other `/scene/` requests will use the user specified scene, and possibly modify it. For example, initially a scene may be empty and then if a load model request is made then the cached scene will have one model loaded. Calling the load model endpoint again will load another copy of the model resulting in two models in the cached scene.  ## Blocking Calls & Asynchronous Requests Unless otherwise stated, API calls are blocking: the HTTP request will not return until the operation has completed.  Some requests like running the auto support action on a scene with many complicated models could take over 1 minute (depending on computer resources). The Server has a timeout of 10 minutes for all requests.  Some long-running operations can be called asynchronously by adding `?async=true` to the request. These requests will return immediately and the operation will be tracked separately. The caller can poll for completion using the `/operations/{operation_id}/` endpoint, and track the percentage progress of the outstanding operation.  Requests involving the scene will always use the scene state at the time the request was made, without any partially completed operations. For example, if a “get scene” request is made during a “auto support” request that has not finished, then the “get scene” request will return data that will not include the auto support changes.  Multiple requests editing the same scene should NOT be made in parallel. If an \"auto layout\" request is made during an \"auto support\" request that has not finished, whichever operation finishes last will \"win\": either an auto-layout of unsupported models or the original layout with supports. PreformServer currently gives no warning when this happens.  ## File Paths When saving and loading files, the local API inputs expect full operating system paths to local files on disk.  Correct file path: - `C:\\Projects\\Models\\part.stl`  Incorrect file paths: - `.\\Models\\part.stl` - `%ENV_VAR%\\part.stl` - `part.stl` - `https://filestorage.com/part.stl`  # Errors Conventional HTTP response codes are used to indicate the success or failure of an API request. In general: Codes in the 2xx range indicate success. Codes in the 4xx range indicate an error that failed given the information provided. Codes in the 5xx range indicate an error with Formlabs' servers.  # Security The HTTP Server that PreForm uses to communicate is only exposed to the local network of your computer and not to the public Internet, unless you have configured your computer to expose the port running the PreForm Server to the Internet.  Some requests require an Internet connection, require Dashboard login, and make web requests to perform their action (such as printing to a remote printer). 

    The version of the OpenAPI document: 0.9.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import io
import json
import re
import ssl

import urllib3

from formlabs_local_api.exceptions import ApiException, ApiValueError

SUPPORTED_SOCKS_PROXIES = {"socks5", "socks5h", "socks4", "socks4a"}
RESTResponseType = urllib3.HTTPResponse


def is_socks_proxy_url(url):
    if url is None:
        return False
    split_section = url.split("://")
    if len(split_section) < 2:
        return False
    else:
        return split_section[0].lower() in SUPPORTED_SOCKS_PROXIES


class RESTResponse(io.IOBase):

    def __init__(self, resp) -> None:
        self.response = resp
        self.status = resp.status
        self.reason = resp.reason
        self.data = None

    def read(self):
        if self.data is None:
            self.data = self.response.data
        return self.data

    def getheaders(self):
        """Returns a dictionary of the response headers."""
        return self.response.headers

    def getheader(self, name, default=None):
        """Returns a given response header."""
        return self.response.headers.get(name, default)


class RESTClientObject:

    def __init__(self, configuration) -> None:
        # urllib3.PoolManager will pass all kw parameters to connectionpool
        # https://github.com/shazow/urllib3/blob/f9409436f83aeb79fbaf090181cd81b784f1b8ce/urllib3/poolmanager.py#L75  # noqa: E501
        # https://github.com/shazow/urllib3/blob/f9409436f83aeb79fbaf090181cd81b784f1b8ce/urllib3/connectionpool.py#L680  # noqa: E501
        # Custom SSL certificates and client certificates: http://urllib3.readthedocs.io/en/latest/advanced-usage.html  # noqa: E501

        # cert_reqs
        if configuration.verify_ssl:
            cert_reqs = ssl.CERT_REQUIRED
        else:
            cert_reqs = ssl.CERT_NONE

        pool_args = {
            "cert_reqs": cert_reqs,
            "ca_certs": configuration.ssl_ca_cert,
            "cert_file": configuration.cert_file,
            "key_file": configuration.key_file,
            "ca_cert_data": configuration.ca_cert_data,
        }
        if configuration.assert_hostname is not None:
            pool_args['assert_hostname'] = (
                configuration.assert_hostname
            )

        if configuration.retries is not None:
            pool_args['retries'] = configuration.retries

        if configuration.tls_server_name:
            pool_args['server_hostname'] = configuration.tls_server_name


        if configuration.socket_options is not None:
            pool_args['socket_options'] = configuration.socket_options

        if configuration.connection_pool_maxsize is not None:
            pool_args['maxsize'] = configuration.connection_pool_maxsize

        # https pool manager
        self.pool_manager: urllib3.PoolManager

        if configuration.proxy:
            if is_socks_proxy_url(configuration.proxy):
                from urllib3.contrib.socks import SOCKSProxyManager
                pool_args["proxy_url"] = configuration.proxy
                pool_args["headers"] = configuration.proxy_headers
                self.pool_manager = SOCKSProxyManager(**pool_args)
            else:
                pool_args["proxy_url"] = configuration.proxy
                pool_args["proxy_headers"] = configuration.proxy_headers
                self.pool_manager = urllib3.ProxyManager(**pool_args)
        else:
            self.pool_manager = urllib3.PoolManager(**pool_args)

    def request(
        self,
        method,
        url,
        headers=None,
        body=None,
        post_params=None,
        _request_timeout=None
    ):
        """Perform requests.

        :param method: http request method
        :param url: http request url
        :param headers: http request headers
        :param body: request json body, for `application/json`
        :param post_params: request post parameters,
                            `application/x-www-form-urlencoded`
                            and `multipart/form-data`
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        """
        method = method.upper()
        assert method in [
            'GET',
            'HEAD',
            'DELETE',
            'POST',
            'PUT',
            'PATCH',
            'OPTIONS'
        ]

        if post_params and body:
            raise ApiValueError(
                "body parameter cannot be used with post_params parameter."
            )

        post_params = post_params or {}
        headers = headers or {}

        timeout = None
        if _request_timeout:
            if isinstance(_request_timeout, (int, float)):
                timeout = urllib3.Timeout(total=_request_timeout)
            elif (
                    isinstance(_request_timeout, tuple)
                    and len(_request_timeout) == 2
                ):
                timeout = urllib3.Timeout(
                    connect=_request_timeout[0],
                    read=_request_timeout[1]
                )

        try:
            # For `POST`, `PUT`, `PATCH`, `OPTIONS`, `DELETE`
            if method in ['POST', 'PUT', 'PATCH', 'OPTIONS', 'DELETE']:

                # no content type provided or payload is json
                content_type = headers.get('Content-Type')
                if (
                    not content_type
                    or re.search('json', content_type, re.IGNORECASE)
                ):
                    request_body = None
                    if body is not None:
                        request_body = json.dumps(body)
                    r = self.pool_manager.request(
                        method,
                        url,
                        body=request_body,
                        timeout=timeout,
                        headers=headers,
                        preload_content=False
                    )
                elif content_type == 'application/x-www-form-urlencoded':
                    r = self.pool_manager.request(
                        method,
                        url,
                        fields=post_params,
                        encode_multipart=False,
                        timeout=timeout,
                        headers=headers,
                        preload_content=False
                    )
                elif content_type == 'multipart/form-data':
                    # must del headers['Content-Type'], or the correct
                    # Content-Type which generated by urllib3 will be
                    # overwritten.
                    del headers['Content-Type']
                    # Ensures that dict objects are serialized
                    post_params = [(a, json.dumps(b)) if isinstance(b, dict) else (a,b) for a, b in post_params]
                    r = self.pool_manager.request(
                        method,
                        url,
                        fields=post_params,
                        encode_multipart=True,
                        timeout=timeout,
                        headers=headers,
                        preload_content=False
                    )
                # Pass a `string` parameter directly in the body to support
                # other content types than JSON when `body` argument is
                # provided in serialized form.
                elif isinstance(body, str) or isinstance(body, bytes):
                    r = self.pool_manager.request(
                        method,
                        url,
                        body=body,
                        timeout=timeout,
                        headers=headers,
                        preload_content=False
                    )
                elif headers['Content-Type'].startswith('text/') and isinstance(body, bool):
                    request_body = "true" if body else "false"
                    r = self.pool_manager.request(
                        method,
                        url,
                        body=request_body,
                        preload_content=False,
                        timeout=timeout,
                        headers=headers)
                else:
                    # Cannot generate the request from given parameters
                    msg = """Cannot prepare a request message for provided
                             arguments. Please check that your arguments match
                             declared content type."""
                    raise ApiException(status=0, reason=msg)
            # For `GET`, `HEAD`
            else:
                r = self.pool_manager.request(
                    method,
                    url,
                    fields={},
                    timeout=timeout,
                    headers=headers,
                    preload_content=False
                )
        except urllib3.exceptions.SSLError as e:
            msg = "\n".join([type(e).__name__, str(e)])
            raise ApiException(status=0, reason=msg)

        return RESTResponse(r)
