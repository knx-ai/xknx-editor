import pytest

from xknxmono.product.parser_v2.knx_id import (
    AllocatorRef,
    Application,
    ArgRef,
    KnxId,
    Module,
    ModuleDef,
    ParamRef,
    RepeatPath,
    SubModule,
    SubModuleDef,
)

_MFR = "0008"
_APP = "7072-21-5CC3-O000A"
_BASE = f"M-{_MFR}_A-{_APP}"


class TestFromString:
    def test_manufacturer_only(self):
        k = KnxId.from_string("M-0008")
        assert k.manufacturer == 0x0008
        assert k.content is None

    def test_manufacturer_and_application(self):
        k = KnxId.from_string(_BASE)
        assert k.manufacturer == 0x0008
        assert isinstance(k.content, Application)
        assert k.content.number == 0x7072
        assert k.content.version == 0x21
        assert k.content.fingerprint == 0x5CC3
        assert k.content.order == "O000A"
        assert k.content.content is None

    def test_app_level_param_ref(self):
        k = KnxId.from_string(f"{_BASE}_P-1_R-1")
        assert isinstance(k.content, Application)
        assert k.content.content == ParamRef(1, 1)

    def test_app_level_repeat(self):
        k = KnxId.from_string(f"{_BASE}_X-4")
        assert isinstance(k.content, Application)
        assert k.content.content == RepeatPath(4)

    def test_module_def(self):
        k = KnxId.from_string(f"{_BASE}_MD-1")
        assert isinstance(k.content, Application)
        assert k.content.content == ModuleDef(1)

    def test_module_def_param_ref(self):
        k = KnxId.from_string(f"{_BASE}_MD-1_P-150_R-243")
        assert isinstance(k.content, Application)
        assert k.content.content == ModuleDef(1, ParamRef(0x150, 0x243))

    def test_module_def_argument(self):
        k = KnxId.from_string(f"{_BASE}_MD-1_A-1")
        assert isinstance(k.content, Application)
        assert k.content.content == ModuleDef(1, ArgRef(1))

    def test_module_def_allocator(self):
        k = KnxId.from_string(f"{_BASE}_MD-1_L-2")
        assert isinstance(k.content, Application)
        assert k.content.content == ModuleDef(1, AllocatorRef(2))

    def test_module_def_level_repeat(self):
        k = KnxId.from_string(f"{_BASE}_MD-1_X-4")
        assert isinstance(k.content, Application)
        assert k.content.content == ModuleDef(1, RepeatPath(4))

    def test_module_ref_without_instance(self):
        k = KnxId.from_string(f"{_BASE}_MD-1_M-200")
        assert isinstance(k.content, Application)
        assert k.content.content == ModuleDef(1, Module(0x200))

    def test_module_instance(self):
        k = KnxId.from_string(f"{_BASE}_MD-1_M-200_MI-1")
        assert isinstance(k.content, Application)
        assert k.content.content == ModuleDef(1, Module(0x200, instance=1))

    def test_module_instance_repeat_index(self):
        k = KnxId.from_string(f"{_BASE}_MD-1_M-200_MI-3")
        assert isinstance(k.content, Application)
        assert isinstance(k.content.content, ModuleDef)
        assert isinstance(k.content.content.content, Module)
        assert k.content.content.content.instance == 3

    def test_module_instance_param_ref(self):
        k = KnxId.from_string(f"{_BASE}_MD-1_M-200_MI-1_P-150_R-243")
        assert isinstance(k.content, Application)
        assert k.content.content == ModuleDef(
            1, Module(0x200, 1, ParamRef(0x150, 0x243))
        )

    def test_submodule_def_under_module_def(self):
        k = KnxId.from_string(f"{_BASE}_MD-1_SM-1")
        assert isinstance(k.content, Application)
        assert k.content.content == ModuleDef(1, SubModuleDef(1))

    def test_submodule_def_argument(self):
        k = KnxId.from_string(f"{_BASE}_MD-1_SM-1_A-1")
        assert isinstance(k.content, Application)
        assert k.content.content == ModuleDef(1, SubModuleDef(1, ArgRef(1)))

    def test_submodule_def_level_repeat(self):
        k = KnxId.from_string(f"{_BASE}_MD-1_SM-1_X-4")
        assert isinstance(k.content, Application)
        assert k.content.content == ModuleDef(1, SubModuleDef(1, RepeatPath(4)))

    def test_submodule_instance(self):
        k = KnxId.from_string(f"{_BASE}_MD-1_M-100_MI-1_SM-1_M-200_MI-1")
        assert isinstance(k.content, Application)
        assert k.content.content == ModuleDef(
            1, Module(0x100, 1, SubModuleDef(1, SubModule(0x200, 1)))
        )

    def test_submodule_instance_param_ref(self):
        k = KnxId.from_string(f"{_BASE}_MD-1_M-100_MI-1_SM-1_M-200_MI-1_P-150_R-243")
        assert isinstance(k.content, Application)
        assert k.content.content == ModuleDef(
            1,
            Module(
                0x100, 1, SubModuleDef(1, SubModule(0x200, 1, ParamRef(0x150, 0x243)))
            ),
        )

    def test_nested_repeats(self):
        k = KnxId.from_string(f"{_BASE}_MD-1_X-1_X-2")
        assert isinstance(k.content, Application)
        assert k.content.content == ModuleDef(1, RepeatPath(1, RepeatPath(2)))

    def test_wrong_first_prefix_raises(self):
        with pytest.raises(ValueError):
            KnxId.from_string("A-0008_M-app")


