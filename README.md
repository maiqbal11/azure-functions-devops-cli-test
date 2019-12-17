## Integration Test for Azure Functions

### Test Python Functions Locally
1. Set the **FunctionAppUrl** environment variable by `$env:FunctionAppUrl = "localhost:7071"`
2. Create and activate a virtual environment
3. To start the test_apps and run the test using run_tests script
    1. Run the test script `.\run_tests\run_local.ps1 -AppPath v2\python\36`
4. Alternatively, to get more error details and test manually
    1. resolve python dependencies by `pip install .\test_apps\v2\python\36\requirements.txt`
    2. start the function host by `cd .\test_apps\v2\python\36; func host start`
    3. run a test collection by `python -m pytest .\tests\v2\python\36`
    4. or run a specific test by `python -m pytest .\tests\v2\python\36\test_v2_python_36_http.py::TestV2Python36Http::test_keyword_async_trigger`
