import os
import base64
import json
import hashlib
import platform
from ctypes import cdll


if platform.uname()[0] == "Windows":
    _lib_filename = "cls_ffi.dll"
elif platform.uname()[0] == "Linux" and platform.uname()[4] == "aarch64":
    _lib_filename = "libcls_ffi_aarch64.so"
elif platform.uname()[0] == "Linux":
    _lib_filename = "libcls_ffi.so"
elif platform.uname()[0] == "Darwin" and platform.uname().machine == "arm64":
    _lib_filename = "libcls_ffi_arm64.dylib"
elif platform.uname()[0] == "Darwin":
    _lib_filename = "libcls_ffi.dylib"
else:
    raise Exception("Unknown platform for CLS")

_ffi_dir = os.path.dirname(__file__)
_lib = cdll.LoadLibrary(os.path.join(_ffi_dir, "libs", _lib_filename))

# Get a path to cls_client, which could be shared between CLIs in the same env,
# but those should be made unique with the combination of project_slug
_cls_client_dir = os.path.abspath(os.path.dirname(_ffi_dir))
_default_instance_id = base64.urlsafe_b64encode(
    hashlib.md5(_cls_client_dir.encode("utf-8")).digest()
)  # bytes on purpose
_default_instance_id = _default_instance_id[:8]
_lib.set_instance_id(_default_instance_id)


def set_debug(debug):
    _lib.set_debug(1 if debug else 0)


def set_version(version):
    _lib.set_version(version.encode("utf-8"))


def set_project_key(project_key):
    _lib.set_project_key(project_key.encode("utf-8"))


def set_project_slug(project_slug):
    _lib.set_project_slug(project_slug.encode("utf-8"))


def set_ci_tracking_enabled(enabled):
    _lib.set_ci_tracking_enabled(1 if enabled else 0)


# Deprecated in favor of set_ci_tracking_enabled
def set_noninteractive_tracking_enabled(enabled):
    set_ci_tracking_enabled(enabled)


def track_event(slug, type, metadata, dispatch):
    _lib.track_event(
        slug.encode("utf-8"),
        type.encode("utf-8"),
        json.dumps(metadata).encode("utf-8"),
        1 if dispatch else 0,
    )


def dispatch_events():
    _lib.dispatch_events()


def set_request_permission_prompt(prompt):
    _lib.set_request_permission_prompt(prompt.encode("utf-8"))


def set_user_id(user_id):
    _lib.set_user_id(user_id.encode("utf-8"))


def set_invocation_id(invocation_id):
    _lib.set_invocation_id(invocation_id.encode("utf-8"))


def set_is_ci(is_ci):
    _lib.set_is_ci(1 if is_ci else 0)


# Deprecated in favor of set_is_ci
def set_is_noninteractive(is_noninteractive):
    set_is_ci(is_noninteractive)
