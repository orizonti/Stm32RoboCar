import os
import os.path
import fnmatch
import logging
import ycm_core
import re
PATH_BROMS = "C:/Users/broms"
NAME_YANDEX_DISK = "/YandexDisk-orizonti"
#PATH_BROMS = "C:/Users/Broms"
#NAME_YANDEX_DISK = "/YandexDisk"

ESP32_PACKAGE_PLATFORMIO = [
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/stack/smp/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/stack/sdp/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/stack/rfcomm/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/stack/l2cap/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/stack/gatt/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/stack/gap/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/stack/btm/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/stack/avrc/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/stack/avdt/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/stack/avct/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/stack/a2dp/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/stack/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/osi/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/hci/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/external/sbc/encoder/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/external/sbc/decoder/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/device/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/common/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/btc/profile/std/smp/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/btc/profile/std/hid/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/btc/profile/std/dis/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/btc/profile/std/battery/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/btc/profile/std/a2dp/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/btc/profile/std/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/btc/profile/esp/blufi/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/btc/profile/esp/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/btc/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/bta/sys/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/bta/sdp/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/bta/jv/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/bta/hh/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/bta/hf_client/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/bta/gatt/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/bta/dm/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/bta/av/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/bta/ar/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/bta/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/api/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/app_trace/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/app_update/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/aws_iot/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/aws_iot/aws-iot-device-sdk-embedded-C/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bootloader_support/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/bt/bluedroid/api/include/api",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/coap/port/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/coap/port/include/coap",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/coap/libcoap/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/coap/libcoap/include/coap",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/console",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/driver/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/esp-tls",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/esp_adc_cal/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/esp_http_client/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/esp_https_ota/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/esp32/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/ethernet/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/expat/port/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/expat/include/expat",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/fatfs/src",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/heap/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/jsmn/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/json/cJSON",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/libsodium/libsodium/src/libsodium/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/libsodium/port_include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/log/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/lwip/include/lwip",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/lwip/include/lwip/port",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/lwip/include/lwip/posix",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/lwip/apps/ping",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/mbedtls/port/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/mbedtls/mbedtls/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/mdns/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/micro-ecc/micro-ecc",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/nghttp/nghttp2/lib/includes",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/nghttp/port/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/newlib/platform_include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/newlib/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/nvs_flash/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/openssl/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/pthread/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/sdmmc/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/smartconfig_ack/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/soc/esp32/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/soc/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/spi_flash/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/spiffs/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/tcpip_adapter/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/ulp/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/vfs/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/wear_levelling/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/wpa_supplicant/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/wpa_supplicant/port/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/xtensa-debug-module/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/tool-unity",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/newlib/include/sys",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/newlib/include/machine",
                            "-I"+ PATH_BROMS + "/.platformio/packages/toolchain-gccarmnoneeabi/lib/gcc/arm-none-eabi/7.2.1/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/toolchain-xtensa32/xtensa-esp32-elf/sysroot/usr/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/toolchain-xtensa32/xtensa-esp32-elf/sysroot/usr/include/machine",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/lwip/lwip/src/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/freertos/include/",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/lwip/port/esp32/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/esp_event/include",
                            "-I"+ PATH_BROMS + "/.platformio/packages/framework-espidf/components/lwip/apps/",
                            ]

ESP32_ROBOCAR = [
                 "-I" + PATH_BROMS + NAME_YANDEX_DISK + "/PROJECTS/RoboCar/ESP32Project/ESP32_RoboCar/include",
                ]


PLATFORMIO_PACKAGE_STM32 = [
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/CMSIS/Include',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/CMSIS/Device/ST/STM32F4xx/Include',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/STM32F4xx_HAL_Driver/Inc',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/Common',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/ampire480272',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/ampire640480',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/cs43l22',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/exc7200',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/ft6x06',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/ili9325',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/ili9341',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/l3gd20',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/lis302dl',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/lis3dsh',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/ls016b8uy',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/lsm303dlhc',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/mfxstm32l152',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/n25q128a',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/n25q256a',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/n25q512a',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/otm8009a',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/ov2640',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/s25fl512s',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/s5k5cag',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/st7735',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/st7789h2',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/stmpe1600',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/stmpe811',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/ts3510',
                    '-I' + PATH_BROMS + '/.platformio/packages/framework-stm32cube/f4/Drivers/BSP/Components/wm8994',
                    '-I' + PATH_BROMS + '/.platformio/packages/tool-unity',
                    ]
STM32_ROBOCAR = ['-I' + PATH_BROMS + NAME_YANDEX_DISK + '/PROJECTS/RoboCar/STM32Project/STM32F407_RoboCar/Inc',
                 '-I' + PATH_BROMS + NAME_YANDEX_DISK + '/PROJECTS/RoboCar/STM32Project/STM32F407_RoboCar/Drivers/STM32F4xx_HAL_Driver/Inc'
                 '-I' + PATH_BROMS + NAME_YANDEX_DISK + '/PROJECTS/RoboCar/STM32Project/STM32F407_RoboCar/Drivers/CMSIS/Device/ST/STM32F4xx/Include',
                 '-I' + PATH_BROMS + NAME_YANDEX_DISK + '/PROJECTS/RoboCar/STM32Project/STM32F407_RoboCar/Middlewares/Third_Party/FreeRTOS/Source/include''-I' + PATH_BROMS + NAME_YANDEX_DISK + '/PROJECTS/RoboCar/STM32Project/STM32F407_RoboCar/Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS/',
'-I' + PATH_BROMS + NAME_YANDEX_DISK + '/PROJECTS/RoboCar/STM32Project/STM32F407_RoboCar/Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM4F',
'-I' + PATH_BROMS + NAME_YANDEX_DISK + '/PROJECTS/RoboCar/STM32Project/STM32F407_RoboCar/Middlewares/Third_Party/FreeRTOS/Source/include',
'-I' + PATH_BROMS + NAME_YANDEX_DISK + '/PROJECTS/RoboCar/STM32Project/STM32F407_RoboCar/include',
'-I' + PATH_BROMS + NAME_YANDEX_DISK + '/PROJECTS/RoboCar/STM32Project/STM32F407_RoboCar/src',
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
            '-I' + PATH_BROMS + NAME_YANDEX_DISK + '/PROJECTS/RoboCar/ESP32Project/ESP32_RoboCar/include/',
            '-I' + PATH_BROMS + '/.platformio/packages/framework-espidf/components/lwip/port/esp32/include',
            '-I' + PATH_BROMS + '/.platformio/packages/framework-espidf/components/esp_event/include',
            '-I' + PATH_BROMS + '/.platformio/packages/framework-espidf/components/lwip/apps/',
           ]

TEST_INCLUDE = [
        "-ID:/Lib/include",
        "-IC:/Users/broms/YandexDisk/PROJECTS/RoboCar/STM32Project/STM32F407_RoboCar/Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS/"
        "-IC:/Users/broms/YandexDisk-orizonti/PROJECTS/RoboCar/STM32Project/STM32F407_RoboCar/Inc"

        #"-IC:/Users/Broms/.platformio/packages/framework-espidf/components/lwip/include/",
        #"-IC:/Users/Broms/.platformio/packages/framework-espidf/components/lwip/include/lwip",
        #"-IC:/Users/Broms/.platformio/packages/framework-espidf/components/lwip/include/lwip/port",
        #"-IC:/Users/Broms/.platformio/packages/framework-espidf/components/lwip/include/lwip/posix",
        #"-IC:/Users/Broms/.platformio/packages/framework-espidf/components/lwip/apps/ping",
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
