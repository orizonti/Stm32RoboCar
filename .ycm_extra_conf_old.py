import os
import os.path
import fnmatch
import logging
import ycm_core
import re
PATH_BROMS = "/Users/broms/"

ESP32_PACKAGE_PLATFORMIO = [
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/stack/smp/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/stack/sdp/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/stack/rfcomm/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/stack/l2cap/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/stack/gatt/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/stack/gap/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/stack/btm/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/stack/avrc/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/stack/avdt/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/stack/avct/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/stack/a2dp/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/stack/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/osi/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/hci/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/external/sbc/encoder/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/external/sbc/decoder/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/device/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/common/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/btc/profile/std/smp/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/btc/profile/std/hid/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/btc/profile/std/dis/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/btc/profile/std/battery/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/btc/profile/std/a2dp/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/btc/profile/std/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/btc/profile/esp/blufi/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/btc/profile/esp/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/btc/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/bta/sys/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/bta/sdp/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/bta/jv/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/bta/hh/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/bta/hf_client/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/bta/gatt/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/bta/dm/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/bta/av/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/bta/ar/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/bta/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/api/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/app_trace/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/app_update/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/aws_iot/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/aws_iot/aws-iot-device-sdk-embedded-C/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bootloader_support/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/bt/bluedroid/api/include/api",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/coap/port/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/coap/port/include/coap",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/coap/libcoap/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/coap/libcoap/include/coap",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/console",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/driver/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/esp-tls",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/esp_adc_cal/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/esp_http_client/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/esp_https_ota/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/esp32/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/ethernet/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/expat/port/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/expat/include/expat",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/fatfs/src",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/heap/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/jsmn/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/json/cJSON",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/libsodium/libsodium/src/libsodium/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/libsodium/port_include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/log/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/lwip/include/lwip",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/lwip/include/lwip/port",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/lwip/include/lwip/posix",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/lwip/apps/ping",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/mbedtls/port/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/mbedtls/mbedtls/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/mdns/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/micro-ecc/micro-ecc",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/nghttp/nghttp2/lib/includes",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/nghttp/port/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/newlib/platform_include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/newlib/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/nvs_flash/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/openssl/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/pthread/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/sdmmc/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/smartconfig_ack/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/soc/esp32/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/soc/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/spi_flash/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/spiffs/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/tcpip_adapter/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/ulp/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/vfs/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/wear_levelling/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/wpa_supplicant/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/wpa_supplicant/port/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/xtensa-debug-module/include",
                            "-IC:/Users/broms/.platformio/packages/tool-unity",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/newlib/include/sys",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/newlib/include/machine",
                            "-IC:/Users/broms/.platformio/packages/toolchain-gccarmnoneeabi/lib/gcc/arm-none-eabi/7.2.1/include",
                            "-IC:/Users/broms/.platformio/packages/toolchain-xtensa32/xtensa-esp32-elf/sysroot/usr/include",
                            "-IC:/Users/broms/.platformio/packages/toolchain-xtensa32/xtensa-esp32-elf/sysroot/usr/include/machine",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/lwip/lwip/src/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/freertos/include/",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/lwip/port/esp32/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/esp_event/include",
                            "-IC:/Users/broms/.platformio/packages/framework-espidf/components/lwip/apps/",
                            ]

ESP32_ROBOCAR = [
                 "-IC:/Users/broms/YandexDisk-orizonti/PROJECTS/RoboCar/ESP32Project/ESP32_RoboCar/include",
                ]


PLATFORMIO_PACKAGE_STM32 = [
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/CMSIS/Include',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/CMSIS/Device/ST/STM32F4xx/Include',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/STM32F4xx_HAL_Driver/Inc',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/Common',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/ampire480272',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/ampire640480',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/cs43l22',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/exc7200',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/ft6x06',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/ili9325',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/ili9341',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/l3gd20',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/lis302dl',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/lis3dsh',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/ls016b8uy',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/lsm303dlhc',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/mfxstm32l152',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/n25q128a',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/n25q256a',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/n25q512a',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/otm8009a',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/ov2640',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/s25fl512s',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/s5k5cag',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/st7735',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/st7789h2',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/stmpe1600',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/stmpe811',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/ts3510',
                    '-IC:/Users/broms/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/wm8994',
                    '-IC:/Users/broms/.platformio/packages/tool-unity',
                    ]