class TestStr:
    def test_round_trip_manufacturer_only(self):
        s = "M-0008"
        assert str(KnxId.from_string(s)) == s

    def test_round_trip_app_level_param_ref(self):
        s = f"{_BASE}_P-1_R-1"
        assert str(KnxId.from_string(s)) == s

    def test_round_trip_app_level_repeat(self):
        s = f"{_BASE}_X-4"
        assert str(KnxId.from_string(s)) == s

    def test_round_trip_module_def_param_ref(self):
        s = f"{_BASE}_MD-1_P-150_R-243"
        assert str(KnxId.from_string(s)) == s

    def test_round_trip_module_def_argument(self):
        s = f"{_BASE}_MD-1_A-1"
        assert str(KnxId.from_string(s)) == s

    def test_round_trip_module_def_allocator(self):
        s = f"{_BASE}_MD-1_L-2"
        assert str(KnxId.from_string(s)) == s

    def test_round_trip_module_def_level_repeat(self):
        s = f"{_BASE}_MD-1_X-4"
        assert str(KnxId.from_string(s)) == s

    def test_round_trip_module_instance(self):
        s = f"{_BASE}_MD-1_M-200_MI-1"
        assert str(KnxId.from_string(s)) == s

    def test_round_trip_module_instance_param_ref(self):
        s = f"{_BASE}_MD-1_M-200_MI-1_P-150_R-243"
        assert str(KnxId.from_string(s)) == s

    def test_round_trip_submodule_def_argument(self):
        s = f"{_BASE}_MD-1_SM-1_A-1"
        assert str(KnxId.from_string(s)) == s

    def test_round_trip_submodule_def_level_repeat(self):
        s = f"{_BASE}_MD-1_SM-1_X-4"
        assert str(KnxId.from_string(s)) == s

    def test_round_trip_submodule_instance(self):
        s = f"{_BASE}_MD-1_M-100_MI-1_SM-1_M-200_MI-1"
        assert str(KnxId.from_string(s)) == s

    def test_round_trip_submodule_instance_param_ref(self):
        s = f"{_BASE}_MD-1_M-100_MI-1_SM-1_M-200_MI-1_P-150_R-243"
        assert str(KnxId.from_string(s)) == s

    def test_round_trip_nested_repeats(self):
        s = f"{_BASE}_MD-1_X-1_X-2"
        assert str(KnxId.from_string(s)) == s
