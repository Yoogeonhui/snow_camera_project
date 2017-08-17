from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')
setup(
  options = {
    'py2exe' : {
        'compressed': 1,
        'optimize': 2,
        'bundle_files': 3, #Options 1 & 2 do not work on a 64bit system
        'dist_dir': 'dist',  # Put .exe in dist/
        'xref': False,
        'skip_archive': False,
        'ascii': False,
        "includes":["sip","cv2","numpy","PyQt5"],
        'dll_excludes': ["MSVCP90.dll", 'api-ms-win-core-heap-obsolete-l1-1-0.dll','api-ms-win-core-string-obsolete-l1-1-0.dll', 'api-ms-win-core-largeinteger-l1-1-0.dll', 'api-ms-win-core-stringansi-l1-1-0.dll', 'api-ms-win-core-privateprofile-l1-1-1.dll', 'api-ms-win-core-rtlsupport-l1-2-0.dll', "api-ms-win-core-libraryloader-l1-2-0.dll", 'api-ms-win-mm-time-l1-1-0.dll', 'api-ms-win-core-debug-l1-1-1.dll', 'api-ms-win-core-sidebyside-l1-1-0.dll', 'api-ms-win-core-kernel32-legacy-l1-1-1.dll', 'api-ms-win-core-timezone-l1-1-0.dll', 'api-ms-win-core-processenvironment-l1-2-0.dll', 'api-ms-win-core-util-l1-1-0.dll', 'api-ms-win-core-atoms-l1-1-0.dll', 'api-ms-win-core-winrt-error-l1-1-1.dll', 'api-ms-win-core-delayload-l1-1-1.dll', 'api-ms-win-core-shlwapi-obsolete-l1-2-0.dll', 'api-ms-win-core-localization-obsolete-l1-3-0.dll', "api-ms-win-core-string-l1-1-0.dll", "api-ms-win-core-libraryloader-l1-2-2.dll", "api-ms-win-core-registry-l1-1-0.dll", "api-ms-win-core-string-l2-1-0.dll", "api-ms-win-core-profile-l1-1-0.dll", "api-ms-win-core-processthreads-l1-1-2.dll", "api-ms-win-core-file-l1-2-1.dll", "api-ms-win-core-heap-l1-2-0.dll","api-ms-win-core-heap-l2-1-0.dll","api-ms-win-core-localization-l1-2-1.dll","api-ms-win-core-sysinfo-l1-2-1.dll","api-ms-win-core-synch-l1-2-0.dll","api-ms-win-core-errorhandling-l1-1-1.dll", "api-ms-win-core-registry-l2-2-0.dll", "api-ms-win-security-base-l1-2-0.dll","api-ms-win-core-handle-l1-1-0.dll","api-ms-win-core-io-l1-1-1.dll","api-ms-win-core-com-l1-1-1.dll","api-ms-win-core-memory-l1-1-2.dll","libzmq.pyd","geos_c.dll","api-ms-win-core-string-l1-1-0.dll","api-ms-win-core-string-l2-1-0.dll","api-ms-win*.dll","api-ms-win-core-libraryloader-l1-2-1.dll","api-ms-win-eventing-provider-l1-1-0.dll","api-ms-win-core-libraryloader-l1-2-2.dll","api-ms-win-core-version-l1-1-1.dll","api-ms-win-core-version-l1-1-0.dll", 'crypt32.dll']

        }
        },
  zipfile=None,
  console = ['main.py'],
)