STM32_ROBOCAR = ['-IC:/Users/broms/YandexDisk-orizonti/PROJECTS/RoboCar/STM32Project/STM32F407_RoboCar/Inc',
    '-IC:/Users/broms/YandexDisk-orizonti/PROJECTS/RoboCar/STM32Project/STM32F407_RoboCar/Drivers/STM32F4xx_HAL_Driver/Inc'
    '-IC:/Users/broms/YandexDisk-orizonti/PROJECTS/RoboCar/STM32Project/STM32F407_RoboCar/Drivers/CMSIS/Device/ST/STM32F4xx/Include',
    '-IC:/Users/broms/YandexDisk-orizonti/PROJECTS/RoboCar/STM32Project/STM32F407_RoboCar/Middlewares/Third_Party/FreeRTOS/Source/include'
    '-IC:/Users/broms/YandexDisk-orizonti/PROJECTS/RoboCar/STM32Project/STM32F407_RoboCar/Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS/',
    '-IC:/Users/broms/YandexDisk-orizonti/PROJECTS/RoboCar/STM32Project/STM32F407_RoboCar/Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM4F',
    '-IC:/Users/broms/YandexDisk-orizonti/PROJECTS/RoboCar/STM32Project/STM32F407_RoboCar/Middlewares/Third_Party/FreeRTOS/Source/include',
    '-IC:/Users/broms/YandexDisk-orizonti/PROJECTS/RoboCar/STM32Project/STM32F407_RoboCar/include',
    '-IC:/Users/broms/YandexDisk-orizonti/PROJECTS/RoboCar/STM32Project/STM32F407_RoboCar/src',
                ]
QT_DIRS = ['-IC:/Qt/Qt5.6.3/5.6.3/msvc2015_64/include/QtCore',
        '-IC:/Qt/Qt5.6.3/5.6.3/msvc2015_64/include/QtWidgets',
        '-IC:/Qt/Qt5.6.3/5.6.3/msvc2015_64/include/QtGui',
        '-IC:/Qt/Qt5.6.3/5.6.3/msvc2015_64/include/QtSerialPort',
        '-IC:/Qt/Qt5.6.3/5.6.3/msvc2015_64/include/QtPrintSupport',
        '-IC:/Qt/Qt5.6.3/5.6.3/msvc2015_64/include',
        ]

STM32HAL_RELATIVE = ['-I../Inc',
                     '-I./Inc',
                     '-I/Inc',
                     '-I../Drivers/STM32F4xx_HAL_Driver/Inc',
                     '-I./Drivers/STM32F4xx_HAL_Driver/Inc',
                     '-I/Drivers/STM32F4xx_HAL_Driver/Inc',
                    ]

RELATIVE = [
            '-I./include',
            '-I./',
           ]

TEST_INCLUDE = [
        "-IC:/Users/broms/YandexDisk-orizonti/PROJECTS/RoboCar/STM32Project/STM32F407_RoboCar/Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS/",
        "-IC:/Users/broms/YandexDisk-orizonti/PROJECTS/RoboCar/STM32Project/STM32F407_RoboCar/Inc",
        "-IC:/Users/broms/YandexDisk-orizonti/PROJECTS/RoboCar/ESP32Project/ESP32_RoboCar/include/",
        "-IC:/Users/broms/YandexDisk-orizonti/PROJECTS/RoboCar/STM32Project/STM32F407_RoboCar/Inc",

        #"-IC:/Users/broms/.platformio/packages/framework-espidf/components/lwip/include/",
        #"-IC:/Users/broms/.platformio/packages/framework-espidf/components/lwip/include/lwip",
        #"-IC:/Users/broms/.platformio/packages/framework-espidf/components/lwip/include/lwip/port",
        #"-IC:/Users/broms/.platformio/packages/framework-espidf/components/lwip/include/lwip/posix",
        #"-IC:/Users/broms/.platformio/packages/framework-espidf/components/lwip/apps/ping",
        #'-IC:/Program Files (x86)/Windows Kits/10/Include/10.0.10240.0/ucrt',
        #'-IC:/Program Files (x86)/Windows Kits/10/Include/10.0.10240.0/ucrt/sys',
]

BASE_FLAGS = [
        '-w',
        '-Wno-inconsistent-missing-override',
        '-Woverloaded-virtual',
        '-Wno-int-to-pointer-cast',
        '-Wno-int-to-pointer-cast',
        '-Wnoendif-labels',
        '-Wimplicit-int',
        '-xc++',
        '-Wextra',
        '-Werror',
        '-Wno-long-long',
        '-Wno-variadic-macros',
        '-fexceptions',
        '-ferror-limit=10000',
        '-DNDEBUG',
        '-std=c++14',
        '-Wall',
        ]

BASE_FLAGS.extend(TEST_INCLUDE)
#BASE_FLAGS.extend(ESP32_ROBOCAR)
#BASE_FLAGS.extend(ESP32_PACKAGE_PLATFORMIO)
BASE_FLAGS.extend(STM32_ROBOCAR)
BASE_FLAGS.extend(PLATFORMIO_PACKAGE_STM32)
BASE_FLAGS.extend(STM32HAL_RELATIVE)
BASE_FLAGS.extend(RELATIVE)
#BASE_FLAGS.extend(QT_DIRS)
SOURCE_EXTENSIONS = [
        '.cpp',
        '.cxx',
        '.cc',
        '.c',
        '.m',
        '.mm'
        ]

