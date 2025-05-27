from setuptools import setup, find_packages  # noqa: H301

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools
NAME = "formlabs_local_api_minimal"
VERSION = "0.9.0"
PYTHON_REQUIRES = ">=3.7"
REQUIRES = [
    "requests >= 2.32.3",
    "psutil >= 5.9.5",
    "typing-extensions >= 4.7.1",
]

setup(
    name=NAME,
    version=VERSION,
    description="Formlabs Local API",
    author="Formlabs",
    author_email="support@formlabs.com",
    url="",
    keywords=["Formlabs Local API"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description_content_type='text/markdown',
    long_description="""\
    # Introduction The Formlabs Local API is designed for integrations that want to automate job preparation, getting local-network printer status, or sending jobs to Formlabs printers without launching the PreForm graphical user interface. A server application must be installed and run on a user&#39;s computer to use this API.  Example use cases: - Scripted job preparation that takes a folder of models, sets up a print,   and uploads it to a printer without user input. - Deep and custom integrations into 3D Modeling and Design software to   prepare print scenes beyond the scope of the PreForm Command Line Arguments.  This API uses RESTful principles. This means the API is organized around resources and collections of resources. Resources and collections are each available at their own URI. You can interact with these resources using standard HTTP Methods on the resource&#39;s URI.  Example endpoint: &#x60;&#x60;&#x60; GET http://localhost:44388/scene/ &#x60;&#x60;&#x60;  Responses from the API server will be in JSON and are documented throughout the reference docs. This API is described by an [OpenAPI Specification](https://spec.openapis.org/oas/v3.1.0). This interactive documentation is automatically generated from the specification file.  # Technical Overview  ## PreFormServer Background Application All Local API integrations involve starting the PreFormServer background application to expose its HTTP API, then making local HTTP API calls in your own code. This application is like [PreForm](https://formlabs.com/software/preform/), Formlabs&#39; regular job preparation application, but it does not open a graphical window, and interaction is done via HTTP API requests. The PreFormServer application is supported on Windows and MacOS with separate downloads for each Operating System.  ### Starting PreFormServer The PreFormServer application can started manually from your Operating System&#39;s command prompt or terminal, but most integrations will start the application programatically from integration code. By default the HTTP Server will listen on port 44388, but this can be changed by passing in a different port number as the command line argument &#x60;--port&#x60; to the PreFormServer application.  The HTTP API server started by the PreFormServer application cannot immediately respond to requests. When the server is ready to accept requests, it will output &#x60;READY FOR INPUT&#x60; in the standard output.  For example, running the PreFormServer application on Windows from the command prompt: &#x60;&#x60;&#x60; PreFormServer.exe &#x60;&#x60;&#x60; will output something like the following: &#x60;&#x60;&#x60; starting HTTP server Listening... HTTP server listening on port  44388 READY FOR INPUT &#x60;&#x60;&#x60;  ## Making API Requests The code to make HTTP API requests to a running PreFormServer can be written directly in your integration code or by using a generated library that does the API calls. The endpoints and format of the HTTP API are described on this page and in the openapi.yaml file.  Formlabs provides an example [Python library](https://github.com/Formlabs/formlabs-api-python) that handles the setup and request formatting.  ## Glossary - **Scene**: The current state of a job that can be printed on a particular printer model.   This includes both the “Scene Settings” and all of the currently loaded models and their support structures. - **Scene Settings**: Printer type and material information of scene. Describes the   build platform size, the printer capabilities, and what material and print settings   it is set up to be printed with.  ## Stateful Interactions The PreForm Server is stateful in that while it is running, it keeps a cache of the current scene and requests will use the cached scene and possibly modify it. For example, initially a scene may be empty and then if a load model request is made then the cached scene will have one model loaded. Calling the load model requests again will load another copy of the model resulting in two models in the cached scene.  ## Blocking Calls &amp; Asynchronous Requests Unless otherwise stated, API calls are blocking: the HTTP request will not return until the operation has completed.  Some requests like running the auto support action on a scene with many complicated models could take over 1 minute (depending on computer resources). The Server has a timeout of 10 minutes for all requests.  Requests made asynchronously will use the last cached state. For example, if a “get scene” request is made during a “auto support” request that has not finished, then the “get scene” request will return data that will not include the auto support changes.  ## File Paths When saving and loading files, the local API inputs expect full operating system paths to local files on disk.  Correct file path: - &#x60;C:\\Projects\\Models\\part.stl&#x60;  Incorrect file paths: - &#x60;.\\Models\\part.stl&#x60; - &#x60;%ENV_VAR%\\part.stl&#x60; - &#x60;part.stl&#x60; - &#x60;https://filestorage.com/part.stl&#x60;  # Errors Conventional HTTP response codes are used to indicate the success or failure of an API request. In general: Codes in the 2xx range indicate success. Codes in the 4xx range indicate an error that failed given the information provided. Codes in the 5xx range indicate an error with Formlabs&#39; servers.  # Security The HTTP Server that PreForm uses to communicate is only exposed to the local network of your computer and not to the public Internet, unless you have configured your computer to expose the port running the PreForm Server to the Internet.  Some requests require an Internet connection, require Dashboard login, and make web requests to perform their action (such as printing to a remote printer). 
    """,  # noqa: E501
    package_data={"formlabs_local_api_minimal": ["py.typed"]},
)
