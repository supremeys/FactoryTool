# QuecPython Production Test Tool Application Guide 

## Overview

The QuecPython production test tool (hereinafter referred to as the production test tool) is used for production testing of products developed based on QuecPython. This tool is available for Windows 7 and above operating systems.

The basic functions of the production testing tool are as follows:

1. Load test scripts and configuration files

    a. Users are required to write test scripts that can be run in the product in units of unit test functions.

    b. Users can bind test information for each test in the configuration file, including test item name, test function name, test method, etc.

2. Supports both automatic and manual testing methods

    a. The automatic test method does not require manual intervention. It automatically tests according to the order in the configuration file and automatically saves the test results. It directly encounters manual test items.

    b. In manual testing, when the current test ends, a window will pop up so that the tester can manually confirm the test results; the tool will save the manually confirmed results.

3. Supports display of test details and viewing of test reports

    a. The test results of each item will be displayed in different colours on the main interface.

    b. The complete test report will be saved in the root directory of the tool for overall viewing.

4. Supports 1 to 4 tests.

## Tool Download

[Click here to go to the download page](https://github.com/QuecPython/FactoryTool/releases)to obtain the production testing tool `FactoryTool.zip`。

![download-page.jpg](./media/download-page.jpg)

## Interface

- **Menu bar**：Includes edit tab and log tab

    - **Edit tab**：For editing test scripts and Excel log files

    - **Log tab**: Used to view test log files and tool run log files

    - **Setting tab**: Used for some advanced settings

- **Load area**：Includes loading test scripts and configuration files
    - **Load Test Script**：A collection of test functions
    - **Load Config File**：Bind test information to each test, including test item name, test function name, test method, etc

- **Factory Test**：Includes device connection ports, test item names, test methods, and test results. The tool has four test areas. Up to four devices can be tested simultaneously at one time, or a device can be tested individually.

> **Ensure that the interaction port of the tested module is not blocked, otherwise the test will fail.**

![1692598668142](./media/1701828343176.jpg)

## Setting Menu - Advanced Settings
![1692598668142](./media/1701828550273.jpg)

After modifying the items in the advanced setting, you need to click on the lower right conner **confirm** for the settings to apply.

1. Start testing automatically

    The test will start automatically when the interaction port is detected.

2. Automatic restart

    The module will automatically restart after testing.

3. IMEI matching

    The IMEI number will be matched with the IMEI number in **IMEI.txt** in the local tool directory. If it exists, the test will pass. Otherwise, the test will not pass.

4. Version detection

    The software version number (the software version number acquisition method can be configured by yourself, **uos.uname()** is used by default to obtain it) will be matched with the configured version number. If it matches, the test will pass. Otherwise, the test will not pass.

5. Test item configuration

    Before configuring this item, you need to select the JSON file. You can select all test items in the JSON file. Only the test items added to the right will be tested (the default is that all test items will be tested)

## Test Script

When writing test scripts, you need to be careful not to change the original template code structure. It is recommended to manually run the test in the module after writing to confirm whether the running results meet expectations. There are two locations that need to be changed in the test script template.

**Import module**：Import the python library used in testing

**Test function**：Write your own test function. The function name can be customized, but it needs to be a **static method** and cannot pass parameters. The function body content is customized according to the test requirements. The function needs to have a return value, which **must be a bool value.**

Test script example:

```python
# Write the modules that need to be imported here
import sim
import net
import uos
import utime

class TestBase(object):
    # ------This area is for testing code------
    @staticmethod
    def det_signal(args):
        utime.sleep(2)
        if sim.getStatus() == 1:
            if net.getConfig()[0] == 5:
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def det_file_space():
        utime.sleep(2)
        if uos.statvfs('usr')[3] > 5:
            return True
        else:
            return False
    # ------This area is for testing code------
```

## Configuration file
The configuration file is a JSON file, and three-dimensional list needs to be configured, which are: test item name, test function name, test mode (1 for manual testing, 0 for automatic testing)

Test script example：

```json
{
     // Test item name, Function of test item, Test method: 0/1/2
    "info": [["Memory test", "det_file_space()", 0],
             ["Signal test", "det_signal('test')", 0]],
    // Test mode 0: Fully automatic test
    // Test mode 1: Manual confirmation of start and manual confirmation of test items results – “tips” is the content of the pop-up window for confirmation at the start   
    // Test mode 2: Manual confirmation is required to start and automatic confirmation of test items results - Confirm the pop-up window prompts content at the start

    // Test item name: Prompt information corresponding to the test item
    "tips": {"Memory test": "Please press button 1"}
}
```

If tips are configured, the text box below the interface test item display will display the prompt information when testing this item.

## Test principle

The production testing tool uses python scripts to test the business functions of QuecPython products. The test scripts are executed through the command interaction port REPL of QuecPython. The test scripts can be adjusted according to the test requirements to complete the production test function.

1. Get module parameters and running status through QuecPython's API interface.
2. Obtain business running status by accessing objects in running business code.
3. Test business functions or hardware functions by calling the interface provided by the business code.
4. Transfer configuration files or write product parameters through the QuecPython API interface.

## Test steps

**Step 1**：Edit test scripts and configuration files

Edit the **module_test.py** test code and **sort_setting.json**，configuration file. The test code and configuration file examples are shown in the figure above.

**Step 2**：Open the tool and select the test script and configuration file

After opening the tool, click the **Select** button to select the test code and configuration file edited in the previous step. If a serial port is detected, each test name and test method will be displayed under the serial port.

![1692599729648](./media/1692599729648.jpg)

**Step 3**：Start testing

- Click the **Start All** button： Start testing all connected modules.

- Click the **Start** button： Start testing the corresponding module.

If manual detection is performed, a pop-up window will prompt whether it is successful. You can manually click **Yes/No** to confirm the result.
![1692599919725](./media/1692599919725.jpg)

**Step 4**：View test results

You can see the test results directly in the test result field:
1. Pass: Green background colour, test result file mark: Pass
2. Failed: Red background colour, test result field mark: Fail
3. Testing: Yellow background colour indicates that the test item is being tested, test result field mark: Testing

![1692599801694](./media/1692599801694.jpg)

**Step 5**：View the test log

Generate the **Test-Result.xlsx** file in the same directory as the tool, including test project content and test result logs.

## Test results

The test results of each module will be written to excel and exported. The excel file can be **opened** through the **Edit Excel file** menu in the menu bar.

Each test will generate a test record in excel (regardless of whether the test is successful or failed). Multiple tests will have multiple records, which are distinguished according to the COM port of the test device.

This file will be saved in the directory of the same level as the tool and will be automatically appended during the test process.

## Secondary development of production test tools

### How to pull from repository

If you have secondary development needs, you can directly pull the code repository.

```shell
git clone --recurse-submodules https://github.com/QuecPython/FactoryTool.git -b interventionable
```

### Configure environment

**Installing dependencies**

```shell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# If the above method fails to install, you can use a separate installation method.
pip install wxpython -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install pypubsub -i https://pypi.tuna.tsinghua.edu.cn/simple
```
**Run code**

```shell
python main.py
```
**Compile into executable program**

```shell
# If you use a separate installation method above, you need to install the pyinstaller library
pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple
# Compile it into an exe program, and the output exe directory is under ./dist/
pyinstaller -F -w --win-private-assemblies --icon images/quectel.ico -w ./main.py
```