SOURCE_DIRECTORIES = [
        '../src',
        './src',
        '/src',
        'src',
        'lib'
        ]

HEADER_EXTENSIONS = [
        '.h',
        '.hxx',
        '.hpp',
        '.hh'
        ]

HEADER_DIRECTORIES = [
        'include',
        'Inc',
        'inc',
        '/',
        ]

def IsHeaderFile(filename):
    extension = os.path.splitext(filename)[1]
    return extension in HEADER_EXTENSIONS

def GetCompilationInfoForFile(database, filename):
    if IsHeaderFile(filename):
        basename = os.path.splitext(filename)[0]
        for extension in SOURCE_EXTENSIONS:
            # Get info from the source files by replacing the extension.
            replacement_file = basename + extension
            if os.path.exists(replacement_file):
                compilation_info = database.GetCompilationInfoForFile(replacement_file)
                if compilation_info.compiler_flags_:
                    return compilation_info
            # If that wasn't successful, try replacing possible header directory with possible source directories.
            for header_dir in HEADER_DIRECTORIES:
                for source_dir in SOURCE_DIRECTORIES:
                    src_file = replacement_file.replace(header_dir, source_dir)
                    if os.path.exists(src_file):
                        compilation_info = database.GetCompilationInfoForFile(src_file)
                        if compilation_info.compiler_flags_:
                            return compilation_info
        return None
    return database.GetCompilationInfoForFile(filename)

def FindNearest(path, target, build_folder):
    candidate = os.path.join(path, target)
    if(os.path.isfile(candidate) or os.path.isdir(candidate)):
        logging.info("Found nearest " + target + " at " + candidate)
        return candidate;

    parent = os.path.dirname(os.path.abspath(path));
    if(parent == path):
        raise RuntimeError("Could not find " + target);

    if(build_folder):
        candidate = os.path.join(parent, build_folder, target)
        if(os.path.isfile(candidate) or os.path.isdir(candidate)):
            logging.info("Found nearest " + target + " in build folder at " + candidate)
            return candidate;

    return FindNearest(parent, target, build_folder)

def MakeRelativePathsInFlagsAbsolute(flags, working_directory):
    if not working_directory:
        return list(flags)
    new_flags = []
    make_next_absolute = False
    path_flags = [ '-isystem', '-I', '-iquote', '--sysroot=' ]
    for flag in flags:
        new_flag = flag

        if make_next_absolute:
            make_next_absolute = False
            if not flag.startswith('/'):
                new_flag = os.path.join(working_directory, flag)

        for path_flag in path_flags:
            if flag == path_flag:
                make_next_absolute = True
                break

            if flag.startswith(path_flag):
                path = flag[ len(path_flag): ]
                new_flag = path_flag + os.path.join(working_directory, path)
                break

        if new_flag:
            new_flags.append(new_flag)
    return new_flags


def FlagsForClangComplete(root):
    try:
        clang_complete_path = FindNearest(root, '.clang_complete')
        clang_complete_flags = open(clang_complete_path, 'r').read().splitlines()
        return clang_complete_flags
    except:
        return None

def FlagsForInclude(root):
    try:
        include_path = FindNearest(root, 'include')
        flags = []
        for dirroot, dirnames, filenames in os.walk(include_path):
            for dir_path in dirnames:
                real_path = os.path.join(dirroot, dir_path)
                flags = flags + ["-I" + real_path]
        return flags
    except:
        return None

def FlagsForCompilationDatabase(root, filename):
    try:
        # Last argument of next function is the name of the build folder for
        # out of source projects
        compilation_db_path = FindNearest(root, 'compile_commands.json', 'build')
        compilation_db_dir = os.path.dirname(compilation_db_path)
        logging.info("Set compilation database directory to " + compilation_db_dir)
        compilation_db =  ycm_core.CompilationDatabase(compilation_db_dir)
        if not compilation_db:
            logging.info("Compilation database file found but unable to load")
            return None
        compilation_info = GetCompilationInfoForFile(compilation_db, filename)
        if not compilation_info:
            logging.info("No compilation info for " + filename + " in compilation database")
            return None
        return MakeRelativePathsInFlagsAbsolute(
                compilation_info.compiler_flags_,
                compilation_info.compiler_working_dir_)
    except:
        return None

def FlagsForFile(filename):
    root = os.path.realpath(filename);
    compilation_db_flags = FlagsForCompilationDatabase(root, filename)
    if compilation_db_flags:
        final_flags = compilation_db_flags
    else:
        final_flags = BASE_FLAGS
        clang_flags = FlagsForClangComplete(root)
        if clang_flags:
            final_flags = final_flags + clang_flags
        include_flags = FlagsForInclude(root)
        if include_flags:
            final_flags = final_flags + include_flags
    return {
            'flags': final_flags,
            'do_cache': True
            }
